"""The public, stateful SAS client."""

import logging
import time
from collections.abc import Mapping

import serial
from multiprocessing import log_to_stderr

from ._commands.events import EventsCommands
from ._commands.aft import AftCommands
from ._commands.tickets import TicketsCommands
from ._commands.bonuses import BonusesCommands
from ._commands.progressives import ProgressivesCommands
from ._commands.meters import MetersCommands
from ._commands.machine import MachineCommands
from ._connection import SerialConnection
from .models.Meters import Meters
from .models.AftStatements import AftStatements
from .models.GameFeatures import GameFeatures
from .models.TitoStatement import Tito
from .models._observed import ObservedValue


class Sas(
    SerialConnection,
    EventsCommands,
    AftCommands,
    TicketsCommands,
    BonusesCommands,
    ProgressivesCommands,
    MetersCommands,
    MachineCommands,
):
    """Explore an EGM through a serial SAS connection.

    Each client retains its own observations and transaction state. Existing
    constructor defaults and serial sequencing are retained for compatibility.
    """

    def __init__(
        self,
        port,  # Serial Port full Address
        timeout=2,  # Connection timeout
        poll_address=0x82,  # Poll Address
        denom=0.01,  # Denomination
        asset_number="01000000",  # Asset Number
        reg_key="0000000000000000000000000000000000000000",  # Reg Key
        pos_id="B374A402",  # Pos ID
        key="44",  # Key
        debug_level="DEBUG",  # Debug Level
        perpetual=False,  # When this is true the lib will try forever to connect to the serial
        check_last_transaction=True,
        wait_for_wake_up=0.00,
    ):
        self._meters = Meters()
        self._aft = AftStatements()
        self._features = GameFeatures()
        self._tickets = Tito()

        # Let's address some internal var
        self.poll_timeout = timeout
        self.address = None
        self.machine_n = None
        self.check_last_transaction = check_last_transaction
        self.denom = denom
        self.asset_number = asset_number
        self.reg_key = reg_key
        self.pos_id = pos_id
        self.transaction = None
        self.my_key = key
        self.poll_address = poll_address
        self.perpetual = perpetual
        self.wait_for_wake_up = wait_for_wake_up

        # Init the Logging system
        self.log = log_to_stderr()
        self.log.setLevel(logging.getLevelName(debug_level))
        self.last_gpoll_event = None

        # Open the serial connection
        while 1:
            try:
                self.connection = serial.Serial(
                    port=port,
                    baudrate=19200,
                    timeout=timeout,
                )
                self.close()
                self.timeout = timeout
                self.log.info("Connection Successful")
                break
            except:
                if not self.perpetual:
                    self.log.critical(
                        "Error while connecting to the machine....Quitting..."
                    )
                    exit(1)  # Make a graceful exit since it's expected behaviour

                self.log.critical("Error while connecting to the machine....")
                time.sleep(1)

        return

    @property
    def meter_values(self) -> Mapping[str, ObservedValue]:
        """A read-only snapshot of observed meter fields, including zero values."""
        return self._meters.snapshot()

    @property
    def aft_values(self) -> Mapping[str, ObservedValue]:
        """A read-only snapshot of observed AFT response fields."""
        return self._aft.snapshot()

    @property
    def game_features(self) -> Mapping[str, ObservedValue]:
        """A read-only snapshot of observed game features, including disabled ones."""
        return self._features.snapshot()

    @property
    def ticket_values(self) -> Mapping[str, ObservedValue]:
        """A read-only snapshot of fields decoded by the ticket response model."""
        return self._tickets.snapshot()

