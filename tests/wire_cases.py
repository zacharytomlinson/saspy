"""Representative existing exchanges, including the legacy failure paths."""


def response(command, payload=b"", address=1):
    # Independent bit-at-a-time CRC for scripted inbound frames.
    data = bytes([address, command]) + payload
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0x8408 if crc & 1 else 0)
    return data + crc.to_bytes(2, "little")


CASES = {
    "discover_address": {
        "responses": [b"\x01"], "calls": [("start", [], {})],
    },
    "discover_after_empty_read": {
        "responses": [b"", b"\x02"], "calls": [("start", [], {})],
    },
    "credits_scaled": {
        "responses": [response(0x1A, bytes.fromhex("00001234"))],
        "calls": [("current_credits", [], {})],
    },
    "credits_raw": {
        "responses": [response(0x1A, bytes.fromhex("00001234"))],
        "calls": [("current_credits", [], {"denom": False})],
    },
    "credits_zero": {
        "responses": [response(0x1A, bytes(4))],
        "calls": [("current_credits", [], {})],
    },
    "custom_wire_settings": {
        "connection": {"timeout": 0.5, "poll_address": 0x80, "wait_for_wake_up": 0.04},
        "responses": [response(0x1A, bytes(4))],
        "calls": [("current_credits", [], {})],
    },
    "empty_reply": {"responses": [b""], "calls": [("current_credits", [], {})]},
    "partial_reply": {"responses": [b"\x01"], "calls": [("current_credits", [], {})]},
    "bad_crc": {
        "responses": [bytes.fromhex("011a000012340000")],
        "calls": [("current_credits", [], {})],
    },
    "different_command": {
        "responses": [response(0x11, bytes(4))],
        "calls": [("current_credits", [], {})],
    },
    "write_failure": {
        "responses": [b""], "fail_write": 2,
        "calls": [("current_credits", [], {})],
    },
    "startup_ack": {"responses": [b"\x01"], "calls": [("startup", [], {})]},
    "startup_nack": {"responses": [b"\x81"], "calls": [("startup", [], {})]},
    "startup_timeout": {"responses": [b""], "calls": [("startup", [], {})]},
    "general_poll_repetition": {
        "responses": [b"\x11", b"\x11", b"\x12"],
        "calls": [("events_poll", [], {})] * 3,
    },
    "general_poll_unknown": {"responses": [b"\xfe"], "calls": [("events_poll", [], {})]},
    "general_poll_empty": {"responses": [b""], "calls": [("events_poll", [], {})]},
    "rte_enable": {
        "responses": [b"\x01"], "calls": [("en_dis_rt_event_reporting", [True], {})],
    },
    "grouped_meters": {
        "responses": [response(0x19, bytes.fromhex("0000012300000000000004560000078900000002"))],
        "calls": [("meters_11_15", [], {"denom": False})],
    },
    "game_meters_binary_number": {
        "responses": [response(0x52, bytes.fromhex("001000000001000000020000000300000004"))],
        "calls": [("game_meters", [16], {"denom": False})],
    },
    "game_meters_selected_game": {
        "responses": [response(0x55, b"\x00\x01"), response(0x52, b"\x00\x01" + bytes(16))],
        "calls": [("game_meters", [], {})],
    },
    "machine_denomination_then_credits": {
        "responses": [response(0x1F, b"ABCDE\x04" + bytes(14)), response(0x1A, bytes.fromhex("00000012"))],
        "calls": [("gaming_machine_id", [], {}), ("current_credits", [], {})],
    },
    "aft_registration": {
        "responses": [response(0x73, bytes(30))],
        "calls": [("aft_register_gaming_machine", [], {})],
    },
    "aft_register": {
        "responses": [response(0x73, bytes(30))], "calls": [("aft_register", [], {})],
    },
    "aft_unregister": {
        "responses": [response(0x73, bytes(30))], "calls": [("aft_unregister", [], {})],
    },
    "aft_last_transaction": {
        "responses": [response(0x72, bytes(86))], "calls": [("aft_get_last_trx", [], {})],
    },
    "aft_cancel_followup": {
        "state": {"transaction": 0x2020202020202020202020202020202021},
        "responses": [response(0x73, bytes(30)), response(0x72, bytes(86)), response(0x73, bytes(30))],
        "calls": [("aft_cancel_request", [], {})],
    },
    "ticket_info": {
        "responses": [b"\x01"], "calls": [("cash_out_ticket_info", [], {})],
    },
    "legacy_bonus": {
        "responses": [b"\x01"], "calls": [("initiate_legacy_bonus_pay", [1.0], {"games": 1})],
    },
    "flush_and_close": {
        "responses": [], "calls": [("flush", [], {}), ("flush_hard", [], {}), ("close", [], {})],
    },
}
