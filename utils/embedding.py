from langchain_huggingface import HuggingFaceEmbeddings
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

class EmbeddingGenerator:
    _instance = None
    _embeddings = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingGenerator, cls).__new__(cls)
            logger.info(f"Loading LangChain embedding model: {Config.EMBEDDING_MODEL_NAME}")
            try:
                cls._embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise e
        return cls._instance

    def get_embedding_function(self):
        return self._embeddings

def get_embedding_function():
    return EmbeddingGenerator().get_embedding_function()
