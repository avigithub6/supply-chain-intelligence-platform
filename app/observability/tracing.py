import logging
from dataclasses import dataclass

from app.observability.latency import LatencyTimer
from app.observability.request_ids import generate_request_id


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RAGExecutionMetrics:
    request_id: str
    total_latency_ms: float
    retrieval_count: int
    success: bool
    error_type: str | None = None


class RAGExecutionTracker:
    """
    Track one RAG request from start to completion.

    Captures:
    - request ID
    - total latency
    - number of retrieved chunks
    - success/failure
    - error type
    """

    def __init__(self) -> None:
        self.request_id = generate_request_id()
        self.timer = LatencyTimer()

    def finish(
        self,
        retrieval_count: int,
    ) -> RAGExecutionMetrics:
        """Mark a RAG request as successful."""

        metrics = RAGExecutionMetrics(
            request_id=self.request_id,
            total_latency_ms=self.timer.elapsed_ms(),
            retrieval_count=retrieval_count,
            success=True,
        )

        logger.info(
            "RAG execution completed | "
            "request_id=%s | "
            "latency_ms=%.2f | "
            "retrieval_count=%d | "
            "success=%s",
            metrics.request_id,
            metrics.total_latency_ms,
            metrics.retrieval_count,
            metrics.success,
        )

        return metrics

    def fail(
        self,
        error: Exception,
    ) -> RAGExecutionMetrics:
        """Mark a RAG request as failed."""

        metrics = RAGExecutionMetrics(
            request_id=self.request_id,
            total_latency_ms=self.timer.elapsed_ms(),
            retrieval_count=0,
            success=False,
            error_type=type(error).__name__,
        )

        logger.error(
            "RAG execution failed | "
            "request_id=%s | "
            "latency_ms=%.2f | "
            "success=%s | "
            "error_type=%s | "
            "error=%s",
            metrics.request_id,
            metrics.total_latency_ms,
            metrics.success,
            metrics.error_type,
            str(error),
        )

        return metrics