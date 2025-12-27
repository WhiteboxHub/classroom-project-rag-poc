import pypdf
from typing import List, Tuple
from ingestion.metadata import DocumentMetadata
from utils.logging import setup_logger

logger = setup_logger(__name__)

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Tuple[str, DocumentMetadata]]:
        """
        Returns a list of tuples: (text_content, metadata)
        """
        logger.info(f"Loading PDF from {self.file_path}")
        documents = []
        try:
            with open(self.file_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                total_pages = len(reader.pages)
                logger.info(f"Found {total_pages} pages")
                
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        meta = DocumentMetadata(
                            source=self.file_path,
                            page=i + 1
                        )
                        documents.append((text, meta))
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise e
            
        logger.info(f"Loaded {len(documents)} pages with content")
        return documents
