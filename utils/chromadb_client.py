import chromadb
from langchain_chroma import Chroma
from utils.config import Config
from utils.embedding import get_embedding_function
from utils.logging import setup_logger
import os

logger = setup_logger(__name__)

USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", "False").lower() == "true"

_client = None

def get_vectorstore():
    global _client
    try:
        embedding_function = get_embedding_function()
        
        # Disable telemetry in settings
        settings = chromadb.config.Settings(anonymized_telemetry=False)
        
        if USE_LOCAL_DB:
            if _client is None:
                logger.info("Initializing Local ChromaDB (PersistentClient)...")
                _client = chromadb.PersistentClient(path="./chroma_db_data", settings=settings)
            
            vectorstore = Chroma(
                client=_client,
                collection_name=Config.COLLECTION_NAME,
                embedding_function=embedding_function,
            )
        else:
            if _client is None:
                logger.info(f"Initializing Remote ChromaDB (HttpClient) at {Config.CHROMADB_HOST}:{Config.CHROMADB_PORT}")
                _client = chromadb.HttpClient(
                    host=Config.CHROMADB_HOST, 
                    port=Config.CHROMADB_PORT,
                    settings=settings
                )
            
            vectorstore = Chroma(
                client=_client,
                collection_name=Config.COLLECTION_NAME,
                embedding_function=embedding_function
            )
        return vectorstore
    except Exception as e:
        logger.error(f"Failed to initialize Chroma vectorstore: {e}")
        raise e

