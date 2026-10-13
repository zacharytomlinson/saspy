from ..models import GPoll
from ..errors import EMGGpollBadResponse, NoSasConnection


class EventsCommands:
    """Existing events operations used by the Sas client."""

    def events_poll(self):
        """Events Poll function

        See Also
        --------
        WiKi : https://github.com/zacharytomlinson/saspy/wiki/4.-Important-To-Know#event-reporting
        """
        self._conf_event_port()

        cmd = [0x80 + self.address]
        self.connection.write([self.poll_address])

        try:
            self.connection.write(cmd)
            event = self.connection.read(1)
            if event == "":
                raise NoSasConnection
            event = GPoll.GPoll.get_status(event.hex())
        except KeyError as e:
            raise EMGGpollBadResponse
        except Exception as e:
            raise e

        if self.last_gpoll_event != event:
            self.last_gpoll_event = event
        else:
            event = GPoll.GPoll.STATUS_MAP["00"]

        return event

    def en_dis_rt_event_reporting(self, enable=False):
        """For situations where real time event reporting is desired, the gaming machine can be configured to report events in response to long polls as well as general polls. This allows events such as reel stops, coins in, game end, etc., to be reported in a timely manner
        Returns
        -------
        bool
            True if successful, False otherwise.

        See Also
        --------
        WiKi : https://github.com/zacharytomlinson/saspy/wiki/4.-Important-To-Know#event-reporting
        """
        if not enable:
            enable = [0]
        else:
            enable = [1]

        cmd = [0x0E]
        cmd.extend(bytearray(enable))

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    @staticmethod
    def event_response_to_long_poll():
        # TODO: FF
        return NotImplemented
