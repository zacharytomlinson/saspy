"""Compatibility import for existing scripts; new code can use ``saspy``."""

from saspy import Sas, __version__

__all__ = ["Sas", "__version__"]
