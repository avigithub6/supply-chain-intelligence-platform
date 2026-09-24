import pytest

from app.evaluation.evaluation_metrics import (
    calculate_retrieval_metrics,
    hit_rate_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_precision_at_k() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
        "doc-3",
        "doc-4",
    ]

    relevant = {
        "doc-1",
        "doc-3",
    }

    result = precision_at_k(
        retrieved,
        relevant,
        k=4,
    )

    assert result == 0.5


def test_precision_at_k_uses_only_top_k() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
        "doc-3",
    ]

    relevant = {
        "doc-3",
    }

    result = precision_at_k(
        retrieved,
        relevant,
        k=2,
    )

    assert result == 0.0


def test_recall_at_k() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
        "doc-3",
        "doc-4",
    ]

    relevant = {
        "doc-1",
        "doc-3",
    }

    result = recall_at_k(
        retrieved,
        relevant,
        k=4,
    )

    assert result == 1.0


def test_recall_at_k_partial() -> None:
    retrieved = [
        "doc-1",
        "doc-4",
        "doc-5",
    ]

    relevant = {
        "doc-1",
        "doc-2",
        "doc-3",
    }

    result = recall_at_k(
        retrieved,
        relevant,
        k=3,
    )

    assert result == pytest.approx(
        1 / 3
    )


def test_hit_rate_at_k_when_relevant_document_exists() -> None:
    retrieved = [
        "doc-5",
        "doc-2",
        "doc-7",
    ]

    relevant = {
        "doc-2",
    }

    result = hit_rate_at_k(
        retrieved,
        relevant,
        k=3,
    )

    assert result == 1.0


def test_hit_rate_at_k_when_no_relevant_document_exists() -> None:
    retrieved = [
        "doc-5",
        "doc-6",
        "doc-7",
    ]

    relevant = {
        "doc-2",
    }

    result = hit_rate_at_k(
        retrieved,
        relevant,
        k=3,
    )

    assert result == 0.0


def test_reciprocal_rank_first_result() -> None:
    retrieved = [
        "doc-2",
        "doc-3",
        "doc-4",
    ]

    relevant = {
        "doc-2",
    }

    result = reciprocal_rank(
        retrieved,
        relevant,
    )

    assert result == 1.0


def test_reciprocal_rank_second_result() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
        "doc-3",
    ]

    relevant = {
        "doc-2",
    }

    result = reciprocal_rank(
        retrieved,
        relevant,
    )

    assert result == 0.5


def test_reciprocal_rank_no_match() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
    ]

    relevant = {
        "doc-5",
    }

    result = reciprocal_rank(
        retrieved,
        relevant,
    )

    assert result == 0.0


def test_empty_retrieved_documents() -> None:
    assert precision_at_k(
        [],
        {"doc-1"},
        k=5,
    ) == 0.0

    assert recall_at_k(
        [],
        {"doc-1"},
        k=5,
    ) == 0.0

    assert hit_rate_at_k(
        [],
        {"doc-1"},
        k=5,
    ) == 0.0


def test_empty_relevant_documents() -> None:
    retrieved = [
        "doc-1",
        "doc-2",
    ]

    assert precision_at_k(
        retrieved,
        set(),
        k=2,
    ) == 0.0

    assert recall_at_k(
        retrieved,
        set(),
        k=2,
    ) == 0.0

    assert hit_rate_at_k(
        retrieved,
        set(),
        k=2,
    ) == 0.0

    assert reciprocal_rank(
        retrieved,
        set(),
    ) == 0.0


def test_invalid_k() -> None:
    with pytest.raises(ValueError):
        precision_at_k(
            ["doc-1"],
            {"doc-1"},
            k=0,
        )

    with pytest.raises(ValueError):
        recall_at_k(
            ["doc-1"],
            {"doc-1"},
            k=-1,
        )

    with pytest.raises(ValueError):
        hit_rate_at_k(
            ["doc-1"],
            {"doc-1"},
            k=0,
        )


def test_invalid_retrieved_documents_type() -> None:
    with pytest.raises(TypeError):
        precision_at_k(
            "doc-1",
            {"doc-1"},
            k=1,
        )


def test_invalid_relevant_documents_type() -> None:
    with pytest.raises(TypeError):
        recall_at_k(
            ["doc-1"],
            ["doc-1"],
            k=1,
        )


def test_calculate_retrieval_metrics() -> None:
    retrieved = [
        "doc-1",
        "doc-4",
        "doc-5",
    ]

    relevant = {
        "doc-1",
        "doc-2",
    }

    result = calculate_retrieval_metrics(
        retrieved_documents=retrieved,
        relevant_documents=relevant,
        k=3,
    )

    assert result.precision_at_k == pytest.approx(
        1 / 3
    )

    assert result.recall_at_k == 0.5

    assert result.hit_rate_at_k == 1.0

    assert result.reciprocal_rank == 1.0