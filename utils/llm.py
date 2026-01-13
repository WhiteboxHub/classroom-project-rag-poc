import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

def get_llm():
    provider = Config.LLM_PROVIDER.lower()

    try:
        if provider == "groq":
            logger.info("Using Groq LLM")
            return ChatGroq(
                groq_api_key=Config.GROQ_API_KEY,
                model=Config.GROQ_MODEL_NAME,
                temperature=0
            )

        elif provider == "openai":
            logger.info("Using OpenAI LLM")
            return ChatOpenAI(
                api_key=Config.OPENAI_API_KEY,
                model=Config.OPENAI_MODEL_NAME,
                temperature=0
            )

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    except Exception as e:
        logger.error(f"Failed to create LLM: {e}")
        raise e


# Backward compatibility
class LLMGenerator:
    def __init__(self):
        self.llm = get_llm()

    def generate(self, messages):
        response = self.llm.invoke(messages)
        return response.content
