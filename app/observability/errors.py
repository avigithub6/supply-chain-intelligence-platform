import logging


logger = logging.getLogger(__name__)


def log_observability_error(
    *,
    request_id: str,
    operation: str,
    error: Exception,
) -> None:
    """Log an application error with its request ID."""

    logger.exception(
        "Operation failed | "
        "request_id=%s | "
        "operation=%s | "
        "error_type=%s | "
        "error=%s",
        request_id,
        operation,
        type(error).__name__,
        str(error),
    )