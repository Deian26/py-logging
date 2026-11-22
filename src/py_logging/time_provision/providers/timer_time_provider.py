import time
from typing import Optional

from ..itime_provider import ITimeProvider


class TimerTimeProvider(ITimeProvider):
    """Implements a basic, OS-based timer that provides time."""

    def __init__(self) -> None:
        """
        """

        self._start_time_ns:Optional[int] = None
        self._elapsed_time_ns:int = 0

    def start(self):
        self._start_time_ns = time.perf_counter_ns() # store starting time

    def stop(self):
        # reset times
        self._start_time_ns = None
        self._elapsed_time_ns = 0

    def pause(self):
        if not self._start_time_ns:
            raise RuntimeError("Timer cannot be paused because it was not started yet or was paused and never resumed!")
        
        # compute elapsed time so far
        self._elapsed_time_ns = time.perf_counter_ns() - self._start_time_ns
        self._start_time_ns = None # reset stored timestamp (will be acquired again when 'start()' is called to resume the timer)

    def get_time_ns(self) -> int:
        if not self._start_time_ns:
            raise RuntimeError("Timer cannot be paused because it was not started yet or was paused and never resumed!")
        
        self._elapsed_time_ns += time.perf_counter_ns() - self._start_time_ns
        return self._elapsed_time_ns