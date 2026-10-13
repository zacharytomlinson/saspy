"""Characterize the Python serial behavior independently of spec corrections."""

import json
from pathlib import Path

import pytest

from saspy import Sas

from .serial_recorder import exercise
from .wire_cases import CASES


BASELINE = json.loads((Path(__file__).parent / "fixtures/legacy_wire.json").read_text())


@pytest.mark.parametrize("name", CASES)
def test_legacy_exchange_is_preserved(name):
    assert exercise(Sas, CASES[name]) == BASELINE["cases"][name]
