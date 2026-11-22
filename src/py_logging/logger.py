"""Logger API."""

from typing import Any, TextIO, Optional
from datetime import datetime, timezone

from .logging_levels import LogLevel
from .time_provision.itime_provider import ITimeProvider


class Logger:
    """Implements logging."""
    # static attributes
    _LOG_HEADER:str = "Date and time are in the provided timezone: {tz}.\nRelative timestamps are provided by the time provider passed to the constructor: {time_provider}, measurement unit: us.\n\n### START OF LOG @ {ts} ###\n"
    _LOG_FOOTER: str = "### END OF LOG @ {ts} ###\n"

    # dynamic attributes
    _fp:TextIO

    def __init__(self, fp: TextIO, tz:timezone, time_provider:ITimeProvider):
        """
        Args:
            fp: text read/write handle; this is where data will be logged.
                This must be an already opened text stream.
            tz: timezone used to log the date and time
            time_provider: the provider for the relative timestamps from each logged event
        
        Raises:
            TypeError if the provided arguments are not of the correct type
            RuntimeError if the text stream could not be written to
        """
        if not isinstance(fp, TextIO):
            raise TypeError(f"'fp' must be a valid text stream (TextIO), not '{type(fp)}' !")
        
        self._fp = fp
        self._tz = tz
        self._time_provider = time_provider
        
        # write log header
        if self._fp.closed:
            raise RuntimeError("The text stream is closed, the log header could not be written!")

        self._fp.write(Logger._LOG_HEADER.format(tz = tz,
                                                 time_provider = time_provider.name, 
                                                 ts = datetime.now()))

    def __del__(self):
        """Destructor. Closes the log.
        
        Raises:
            RuntimeError if the log footer could not be written
        """
        if self._fp.closed:
            raise RuntimeError("The text stream has been closed, the log footer could not be written!")   

        # write log footer
        self._fp.write(self._LOG_FOOTER)
        self._fp.close()

    def log(self, data:Any, level:LogLevel):
        """Logs the provided data with the provided logging level.
        
        Args:
            data: any value to be logged
            level: logging level

        Raises:
            RuntimeError if the data could not be logged
        """
        # format message
        msg = f"[{datetime.now()}][{self._time_provider.get_time_us()}] > [{level.value}] {data}\n"

        # write message to stream
        if self._fp.closed:
            raise RuntimeError("The text stream has been closed! Data cannot be logged!")
        
        self._fp.write(str(msg))

    #region convenience-methods
    def log_warning(self, data:Any):
        """Logs a warning."""
        return self.log(data = data, #NOTE: Return in case 'log' will change its signature and return a value in the future
                        level = LogLevel.WARNING)
        
    def log_error(self, data:Any):
        """Logs an error."""
        return self.log(data = data,
                        level = LogLevel.ERROR)

    def log_fatal(self, data:Any):
        """Logs a fatal error."""
        return self.log(data = data,
                        level = LogLevel.FATAL)

    def log_dbg(self, data:Any):
        """Logs a debug messsage."""
        return self.log(data = data,
                        level = LogLevel.DEBUG)
    #endregion