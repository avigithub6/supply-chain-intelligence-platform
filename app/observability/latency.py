import time


class LatencyTimer:
    """Measure elapsed execution time in milliseconds."""

    def __init__(self) -> None:
        self._start_time = time.perf_counter()

    def elapsed_ms(self) -> float:
        """Return elapsed time in milliseconds."""
        elapsed_seconds = (
            time.perf_counter() - self._start_time
        )

        return elapsed_seconds * 1000