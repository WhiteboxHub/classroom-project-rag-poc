from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from utils.chromadb_client import get_vectorstore
from utils.config import Config
from utils.logging import setup_logger
from utils.language_detection import LanguageDetector

logger = setup_logger(__name__)

class IngestionPipeline:
    def __init__(self):
        self.file_path = Config.PDF_PATH
        self.vectorstore = get_vectorstore()
        self.language_detector = LanguageDetector()

    def run(self):
        logger.info("Starting multilingual ingestion pipeline (LangChain)")
        
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

        # 3. Detect language and add to metadata for each chunk
        chunks_with_language = []
        language_stats = {}
        
        for chunk in chunks:
            # Detect language from chunk content
            detected_language = self.language_detector.detect_language(chunk.page_content)
            
            # Update metadata with language information
            if chunk.metadata is None:
                chunk.metadata = {}
            
            chunk.metadata["language"] = detected_language
            
            # Track language statistics
            language_stats[detected_language] = language_stats.get(detected_language, 0) + 1
            
            chunks_with_language.append(chunk)
        
        # Log language distribution
        logger.info(f"Language distribution: {language_stats}")
        for lang_code, count in language_stats.items():
            lang_name = self.language_detector.get_language_name(lang_code)
            logger.info(f"  - {lang_name} ({lang_code}): {count} chunks")

        # 4. Store
        if chunks_with_language:
            # Upsert logic is handled by adding documents. 
            # Note: naive adding might duplicate if run repeatedly without IDs. 
            # Ideally generate stable IDs based on content hash, but standard add_documents creates new IDs.
            # For POC we'll just add.
            self.vectorstore.add_documents(chunks_with_language)
            logger.info("Ingested chunks with language metadata into ChromaDB")
        else:
            logger.warning("No chunks to ingest")

if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run()
