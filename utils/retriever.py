from typing import List, Dict, Any
from utils.chromadb_client import get_collection
from utils.embedding import EmbeddingGenerator
from utils.logging import setup_logger

logger = setup_logger(__name__)

class Retriever:
    def __init__(self, top_k: int = 5):
        self.collection = get_collection()
        self.embedder = EmbeddingGenerator()
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.generate_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )
        
        # Parse results into a cleaner format
        retrieved_docs = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                doc = {
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "distance": results['distances'][0][i] if results['distances'] else None
                }
                retrieved_docs.append(doc)
                
        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
        return retrieved_docs
