from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.rag.chunking import DocumentChunk


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        model: SentenceTransformer | None = None,
    ) -> None:
        self.model = model or SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[list[float]]:
        if not chunks:
            return []

        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return [
            embedding.tolist()
            for embedding in embeddings
        ]


@lru_cache
def get_embedding_service() -> EmbeddingService:
    """
    Return one cached embedding service per application process.

    This prevents the SentenceTransformer model from being
    loaded repeatedly for every API request.
    """

    return EmbeddingService()