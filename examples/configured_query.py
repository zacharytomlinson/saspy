"""Load application settings from YAML and query an EGM."""

import argparse

from saspy import Sas

from config_handler import ConfigHandler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="Path to the application's YAML settings")
    args = parser.parse_args()

    config = ConfigHandler(args.config)
    config.read_config_file()
    machine = Sas(
        port=config.get_config_value("connection", "serial_port"),
        timeout=config.get_config_value("connection", "timeout"),
        poll_address=config.get_config_value("events", "poll_address"),
        denom=config.get_config_value("machine", "denomination"),
        asset_number=config.get_config_value("machine", "asset_number"),
        reg_key=config.get_config_value("machine", "reg_key"),
        pos_id=config.get_config_value("machine", "pos_id"),
        key=str(config.get_config_value("security", "key")),
        debug_level=config.get_config_value("debug", "level"),
        perpetual=config.get_config_value("connection", "infinite"),
    )
    try:
        print("Address:", machine.start())
        print("Denomination:", machine.gaming_machine_id())
        print("Credits:", machine.current_credits())
    finally:
        machine.close()


if __name__ == "__main__":
    main()
