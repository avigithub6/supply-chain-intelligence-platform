import pytest

from app.evaluation.rag_eval import evaluate_retrieval
from app.rag.retriever import RetrievedChunk


def create_chunk(
    source: str,
    chunk_index: int = 0,
) -> RetrievedChunk:
    return RetrievedChunk(
        content="Supplier shipment delay policy.",
        source=source,
        category="supplier_sla",
        file_name=source.split("/")[-1],
        chunk_index=chunk_index,
        retrieval_score=0.90,
    )


def test_evaluate_retrieval() -> None:
    chunks = [
        create_chunk(
            "supplier_sla/supplier_delay_policy.txt",
            chunk_index=0,
        ),
        create_chunk(
            "policies/customer_delay_policy.txt",
            chunk_index=1,
        ),
        create_chunk(
            "sop/inventory_replenishment_sop.txt",
            chunk_index=2,
        ),
    ]

    relevant_sources = {
        "supplier_sla/supplier_delay_policy.txt",
    }

    result = evaluate_retrieval(
        chunks=chunks,
        relevant_sources=relevant_sources,
        k=3,
    )

    assert result.precision_at_k == pytest.approx(
        1 / 3
    )

    assert result.recall_at_k == 1.0

    assert result.hit_rate_at_k == 1.0

    assert result.reciprocal_rank == 1.0


def test_evaluate_retrieval_multiple_relevant_sources() -> None:
    chunks = [
        create_chunk(
            "supplier_sla/supplier_delay_policy.txt",
            chunk_index=0,
        ),
        create_chunk(
            "supplier_sla/supplier_sla_policy.txt",
            chunk_index=1,
        ),
        create_chunk(
            "policies/customer_delay_policy.txt",
            chunk_index=2,
        ),
    ]

    relevant_sources = {
        "supplier_sla/supplier_delay_policy.txt",
        "supplier_sla/supplier_sla_policy.txt",
    }

    result = evaluate_retrieval(
        chunks=chunks,
        relevant_sources=relevant_sources,
        k=3,
    )

    assert result.precision_at_k == pytest.approx(
        2 / 3
    )

    assert result.recall_at_k == 1.0

    assert result.hit_rate_at_k == 1.0

    assert result.reciprocal_rank == 1.0


def test_evaluate_retrieval_respects_k() -> None:
    chunks = [
        create_chunk(
            "policies/customer_delay_policy.txt",
            chunk_index=0,
        ),
        create_chunk(
            "supplier_sla/supplier_delay_policy.txt",
            chunk_index=1,
        ),
    ]

    relevant_sources = {
        "supplier_sla/supplier_delay_policy.txt",
    }

    result = evaluate_retrieval(
        chunks=chunks,
        relevant_sources=relevant_sources,
        k=1,
    )

    assert result.precision_at_k == 0.0

    assert result.recall_at_k == 0.0

    assert result.hit_rate_at_k == 0.0

    assert result.reciprocal_rank == 0.5


def test_evaluate_retrieval_empty_chunks() -> None:
    result = evaluate_retrieval(
        chunks=[],
        relevant_sources={
            "supplier_sla/supplier_delay_policy.txt",
        },
        k=3,
    )

    assert result.precision_at_k == 0.0

    assert result.recall_at_k == 0.0

    assert result.hit_rate_at_k == 0.0

    assert result.reciprocal_rank == 0.0


def test_evaluate_retrieval_no_relevant_sources() -> None:
    chunks = [
        create_chunk(
            "policies/customer_delay_policy.txt",
        ),
    ]

    result = evaluate_retrieval(
        chunks=chunks,
        relevant_sources=set(),
        k=3,
    )

    assert result.precision_at_k == 0.0

    assert result.recall_at_k == 0.0

    assert result.hit_rate_at_k == 0.0

    assert result.reciprocal_rank == 0.0


def test_evaluate_retrieval_rejects_invalid_k() -> None:
    with pytest.raises(ValueError):
        evaluate_retrieval(
            chunks=[],
            relevant_sources=set(),
            k=0,
        )


def test_evaluate_retrieval_rejects_negative_k() -> None:
    with pytest.raises(ValueError):
        evaluate_retrieval(
            chunks=[],
            relevant_sources=set(),
            k=-1,
        )