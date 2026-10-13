"""Plug-and-play exploration of the SAS protocol."""

from .client import Sas
from . import errors

__version__ = "2.0.0"

__all__ = ["Sas", "errors", "__version__"]
