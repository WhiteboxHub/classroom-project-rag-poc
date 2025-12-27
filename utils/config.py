import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
    
    # Local Embeddings
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    
    # ChromaDB
    CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
    CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", 8000))
    COLLECTION_NAME = "rag_collection"
    
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    DATA_DIR = "data"
    PDF_PATH = os.path.join(DATA_DIR, "provider_manual.pdf")

    # Postgres
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "rag_db")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    # AWS Bedrock (Optional)
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            logging.warning("OPENAI_API_KEY is not set. Some features may not work.")
