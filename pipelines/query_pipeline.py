from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from utils.chromadb_client import get_vectorstore
from utils.llm import get_llm
from pipelines.prompt_pipeline import PromptPipeline
from utils.logging import setup_logger

logger = setup_logger(__name__)

class QueryPipeline:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        self.llm = get_llm()
        self.prompt_pipeline = PromptPipeline()

    def run(self, query: str, stream: bool = False):
        logger.info(f"Processing query: {query}")
        
        # 1. Setup Retriever
        retriever = self.vectorstore.as_retriever()
        
        # 2. Setup Chain
        # We will use the system prompt content but convert to LangChain Template
        system_prompt_text = self.prompt_pipeline.get_system_prompt()
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("system", "Context: {context}"),
            ("user", "{input}")
        ])
        
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # 3. Invoke
        # Response contains 'answer' and 'context'
        if stream:
             logger.warning("Streaming not strictly implemented in this simple chain wrapper yet, returning full response")
        
        response = retrieval_chain.invoke({"input": query})
        
        answer = response["answer"]
        context_docs = response["context"]
        
        # Format sources to match previous contract somewhat
        formatted_sources = []
        for doc in context_docs:
            formatted_sources.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
            
        return answer, formatted_sources
