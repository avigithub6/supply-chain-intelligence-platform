from app.rag.chunking import DocumentChunk
from app.rag.qdrant_store import QdrantStore


class FakeCollection:
    def __init__(self, name: str) -> None:
        self.name = name


class FakeCollectionsResponse:
    def __init__(self, names: list[str]) -> None:
        self.collections = [
            FakeCollection(name)
            for name in names
        ]


class FakeClient:
    def __init__(
        self,
        existing_collections: list[str] | None = None,
    ) -> None:
        self.existing_collections = (
            existing_collections or []
        )

        self.created_collection = None
        self.upserted_points = None

    def get_collections(self):
        return FakeCollectionsResponse(
            self.existing_collections
        )

    def create_collection(
        self,
        collection_name,
        vectors_config,
    ):
        self.created_collection = {
            "name": collection_name,
            "vectors_config": vectors_config,
        }

    def upsert(
        self,
        collection_name,
        points,
    ):
        self.upserted_points = {
            "collection_name": collection_name,
            "points": points,
        }


def create_test_chunk() -> DocumentChunk:
    return DocumentChunk(
        content="Supplier shipment is delayed.",
        source="supplier_sla/test.txt",
        category="supplier_sla",
        file_name="test.txt",
        chunk_index=0,
    )


def test_collection_does_not_exist() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    assert store.collection_exists() is False


def test_collection_exists() -> None:
    client = FakeClient(
        existing_collections=[
            "test_collection"
        ]
    )

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    assert store.collection_exists() is True


def test_create_collection() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    store.create_collection()

    assert client.created_collection is not None

    assert (
        client.created_collection["name"]
        == "test_collection"
    )


def test_create_collection_only_once() -> None:
    client = FakeClient(
        existing_collections=[
            "test_collection"
        ]
    )

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    store.create_collection()

    assert client.created_collection is None


def test_upsert_chunks() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    chunks = [
        create_test_chunk(),
    ]

    embeddings = [
        [0.1, 0.2, 0.3, 0.4],
    ]

    store.upsert_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    assert client.upserted_points is not None

    assert (
        client.upserted_points["collection_name"]
        == "test_collection"
    )

    assert len(
        client.upserted_points["points"]
    ) == 1


def test_upsert_chunk_metadata() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    chunks = [
        create_test_chunk(),
    ]

    embeddings = [
        [0.1, 0.2, 0.3, 0.4],
    ]

    store.upsert_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    point = (
        client
        .upserted_points["points"][0]
    )

    assert point.payload["content"] == (
        "Supplier shipment is delayed."
    )

    assert point.payload["source"] == (
        "supplier_sla/test.txt"
    )

    assert point.payload["category"] == (
        "supplier_sla"
    )

    assert point.payload["file_name"] == (
        "test.txt"
    )

    assert point.payload["chunk_index"] == 0


def test_upsert_mismatched_data() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    chunks = [
        create_test_chunk(),
    ]

    embeddings = []

    try:
        store.upsert_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Number of chunks and embeddings must be equal."
        )


def test_upsert_empty_chunks() -> None:
    client = FakeClient()

    store = QdrantStore(
        client=client,
        collection_name="test_collection",
    )

    store.upsert_chunks(
        chunks=[],
        embeddings=[],
    )

    assert client.upserted_points is None

def test_chunk_point_id_is_deterministic() -> None:
    chunk = create_test_chunk()

    first_id = QdrantStore._generate_point_id(
        chunk
    )

    second_id = QdrantStore._generate_point_id(
        chunk
    )

    assert first_id == second_id

def test_different_chunks_have_different_point_ids() -> None:
    first_chunk = create_test_chunk()

    second_chunk = DocumentChunk(
        content="Another supplier policy.",
        source="supplier_sla/test.txt",
        category="supplier_sla",
        file_name="test.txt",
        chunk_index=1,
    )

    first_id = QdrantStore._generate_point_id(
        first_chunk
    )

    second_id = QdrantStore._generate_point_id(
        second_chunk
    )

    assert first_id != second_id        