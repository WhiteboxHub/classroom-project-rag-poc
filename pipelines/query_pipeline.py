from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from typing import List
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from utils.chromadb_client import get_vectorstore
from utils.llm import get_llm
from utils.config import Config
from utils.language_detection import LanguageDetector
from pipelines.prompt_pipeline import PromptPipeline
from utils.logging import setup_logger

logger = setup_logger(__name__)

class LanguageAwareRetriever(BaseRetriever):
    """
    Custom retriever wrapper that filters documents by language if enabled.
    This ensures filtering happens before documents are passed to the chain.
    """
    
    def __init__(self, base_retriever: BaseRetriever, query_language: str, language_detector: LanguageDetector, filter_enabled: bool = False):
        super().__init__()
        self.base_retriever = base_retriever
        self.query_language = query_language
        self.language_detector = language_detector
        self.filter_enabled = filter_enabled
    
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None
    ) -> List[Document]:
        """Retrieve and optionally filter documents by language."""
        # Get documents from base retriever
        docs = self.base_retriever.get_relevant_documents(query, run_manager=run_manager)
        
        if not self.filter_enabled:
            return docs
        
        # Filter documents by language
        matching_lang_docs = []
        for doc in docs:
            doc_language = doc.metadata.get("language", Config.DEFAULT_LANGUAGE)
            if doc_language == self.query_language:
                matching_lang_docs.append(doc)
        
        # If we have good language match (at least half), use only matching docs
        if len(matching_lang_docs) >= max(1, len(docs) // 2):
            logger.info(f"Filtering to {len(matching_lang_docs)} documents matching language {self.query_language} "
                       f"(out of {len(docs)} total)")
            return matching_lang_docs
        else:
            # Not enough same-language results, return all (multilingual retrieval)
            logger.info(f"Limited same-language matches ({len(matching_lang_docs)}), using all {len(docs)} documents "
                       f"for multilingual retrieval")
            return docs
    
    async def _aget_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None
    ) -> List[Document]:
        """Async version of retrieval."""
        docs = await self.base_retriever.aget_relevant_documents(query, run_manager=run_manager)
        
        if not self.filter_enabled:
            return docs
        
        matching_lang_docs = [doc for doc in docs 
                             if doc.metadata.get("language", Config.DEFAULT_LANGUAGE) == self.query_language]
        
        if len(matching_lang_docs) >= max(1, len(docs) // 2):
            return matching_lang_docs
        return docs

class QueryPipeline:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.llm = get_llm()
        self.prompt_pipeline = PromptPipeline()
        self.language_detector = LanguageDetector()

    def run(self, query: str, stream: bool = False):
        logger.info(f"Processing multilingual query: {query}")
        
        # 1. Detect query language
        query_language = self.language_detector.detect_language(query)
        lang_name = self.language_detector.get_language_name(query_language)
        logger.info(f"Detected query language: {lang_name} ({query_language})")
        
        # 2. Setup Retriever with optional language filtering
        base_retriever = self.vectorstore.as_retriever()
        
        # Wrap with language-aware retriever if filtering is enabled
        if Config.ENABLE_LANGUAGE_FILTERING:
            retriever = LanguageAwareRetriever(
                base_retriever=base_retriever,
                query_language=query_language,
                language_detector=self.language_detector,
                filter_enabled=True
            )
            logger.info("Language-based filtering enabled for retrieval")
        else:
            retriever = base_retriever
            logger.info("Using multilingual retrieval (no language filtering)")
        
        # 3. Setup Chain
        # We will use the system prompt content but convert to LangChain Template
        system_prompt_text = self.prompt_pipeline.get_system_prompt()
        
        # Enhance prompt to indicate multilingual support
        multilingual_system_prompt = f"""{system_prompt_text}

Note: The user's query is in {lang_name} ({query_language}). Please respond in the same language as the query when possible."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", multilingual_system_prompt),
            ("system", "Context: {context}"),
            ("user", "{input}")
        ])
        
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # 4. Invoke
        # Response contains 'answer' and 'context'
        if stream:
             logger.warning("Streaming not strictly implemented in this simple chain wrapper yet, returning full response")
        
        response = retrieval_chain.invoke({"input": query})
        
        answer = response["answer"]
        context_docs = response["context"]
        
        # Format sources to match previous contract somewhat
        formatted_sources = []
        for doc in context_docs:
            doc_language = doc.metadata.get("language", "unknown")
            formatted_sources.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "language": doc_language
            })
        
        logger.info(f"Retrieved {len(formatted_sources)} documents for response")
        return answer, formatted_sources
