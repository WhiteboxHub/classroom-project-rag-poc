from langchain_openai import ChatOpenAI
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

def get_llm():
    try:
        llm = ChatOpenAI(
            model=Config.OPENAI_MODEL_NAME,
            temperature=0,
            api_key=Config.OPENAI_API_KEY
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to create LangChain LLM: {e}")
        raise e

# Kept for backward compatibility if needed, but refactored to use LangChain
class LLMGenerator:
    def __init__(self):
        self.llm = get_llm()

    def generate(self, messages):
        # LangChain invoke expects string or list of messages
        # Depending on how it's called, we might need to adapt
        response = self.llm.invoke(messages)
        return response.content
