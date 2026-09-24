from functools import lru_cache

from qdrant_client import QdrantClient

from app.core.config import settings


@lru_cache
def get_qdrant_client() -> QdrantClient:
    """
    Create and cache the Qdrant client.

    The client is created once per application process and
    reused by the RAG components.
    """

    return QdrantClient(
        url=settings.qdrant_url,
    )