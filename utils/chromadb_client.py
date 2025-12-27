import chromadb
from langchain_chroma import Chroma
from utils.config import Config
from utils.embedding import get_embedding_function
from utils.logging import setup_logger

logger = setup_logger(__name__)

def get_vectorstore():
    try:
        # HttpClient settings
        client_settings = chromadb.config.Settings(
            chroma_server_host=Config.CHROMADB_HOST,
            chroma_server_http_port=Config.CHROMADB_PORT
        )
        
        # We can also pass the client directly if we want, but LangChain Chroma client handling is specific
        # Ideally we use the client to connect
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
