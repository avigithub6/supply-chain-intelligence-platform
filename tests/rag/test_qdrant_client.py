from app.rag.qdrant_client import get_qdrant_client


def test_qdrant_client_is_cached() -> None:
    first_client = get_qdrant_client()
    second_client = get_qdrant_client()

    assert first_client is second_client