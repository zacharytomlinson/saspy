import json
from pathlib import Path

import pytest

from saspy import _crc


LEGACY = json.loads((Path(__file__).parent / "fixtures/legacy_crc.json").read_text())


@pytest.mark.parametrize(
    "payload, expected",
    [
        ("021a00000000", "bef0"),
        ("011c0024860500215555025104050000000000001061000001600000008900000185", "5a59"),
        ("0274ff", "642d"),
    ],
)
def test_crc_matches_existing_c_vectors(payload, expected):
    # SAS 3ad20b7, tests/crc_test.c: existing asserted vectors, not timing rules.
    assert bytes(_crc.calculate(bytes.fromhex(payload))).hex() == expected


@pytest.mark.parametrize("vector", LEGACY["vectors"], ids=lambda vector: vector["name"])
@pytest.mark.parametrize("mode", _crc.Endianness, ids=lambda mode: mode.name)
def test_crc_preserves_original_python_outputs(vector, mode):
    # Captured from the original utils/Crc.py at LEGACY["revision"]. Keep its
    # existing seed and byte-order behavior, even where it looks surprising.
    actual = _crc.calculate(bytes.fromhex(vector["payload"]), vector["seed"], mode)
    assert actual == vector["expected"][mode.name]
