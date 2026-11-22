"""Time provider interface."""

from abc import ABC, abstractmethod
from typing import final


class ITimeProvider(ABC):
    """Defines classes that provide the date and time for logging events.
    The max resolution is us, but actual implementations may not provide time to
    that level."""

    # static
    _NOT_IMPL_ERROR_MSG: str = "This interface must be implemented by an implementing class!"

    @property
    @final
    def name(self) -> str:
        """Time provider name."""
        return self.__class__.__name__

    @abstractmethod
    def start(self):
        """Starts or resumes the time counting, if possible.
        If the provider cannot start/stop/restart/pause the time, this does nothing.
        
        Raises:
            RuntimeError if the procedure fails
        """

        raise NotImplementedError(ITimeProvider._NOT_IMPL_ERROR_MSG)

    @abstractmethod
    def stop(self):
        """Stops the time counting, if possible.
        If the provider cannot start/stop/restart/pause the time, this does nothing.
        
        Raises:
            RuntimeError if the procedure fails
        """

        raise NotImplementedError(ITimeProvider._NOT_IMPL_ERROR_MSG)

    @abstractmethod
    def pause(self):
        """Pauses the time counting, if possible.
        If the provider cannot start/stop/restart/pause the time, this does nothing.
        
        Raises:
            RuntimeError if the procedure fails
        """

        raise NotImplementedError(ITimeProvider._NOT_IMPL_ERROR_MSG)

    @abstractmethod
    def get_time_ns(self) -> int:
        """Returns the provider's current time in ns.
        If the provider does not support ns level time, this will 
        return the highes resolution support converted to ns."""

        raise NotImplementedError(ITimeProvider._NOT_IMPL_ERROR_MSG)

    @final
    def get_time_us(self) -> float:
        """Returns the provider's time in us."""
        return self.get_time_ns() / 1_000

    @final
    def get_time_ms(self) -> float:
        """Returns the provider's current time in ms."""
        return self.get_time_us() / 1_000

    @final
    def get_time_s(self) -> float:
        """Returns the provider's current time in seconds."""
        return self.get_time_ms() / 1_000
