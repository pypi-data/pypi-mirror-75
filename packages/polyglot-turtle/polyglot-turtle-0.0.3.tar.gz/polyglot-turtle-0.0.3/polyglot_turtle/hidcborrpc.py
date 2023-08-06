# SPDX-License-Identifier: MIT

import re
from typing import List, Tuple, Union

import cbor2
import hid
from simplehdlc import SimpleHDLC


class CommandExecutionTimeoutException(Exception):
    pass


class CommandExecutionFailedException(Exception):
    pass


class ConnectFailedException(Exception):
    pass


class IdMismatchException(Exception):
    pass


class HidCborRpcDevice(object):
    def __init__(self, serial_number: str, vendor_id: int, product_id: int, timeout: int):
        if serial_number is not None:
            if not re.match(r"[0-9A-F]{32}", serial_number.upper()):
                raise ValueError("Serial number is invalid")
            self._serial_number = serial_number.upper()
        else:
            self._serial_number = None

        if not 0 <= vendor_id <= 0xFFFF:
            raise ValueError("Vendor ID is invalid")

        if not 0 <= product_id <= 0xFFFF:
            raise ValueError("Product ID is invalid")

        self._vendor_id = vendor_id
        self._product_id = product_id

        self._timeout = timeout

        self._hid = hid.device()
        self._hid.open(serial_number=self._serial_number,  vendor_id=self._vendor_id, product_id=self._product_id)

        self._hdlc = SimpleHDLC(self._hdlc_decode_success, 4096)
        self._last_hdlc_response = None

        self._cbor_id = 1
        self._function_index_table = {}
        self._max_size = 512

        self._ping()
        if self._get_rpc_version() != 1:
            raise ConnectFailedException("Invalid RPC version")

        self._update_function_index_table()

        self._max_size = self._execute_command("max_size")

    def _ping(self):
        if self._execute_command("__ping") != "pong":
            raise CommandExecutionFailedException("Device did not correctly respond to ping")

    def _update_function_index_table(self):
        self._function_index_table = self._execute_command("__funcs")

    def _get_rpc_version(self):
        return self._execute_command("__version")

    def _hdlc_decode_success(self, payload):
        self._last_hdlc_response = payload

    def _execute_command(self, function_name: str, args: Union[List, Tuple] = tuple(), force_id: int = None,
                         allow_lookup: bool = True):
        command = {}

        if force_id is None:
            command["id"] = self._cbor_id
            self._cbor_id += 1
        else:
            command["id"] = force_id

        if allow_lookup and function_name in self._function_index_table:
            command["func"] = self._function_index_table[function_name]
        else:
            command["func"] = function_name

        command["args"] = args

        encoded = SimpleHDLC.encode(cbor2.dumps(command))

        if len(encoded) > self._max_size:
            raise ValueError("Packet is too long to send to device")

        tx_count = 0
        while True:
            bytes_remaining = len(encoded) - tx_count
            if bytes_remaining <= 0:
                break

            if bytes_remaining >= 64:
                self._hid.write(b"\x00" + encoded[tx_count:tx_count+64])
            else:
                buf = encoded[tx_count:]
                buf = buf + bytes([SimpleHDLC.FRAME_BOUNDARY_MARKER] * (64-len(buf)))
                assert len(buf) == 64
                self._hid.write(b"\x00" + buf)
            tx_count += 64

        while True:
            response = bytes(self._hid.read(64, timeout_ms=1000*self._timeout))

            if len(response) == 0:
                raise CommandExecutionTimeoutException
            else:
                self._hdlc.parse(response)

            if self._last_hdlc_response is not None:
                break

        result = cbor2.loads(self._last_hdlc_response)
        self._last_hdlc_response = None

        if result.get("id") != command["id"]:
            raise IdMismatchException

        if 'err' in result:
            error_msg = "received status code {} with the message: {}".format(result['err']['c'], result['err']['msg'])
            raise CommandExecutionFailedException(error_msg)

        return result['res']