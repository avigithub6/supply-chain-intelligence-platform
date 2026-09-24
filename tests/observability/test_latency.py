import time

from app.observability.latency import LatencyTimer


def test_latency_timer_returns_non_negative_value() -> None:
    timer = LatencyTimer()

    latency = timer.elapsed_ms()

    assert latency >= 0.0


def test_latency_timer_measures_elapsed_time() -> None:
    timer = LatencyTimer()

    time.sleep(0.001)

    latency = timer.elapsed_ms()

    assert latency > 0.0