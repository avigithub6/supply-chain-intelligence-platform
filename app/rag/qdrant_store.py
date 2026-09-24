from uuid import UUID, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import settings
from app.rag.chunking import DocumentChunk


VECTOR_SIZE = 384

# Stable namespace used for deterministic Qdrant point IDs.
POINT_NAMESPACE = UUID(
    "5d9b6c2e-8f4e-4d72-9f6b-1f3c9d8a7e21"
)


class QdrantStore:
    def __init__(
        self,
        client: QdrantClient,
        collection_name: str = settings.qdrant_collection_name,
    ) -> None:
        self.client = client
        self.collection_name = collection_name

    def create_collection(self) -> None:
        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        if self.collection_name in existing_names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    def collection_exists(self) -> bool:
        collections = self.client.get_collections()

        existing_names = {
            collection.name
            for collection in collections.collections
        }

        return self.collection_name in existing_names

    def upsert_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must be equal."
            )

        if not chunks:
            return

        self.create_collection()

        points: list[PointStruct] = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):
            point_id = self._generate_point_id(
                chunk
            )

            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "source": chunk.source,
                    "category": chunk.category,
                    "file_name": chunk.file_name,
                    "chunk_index": chunk.chunk_index,
                },
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):
        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty."
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0."
            )

        if not self.collection_exists():
            return []

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        )

    @staticmethod
    def _generate_point_id(
        chunk: DocumentChunk,
    ) -> str:
        """
        Generate a deterministic UUID for a document chunk.

        The same source and chunk index always produce
        the same Qdrant point ID.
        """

        identifier = (
            f"{chunk.source}:"
            f"{chunk.chunk_index}"
        )

        return str(
            uuid5(
                POINT_NAMESPACE,
                identifier,
            )
        )