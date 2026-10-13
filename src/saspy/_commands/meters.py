import binascii


class MetersCommands:
    """Existing meters operations used by the Sas client."""

    def send_meters_10_15(self, denom=True):
        """Send meters 10 through 15

        Parameters
        ----------
        denom : bool
            If True will return the values of the meters in float format (i.e. 123.23)
            otherwise as int (i.e. 12323)

        Returns
        -------
        Mixed
            Object containing the translated meters or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x0F]
        data = self._send_command(cmd, crc_need=False, size=28)
        if data:
            meters = {}
            if denom:
                self._meters.values["total_cancelled_credits_meter"] = round(
                    int((binascii.hexlify(bytearray(data[1:5])))) * self.denom, 2
                )
                self._meters.values["total_in_meter"] = round(
                    int(binascii.hexlify(bytearray(data[5:9]))) * self.denom, 2
                )
                self._meters.values["total_out_meter"] = round(
                    int(binascii.hexlify(bytearray(data[9:13]))) * self.denom, 2
                )
                self._meters.values["total_droup_meter"] = round(
                    int(binascii.hexlify(bytearray(data[13:17]))) * self.denom, 2
                )
                self._meters.values["total_jackpot_meter"] = round(
                    int(binascii.hexlify(bytearray(data[17:21]))) * self.denom, 2
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[21:25]))
                )
            else:
                self._meters.values["total_cancelled_credits_meter"] = int(
                    (binascii.hexlify(bytearray(data[1:5])))
                )
                self._meters.values["total_in_meter"] = int(
                    binascii.hexlify(bytearray(data[5:9]))
                )
                self._meters.values["total_out_meter"] = int(
                    binascii.hexlify(bytearray(data[9:13]))
                )
                self._meters.values["total_droup_meter"] = int(
                    binascii.hexlify(bytearray(data[13:17]))
                )
                self._meters.values["total_jackpot_meter"] = int(
                    binascii.hexlify(bytearray(data[17:21]))
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[21:25]))
                )

            return self._meters.get_non_empty_status_map()

        return None

    def total_bet_meter(self, denom=True):
        """Send total coin in meter
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
        This is a LONG POLL COMMAND - Pretty sure that the param should not be used @todo CHECK ME
        """
        cmd = [0x11]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def total_win_meter(self, denom=True):
        """Send total coin out meter
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
        This is a LONG POLL COMMAND - Pretty sure that the param should not be used @todo CHECK ME
        """
        cmd = [0x12]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def total_drop_meter(self, denom=True):
        """Send total drop meter
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
        This is a LONG POLL COMMAND - Pretty sure that the param should not be used @todo CHECK ME
        """
        cmd = [0x13]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def total_jackpot_meter(self, denom=True):
        """Send total jackpot meter
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
        This is a LONG POLL COMMAND - Pretty sure that the param should not be used @todo CHECK ME
        """
        cmd = [0x14]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def games_played_meter(self):
        """Send games played meter

        Returns
        -------
        Mixed
            INT | None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x15]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def games_won_meter(self, denom=True):
        """Send games won meter
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
        This is a LONG POLL COMMAND - Pretty sure that the param should not be used @todo CHECK ME
        """
        cmd = [0x16]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def games_lost_meter(self):
        """Send games won meter
        Returns
        -------
        Mixed
            INT | None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x17]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def games_powerup_door_opened(self):
        """Send meters 10 through 15

        Returns
        -------
        Mixed
            Object containing the translated meters or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x18]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            self._meters.values["games_last_power_up"] = int(
                binascii.hexlify(bytearray(data[1:3]))
            )
            self._meters.values["games_last_slot_door_close"] = int(
                binascii.hexlify(bytearray(data[1:5]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def meters_11_15(self, denom=True):
        """Send meters 11 through 15

        Parameters
        ----------
        denom : bool
            If True will return the values of the meters in float format (i.e. 123.23)
            otherwise as int (i.e. 12323)

        Returns
        -------
        Mixed
            Object containing the translated meters or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x19]
        data = self._send_command(cmd, crc_need=False, size=24)
        if data:
            if not denom:
                self._meters.values["total_bet_meter"] = int(
                    binascii.hexlify(bytearray(data[1:5]))
                )
                self._meters.values["total_win_meter"] = int(
                    binascii.hexlify(bytearray(data[5:9]))
                )
                self._meters.values["total_in_meter"] = int(
                    binascii.hexlify(bytearray(data[9:13]))
                )
                self._meters.values["total_jackpot_meter"] = int(
                    binascii.hexlify(bytearray(data[13:17]))
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[17:21]))
                )
            else:
                self._meters.values["total_bet_meter"] = round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
                self._meters.values["total_win_meter"] = round(
                    int(binascii.hexlify(bytearray(data[5:9]))) * self.denom, 2
                )
                self._meters.values["total_in_meter"] = round(
                    int(binascii.hexlify(bytearray(data[9:13]))) * self.denom, 2
                )
                self._meters.values["total_jackpot_meter"] = round(
                    int(binascii.hexlify(bytearray(data[13:17]))) * self.denom, 2
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[17:21]))
                )
            return self._meters.get_non_empty_status_map()

        return None

    def current_credits(self, denom=True):
        """Send current credits

        Parameters
        ----------
        denom : bool
            If True will return the value in float format (i.e. 123.23)
            otherwise as int (i.e. 12323)

        Returns
        -------
        Mixed
            round | int | None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x1A]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            if denom:
                return round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
            else:
                return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def meters(self, denom=True):
        """Send Meters

        Parameters
        ----------
        denom : bool
            If True will return the value in float format (i.e. 123.23)
            otherwise as int (i.e. 12323)

        Returns
        -------
        Mixed
            Object containing the translated meters (in int or float) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x1C]
        data = self._send_command(cmd, crc_need=False, size=36)
        if data:
            if not denom:
                self._meters.values["total_bet_meter"] = int(
                    binascii.hexlify(bytearray(data[1:5]))
                )
                self._meters.values["total_win_meter"] = int(
                    binascii.hexlify(bytearray(data[5:9]))
                )
                self._meters.values["total_drop_meter"] = int(
                    binascii.hexlify(bytearray(data[9:13]))
                )
                self._meters.values["total_jackpot_meter"] = int(
                    binascii.hexlify(bytearray(data[13:17]))
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[17:21]))
                )
                self._meters.values["games_won_meter"] = int(
                    binascii.hexlify(bytearray(data[21:25]))
                )
                self._meters.values["slot_door_opened_meter"] = int(
                    binascii.hexlify(bytearray(data[25:29]))
                )
                self._meters.values["power_reset_meter"] = int(
                    binascii.hexlify(bytearray(data[29:33]))
                )
            else:
                self._meters.values["total_bet_meter"] = round(
                    int(binascii.hexlify(bytearray(data[1:5]))) * self.denom, 2
                )
                self._meters.values["total_win_meter"] = round(
                    int(binascii.hexlify(bytearray(data[5:9]))) * self.denom, 2
                )
                self._meters.values["total_drop_meter"] = round(
                    int(binascii.hexlify(bytearray(data[9:13]))) * self.denom, 2
                )
                self._meters.values["total_jackpot_meter"] = round(
                    int(binascii.hexlify(bytearray(data[13:17]))) * self.denom, 2
                )
                self._meters.values["games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[17:21]))
                )
                self._meters.values["games_won_meter"] = round(
                    int(binascii.hexlify(bytearray(data[21:25]))) * self.denom, 2
                )
                self._meters.values["slot_door_opened_meter"] = int(
                    binascii.hexlify(bytearray(data[25:29]))
                )
                self._meters.values["power_reset_meter"] = int(
                    binascii.hexlify(bytearray(data[29:33]))
                )

            return self._meters.get_non_empty_status_map()

        return None

    def total_bill_meters(self):
        """Send total bill meters (# of bills)

        Returns
        -------
        Mixed
            Object containing the translated meters or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x1E]
        data = self._send_command(cmd, crc_need=False, size=28)
        if data:
            self._meters.values["s1_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[1:5]))
            )
            self._meters.values["s5_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[5:9]))
            )
            self._meters.values["s10_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[9:13]))
            )
            self._meters.values["s20_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[13:17]))
            )
            self._meters.values["s50_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[17:21]))
            )
            self._meters.values["s100_bills_accepted_meter"] = int(
                binascii.hexlify(bytearray(data[21:25]))
            )

            return self._meters.get_non_empty_status_map()

        return None

    def total_dollar_value_of_bills_meter(self):
        """Send total dollar value of bills meter

        Returns
        -------
        Mixed
            int | none

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x20]
        data = self._send_command(cmd, crc_need=False, size=8)

        if data:
            return int(binascii.hexlify(bytearray(data[1:])))

        return None

    def true_coin_in(self):
        """Send true coin in

        Returns
        -------
        Mixed
            int (meter in # of coins/tokens) | none

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x2A]
        data = self._send_command(cmd, crc_need=False)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def true_coin_out(self):
        """Send true coin out

        Returns
        -------
        Mixed
            int (meter in # of coins/tokens) | none

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x2B]
        data = self._send_command(cmd, crc_need=False)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def curr_hopper_level(self):
        """Send current hopper level

        Returns
        -------
        Mixed
            int (meter in # of coins/tokens) | none

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x2C]
        data = self._send_command(cmd, crc_need=False)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def total_hand_paid_cancelled_credit(self):
        """Send total hand paid cancelled credits

        Notes
        -------
        WARNING ! @todo i return: 2-byte BCD game number and 4-byte BCD meter in SAS accounting denom units. Therefore this code is WRONG

        This is a LONG POLL COMMAND
        """
        cmd = [0x2D]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    @staticmethod
    def selected_meters_for_game():
        # 2F
        # TODO: selected_meters_for_game
        # As per above...NOT ME ! @well-it-wasnt-me
        return None

    def send_1_bills_in_meters(self):
        """Send 1$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x31]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_2_bills_in_meters(self):
        """Send 2$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x32]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_5_bills_in_meters(self):
        """Send 5$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x33]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_10_bills_in_meters(self):
        """Send 10$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x34]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_20_bills_in_meters(self):
        """Send 20$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x35]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_50_bills_in_meters(self):
        """Send 50$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x36]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_100_bills_in_meters(self):
        """Send 100$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x37]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_500_bills_in_meters(self):
        """Send 500$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x38]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_1000_bills_in_meters(self):
        """Send 1.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x39]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_200_bills_in_meters(self):
        """Send 200$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3A]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_25_bills_in_meters(self):
        """Send 25$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3B]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_2000_bills_in_meters(self):
        """Send 2.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3C]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))
        return None

    def send_2500_bills_in_meters(self):
        """Send 2.500$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3E]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_5000_bills_in_meters(self):
        """Send 5.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3F]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_10000_bills_in_meters(self):
        """Send 10.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x40]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_20000_bills_in_meters(self):
        """Send 20.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x41]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_25000_bills_in_meters(self):
        """Send 25.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x42]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_50000_bills_in_meters(self):
        """Send 50.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x43]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_100000_bills_in_meters(self):
        """Send 100.000$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x44]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def send_250_bills_in_meters(self):
        """Send 250$ bills in meters

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x45]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def credit_amount_of_all_bills_accepted(self):
        """Send credit amount of all bills accepted

        Returns
        -------
        mixed
            meter in SAS accounting denom units or None

        """
        cmd = [0x46]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def coin_amount_accepted_from_external_coin_acceptor(self):
        """Send coin amount accepted from an external coin acceptor

        Returns
        -------
        mixed
             meter in SAS accounting denom units or None

        """
        cmd = [0x47]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def number_of_bills_currently_in_stacker(self):
        """Send number of bills currently in the stacker
        Returns
        -------
        mixed
            int ( meter in # of bills )  or None
        """
        cmd = [0x49]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def total_credit_amount_of_all_bills_in_stacker(self):
        """Send total credit amount of all bills currently in the stacker

        Returns
        -------
        mixed
            int (# of bills) or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x4A]
        data = self._send_command(cmd, crc_need=False, size=8)
        if data:
            return int(binascii.hexlify(bytearray(data[1:5])))

        return None

    def game_meters(self, n=None, denom=True):
        # 52
        cmd = [0x52]

        if not n:
            n = self.selected_game_number(in_hex=False)
        cmd.extend([((n >> 8) & 0xFF), (n & 0xFF)])

        data = self._send_command(cmd, crc_need=True, size=22)
        if data:
            meters = {}
            if not denom:
                self._meters.values["game_n_number"] = str(
                    binascii.hexlify(bytearray(data[1:3]))
                )
                self._meters.values["game_n_coin_in_meter"] = int(
                    binascii.hexlify(bytearray(data[3:7]))
                )
                self._meters.values["game_n_coin_out_meter"] = int(
                    binascii.hexlify(bytearray(data[7:11]))
                )
                self._meters.values["game_n_jackpot_meter"] = int(
                    binascii.hexlify(bytearray(data[11:15]))
                )
                self._meters.values["geme_n_games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[15:]))
                )
            else:
                self._meters.values["game_n_number"] = str(
                    binascii.hexlify(bytearray(data[1:3]))
                )
                self._meters.values["game_n_coin_in_meter"] = round(
                    int(binascii.hexlify(bytearray(data[3:7]))) * self.denom, 2
                )
                self._meters.values["game_n_coin_out_meter"] = round(
                    int(binascii.hexlify(bytearray(data[7:11]))) * self.denom, 2
                )
                self._meters.values["game_n_jackpot_meter"] = round(
                    int(binascii.hexlify(bytearray(data[11:15]))) * self.denom, 2
                )
                self._meters.values["geme_n_games_played_meter"] = int(
                    binascii.hexlify(bytearray(data[15:]))
                )

            return self._meters.get_non_empty_status_map()

        return None

    @staticmethod
    def extended_meters_for_game():
        # TODO: extended_meters_for_game
        # 6F
        return None

    @staticmethod
    def extended_meters_game_alt():
        # TODO: AF
        return NotImplemented
