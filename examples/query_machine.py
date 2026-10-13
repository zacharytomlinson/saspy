"""Query an EGM using an installed saspy checkout."""

import argparse

from saspy import Sas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("port", help="Serial device, for example /dev/ttyUSB0 or COM3")
    args = parser.parse_args()

    machine = Sas(port=args.port)
    try:
        print("Address:", machine.start())
        print("Denomination:", machine.gaming_machine_id())
        print("Credits:", machine.current_credits())
        machine.meters_11_15(denom=False)
        print("Observed meters:", dict(machine.meter_values))
    finally:
        machine.close()


if __name__ == "__main__":
    main()
