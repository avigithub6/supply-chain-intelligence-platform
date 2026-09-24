from app.observability.request_ids import (
    generate_request_id,
)


def test_generate_request_id_returns_string() -> None:
    request_id = generate_request_id()

    assert isinstance(request_id, str)
    assert request_id


def test_generate_request_id_is_unique() -> None:
    first_id = generate_request_id()
    second_id = generate_request_id()

    assert first_id != second_id