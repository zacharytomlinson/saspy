"""Record the serial boundary without replacing SAS command or codec logic."""

from unittest.mock import patch


class RecordingSerial:
    def __init__(self, responses, trace, fail_write=None):
        self.responses = list(responses)
        self.trace = trace
        self.fail_write = fail_write
        self.write_count = 0
        self.is_open = True

    def __setattr__(self, name, value):
        if name in {"timeout", "parity", "stopbits"}:
            self.trace.append(["set", name, value])
        object.__setattr__(self, name, value)

    def open(self):
        self.trace.append(["open"])
        self.is_open = True

    def close(self):
        self.trace.append(["close"])
        self.is_open = False

    def flush(self):
        self.trace.append(["flush"])

    def reset_input_buffer(self):
        self.trace.append(["reset_input_buffer"])

    def reset_output_buffer(self):
        self.trace.append(["reset_output_buffer"])

    def write(self, data):
        payload = bytes(data)
        self.trace.append(["write", payload.hex()])
        self.write_count += 1
        if self.write_count == self.fail_write:
            raise OSError("scripted write failure")
        return len(payload)

    def read(self, size):
        # The next item is the bytes available before this read's timeout.
        data = self.responses.pop(0) if self.responses else b""
        if len(data) > size:
            self.responses.insert(0, data[size:])
            data = data[:size]
        self.trace.append(["read", size, data.hex()])
        return data


def normalize(value):
    if isinstance(value, bytes):
        return {"bytes": value.hex()}
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [normalize(item) for item in value]
    if value is NotImplemented:
        return {"not_implemented": True}
    return value


def exercise(client_type, case):
    trace = []
    port = RecordingSerial(case["responses"], trace, case.get("fail_write"))

    def create_port(**kwargs):
        trace.append(["serial", kwargs])
        return port

    with patch("serial.Serial", side_effect=create_port), patch(
        "time.sleep", side_effect=lambda seconds: trace.append(["sleep", seconds])
    ):
        client = client_type("/dev/test-sas", **case.get("connection", {}))
        client.address = 1
        client.machine_n = "01"
        for name, value in case.get("state", {}).items():
            setattr(client, name, value)
        results = []
        for method, args, kwargs in case["calls"]:
            try:
                results.append(normalize(getattr(client, method)(*args, **kwargs)))
            except Exception as error:
                results.append({"exception": type(error).__name__})
        state = {
            name: normalize(getattr(client, name))
            for name in ("address", "machine_n", "denom", "transaction", "last_gpoll_event")
        }
    return {"trace": trace, "results": results, "state": state}
