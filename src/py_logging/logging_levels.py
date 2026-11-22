"""Stores logging levels."""

from enum import StrEnum

class LogLevel(StrEnum):
    """Logging levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"
    DEBUG = "DEBUG"
    