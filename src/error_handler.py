"""Compatibility imports for the original exception module."""

from saspy.errors import (
    ErrorHandler,
    BadCRC,
    AFTBadAmount,
    BadTransactionID,
    NoSasConnection,
    SASOpenError,
    EMGGpollBadResponse,
    BadCommandIsRunning,
)

__all__ = ['ErrorHandler', 'BadCRC', 'AFTBadAmount', 'BadTransactionID', 'NoSasConnection', 'SASOpenError', 'EMGGpollBadResponse', 'BadCommandIsRunning']
