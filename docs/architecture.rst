Library organization
====================

SASPY is an exploratory, synchronous desktop library. ``Sas`` is the public
entry point and owns both the connection and state retained across calls. Users
can issue the existing methods directly from a REPL, notebook, or script.

Ownership
---------

``client.py`` owns construction and the per-client observations. Address,
denomination, transaction ID, and last general-poll event remain attributes on
that client. The former process-wide response dictionaries now belong to each
client. ``meter_values``, ``aft_values``, ``game_features``, and ``ticket_values`` expose read-only
copies, including zero and disabled values; unobserved fields are absent.

The internal command classes contribute methods to ``Sas`` through inheritance.
They are implementation modules, not independently constructed services or a
second public API. They have no separate connection or state.

.. list-table:: Implementation responsibilities
   :header-rows: 1
   :widths: 25 75

   * - Module
     - Responsibility
   * - ``_connection``
     - Existing serial lifecycle, wake-up/parity sequence, exchange and encoding helpers
   * - ``_commands.machine``
     - Identification, game selection/configuration, controls, clock and authentication
   * - ``_commands.meters``
     - Accounting queries, grouped meters and bill counters
   * - ``_commands.events``
     - General polls and existing event-mode control
   * - ``_commands.aft``
     - Existing transfer, registration, lock and transaction operations
   * - ``_commands.tickets``
     - Validation, ticket information and redemption
   * - ``_commands.bonuses``
     - Legacy bonus and tournament operations
   * - ``_commands.progressives``
     - Existing progressive entry points, including unimplemented ones
   * - ``models``
     - Protocol lookup tables and instance-owned decoded fields
   * - ``examples``
     - Script entry points and optional application YAML configuration

Wire preservation
-----------------

The extraction baseline is saspy commit ``e2224b2``. All 146 existing methods,
including the constructor and unsupported entry points, are retained. Command
bodies were moved mechanically; references to response dictionaries were
redirected to per-client collections. Packet construction, CRC arithmetic, port
operations, requested delays, response reads, follow-up calls and existing error
paths were preserved.

``tests/fixtures/legacy_wire.json`` was captured from that original source
before extraction. The 30 scenarios exercise the actual command, encoding, and
serial-exchange methods against a recording serial port. They compare each
write independently, port settings, open/close and flush operations, read sizes
and bytes, requested sleeps, method results, and retained session attributes.
Cases include empty/partial/corrupt replies, write failure, repeat events,
machine discovery, denomination changes, and AFT registration/cancellation.
Some scenarios deliberately preserve existing failures.

The C library at ``SAS`` commit ``3ad20b7`` supplies three independently asserted
CRC vectors from ``tests/crc_test.c``. Its scheduling and transport implementation
are not the Python behavior baseline. The SAS 6.03 document supplies protocol
intent, not authorization to change the existing byte sequence during extraction.

These checks establish software behavior for the covered scenarios. They do not
measure UART timing or establish EGM compatibility. No EGM was available.

API work after extraction
-------------------------

The constructor's existing parameters, defaults, logging configuration, and
connection/retry policy remain intact in this first pass. Reducing that surface
requires explicitly separating connection settings, learned machine facts, and
host-supplied AFT identity without silently changing effective wire inputs.
In particular, ``key`` is inserted as a length-like byte after command ``72``
in several legacy methods; it must not be renamed as a security credential
without first resolving its actual role.

Existing command return dictionaries retain their historical truthy-value filter.
The new observation properties preserve zero values without changing those return
contracts. Scalar queries are not newly cached. Existing field names and grouping
are retained, so the meter observation collection also contains some machine and
ticket information. A later typed-result pass can refine these representations
against the same serial traces.

Known encoding, framing, response-decoding, and AFT issues remain separate from
this extraction. This includes BCD versus binary game numbers, variable-length
responses, event classification, and transfer completion rules. No new discovery,
retry, acknowledgment, registration, or polling loop is added by this reorganization.
