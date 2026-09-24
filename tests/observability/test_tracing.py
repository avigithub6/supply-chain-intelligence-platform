from app.observability.tracing import (
    RAGExecutionTracker,
)


def test_tracker_generates_request_id() -> None:
    tracker = RAGExecutionTracker()

    assert tracker.request_id
    assert isinstance(
        tracker.request_id,
        str,
    )


def test_finish_returns_success_metrics() -> None:
    tracker = RAGExecutionTracker()

    metrics = tracker.finish(
        retrieval_count=3
    )

    assert metrics.request_id == tracker.request_id
    assert metrics.retrieval_count == 3
    assert metrics.total_latency_ms >= 0.0
    assert metrics.success is True
    assert metrics.error_type is None


def test_fail_returns_error_metrics() -> None:
    tracker = RAGExecutionTracker()

    error = RuntimeError(
        "Qdrant connection failed"
    )

    metrics = tracker.fail(error)

    assert metrics.request_id == tracker.request_id
    assert metrics.retrieval_count == 0
    assert metrics.total_latency_ms >= 0.0
    assert metrics.success is False
    assert metrics.error_type == "RuntimeError"


def test_each_tracker_has_unique_request_id() -> None:
    first_tracker = RAGExecutionTracker()
    second_tracker = RAGExecutionTracker()

    assert (
        first_tracker.request_id
        != second_tracker.request_id
    )