import binascii


class TicketsCommands:
    """Existing tickets operations used by the Sas client."""

    def cash_out_ticket_info(self):
        """Send cash out ticket information

        Returns
        -------
        mixed
            dict or None

        Notes
        -------
        This is a LONG POLL COMMAND
        """
        cmd = [0x3D]
        data = self._send_command(cmd, crc_need=False)
        if data:
            return {
                "cashout_ticket_number": int(binascii.hexlify(bytearray(data[1:3]))),
                "cashout_amount_in_cents": int(binascii.hexlify(bytearray(data[3:]))),
            }

        return None

    def set_secure_enhanced_validation_id(
        self, machine_id=[0x01, 0x01, 0x01], seq_num=[0x00, 0x00, 0x01]
    ):
        """
        For a gaming machine to perform secure enhanced ticket/receipt/handpay validation, the host must use
        the type S long poll. The host may also use this long poll to retrieve the current gaming
        machine validation ID and validation sequence number by issuing the 4C command with a gaming
        machine validation ID of zero. If a gaming machine is not configured to perform secure enhanced
        validation, or is responding to a host that is not the validation controller, it ignores this long poll

        :param machine_id: 3 binary - Gaming machine validation ID number
        :param seq_num: 3 binary - Starting sequence number (incremented before being assigned to each event)
        :return:
        """
        # 4C
        # FIXME: set_secure_enhanced_validation_ID @todo... im beat...@well-it-wasnt-me
        cmd = [0x4C, machine_id, seq_num]
        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._tickets.values["machine_ID"] = int(
                binascii.hexlify(bytearray(data[1:4]))
            )
            self._tickets.values["sequence_number"] = int(
                binascii.hexlify(bytearray(data[4:8]))
            )
            return data

        return None

    def enhanced_validation_information(self, curr_validation_info=0):
        """Send Enhanced Validation Information Command

        Parameters
        ----------
        curr_validation_info :
            Function code; 00 = read current validation info | 01-1F = validation info from buffer index n | FF = look ahead at current validation info

        Returns
        -------
        mixed :
            dict | none
        """
        # FIXME: enhanced_validation_information
        cmd = [0x4D, curr_validation_info]
        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._tickets.values["validation_type"] = int(
                binascii.hexlify(bytearray(data[1:2]))
            )
            self._tickets.values["index_number"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._tickets.values["date_validation_operation"] = str(
                binascii.hexlify(bytearray(data[3:7]))
            )
            self._tickets.values["time_validation_operation"] = str(
                binascii.hexlify(bytearray(data[7:10]))
            )
            self._tickets.values["validation_number"] = str(
                binascii.hexlify(bytearray(data[10:18]))
            )
            self._tickets.values["amount"] = int(
                binascii.hexlify(bytearray(data[18:23]))
            )
            self._tickets.values["ticket_number"] = int(
                binascii.hexlify(bytearray(data[23:25]))
            )
            self._tickets.values["validation_system_ID"] = int(
                binascii.hexlify(bytearray(data[25:26]))
            )
            self._tickets.values["expiration_date_printed_on_ticket"] = str(
                binascii.hexlify(bytearray(data[26:30]))
            )
            self._tickets.values["pool_id"] = int(
                binascii.hexlify(bytearray(data[30:32]))
            )

            return self._tickets.get_non_empty_status_map()

        return None

    def validation_meters(self, type_of_validation=0x00):
        """Send validation meters
        Parameters
        ----------
        type_of_validation : int
            Type of validation

            ==============      =====
            Code (Binary)       Validation type
            ==============      =====
            00                   Cashable ticket from cashout or win, no handpay lockup
            01                   Restricted promotional ticket from cashout
            02                   Cashable ticket from AFT transfer
            03                   Restricted ticket from AFT transfer
            04                   Debit ticket from AFT transfer
            10                   Cancelled credit handpay (receipt printed
            20                   Jackpot handpay (receipt printed)
            40                   Cancelled credit handpay (no receipt)
            60                   Jackpot handpay (no receipt)
            80                   Cashable ticket redeemed
            81                   Restricted promotional ticket redeemed
            82                   Nonrestricted promotional ticket redeemed
            ==============      =====


        Returns
        -------
        mixed :
            dict | none

        Notes
        -------
        Understanding the response:
            - bin_validation_type :
                See the table "Type of validation"
            - total_validations : 4 BCD
                Total number of validations of type
            - cumulative_amount : 5 BCD
                Cumulative validation amount in units of cents
        """
        # FIXME: validation_meters
        cmd = [0x50, type_of_validation]
        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._meters.values["bin_validation_type"] = int(
                binascii.hexlify(bytearray(data[1]))
            )
            self._meters.values["total_validations"] = int(
                binascii.hexlify(bytearray(data[2:6]))
            )
            self._meters.values["cumulative_amount"] = str(
                binascii.hexlify(bytearray(data[6:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def pending_cashout_info(self):
        # 57
        cmd = [0x57]
        data = self._send_command(cmd, crc_need=False)
        if data:
            self._tickets.values["cashout_type"] = int(
                binascii.hexlify(bytearray(data[1:2]))
            )
            self._tickets.values["cashout_amount"] = str(
                binascii.hexlify(bytearray(data[2:]))
            )
            return self._tickets.get_non_empty_status_map()

        return None

    def rcv_validation_number(self, validation_id=1, valid_number=0):
        """Receive Validation number
        Parameters
        ----------
        validation_id : int
            Validation System ID Code (00 = system validation denied)

        valid_number : int
            validation number to use for cashout (not used if validation denied)

        Returns
        -------
        Mixed
            str | none - 00 = command ack | 80 = Not in cashout | 81 = Improper validation rejected
        """
        cmd = [
            0x58,
            self._bcd_coder_array(validation_id, 1),
            self._bcd_coder_array(valid_number, 8),
        ]
        data = self._send_command(cmd, crc_need=True)
        if data:
            return str(binascii.hexlify(bytearray(data[1])))

        return None

    def ticket_validation_data(self):
        # 70
        # FIXME: ticket_validation_data
        # @todo This is wrong for sure....this should reply 9 BCD BCD-encoded 18 digit decimal validation number. The first two digits are a 2
        # digit system ID code indicating how to interpret the following 16 digits.
        # System ID code 00 indicates that the following 16 digits represent a SAS
        # secure enhanced validation number. Other system ID codes and parsing codes
        # will be assigned by IGT as needed
        cmd = [0x70]
        data = self._send_command(cmd, True, crc_need=False)
        if data:
            self._meters.values["ticket_status"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._meters.values["ticket_amount"] = str(
                binascii.hexlify(bytearray(data[3:8]))
            )
            self._meters.values["parsing_code"] = int(
                binascii.hexlify(bytearray(data[8:9]))
            )
            self._meters.values["validation_data"] = str(
                binascii.hexlify(bytearray(data[9:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def redeem_ticket(
        self,
        transfer_code=0,
        transfer_amount=0,
        parsing_code=0,
        validation_data=0,
        restricted_expiration=0,
        pool_id=0,
    ):
        # 71
        # FIXME: redeem_ticket
        cmd = [
            0x71,
            0x21,
            transfer_code,
            self._bcd_coder_array(transfer_amount, 5),
            parsing_code,
            self._bcd_coder_array(validation_data, 8),
            self._bcd_coder_array(restricted_expiration, 4),
            self._bcd_coder_array(pool_id, 2),
        ]
        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._meters.values["machine_status"] = int(
                binascii.hexlify(bytearray(data[2:3]))
            )
            self._meters.values["transfer_amount"] = int(
                binascii.hexlify(bytearray(data[3:8]))
            )
            self._meters.values["parsing_code"] = int(
                binascii.hexlify(bytearray(data[8:9]))
            )
            self._meters.values["validation_data"] = str(
                binascii.hexlify(bytearray(data[9:]))
            )
            return self._meters.get_non_empty_status_map()

        return None

    def extended_validation_status(
        self,
        control_mask=[0, 0],
        status_bits=[0, 0],
        cashable_ticket_receipt_exp=0,
        restricted_ticket_exp=0,
    ):
        # 7B
        cmd = [
            0x7B,
            0x08,
            control_mask,
            status_bits,
            self._bcd_coder_array(cashable_ticket_receipt_exp, 2),
            self._bcd_coder_array(restricted_ticket_exp, 2),
        ]

        data = self._send_command(cmd, True, crc_need=True)
        if data:
            self._aft.values["asset_number"] = str(
                binascii.hexlify(bytearray(data[2:6]))
            )
            self._aft.values["status_bits"] = str(
                binascii.hexlify(bytearray(data[6:8]))
            )
            self._aft.values["cashable_ticket_receipt_exp"] = str(
                binascii.hexlify(bytearray(data[8:10]))
            )
            self._aft.values["restricted_ticket_exp"] = str(
                binascii.hexlify(bytearray(data[10:]))
            )

            return self._aft.get_non_empty_status_map()

        return None

    def set_extended_ticket_data(self):
        # TODO: 7C
        return NotImplemented

    def set_ticket_data(self):
        # TODO: 7D
        return NotImplemented
