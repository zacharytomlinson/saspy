import time
import binascii


class BonusesCommands:
    """Existing bonuses operations used by the Sas client."""

    def initiate_legacy_bonus_pay(
        self,
        money,
        tax="00",
        games=None,
    ):
        # 8A
        if not games:
            for i in range(3):
                try:
                    games = self.selected_game_number(in_hex=False)
                except:
                    pass
                if not games:
                    time.sleep(0.04)
                else:
                    break

        if not games or games <= 0:
            return None

        t_cmd = str(int(round(money / self.denom, 2)))
        t_cmd = ("0" * (8 - len(t_cmd)) + t_cmd) + tax

        cmd = [0x8A]
        count = 0
        for i in range(len(t_cmd) // 2):
            cmd.append(int(t_cmd[count : count + 2], 16))
            count += 2

        if self._send_command(cmd, True, crc_need=True) == self.address:
            return True

        return False

    @staticmethod
    def initiate_multiplied_jackpot_mode():
        # TODO: 8B
        return NotImplemented

    @staticmethod
    def enter_exit_tournament_mode():
        # TODO: 8C
        return NotImplemented

    @staticmethod
    def legacy_bonus_win_info():
        # TODO: 90
        return NotImplemented

    @staticmethod
    def tournament_games_played():
        # TODO: 95
        return NotImplemented

    @staticmethod
    def tournament_games_won():
        # TODO: 96
        return NotImplemented

    @staticmethod
    def tournament_credits_wagered():
        # TODO: 97
        return NotImplemented

    @staticmethod
    def tournament_credits_won():
        # TODO: 98
        return NotImplemented

    @staticmethod
    def meters_95_98():
        # TODO: 99
        return NotImplemented

    def legacy_bonus_meters(self, denom=True, n=0):
        # 9A
        cmd = [0x9A, ((n >> 8) & 0xFF), (n & 0xFF)]
        data = self._send_command(cmd, crc_need=True, size=18)
        if data:
            if not denom:
                self._meters.values["game number"] = int(
                    binascii.hexlify(bytearray(data[2:3]))
                )
                self._meters.values["deductible"] = int(
                    binascii.hexlify(bytearray(data[3:7]))
                )
                self._meters.values["non-deductible"] = int(
                    binascii.hexlify(bytearray(data[7:11]))
                )
                self._meters.values["wager match"] = int(
                    binascii.hexlify(bytearray(data[11:15]))
                )
            else:
                self._meters.values["game number"] = int(
                    binascii.hexlify(bytearray(data[2:3]))
                )
                self._meters.values["deductible"] = round(
                    int(binascii.hexlify(bytearray(data[3:7]))) * self.denom, 2
                )
                self._meters.values["non-deductible"] = round(
                    int(binascii.hexlify(bytearray(data[7:11]))) * self.denom, 2
                )
                self._meters.values["wager match"] = round(
                    int(binascii.hexlify(bytearray(data[11:15]))) * self.denom, 2
                )
            return self._meters.get_non_empty_status_map()

        return None
