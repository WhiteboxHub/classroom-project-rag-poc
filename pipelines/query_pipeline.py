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
        
        # 2. Get Context
        context_docs = retriever.invoke(query)
        
        # 3. Setup Prompt
        system_prompt_text = self.prompt_pipeline.get_system_prompt()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("system", "Context: {context}"),
            ("user", "{input}")
        ])
        
        # 4. Format sources
        formatted_sources = []
        for doc in context_docs:
            formatted_sources.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })

        # Format context for both streaming and non-streaming
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        messages = prompt.format_messages(context=context_text, input=query)

        if stream:
            # For streaming
            return self.llm.stream(messages), formatted_sources
        else:
            # For non-streaming
            answer = self.llm.invoke(messages)
            return answer.content, formatted_sources
