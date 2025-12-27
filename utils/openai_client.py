from openai import OpenAI
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            if not Config.OPENAI_API_KEY:
                logger.error("OpenAI API Key missing")
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            cls._instance.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        return cls._instance

    def get_client(self):
        return self.client

def get_openai_client():
    return OpenAIClient().get_client()
