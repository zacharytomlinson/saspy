"""Instance-owned decoded fields; protocol lookup tables remain class constants."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import TypeAlias


ObservedValue: TypeAlias = int | float | str | bytes


class ObservedFields:
    """Retain observations without sharing them with another client.

    Unknown fields are None. Snapshots contain only observed values and preserve
    zero. The original command return filtering remains available separately.
    """

    fields: tuple[str, ...] = ()

    def __init__(self) -> None:
        self.values: dict[str, ObservedValue | None] = dict.fromkeys(self.fields)

    def get_status(self, key: str) -> ObservedValue | None:
        return self.values.get(key, f"Unknown key: {key}")

    def get_non_empty_status_map(self) -> dict[str, ObservedValue]:
        """Preserve the historical command return shape, including its filtering."""
        return {key: value for key, value in self.values.items() if value}

    def snapshot(self) -> Mapping[str, ObservedValue]:
        return MappingProxyType({key: value for key, value in self.values.items() if value is not None})
