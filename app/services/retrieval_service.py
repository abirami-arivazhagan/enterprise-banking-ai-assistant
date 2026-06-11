from rag.retrievers.hybrid import (
    HybridRetriever
)
from rag.rerankers.cross_encoder_reranker import (
    CrossEncoderReranker
)
from rag.qa.qa_chain import (
    QAChain
)
from rbac.validator import (
    validate_role_access
)

class RetrievalService:
    def __init__(self):
        self.retriever = (
            HybridRetriever()
        )
        self.reranker = (
            CrossEncoderReranker()
        )
        self.qa_chain = QAChain()
    def ask(
        self,
        query,
        chat_history=None,
        role="customer"
    ):
        retrieved_docs = (
            self.retriever.retrieve(
                query,
                k=12
            )
        )
        retrieved_docs = [
            doc
            for doc in retrieved_docs
            if validate_role_access(
                role,
                doc
            )
        ]
        reranked_docs = (
            self.reranker.rerank(
                query,
                retrieved_docs
            )
        )
        response = (
            self.qa_chain.generate_answer(
                query,
                reranked_docs,
                chat_history=chat_history,
                role=role
            )
        )
        return response
