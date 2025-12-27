import logging
from utils.retriever import Retriever

logger = logging.getLogger(__name__)

class RetrieverEval:
    def __init__(self):
        self.retriever = Retriever()

    def eval_query(self, query, relevant_doc_ids):
        # logic to check if retrieved docs match relevant_doc_ids
        pass
