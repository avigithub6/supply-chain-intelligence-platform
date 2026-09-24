from dataclasses import dataclass

from app.evaluation.evaluation_metrics import (
    hit_rate_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from app.rag.retriever import RetrievedChunk


@dataclass(frozen=True)
class RAGEvaluationResult:
    precision_at_k: float
    recall_at_k: float
    hit_rate_at_k: float
    reciprocal_rank: float


def evaluate_retrieval(
    chunks: list[RetrievedChunk],
    relevant_sources: set[str],
    k: int = 3,
) -> RAGEvaluationResult:
    if k <= 0:
        raise ValueError(
            "k must be greater than 0."
        )

    retrieved_sources = [
        chunk.source
        for chunk in chunks
    ]

    return RAGEvaluationResult(
        precision_at_k=precision_at_k(
            retrieved_sources,
            relevant_sources,
            k,
        ),
        recall_at_k=recall_at_k(
            retrieved_sources,
            relevant_sources,
            k,
        ),
        hit_rate_at_k=hit_rate_at_k(
            retrieved_sources,
            relevant_sources,
            k,
        ),
        reciprocal_rank=reciprocal_rank(
            retrieved_sources,
            relevant_sources,
        ),
    )