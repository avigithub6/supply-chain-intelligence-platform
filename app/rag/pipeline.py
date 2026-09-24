from app.rag.chunking import chunk_documents
from app.rag.embeddings import EmbeddingService
from app.rag.ingestion import load_knowledge_documents
from app.rag.qdrant_client import get_qdrant_client
from app.rag.qdrant_store import QdrantStore


def build_knowledge_index(
    knowledge_base_path: str = "knowledge_base",
) -> int:
    """
    Build the knowledge index from the local knowledge base.
    """

    documents = load_knowledge_documents(
        knowledge_base_path
    )

    if not documents:
        return 0

    chunks = chunk_documents(
        documents
    )

    if not chunks:
        return 0

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_chunks(
        chunks
    )

    qdrant_client = get_qdrant_client()

    qdrant_store = QdrantStore(
        client=qdrant_client
    )

    qdrant_store.upsert_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    return len(chunks)


if __name__ == "__main__":
    indexed_chunks = build_knowledge_index()

    print(
        "Knowledge index built successfully."
    )

    print(
        f"Indexed chunks: {indexed_chunks}"
    )