# SASPY
[![Documentation Status](https://readthedocs.org/projects/saspy/badge/?version=latest)](https://saspy.readthedocs.io/en/latest/?badge=latest)

<p align="center">
<img src="https://github.com/zacharytomlinson/saspy/assets/15037424/e8a8efc8-e83f-44f9-9ca1-7543a280e6b3" width="300" height="auto">
</p>
Slots Accounting System (SAS) Protocol is a standard when comes to Slot Machine and VLTs. And because we were bored and with not enough things to do we decided to build this library

## Scope
SASPY is a Python library for exploring an EGM through an RS-232 adapter. One
`Sas` client owns its connection, transaction state, and decoded observations.
Applications decide when to poll and which operations to perform.

Install this checkout with Python 3.11 or later:

```bash
python -m pip install -e .
```

```python
from saspy import Sas

machine = Sas(port="/dev/ttyUSB0")
try:
    print(machine.start())
    print(machine.gaming_machine_id())
    print(machine.current_credits())

    machine.meters_11_15(denom=False)
    readings = machine.meter_values
    print(dict(readings))
finally:
    machine.close()
```

`meter_values`, `aft_values`, `game_features`, and `ticket_values` expose read-only snapshots of
fields decoded by the existing response models. An unobserved field is absent;
an observed zero is present. Snapshots remain unchanged after subsequent polls,
and clients do not share observations. Individual scalar queries keep their
existing return values; this first extraction does not add caching to them.

Existing `from sas import Sas` and `from error_handler import BadCRC` imports
remain available after installation. New code can use `saspy` and `saspy.errors`.

The first package extraction preserves existing constructor defaults, command
encodings, serial operations, requested delays, and command return conventions.
It does not introduce protocol corrections or claim EGM validation. The ownership
map, remaining API work, and verification boundaries are in
[the architecture notes](docs/architecture.rst).

Examples live in `examples/`. To use the optional YAML configuration example,
install `python -m pip install -e '.[examples]'` and run
`python examples/configured_query.py examples/config.yml`. The library itself
does not load a configuration file.

For hardware-free checks:

```bash
python -m pip install -e '.[test]'
python -m pytest
```

# Documentation
Since this library is still under heavy development (but at least is working !) comments are still not complete and there is a draft of documentation into `docs/` folder. 

All the latest documentation regarding this library can be found on [Read The Docs](https://saspy.readthedocs.io/)

In the meantime feel free to checkout the [WiKi of this project](https://github.com/zacharytomlinson/saspy/wiki) where you are gonna find response and solutions to common problems we faced during our journey

# Contribute
Not many rules. Fork the repo, write your code, create pull request. Remember to use black for formatting and give a shot to pylint.

## Issue & Implementation
Please, use the [Issues tab](https://github.com/zacharytomlinson/saspy/issues) to propose an eventual enhancement or to submit an issue.

# Authors
This project was initiated by [thomas-pythonas](https://github.com/thomas-pythonas) in 2018 and has no update since then.

Current author and mantainer are:

- [Zachary Tomlinson](https://github.com/zacharytomlinson)
- [Antonio D'Angelo](https://github.com/well-it-wasnt-me)

# Thanks to
* [Grigor Kolev](https://github.com/dedalgr) for his precious help
