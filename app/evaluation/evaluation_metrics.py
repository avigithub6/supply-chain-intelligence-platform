from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    hit_rate_at_k: float
    reciprocal_rank: float


def _validate_inputs(
    retrieved_documents: list[str],
    relevant_documents: set[str],
    k: int,
) -> None:
    if k <= 0:
        raise ValueError(
            "k must be greater than 0."
        )

    if not isinstance(
        retrieved_documents,
        list,
    ):
        raise TypeError(
            "retrieved_documents must be a list."
        )

    if not isinstance(
        relevant_documents,
        set,
    ):
        raise TypeError(
            "relevant_documents must be a set."
        )


def precision_at_k(
    retrieved_documents: list[str],
    relevant_documents: set[str],
    k: int,
) -> float:
    _validate_inputs(
        retrieved_documents,
        relevant_documents,
        k,
    )

    top_k = retrieved_documents[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(
        document in relevant_documents
        for document in top_k
    )

    return relevant_count / len(top_k)


def recall_at_k(
    retrieved_documents: list[str],
    relevant_documents: set[str],
    k: int,
) -> float:
    _validate_inputs(
        retrieved_documents,
        relevant_documents,
        k,
    )

    if not relevant_documents:
        return 0.0

    top_k = retrieved_documents[:k]

    relevant_count = sum(
        document in relevant_documents
        for document in top_k
    )

    return relevant_count / len(
        relevant_documents
    )


def hit_rate_at_k(
    retrieved_documents: list[str],
    relevant_documents: set[str],
    k: int,
) -> float:
    _validate_inputs(
        retrieved_documents,
        relevant_documents,
        k,
    )

    top_k = retrieved_documents[:k]

    if not top_k or not relevant_documents:
        return 0.0

    return float(
        any(
            document in relevant_documents
            for document in top_k
        )
    )


def reciprocal_rank(
    retrieved_documents: list[str],
    relevant_documents: set[str],
) -> float:
    if not isinstance(
        retrieved_documents,
        list,
    ):
        raise TypeError(
            "retrieved_documents must be a list."
        )

    if not isinstance(
        relevant_documents,
        set,
    ):
        raise TypeError(
            "relevant_documents must be a set."
        )

    if not relevant_documents:
        return 0.0

    for rank, document in enumerate(
        retrieved_documents,
        start=1,
    ):
        if document in relevant_documents:
            return 1.0 / rank

    return 0.0


def calculate_retrieval_metrics(
    retrieved_documents: list[str],
    relevant_documents: set[str],
    k: int,
) -> RetrievalMetrics:
    return RetrievalMetrics(
        precision_at_k=precision_at_k(
            retrieved_documents,
            relevant_documents,
            k,
        ),
        recall_at_k=recall_at_k(
            retrieved_documents,
            relevant_documents,
            k,
        ),
        hit_rate_at_k=hit_rate_at_k(
            retrieved_documents,
            relevant_documents,
            k,
        ),
        reciprocal_rank=reciprocal_rank(
            retrieved_documents,
            relevant_documents,
        ),
    )