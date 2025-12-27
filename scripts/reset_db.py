import shutil
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import Config
from utils.logging import setup_logger

logger = setup_logger(__name__)

def reset_db():
    db_path = Config.CHROMADB_PATH
    if os.path.exists(db_path):
        logger.info(f"Removing ChromaDB at {db_path}")
        shutil.rmtree(db_path)
    else:
        logger.info("No ChromaDB found to reset.")

    # Also reset SQLite chat history if desired
    # if os.path.exists("chat_history.db"):
    #     os.remove("chat_history.db")
    
    logger.info("DB Reset Complete.")

if __name__ == "__main__":
    reset_db()
