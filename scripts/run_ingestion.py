import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipelines.ingestion_pipeline import IngestionPipeline
from utils.logging import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        pipeline = IngestionPipeline()
        pipeline.run()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
