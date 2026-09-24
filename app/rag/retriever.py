from dataclasses import dataclass

from app.rag.embeddings import EmbeddingService
from app.rag.qdrant_store import QdrantStore


@dataclass
class RetrievedChunk:
    content: str
    source: str
    category: str
    file_name: str
    chunk_index: int
    retrieval_score: float
    rerank_score: float | None = None


class KnowledgeRetriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        qdrant_store: QdrantStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.qdrant_store = qdrant_store

    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0."
            )

        query_embedding = (
            self.embedding_service.embed_text(
                query
            )
        )

        search_result = self.qdrant_store.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        retrieved_chunks: list[RetrievedChunk] = []

        for result in search_result.points:
            payload = result.payload or {}

            retrieved_chunks.append(
                RetrievedChunk(
                    content=str(
                        payload.get("content", "")
                    ),
                    source=str(
                        payload.get("source", "")
                    ),
                    category=str(
                        payload.get("category", "")
                    ),
                    file_name=str(
                        payload.get("file_name", "")
                    ),
                    chunk_index=int(
                        payload.get("chunk_index", 0)
                    ),
                    retrieval_score=float(
                        result.score
                    ),
                )
            )

        return retrieved_chunks