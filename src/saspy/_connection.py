import serial
import time
import binascii
from . import _crc as Crc
from ._decorators import deprecated
from .errors import BadCRC, BadCommandIsRunning, NoSasConnection, SASOpenError


class SerialConnection:
    """Existing connection operations used by the Sas client."""

    def is_open(self):
        return self.connection.is_open

    def flush(self):
        try:
            if self.is_open() == False:
                self.open()
            self.connection.flush()
        except Exception as e:
            self.log.error(e, exc_info=True)

    def flush_hard(self):
        """Flush the serial buffer in input and output"""
        try:
            if not self.is_open():
                self.open()
            self.connection.reset_output_buffer()
            self.connection.reset_input_buffer()
        except Exception as e:
            self.log.error(e, exc_info=True)

    def start(self):
        """Warm Up the connection to the VLT"""

        self.log.info("Connecting to the machine...")
        while True:
            if not self.is_open():
                try:
                    self.open()
                    if not self.is_open():
                        self.log.error("Port is NOT open")
                except SASOpenError:
                    self.log.critical("No SAS Port")
                except Exception as e:
                    self.log.critical(e, exc_info=True)
            else:
                self.connection.reset_output_buffer()
                self.connection.reset_input_buffer()
                response = self.connection.read(1)

                if not response:
                    self.log.error("No SAS Connection")
                    time.sleep(1)

                if response != b"":
                    self.address = int(binascii.hexlify(response))
                    self.machine_n = response.hex()
                    self.log.info("Address Recognized " + str(self.address))
                    break
                else:
                    self.log.error("No SAS Connection")
                    time.sleep(1)

        self.close()
        return self.machine_n

    def close(self):
        """Close the connection to the serial port"""
        self.connection.close()

    def open(self):
        """Open connection to the VLT"""
        try:
            if self.connection.is_open is not True:
                self.connection.open()
        except:
            raise SASOpenError

    def _conf_event_port(self):
        """Do magick to make SAS Happy and work with their effing wakeup bit"""
        self.open()
        self.connection.flush()
        self.connection.timeout = self.poll_timeout
        self.connection.parity = serial.PARITY_NONE
        self.connection.stopbits = serial.STOPBITS_TWO
        self.connection.reset_input_buffer()

    def _conf_port(self):
        """As per _conf_event_port Do magick to make SAS Happy and work with their effing parity"""
        self.open()
        self.connection.flush()
        self.connection.timeout = self.timeout
        self.connection.parity = serial.PARITY_MARK
        self.connection.stopbits = serial.STOPBITS_ONE
        self.connection.reset_input_buffer()

    def _send_command(
        self, command, no_response=False, timeout=None, crc_need=True, size=1
    ):
        """Main function to physically send commands to the VLT"""
        try:
            buf_header = [self.address]
            self._conf_port()

            buf_header.extend(command)

            if crc_need:
                buf_header.extend(Crc.calculate(bytes(buf_header)))

            self.connection.write([self.poll_address, self.address])
            time.sleep(self.wait_for_wake_up)
            self.close()
            self.connection.parity = serial.PARITY_SPACE
            self.open()
            self.connection.write((buf_header[1:]))

        except Exception as e:
            self.log.error(e, exc_info=True)

        try:
            response = self.connection.read(size)

            if no_response:
                try:
                    return int(binascii.hexlify(response))
                except ValueError as e:
                    self.log.critical("no sas response %s" % (str(buf_header[1:])))
                    return None
            else:
                if not response:
                    raise NoSasConnection
                elif int(binascii.hexlify(response)[2:4], 16) != buf_header[1]:
                    raise BadCommandIsRunning(
                        "response %s run %s"
                        % (
                            binascii.hexlify(response),
                            binascii.hexlify(bytearray(buf_header)),
                        )
                    )

            response = Crc.validate(response)

            self.log.debug("sas response %s", binascii.hexlify(response))

            return response

        except Exception as e:
            self.log.critical(e, exc_info=True)
        return None

    @deprecated("use utils.Crc validation fuction")
    def _check_response(rsp):
        """Function in charge of the CRC Check"""
        if rsp == "":
            raise NoSasConnection

        mac_crc = [int.from_bytes(rsp[-2:-1]), int.from_bytes(rsp[-1:])]
        my_crc = Crc.calculate(rsp[0:-2])

        if mac_crc != my_crc:
            raise BadCRC(binascii.hexlify(rsp))
        else:
            return rsp[1:-2]

    def _bcd_coder_array(self, value=0, length=4):
        return self._int_to_bcd(value, length)

    @staticmethod
    def _int_to_bcd(
        number=0,
        length=5,
    ):
        n = m = bval = 0
        p = length - 1
        result = []
        for i in range(0, length):
            result.extend([0x00])

        while p >= 0:
            if number != 0:
                digit = number % 10
                number = number / 10
                m = m + 1
            else:
                digit = 0

            if n & 1:
                bval |= digit << 4
                result[p] = bval
                p = p - 1
                bval = 0
            else:
                bval = digit

            n = n + 1

        return result
