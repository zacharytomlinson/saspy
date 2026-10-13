import time
import binascii
import datetime
from ..models import AftReceiptStatus, AftTransferStatus, AftTransferType
from ..errors import AFTBadAmount, BadCRC, BadTransactionID


class AftCommands:
    """Existing aft operations used by the Sas client."""

    def aft_jp(self, money, amount=1, lock_timeout=0, games=None):
        # FIXME: make logically coherent
        # self.lock_emg(lock_time=500, condition=1)
        money_1 = money_2 = money_3 = "0000000000"
        if self.denom > 0.01:
            return None

        if not games:
            for i in range(3):
                games = self.selected_game_number(in_hex=False)
                if not games:
                    time.sleep(0.04)
                else:
                    break

        if not games or games == 0 or games < 1:
            return "NoGame"

        if not money:
            money = str(self.current_credits(denom=False))
        else:
            money = str(int((money / self.denom)))
            money = money.replace(".", "")

        money = "0" * (10 - len(money)) + money

        match amount:
            case 1:
                money_1 = money
            case 2:
                money_2 = money
            case 3:
                money_3 = money
            case _:
                raise AFTBadAmount

        last_transaction = self.aft_format_transaction()
        len_transaction_id = hex(len(last_transaction) // 2)[
            2:
        ]  # the division result should be converted to an integer before using hex, added extra / to solve this
        if len(len_transaction_id) < 2:
            len_transaction_id = "0" + len_transaction_id
        elif len(len_transaction_id) % 2 == 1:
            len_transaction_id = "0" + len_transaction_id

        cmd = """72{my_key}{index}00{transfer_code}{money_1}{money_2}{money_3}
                 00{asset}{key}{len_transaction}{transaction}{times}0C0000""".format(
            transfer_code="11",
            index="00",
            money_1=money_1,
            money_2=money_2,
            money_3=money_3,
            asset=self.asset_number,
            key=self.reg_key,
            len_transaction=len_transaction_id,
            transaction=last_transaction,
            times=datetime.datetime.strftime(datetime.datetime.now(), "%m%d%Y"),
            my_key=self.my_key,
        )

        new_cmd = []
        count = 0
        for i in range(
            len(cmd) // 2
        ):  # Python3...not my fault...might be better using range(0, len(cmd), 2) ?
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        response = None
        self.aft_register()
        if lock_timeout > 0:
            self.aft_game_lock(lock_timeout, condition=1)

        data = self._send_command(new_cmd, crc_need=True, size=82)

        if data:
            a = int(binascii.hexlify(bytearray(data[26:27])), 16)
            response = {
                "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                "Transaction buffer position": int(
                    binascii.hexlify(bytearray(data[2:3]))
                ),
                "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                    binascii.hexlify(bytearray(data[3:4]))
                ),
                "Receipt status": AftTransferStatus.AftTransferStatus.get_status(
                    binascii.hexlify(bytearray(data[4:5]))
                ),
                "Transfer type": AftTransferStatus.AftTransferStatus.get_status(
                    binascii.hexlify(bytearray(data[5:6]))
                ),
                "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                * self.denom,
                "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                * self.denom,
                "Nonrestricted amount": int(binascii.hexlify(bytearray(data[16:21])))
                * self.denom,
                "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                "Asset number": binascii.hexlify(bytearray(data[22:26])),
                "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                "Transaction ID": binascii.hexlify(
                    bytearray(data[27 : (27 + a)])
                ),  # WARNING: technically should be (27 + 2 * a) due to an off error.... @todo...somebody see me !
            }
        try:
            self.aft_unregister()
        except:
            self.log.warning("AFT UNREGISTER ERROR: won to host")

        return response

    def aft_out(self, money=None, amount=1, lock_timeout=0):
        """
        aft_out is a function to make a machine cashout (effectively removes the credit in the machine)
        :param money:
        :param amount:
        :param lock_timeout:
        :param kwargs:
        :return:
        """
        # self.lock_emg(lock_time=500, condition=1)
        money_1 = money_2 = money_3 = "0000000000"
        if self.denom > 0.01:
            return None

        if not money:
            money = str(self.current_credits(denom=False))
        else:
            money = str(int((money / self.denom))).replace(".", "")

        money = "0" * (10 - len(money)) + money

        match amount:
            case 1:
                money_1 = money
            case 2:
                money_2 = money
            case 3:
                money_3 = money
            case _:
                raise AFTBadAmount

        last_transaction = self.aft_format_transaction()
        len_transaction_id = hex(len(last_transaction) // 2)[2:]
        if len(len_transaction_id) < 2:
            len_transaction_id = "0" + len_transaction_id
        elif len(len_transaction_id) % 2 == 1:
            len_transaction_id = "0" + len_transaction_id

        cmd = """72{my_key}{index}00{transfer_code}{money_1}{money_2}{money_3}
                 00{asset}{key}{len_transaction}{transaction}{times}0C0000""".format(
            transfer_code="80",
            index="00",
            money_1=money_1,
            money_2=money_2,
            money_3=money_3,
            asset=self.asset_number,
            key=self.reg_key,
            len_transaction=len_transaction_id,
            transaction=last_transaction,
            times=datetime.datetime.strftime(datetime.datetime.now(), "%m%d%Y"),
            my_key=self.my_key,
        )

        new_cmd = []
        count = 0
        for i in range(len(cmd) // 2):
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        response = None
        self.aft_register()
        if lock_timeout > 0:
            self.aft_game_lock(lock_timeout, condition=1)
        try:
            data = self._send_command(new_cmd, crc_need=True, size=82)
            if data:
                a = int(binascii.hexlify(bytearray(data[26:27])), 16)
                response = {
                    "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                    "Transaction buffer position": int(
                        binascii.hexlify(bytearray(data[2:3]))
                    ),
                    "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[3:4]))
                    ),
                    "Receipt status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[4:5]))
                    ),
                    "Transfer type": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[5:6]))
                    ),
                    "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                    * self.denom,
                    "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                    * self.denom,
                    "Nonrestricted amount": int(
                        binascii.hexlify(bytearray(data[16:21]))
                    )
                    * self.denom,
                    "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                    "Asset number": binascii.hexlify(bytearray(data[22:26])),
                    "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                    "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
                }
        except Exception as e:
            self.log.error(e, exc_info=True)

        self.aft_unregister()

        return response

    def aft_cashout_enable(self, amount=1, money="0000000000"):
        money_1 = money_2 = money_3 = "0000000000"

        match amount:
            case 1:
                money_1 = money
            case 2:
                money_2 = money
            case 3:
                money_3 = money
            case _:
                raise AFTBadAmount

        last_transaction = self.aft_format_transaction()
        len_transaction_id = hex(len(last_transaction) // 2)[2:]
        if len(len_transaction_id) < 2:
            len_transaction_id = "0" + len_transaction_id
        elif len(len_transaction_id) % 2 == 1:
            len_transaction_id = "0" + len_transaction_id

        cmd = """72{my_key}00{index}{transfer_code}{money_1}{money_2}{money_3}
                 02{asset}{key}{len_transaction}{transaction}{times}0C0000""".format(
            transfer_code="80",
            index="00",
            money_1=money_1,
            money_2=money_2,
            money_3=money_3,
            asset=self.asset_number,
            key=self.reg_key,
            len_transaction=len_transaction_id,
            transaction=last_transaction,
            times=datetime.datetime.strftime(datetime.datetime.now(), "%m%d%Y"),
            my_key=self.my_key,
        )

        new_cmd = []
        count = 0
        for i in range(len(cmd) // 2):
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        self.aft_register()

        response = None
        try:
            data = self._send_command(new_cmd, crc_need=True, size=82)
            if data:
                a = int(binascii.hexlify(bytearray(data[26:27])), 16)
                response = {
                    "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                    "Transaction buffer position": int(
                        binascii.hexlify(bytearray(data[2:3]))
                    ),
                    "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[3:4]))
                    ),
                    "Receipt status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[4:5]))
                    ),
                    "Transfer type": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[5:6]))
                    ),
                    "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                    * self.denom,
                    "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                    * self.denom,
                    "Nonrestricted amount": int(
                        binascii.hexlify(bytearray(data[16:21]))
                    )
                    * self.denom,
                    "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                    "Asset number": binascii.hexlify(bytearray(data[22:26])),
                    "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                    "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
                }
        except Exception as e:
            self.log.critical(e, exc_info=True)

        self.aft_unregister()
        try:
            self.aft_clean_transaction_poll()
        except:
            self.log.critical("Triggered unknown exception in aft_cashout_enable")
            return False

        return True

    def aft_won(self, money="0000000000", amount=1, games=None, lock_timeout=0):
        money_1 = money_2 = money_3 = "0000000000"
        if self.denom > 0.01:
            return None

        if not games:
            for i in range(3):
                try:
                    games = self.selected_game_number(in_hex=False)
                except:
                    time.sleep(0.04)
                else:
                    break

        if not games or games < 1:
            return "NoGame"

        money = str(int(money / self.denom)).replace(".", "")
        money = "0" * (10 - len(money)) + money

        match amount:
            case 1:
                money_1 = money
            case 2:
                money_2 = money
            case 3:
                money_3 = money
            case _:
                raise AFTBadAmount

        last_transaction = self.aft_format_transaction()
        len_transaction_id = hex(len(last_transaction) // 2)[2:]
        if len(len_transaction_id) < 2:
            len_transaction_id = "0" + len_transaction_id
        elif len(len_transaction_id) % 2 == 1:
            len_transaction_id = "0" + len_transaction_id

        cmd = """72{my_key}{transfer_code}{index}{money_1}{money_2}{money_3}"
               "00{asset}{key}{len_transaction}{transaction}{times}0C0000""".format(
            transfer_code="0000",
            index="10",
            money_1=money_1,
            money_2=money_2,
            money_3=money_3,
            asset=self.asset_number,
            key=self.reg_key,
            len_transaction=len_transaction_id,
            transaction=last_transaction,
            times=datetime.datetime.strftime(datetime.datetime.now(), "%m%d%Y"),
            my_key=self.my_key,
        )

        new_cmd = []
        count = 0
        for i in range(len(cmd) // 2):
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        response = None
        self.aft_register()
        if lock_timeout > 0:
            self.aft_game_lock(lock_timeout, condition=3)
        try:
            data = self._send_command(new_cmd, crc_need=True, size=82)
            if data:
                a = int(binascii.hexlify(bytearray(data[26:27])), 16)
                response = {
                    "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                    "Transaction buffer position": int(
                        binascii.hexlify(bytearray(data[2:3]))
                    ),
                    "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[3:4]))
                    ),
                    "Receipt status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[4:5]))
                    ),
                    "Transfer type": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[5:6]))
                    ),
                    "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                    * self.denom,
                    "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                    * self.denom,
                    "Nonrestricted amount": int(
                        binascii.hexlify(bytearray(data[16:21]))
                    )
                    * self.denom,
                    "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                    "Asset number": binascii.hexlify(bytearray(data[22:26])),
                    "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                    "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
                }
        except Exception as e:
            self.log.error(e, exc_info=True)

        self.aft_unregister()

        return response

    def aft_in(self, money, amount=1):
        """
        aft_in is the function you want to use to charge money into your machine

        :param money:
        :param amount:
        :param lock_timeout:
        :param kwargs:
        :return:
        """
        money_1 = money_2 = money_3 = "0000000000"
        if self.denom > 0.01:
            return None

        money = str(int(money / self.denom)).replace(".", "")
        money = "0" * (10 - len(money)) + money

        match amount:
            case 1:
                money_1 = money
            case 2:
                money_2 = money
            case 3:
                money_3 = money
            case _:
                raise AFTBadAmount

        last_transaction = self.aft_format_transaction()
        len_transaction_id = hex(len(last_transaction) // 2)[2:]
        if len(len_transaction_id) < 2:
            len_transaction_id = "0" + len_transaction_id
        elif len(len_transaction_id) % 2 == 1:
            len_transaction_id = "0" + len_transaction_id

        cmd = """72{my_key}{transfer_code}{index}00{money_1}{money_2}{money_3}
                 00{asset}{key}{len_transaction}{transaction}{times}0C0000""".format(
            transfer_code="00",
            index="00",
            money_1=money_1,
            money_2=money_2,
            money_3=money_3,
            asset=self.asset_number,
            key=self.reg_key,
            len_transaction=len_transaction_id,
            transaction=last_transaction,
            times=datetime.datetime.strftime(datetime.datetime.now(), "%m%d%Y"),
            my_key=self.my_key,
        )

        new_cmd = []
        count = 0
        for i in range(len(cmd) // 2):
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        try:
            data = self._send_command(new_cmd, crc_need=True, size=82)
            if data:
                a = int(binascii.hexlify(bytearray(data[26:27])), 16)
                response = {
                    "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                    "Transaction buffer position": int(
                        binascii.hexlify(bytearray(data[2:3]))
                    ),
                    "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                        [binascii.hexlify(bytearray(data[3:4]))]
                    ),
                    "Receipt status": AftReceiptStatus.AftReceiptStatus.get_status(
                        [binascii.hexlify(bytearray(data[4:5]))]
                    ),
                    "Transfer type": AftTransferType.AftTransferType.get_status(
                        [binascii.hexlify(bytearray(data[5:6]))]
                    ),
                    "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                    * self.denom,
                    "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                    * self.denom,
                    "Nonrestricted amount": int(
                        binascii.hexlify(bytearray(data[16:21]))
                    )
                    * self.denom,
                    "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                    "Asset number": binascii.hexlify(bytearray(data[22:26])),
                    "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                    "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
                }

                self.aft_unregister()
                return response

        except Exception as e:
            self.aft_unregister()
            self.log.error(e, exc_info=True)

    def aft_clean_transaction_poll(self, register=False):
        """Remember to loop this function AFTER calling aft_in.
        If it raises an error or returns 'Transfer pending (not complete)'
        you continue to execute until 'Full transfer successful'.
        Otherwise, you break the cycle and make the request invalid.
        """
        if register:
            self.aft_register()

        if not self.transaction:
            self.aft_get_last_trx()

        cmd = "7202FF00"
        count = 0
        new_cmd = []
        for i in range(len(cmd) // 2):
            new_cmd.append(int(cmd[count : count + 2], 16))
            count += 2

        response = None
        try:
            data = self._send_command(new_cmd, crc_need=True, size=90)
            if data:
                a = int(binascii.hexlify(bytearray(data[26:27])), 16)
                response = {
                    "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                    "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[3:4]))
                    ),
                    "Receipt status": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[4:5]))
                    ),
                    "Transfer type": AftTransferStatus.AftTransferStatus.get_status(
                        binascii.hexlify(bytearray(data[5:6]))
                    ),
                    "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                    * self.denom,
                    "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                    * self.denom,
                    "Nonrestricted amount": int(
                        binascii.hexlify(bytearray(data[16:21]))
                    )
                    * self.denom,
                    "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                    "Asset number": binascii.hexlify(bytearray(data[22:26])),
                    "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                    "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
                }

            if register:
                try:
                    self.aft_unregister()
                except:
                    self.log.warning("AFT UNREGISTER ERROR: clean poll")

            if hex(self.transaction)[2:-1] == response["Transaction ID"]:
                return response
            else:
                if self.check_last_transaction:
                    raise BadTransactionID(
                        "last: %s, new:%s "
                        % (hex(self.transaction)[2:-1], response["Transaction ID"])
                    )
                else:
                    self.log.info(
                        "last: %s, new:%s "
                        % (hex(self.transaction)[2:-1], response["Transaction ID"])
                    )
        except BadCRC:
            pass

        return False

    def aft_transfer_funds(
        self,
        transfer_code=0x00,
        transaction_index=0x00,
        transfer_type=0x00,
        cashable_amount=0,
        restricted_amount=0,
        non_restricted_amount=0,
        transfer_flags=0x00,
        asset_number=b"\x00\x00\x00\x00\x00",
        registration_key=0,
        transaction_id="",
        expiration=0,
        pool_id=0,
        receipt_data="",
        lock_timeout=0,
    ):
        # 72
        cmd = [
            0x72,
            2 * len(transaction_id) + 53,
            transfer_code,
            transaction_index,
            transfer_type,
            self._bcd_coder_array(cashable_amount, 5),
            self._bcd_coder_array(restricted_amount, 5),
            self._bcd_coder_array(non_restricted_amount, 5),
            transfer_flags,
            asset_number,
            self._bcd_coder_array(registration_key, 20),
            len(transaction_id),
            self._bcd_coder_array(expiration, 4),
            self._bcd_coder_array(pool_id, 2),
            len(receipt_data),
            receipt_data,
            self._bcd_coder_array(lock_timeout, 2),
        ]

        data = self._send_command(cmd, crc_need=True)
        if data:
            self._aft.values["transaction_buffer_position"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._aft.values["transfer_status"] = int(
                binascii.hexlify(bytearray(data[3:4]))
            )
            self._aft.values["receipt_status"] = int(
                binascii.hexlify(bytearray(data[4:5]))
            )
            self._aft.values["transfer_type"] = int(
                binascii.hexlify(bytearray(data[5:6]))
            )
            self._aft.values["cashable_amount"] = int(
                binascii.hexlify(bytearray(data[6:11]))
            )
            self._aft.values["restricted_amount"] = int(
                binascii.hexlify(bytearray(data[11:16]))
            )
            self._aft.values["nonrestricted_amount"] = int(
                binascii.hexlify(bytearray(data[16:21]))
            )
            self._aft.values["transfer_flags"] = int(
                binascii.hexlify(bytearray(data[21:22]))
            )
            self._aft.values["asset_number"] = binascii.hexlify(
                bytearray(data[22:26])
            )
            self._aft.values["transaction_id_length"] = int(
                binascii.hexlify(bytearray(data[26:27]))
            )
            a = int(binascii.hexlify(bytearray(data[26:27])))
            self._aft.values["transaction_id"] = str(
                binascii.hexlify(bytearray(data[27 : (27 + a + 1)]))
            )
            a = 27 + a + 1
            self._aft.values["transaction_date"] = str(
                binascii.hexlify(bytearray(data[a : a + 5]))
            )
            a = a + 5
            self._aft.values["transaction_time"] = str(
                binascii.hexlify(bytearray(data[a : a + 4]))
            )
            self._aft.values["expiration"] = str(
                binascii.hexlify(bytearray(data[a + 4 : a + 9]))
            )
            self._aft.values["pool_id"] = str(
                binascii.hexlify(bytearray(data[a + 9 : a + 11]))
            )
            self._aft.values[
                "cumulative_cashable_amount_meter_size"
            ] = binascii.hexlify(bytearray(data[a + 11 : a + 12]))
            b = a + int(binascii.hexlify(bytearray(data[a + 11 : a + 12])))
            self._aft.values[
                "cumulative_cashable_amount_meter"
            ] = binascii.hexlify(bytearray(data[a + 12 : b + 1]))
            self._aft.values[
                "cumulative_restricted_amount_meter_size"
            ] = binascii.hexlify(bytearray(data[b + 1 : b + 2]))
            c = b + 2 + int(binascii.hexlify(bytearray(data[b + 1 : b + 2])))
            self._aft.values[
                "cumulative_restricted_amount_meter"
            ] = binascii.hexlify(bytearray(data[b + 2 : c]))
            self._aft.values[
                "cumulative_nonrestricted_amount_meter_size"
            ] = binascii.hexlify(bytearray(data[c : c + 1]))
            b = int(binascii.hexlify(bytearray(data[c : c + 1]))) + c
            self._aft.values[
                "cumulative_nonrestricted_amount_meter"
            ] = binascii.hexlify(bytearray(data[c + 1 :]))

            return self._aft.get_non_empty_status_map()

        return None

    def aft_get_last_trx(self):
        cmd = [0x72, 0x02, 0xFF, 0x00]
        data = self._send_command(cmd, crc_need=True, size=90)
        if data:
            try:
                if not self.aft_get_last_transaction:
                    raise ValueError

                count = int(binascii.hexlify(data[26:27]), 16)
                transaction = binascii.hexlify(data[27 : 27 + count])
                if transaction == "2121212121212121212121212121212121":
                    transaction = "2020202020202020202020202020202021"
                self.transaction = int(transaction, 16)

                return self.transaction

            except ValueError as e:
                self.log.warning(e, exc_info=True)
                self.transaction = int("2020202020202020202020202020202021", 16)
                self.log.warning("AFT no transaction")

            except Exception as e:
                self.log.error(e, exc_info=True)
                self.transaction = int("2020202020202020202020202020202021", 16)
                self.log.warning("AFT no transaction")

        else:
            self.transaction = int("2020202020202020202020202020202021", 16)
            self.log.warning("AFT no transaction")

        return self.transaction

    def aft_format_transaction(self, from_egm=False):
        if from_egm:
            self.aft_get_last_trx()

        if self.transaction is None:
            self.aft_get_last_trx()

        self.transaction += 1
        transaction = hex(self.transaction)[2:-1]
        count = 0
        tmp = []
        for i in range(len(transaction) // 2):
            tmp.append(transaction[count : count + 2])
            count += 2

        tmp.reverse()
        for i in range(len(tmp)):
            if int(tmp[i], 16) >= 124:
                tmp[i] = "20"
                tmp[i + 1] = hex(int(tmp[i + 1], 16) + 1)[2:]

        tmp.reverse()
        response = ""
        for i in tmp:
            response += i
        if response == "2121212121212121212121212121212121":
            response = "2020202020202020202020202020202021"

        self.transaction = int(response, 16)
        return response

    def aft_register(self, reg_code=0x01):
        try:
            return self.aft_register_gaming_machine(reg_code=reg_code)
        except Exception as e:
            self.log.error(e, exc_info=True)
            return None

    def aft_unregister(self, reg_code=0x80):
        try:
            return self.aft_register_gaming_machine(reg_code=reg_code)
        except Exception as e:
            self.log.error(e, exc_info=True)
            return None

    def aft_register_gaming_machine(self, reg_code=0xFF):
        # 73
        cmd = [0x73, 0x00, reg_code]

        if reg_code == 0xFF:
            cmd[1] = 0x01
        else:
            tmp = self.asset_number + self.reg_key + self.pos_id
            cmd[1] = 0x1D
            count = 0
            for i in range(len(tmp) // 2):
                cmd.append(int(tmp[count : count + 2], 16))
                count += 2

        data = self._send_command(cmd, crc_need=True, size=34)

        if data:
            self._aft.values["registration_status"] = (
                binascii.hexlify(data[3:7])
            )

            self._aft.values["registration_key"] = str(
                binascii.hexlify(data[7:27])
            )
            self._aft.values["POS_ID"] = str(
                binascii.hexlify((data[27:]))
            )
            return self._aft.get_non_empty_status_map()

        return None

    def aft_game_lock(self, lock_timeout=100, condition=00):
        return self.aft_game_lock_and_status_request(
            lock_code=0x00, lock_timeout=lock_timeout, transfer_condition=condition
        )

    def aft_game_unlock(self):
        return self.aft_game_lock_and_status_request(lock_code=0x80)

    def aft_game_lock_and_status_request(
        self, lock_code=0x00, transfer_condition=00, lock_timeout=0
    ):
        # 74
        cmd = [
            0x74,
            lock_code,
            transfer_condition,
            self._bcd_coder_array(lock_timeout, 2),
        ]

        data = self._send_command(cmd, crc_need=True, size=40)
        if data:
            self._aft.values["asset_number"] = str(
                binascii.hexlify(bytearray(data[2:6]))
            )
            self._aft.values["game_lock_status"] = str(
                binascii.hexlify(bytearray(data[6:7]))
            )
            self._aft.values["avilable_transfers"] = str(
                binascii.hexlify(bytearray(data[7:8]))
            )
            self._aft.values["host_cashout_status"] = str(
                binascii.hexlify(bytearray(data[8:9]))
            )
            self._aft.values["AFT_status"] = str(
                binascii.hexlify(bytearray(data[9:10]))
            )
            self._aft.values["max_buffer_index"] = str(
                binascii.hexlify(bytearray(data[10:11]))
            )
            self._aft.values["current_cashable_amount"] = str(
                binascii.hexlify(bytearray(data[11:16]))
            )
            self._aft.values["current_restricted_amount"] = str(
                binascii.hexlify(bytearray(data[16:21]))
            )
            self._aft.values["current_non_restricted_amount"] = (
                str(binascii.hexlify(bytearray(data[21:26])))
            )
            self._aft.values["restricted_expiration"] = str(
                binascii.hexlify(bytearray(data[26:29]))
            )
            self._aft.values["restricted_pool_ID"] = str(
                binascii.hexlify(bytearray(data[29:31]))
            )

            return self._aft.get_non_empty_status_map()

        return None

    def aft_cancel_request(self):
        cmd = [0x72, 0x01, 0x80]
        self.aft_register()
        response = None
        data = self._send_command(cmd, crc_need=True, size=90)
        if data:
            a = int(binascii.hexlify(bytearray(data[26:27])), 16)
            response = {
                "Length": int(binascii.hexlify(bytearray(data[26:27])), 16),
                "Transfer status": AftTransferStatus.AftTransferStatus.get_status(
                    binascii.hexlify(bytearray(data[3:4]))
                ),
                "Receipt status": AftReceiptStatus.AftReceiptStatus.get_status(
                    binascii.hexlify(bytearray(data[4:5]))
                ),
                "Transfer type": AftTransferType.AftTransferType.get_status(
                    binascii.hexlify(bytearray(data[5:6]))
                ),
                "Cashable amount": int(binascii.hexlify(bytearray(data[6:11])))
                * self.denom,
                "Restricted amount": int(binascii.hexlify(bytearray(data[11:16])))
                * self.denom,
                "Nonrestricted amount": int(binascii.hexlify(bytearray(data[16:21])))
                * self.denom,
                "Transfer flags": binascii.hexlify(bytearray(data[21:22])),
                "Asset number": binascii.hexlify(bytearray(data[22:26])),
                "Transaction ID length": binascii.hexlify(bytearray(data[26:27])),
                "Transaction ID": binascii.hexlify(bytearray(data[27 : (27 + a)])),
            }
        try:
            self.aft_unregister()
        except:
            self.log.warning("AFT UNREGISTER ERROR")

        if response["Transaction ID"] == hex(self.transaction)[2:-1]:
            return response

        return False

    def aft_receipt_data(self):
        # TODO: 75
        return NotImplemented

    def aft_set_custom_ticket_data(self):
        # TODO: 76
        return NotImplemented
