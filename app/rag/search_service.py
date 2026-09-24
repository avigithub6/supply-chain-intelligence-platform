from dataclasses import dataclass

from app.rag.reranker import KnowledgeReranker
from app.rag.retriever import KnowledgeRetriever, RetrievedChunk


@dataclass
class KnowledgeSearchResult:
    chunks: list[RetrievedChunk]
    query: str


class KnowledgeSearchService:
    def __init__(
        self,
        retriever: KnowledgeRetriever,
        reranker: KnowledgeReranker,
    ) -> None:
        self.retriever = retriever
        self.reranker = reranker

    def search(
        self,
        query: str,
        retrieval_limit: int = 5,
        top_k: int = 3,
    ) -> KnowledgeSearchResult:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if retrieval_limit <= 0:
            raise ValueError(
                "retrieval_limit must be greater than 0."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        retrieved_chunks = self.retriever.retrieve(
            query=query,
            limit=retrieval_limit,
        )

        reranked_chunks = self.reranker.rerank(
            query=query,
            chunks=retrieved_chunks,
            top_k=top_k,
        )

        return KnowledgeSearchResult(
            query=query,
            chunks=reranked_chunks,
        )