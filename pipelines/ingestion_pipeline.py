from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.chromadb_client import get_vectorstore
from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

class IngestionPipeline:
    def __init__(self):
        self.file_path = Config.PDF_PATH
        self.vectorstore = get_vectorstore()

    def run(self):
        logger.info("Starting ingestion pipeline (LangChain)")
        
        # 1. Load
        loader = PyPDFLoader(self.file_path)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages")

        # 2. Split
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")

        # 3. Store
        if chunks:
            # Upsert logic is handled by adding documents. 
            # Note: naive adding might duplicate if run repeatedly without IDs. 
            # Ideally generate stable IDs based on content hash, but standard add_documents creates new IDs.
            # For POC we'll just add.
            self.vectorstore.add_documents(chunks)
            logger.info("Ingested chunks into ChromaDB")
        else:
            logger.warning("No chunks to ingest")

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
