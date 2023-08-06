import pytest
from nx_work_log.nx_work_log import MinuteTimer


@pytest.fixture()
def minute_timer(minute_timer_callback):
    minute_timer = MinuteTimer(minute_timer_callback)

    yield minute_timer

    minute_timer.cancel()
