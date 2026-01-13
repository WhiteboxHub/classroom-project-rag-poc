import chromadb
from langchain_chroma import Chroma
from utils.config import Config
from utils.embedding import get_embedding_function
from utils.logging import setup_logger
import os

logger = setup_logger(__name__)

USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", "False").lower() == "true"

def get_vectorstore():
    try:
        if USE_LOCAL_DB:
            logger.info("Initializing Local ChromaDB (PersistentClient)...")
            # Uses a local folder 'chroma_db_data' to store vector data
            client = chromadb.PersistentClient(path="./chroma_db_data")
            
            vectorstore = Chroma(
                client=client,
                collection_name=Config.COLLECTION_NAME,
                embedding_function=get_embedding_function(),
            )
        else:
            # HttpClient settings
            client_settings = chromadb.config.Settings(
                chroma_server_host=Config.CHROMADB_HOST,
                chroma_server_http_port=Config.CHROMADB_PORT
            )
            
            client = chromadb.HttpClient(host=Config.CHROMADB_HOST, port=Config.CHROMADB_PORT)
            
            vectorstore = Chroma(
                client=client,
                collection_name=Config.COLLECTION_NAME,
                embedding_function=get_embedding_function()
            )
        return vectorstore
    except Exception as e:
        logger.error(f"Failed to initialize Chroma vectorstore: {e}")
        raise e

