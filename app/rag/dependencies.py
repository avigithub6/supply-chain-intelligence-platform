from functools import lru_cache

from app.rag.embeddings import get_embedding_service
from app.rag.qdrant_client import get_qdrant_client
from app.rag.qdrant_store import QdrantStore
from app.rag.reranker import KnowledgeReranker
from app.rag.retriever import KnowledgeRetriever
from app.rag.search_service import KnowledgeSearchService


@lru_cache
def get_qdrant_store() -> QdrantStore:
    """
    Return a cached Qdrant store.
    """

    return QdrantStore(
        client=get_qdrant_client()
    )


@lru_cache
def get_knowledge_retriever() -> KnowledgeRetriever:
    """
    Return a cached knowledge retriever.
    """

    return KnowledgeRetriever(
        embedding_service=get_embedding_service(),
        qdrant_store=get_qdrant_store(),
    )


@lru_cache
def get_knowledge_reranker() -> KnowledgeReranker:
    """
    Return a cached knowledge reranker.
    """

    return KnowledgeReranker()


@lru_cache
def get_knowledge_search_service() -> KnowledgeSearchService:
    """
    Build and cache the complete RAG search service.
    """

    return KnowledgeSearchService(
        retriever=get_knowledge_retriever(),
        reranker=get_knowledge_reranker(),
    )