class Transfer:
    """Class representing the transfer info for AFT"""

    TYPE_MAP = {
        "00": "Transfer in-house amount from host to gaming machine",
        "10": "Transfer bonus coin out win amount from host to gaming machine",
        "11": "Transfer bonus jackpot win amount from host to gaming machine (force attendant pay lockup)",
        "20": "Transfer in-house amount from host to ticket (only one amount type allowed per transfer)",
        "40": "Transfer debit amount from host to gaming machine",
        "60": "Transfer debit amount from host to ticket",
        "80": "Transfer in-house amount from gaming machine to host",
        "90": "Transfer win amount (in-house) from gaming machine to host",
    }

    STATUS_MAP = {
        "00": "Full transfer successful",
        "01": "Partial transfer successful Binary codes 010xxxxx indicate transfer pending",
        "40": "Transfer pending (not complete)",
        "80": "Transfer cancelled by host",
        "81": "Transaction ID not unique (same as last successful transfer logged in history)",
        "82": "Not a valid transfer function (unsupported type, amount, index, etc.)",
        "83": "Not a valid transfer amount or expiration (non-BCD, etc.)",
        "84": "Transfer amount exceeds the gaming machine transfer limit",
        "85": "Transfer amount not an even multiple of gaming machine denomination",
        "86": "Gaming machine unable to perform partial transfers to the host",
        "87": "Gaming machine unable to perform transfers at this time (door open, tilt, disabled, cashout in progress, etc.)",
        "88": "Gaming machine not registered (required for debit transfers)",
        "89": "Registration key does not match",
        "8a": "No POS ID (required for debit transfers)",
        "8b": "No won credits available for cashout",
        "8c": "No gaming machine denomination set (unable to perform cents to credits conversion)",
        "8d": "Expiration not valid for transfer to ticket (already expired)",
        "8e": "Transfer to ticket device not available",
        "8f": "Unable to accept transfer due to existing restricted amounts from different pool",
        "90": "Unable to print transaction receipt (receipt device not currently available)",
        "91": "Insufficient data to print transaction receipt (required fields missing)",
        "92": "Transaction receipt not allowed for specified transfer type",
        "93": "Asset number zero or does not match",
        "94": "Gaming machine not locked (transfer specified lock required)",
        "95": "Transaction ID not valid",
        "9f": "Unexpected error Binary codes 110xxxxx indicate incompatible or unsupported poll",
        "c0": "Not compatible with current transfer in progress",
        "c1": "Unsupported transfer code Binary codes 111xxxxx indicate no transfer information available",
        "ff": "No transfer information available",
    }

    @classmethod
    def get_status(cls, key):
        """Get the status value for the given key.

        Args:
            key (str): The key for the status.

        Returns:
            str: The corresponding status value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.STATUS_MAP.get(key, f"Unknown key: {key}")

    @classmethod
    def get_type(cls, key):
        """Get the type value for the given key.

        Args:
            key (str): The key for the type.

        Returns:
            str: The corresponding type value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.TYPE_MAP.get(key, f"Unknown key: {key}")


class Statements:
    """Class representing the statements for AFT"""

    STATUS_MAP = {
        "registration_status": [],
        "asset_number": [],
        "registration_key": [],
        "POS_ID": [],
        "transaction_buffer_position": [],
        "transfer_status": [],
        "receipt_status": [],
        "transfer_type": [],
        "cashable_amount": [],
        "restricted_amount": [],
        "nonrestricted_amount": [],
        "transfer_flags": [],
        "transaction_ID_lenght": [],
        "transaction_ID": [],
        "transaction_date": [],
        "transaction_time": [],
        "expiration": [],
        "pool_ID": [],
        "cumulative_casable_amount_meter_size": [],
        "cumulative_casable_amount_meter": [],
        "cumulative_restricted_amount_meter_size": [],
        "cumulative_restricted_amount_meter": [],
        "cumulative_nonrestricted_amount_meter_size": [],
        "cumulative_nonrestricted_amount_meter": [],
        "game_lock_status": [],
        "avilable_transfers": [],
        "host_cashout_status": [],
        "AFT_status": [],
        "max_buffer_index": [],
        "current_cashable_amount": [],
        "current_restricted_amount": [],
        "current_non_restricted_amount": [],
        "restricted_expiration": [],
        "restricted_pool_ID": [],
    }

    @classmethod
    def get_status(cls, key):
        """Get the status value for the given key.

        Args:
            key (str): The key for the status.

        Returns:
            str: The corresponding status value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.STATUS_MAP.get(key, f"Unknown key: {key}")

    @classmethod
    def get_non_empty_status_map(cls):
        """Return a dictionary containing only keys with non-empty values."""
        non_empty_map = {key: value for key, value in cls.STATUS_MAP.items() if value}
        return non_empty_map


class Registration:
    """Class representing the registration for AFT"""

    STATUS_MAP = {
        "00": "Gaming machine registration ready",
        "01": "Gaming machine registered",
        "40": "Gaming machine registration pending",
        "80": "Gaming machine not registered",
    }

    @classmethod
    def get_status(cls, key):
        """Get the status value for the given key.

        Args:
            key (str): The key for the status.

        Returns:
            str: The corresponding status value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.STATUS_MAP.get(key, f"Unknown key: {key}")

class Receipt:
    """Class representing the receipt for AFT"""

    STATUS_MAP = {
        "00": "Receipt printed",
        "20": "Receipt printing in progress (not complete)",
        "40": "Receipt pending (not complete)",
        "ff": "No receipt requested or receipt not printed",
    }

    @classmethod
    def get_status(cls, key):
        """Get the status value for the given key.

        Args:
            key (str): The key for the status.

        Returns:
            str: The corresponding status value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.STATUS_MAP.get(key, f"Unknown key: {key}")


class Lock:
    """Class representing the lock for AFT"""

    STATUS_MAP = {
        "00": "Game locked",
        "40": "Game lock pending",
        "ff": "Game not locked",
    }

    @classmethod
    def get_status(cls, key):
        """Get the status value for the given key.

        Args:
            key (str): The key for the status.

        Returns:
            str: The corresponding status value or an error message if the key is not found.
        """
        # Use get() method to retrieve the value, or return an error message.
        return cls.STATUS_MAP.get(key, f"Unknown key: {key}")