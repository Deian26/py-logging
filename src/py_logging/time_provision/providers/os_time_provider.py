import time

from ..itime_provider import ITimeProvider


class OsTimeProvider(ITimeProvider):
    """Provides time from the OS."""

    def start(self):
        pass # cannot start timer

    def stop(self):
        pass # cannot stop timer

    def pause(self):
        pass # cannot pause timer

    def get_time_ns(self) -> int:
        return time.time_ns()
    