# from langchain_openai import ChatOpenAI
# from utils.config import Config
# from utils.logging import setup_logger

# logger = setup_logger(__name__)

# def get_llm():
#     try:
#         llm = ChatOpenAI(
#             model=Config.OPENAI_MODEL_NAME,
#             temperature=0,
#             api_key=Config.OPENAI_API_KEY
#         )
#         return llm
#     except Exception as e:
#         logger.error(f"Failed to create LangChain LLM: {e}")
#         raise e

# # Kept for backward compatibility if needed, but refactored to use LangChain
# class LLMGenerator:
#     def __init__(self):
#         self.llm = get_llm()

#     def generate(self, messages):
#         # LangChain invoke expects string or list of messages
#         # Depending on how it's called, we might need to adapt
#         response = self.llm.invoke(messages)
#         return response.content

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

def get_llm():
    """
    Returns an LLM instance using OpenAI if available,
    otherwise falls back to Groq.
    """
    try:
        # Prefer OpenAI if API key is set
        if getattr(Config, "OPENAI_API_KEY", None):
            logger.info("Using OpenAI LLM.")
            return ChatOpenAI(
                model=Config.OPENAI_MODEL_NAME,
                temperature=0,
                api_key=Config.OPENAI_API_KEY
            )

        # Fallback to Groq if OpenAI is not configured
        elif getattr(Config, "GROQ_API_KEY", None):
            logger.info("OpenAI not found. Falling back to Groq LLM.")
            return ChatGroq(
                model=Config.GROQ_MODEL_NAME,
                temperature=0,
                api_key=Config.GROQ_API_KEY
            )

        else:
            raise ValueError("No LLM API keys found. Provide OPENAI_API_KEY or GROQ_API_KEY.")

    except Exception as e:
        logger.error(f"Failed to create LLM: {e}")
        raise e


class LLMGenerator:
    def __init__(self):
        self.llm = get_llm()

    def generate(self, messages):
        response = self.llm.invoke(messages)
        return response.content
