from unittest.mock import patch

import pytest

from saspy import Sas
from saspy.models.AftStatements import AftStatements
from saspy.models.GameFeatures import GameFeatures
from saspy.models.Meters import Meters
from saspy.models.TitoStatement import Tito

from .serial_recorder import RecordingSerial
from .wire_cases import response


@pytest.mark.parametrize("model", [Meters, AftStatements, GameFeatures, Tito])
def test_observations_are_independent_and_preserve_zero(model):
    first, second = model(), model()
    field = first.fields[0]
    assert first.get_status(field) is None
    assert dict(first.snapshot()) == {}

    first.values[field] = 0
    snapshot = first.snapshot()
    assert dict(snapshot) == {field: 0}
    assert dict(second.snapshot()) == {}

    first.values[field] = 12
    assert snapshot[field] == 0
    assert first.snapshot()[field] == 12
    with pytest.raises(TypeError):
        snapshot[field] = 5


def test_clients_retain_separate_meter_observations_and_stable_results():
    payload = bytes.fromhex("0000012300000000000004560000078900000002")
    ports = [
        RecordingSerial([response(0x19, payload), response(0x19, bytes(20))], []),
        RecordingSerial([response(0x19, bytes(20))], []),
    ]
    with patch("serial.Serial", side_effect=ports), patch("time.sleep"):
        first, second = Sas("/dev/first"), Sas("/dev/second")
        first.address = second.address = 1
        original = first.meters_11_15(denom=False)
        snapshot = first.meter_values
        assert snapshot["total_bet_meter"] == 123
        assert snapshot["total_win_meter"] == 0
        assert dict(second.meter_values) == {}
        assert second.meters_11_15(denom=False) == {}
        assert second.meter_values["total_bet_meter"] == 0
        first.meters_11_15(denom=False)

    assert first.meter_values["total_bet_meter"] == 0
    assert snapshot["total_bet_meter"] == original["total_bet_meter"] == 123


def test_original_import_paths_reexport_the_same_public_types():
    from error_handler import BadCRC
    from sas import Sas as OriginalSas
    from saspy.errors import BadCRC as PackageBadCRC

    assert OriginalSas is Sas
    assert BadCRC is PackageBadCRC
