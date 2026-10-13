import binascii
import datetime
from ..models import Denomination


class MachineCommands:
    """Existing machine operations used by the Sas client."""

    def shutdown(self):
        """Make the VLT unplayable
        :note: This is a LONG POLL COMMAND
        """
        # [0x01]
        if self._send_command([0x01], True, crc_need=True) == self.address:
            return True

        return False

    def startup(self):
        """Synchronize to the host polling cycle

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x02], True, crc_need=True) == self.address:
            return True

        return False

    def sound_off(self):
        """Disable VLT sounds

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x03], True, crc_need=True) == self.address:
            return True

        return False

    def sound_on(self):
        """Enable VLT sounds

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x04], True, crc_need=True) == self.address:
            return True

        return False

    def reel_spin_game_sounds_disabled(self):
        """Reel spin or game play sounds disabled

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x05], True, crc_need=True) == self.address:
            return True

        return False

    def enable_bill_acceptor(self):
        """Enable the Bill Acceptor

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x06], True, crc_need=True) == self.address:
            return True

        return False

    def disable_bill_acceptor(self):
        """Disable the Bill Acceptor

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x07], True, crc_need=True) == self.address:
            return True

        return False

    def configure_bill_denom(self, bill_denom=[0xFF, 0xFF, 0xFF], action_flag=[0xFF]):
        """Configure Bill Denominations

        Parameters
        ----------
        bill_denom : dict
            Bill denominations sent LSB first (0 = disable, 1 = enable)

            =====  =====  ========  ========    =====
            Bit    LSB    2nd Byte  3rd Byte    MSB
            =====  =====  ========  ========    =====
            0      $1     $200      $20000      TBD
            1      $2     $250      $25000      TBD
            2      $5     $500      $50000      TBD
            3      $10    $1000     $100000     TBD
            4      $20    $2000     $200000     TBD
            5      $25    $2500     $250000     TBD
            6      $50    $5000     $500000     TBD
            7      $100   $10000    $1000000    TBD
            =====  =====  ========  ========    =====

        action_flag : dict
            Action of bill acceptor after accepting a bill

            =====  ===========
            Bit    Description
            =====  ===========
            0      0 = Disable bill acceptor after each accepted bill

                   1 = Keep bill acceptor enabled after each accepted bill
            =====  ===========

        Returns
        -------
        bool
            True if successful, False otherwise.

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x08, 0x00]
        cmd.extend(bill_denom)
        cmd.extend(action_flag)

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    def en_dis_game(self, game_number=None, en_dis=False):
        """Enable or Disable a specific game

        Parameters
        ----------
        game_number : bcd
            0001-9999 Game number

        en_dis : bool
            Default is False. True enable a game | False disable it

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        if not game_number:
            game_number = self.selected_game_number()

        game = int(str(game_number), 16)

        if en_dis:
            en_dis = [0]
        else:
            en_dis = [1]

        cmd = [0x09]

        cmd.extend([((game >> 8) & 0xFF), (game & 0xFF)])
        cmd.extend(bytearray(en_dis))

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    def enter_maintenance_mode(self):
        """Put the VLT in a state of maintenance mode
        Returns
        -------
        bool
            True if successful, False otherwise.

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x0A], True, crc_need=True) == self.address:
            return True

        return False

    def exit_maintenance_mode(self):
        """Recover  the VLT from a state of maintenance mode
        Returns
        -------
        bool
            True if successful, False otherwise.

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        if self._send_command([0x0B], True, crc_need=True) == self.address:
            return True

        return False

    def total_cancelled_credits(self, denom=True):
        """Send total cancelled credits meter

        Parameters
        ----------
        denom : bool
            If True will return the values of the meters in float format (i.e. 123.23)
            otherwise as int (i.e. 12323)

        Returns
        -------
        Mixed
            Round | INT | None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x10]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def handpay_info(self):
        """Send handpay information

        Returns
        -------
        Mixed
            Object containing the translated meters or None

        Notes
        -------
        This is a LONG POLL COMMAND - Warning: is missing 2-byte BCD Partial pay amount @todo FIX ME !
        """
        cmd = [0x1B]
        data = self._send_command(cmd, crc_need=False)
        if data:
            self._meters.values["bin_progressive_group"] = int(
                binascii.hexlify(bytearray(data[1:2]))
            )
            self._meters.values["bin_level"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._meters.values["amount"] = int(
                binascii.hexlify(bytearray(data[3:8]))
            )
            self._meters.values["bin_reset_ID"] = int(
                binascii.hexlify(bytearray(data[8:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def gaming_machine_id(self):
        """Gaming machine information command
        @todo Check this one...something smell bad

        According to doc:
            =====================  ======  =================  ========================================================================================================================================
            Field                  Bytes   Value              Description
            =====================  ======  =================  ========================================================================================================================================
            Address                1       binary 01-7F       Address of gaming machine responding
            Command                1       binary 1F          Gaming machine information command
            Game ID                2       ASCII ??           Game ID in ASCII. (see Table C-1 in Appendix C)
            Additional ID          3       ASCII ???          Additional game ID in ASCII. If the gaming machine does not support an additional ID, this field should be padded with ASCII "0"s.
            Denomination           1       binary 00-FF       Binary number representing the SAS accounting denomination of this gaming machine
            Max bet                1       binary 01-FF       Largest configured max bet for the gaming machine, or FF if largest configured max bet greater than or equal to 255
            Progressive Group      1       binary 00-FF       Current configured progressive group for the gaming machine
            Game options           2       binary 0000-FFFF   Game options selected by the operator. The bit configurations are dependent upon the type of gaming machine.
            Paytable ID            6       ASCII ??????       Paytable ID in ASCII
            Base %                 4       ASCII ??.??        Theoretical base pay back percentage for maximum bet in ASCII. The decimal is implied and NOT transmitted.
            CRC                    2       binary 0000-FFFF   16-bit CRC
            =====================  ======  =================  ========================================================================================================================================

        """
        # 1F
        cmd = [0x1F]
        data = self._send_command(cmd, crc_need=False, size=24)
        if data is not None:
            denom = Denomination.Denomination.get_status(data[6:7].hex())
            self.log.info("Recognized " + str(denom))
            self.denom = denom
            return denom
            # meters['ASCII_game_ID']=(((data[1:3])))
            # meters['ASCII_additional_ID']=(((data[3:6])))
            # meters['bin_denomination']=int(self.hexlify(self.bytearray(data[4:5])))
            # meters['bin_max_bet']=(self.hexlify(self.bytearray(data[7:8])))
            # meters['bin_progressive_mode']=int(self.hexlify(self.bytearray(data[8:9])))
            # meters['bin_game_options']=(self.hexlify(self.bytearray(data[9:11])))
            # meters['ASCII_paytable_ID']=(((data[11:17])))
            # meters['ASCII_base_percentage']=(((data[17:21])))

            # return data
        return None

    def rom_signature_verification(self):
        """ROM Signature Verification

        Returns
        -------
        Mixed
            int | none

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x21, 0x00, 0x00]
        data = self._send_command(cmd, crc_need=True)
        if data:
            return int(binascii.hexlify(bytearray(data[1:3])))

        return None

    def delay_game(self, delay_time=100):
        """Delay Game
        Parameters
        ----------
        delay_time : int
            How long in ms to delay a game

        Returns
        -------
        bool
            True for a successful operation, False otherwise

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        delay_time = str(delay_time)
        delay_fmt = "" + ("0" * (4 - len(delay_time)) + delay_time)
        cmd = [0x2E]
        count = 0
        for i in range(len(delay_fmt) // 2):
            cmd.append(int(delay_fmt[count : count + 2], 16))
            count += 2
        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True
        else:
            return False

    def last_accepted_bill_info(self):
        """Send last accepted bill information
        Returns
        -------
        mixed
            dict or None
        """
        cmd = [0x48]
        data = self._send_command(cmd, crc_need=False)
        if data:
            self._meters.values["country_code"] = int(
                binascii.hexlify(bytearray(data[1:2]))
            )
            self._meters.values["bill_denomination"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._meters.values["meter_for_accepted_bills"] = int(
                binascii.hexlify(bytearray(data[3:6]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def current_hopper_status(self):
        """Send Current Hopper Status
        Returns
        -------
        mixed :
            dict | none

        Notes
        ------
        Understanding the values:

        - current_hopper_length
        ==============      =====
        Code (Binary)       Description
        ==============      =====
        02                   Only status and % full
        06                   Status, % full and level
        ==============      =====

        - current_hopper_status
        ==============      =====
        Code (Binary)       Status
        ==============      =====
        00                   Hopper OK
        01                   Flooded Optics
        02                   Reverse Coin
        03                   Coin too short
        04                   Coin Jam
        05                   Hopper runaway
        06                   Optics Disconnected
        07                   Hopper Empty
        08-FE                Reserved
        FF                   Other
        ==============      =====

        - current_hopper_percent_full :
            Current hopper level as 0-100%, or FF if unable to detect hopper level percentage

        - current_hopper_level :
            4 BCD | Current hopper level in number of coins/tokens, only if EGM able to detect
        """
        # FIXME: current_hopper_status
        cmd = [0x4F]
        data = self._send_command(cmd, True, crc_need=False)
        if data:
            self._meters.values["current_hopper_length"] = int(
                binascii.hexlify(bytearray(data[1:2]))
            )
            self._meters.values["current_hopper_status"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._meters.values["current_hopper_percent_full"] = int(
                binascii.hexlify(bytearray(data[3:4]))
            )
            self._meters.values["current_hopper_level"] = int(
                binascii.hexlify(bytearray(data[4:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def total_number_of_games_implemented(self):
        # 51
        cmd = [0x51]
        # FIXME: cmd.extend(type_of_validation)
        data = self._send_command(cmd, crc_need=False, size=6)
        if data:
            return str(binascii.hexlify(bytearray(data[1:])))

        return None

    def game_configuration(self, n=None):
        # 53
        cmd = [0x53]
        # FIXME: game_configuration

        if not n:
            n = self.selected_game_number(in_hex=False)
        cmd.extend([(n & 0xFF), ((n >> 8) & 0xFF)])

        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._meters.values["game_n_number_config"] = int(
                binascii.hexlify(bytearray(data[1:3]))
            )
            self._meters.values["game_n_ASCII_game_ID"] = str(
                binascii.hexlify(bytearray(data[3:5]))
            )
            self._meters.values["game_n_ASCII_additional_id"] = str(
                binascii.hexlify(bytearray(data[5:7]))
            )
            self._meters.values["game_n_bin_denomination"] = str(
                binascii.hexlify(bytearray(data[7]))
            )
            self._meters.values["game_n_bin_progressive_group"] = str(
                binascii.hexlify(bytearray(data[8]))
            )
            self._meters.values["game_n_bin_game_options"] = str(
                binascii.hexlify(bytearray(data[9:11]))
            )
            self._meters.values["game_n_ASCII_paytable_ID"] = str(
                binascii.hexlify(bytearray(data[11:17]))
            )
            self._meters.values["game_n_ASCII_base_percentage"] = str(
                binascii.hexlify(bytearray(data[17:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def sas_version_gaming_machine_serial_id(self):
        # 54
        """
        This function should be checked at begin in order to address
        the changes from sas v6.02 and 6.03
        - Antonio
        @todo...one day i'll see to this....
        """
        cmd = [0x54, 0x00]
        data = self._send_command(cmd, crc_need=False, size=20)
        if data:
            self._meters.values["ASCII_SAS_version"] = (
                int(binascii.hexlify(bytearray(data[2:5]))) * 0.01
            )
            self._meters.values["ASCII_serial_number"] = str(bytearray(data[5:]))
            return self._meters.get_non_empty_status_map()

        return None

    def selected_game_number(self, in_hex=True):
        # 55
        cmd = [0x55]
        data = self._send_command(cmd, crc_need=False, size=6)
        if data:
            if not in_hex:
                return int(binascii.hexlify(bytearray(data[1:])))
            else:
                return binascii.hexlify(bytearray(data[1:]))

        return None

    def enabled_game_numbers(self):
        # 56
        cmd = [0x56]
        data = self._send_command(cmd, crc_need=False)
        if data:
            self._meters.values["number_of_enabled_games"] = int(
                binascii.hexlify(bytearray(data[2]))
            )
            self._meters.values["enabled_games_numbers"] = int(
                binascii.hexlify(bytearray(data[3:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def authentication_info(
        self,
        action=0,
        addressing_mode=0,
        component_name="",
        auth_method=b"\x00\x00\x00\x00",
        seed="",
        seed_length=0,
        offset="",
        offset_length=0,
    ):
        """Authentication Info

        Parameters
        ----------
        action : 1 binary
            Requested authentication action:

            =====  =====
            Value  Description
            =====  =====
            00      Interrogate number of installed components
            01      Read status of component (address required)
            02      Authenticate component (address required)
            03      Interrogate authentication status
            =====  =====

        addressing_mode : 1 binary
            =====  =====
            Value  Description
            =====  =====
            00      Addressing by component index number
            01      Addressing by component name
            =====  =====

        component_name : x bytes
            ASCII component name if addressing mode = 01

        auth_method : 4 binary
            ==============      ============    ======================  =======================
            Code (Binary)       Method          Seed size (max bytes)   Result Size (max bytes)
            ==============      ============    ======================  =======================
            00000000            None            n/a                     n/a
            00000001            CRC16           2 binary                2 binary
            00000002            CRC32           4 binary                4 binary
            00000004            MD5             16 bytes                16 bytes
            00000008            Kobetron I      4 ASCII                 4 ASCII
            00000010            Kobetron II     4 ASCII                 4 ASCII
            00000020            SHA1            20 Bytes                20 Bytes
            ==============      ============    ======================  =======================

        Returns
        -------
        bytearray
            Response ACK/NACK

        Notes
        -------
        Actually the real response is way more long and complex. Planning to map and implement it in the future

        """
        # 6E
        # FIXME: authentication_info
        cmd = [0x6E, 0x00, action]
        if action == 0:
            cmd[1] = 1
        else:
            if action == 1 or action == 3:
                cmd.append(addressing_mode)
                cmd.append(len(bytearray(component_name)))
                cmd.append(bytearray(component_name))
                cmd[1] = len(bytearray(component_name)) + 3
            else:
                if action == 2:
                    cmd.append(addressing_mode)
                    cmd.append(len(bytearray(component_name)))
                    cmd.append(bytearray(component_name))
                    cmd.append(auth_method)
                    cmd.append(seed_length)
                    cmd.append(bytearray(seed))
                    cmd.append(offset_length)
                    cmd.append(bytearray(offset))

                    cmd[1] = (
                        len(bytearray(offset))
                        + len(bytearray(seed))
                        + len(bytearray(component_name))
                        + 6
                    )

        data = self._send_command(cmd, True, crc_need=True)
        if data:
            return data[1]

        return None

    def current_date_time(self):
        # 7E
        cmd = [0x7E]
        data = self._send_command(cmd, crc_need=False, size=11)
        if data:
            data = str(binascii.hexlify(bytearray(data[1:8])))
            return datetime.datetime.strptime(data, "%m%d%Y%H%M%S")

        return None

    def receive_date_time(self, dates, times):
        # 7F
        cmd = [0x7F]
        fmt_cmd = "" + dates.replace(".", "") + times.replace(":", "") + "00"
        count = 0
        for i in range(len(fmt_cmd) // 2):
            cmd.append(int(fmt_cmd[count : count + 2], 16))
            count += 2

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    @staticmethod
    def card_info():
        # TODO: 8E
        return NotImplemented

    @staticmethod
    def physical_reel_stop_info():
        # TODO: 8F
        return NotImplemented

    def remote_handpay_reset(
        self,
    ):
        # 94
        cmd = [0x94]
        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    def toggle_autorebet(self, val=True):
        cmd = [0xAA]
        if not val:
            # AA00
            cmd.append(0x00)
        else:
            # AA01
            cmd.append(0x01)

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    def enabled_features(self, game_number=0):
        # A0
        # FIXME: This makes no sense
        # Basically tells which feature a selected games has. - Antonio

        cmd = [0xA0, self._bcd_coder_array(game_number, 2)]
        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._aft.values["game_number"] = str(
                binascii.hexlify(bytearray(data[1:3]))
            )
            self._aft.values["features_1"] = data[3]
            self._aft.values["features_2"] = data[4]
            self._aft.values["features_3"] = data[5]
            self._features.values["game_number"] = (
                self._aft.get_status("game_number")
            )
            if data[3] & 0b00000001:
                self._features.values["jackpot_multiplier"] = 1
            else:
                self._features.values["jackpot_multiplier"] = 0

            if data[3] & 0b00000010:
                self._features.values["AFT_bonus_awards"] = 1
            else:
                self._features.values["AFT_bonus_awards"] = 0

            if data[3] & 0b00000100:
                self._features.values["legacy_bonus_awards"] = 1
            else:
                self._features.values["legacy_bonus_awards"] = 0

            if data[3] & 0b00001000:
                self._features.values["tournament"] = 1
            else:
                self._features.values["tournament"] = 0

            if data[3] & 0b00010000:
                self._features.values["validation_extensions"] = 1
            else:
                self._features.values["validation_extensions"] = 0

            self._features.values["validation_style"] = (
                data[3] & 0b01100000 >> 5
            )

            if data[3] & 0b10000000:
                self._features.values["ticket_redemption"] = 1
            else:
                self._features.values["ticket_redemption"] = 0

            return self._features.get_non_empty_status_map()

        return None

    @staticmethod
    def cashout_limit():
        # TODO: A4
        return NotImplemented

    @staticmethod
    def enable_jackpot_handpay_reset_method():
        # TODO: A8
        return NotImplemented

    @staticmethod
    def multi_denom_preamble():
        # TODO: B0
        return NotImplemented

    @staticmethod
    def current_player_denomination():
        # TODO: B1
        return NotImplemented

    @staticmethod
    def enabled_player_denominations():
        # TODO: B2
        return NotImplemented

    @staticmethod
    def token_denomination():
        # TODO: B3
        return NotImplemented

    @staticmethod
    def wager_category_info():
        # TODO: B4
        return NotImplemented

    @staticmethod
    def extended_game_info(n=1):
        # TODO: B5
        return NotImplemented
