"""
NativeByteBuffer class is a full copy of telegram's class NativeByteBuffer
https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/jni/tgnet/NativeByteBuffer.cpp
"""

from __future__ import annotations
from typing import Literal
from io import BytesIO
import time
import binascii

from teleporter.core import IP
from teleporter import android

class NativeByteBuffer:
    def __init__(self, data: bytes | bytearray = None):
        self.stream = BytesIO(data)

    def __len__(self) -> int:
        return len(self.stream.getvalue())

    def get_value(self) -> bytes:
        return self.stream.getvalue()

    def read_bytes(self, length: int) -> bytes:
        return self.stream.read(length)

    def read_byte(self) -> int:
        return self.read_bytes(1)[0]

    def read_number(self, length: int, signed: bool = True) -> int:
        return int.from_bytes(self.read_bytes(length), byteorder='little', signed=signed)

    def read_int(self, signed: bool = True) -> int:
        return self.read_number(4, signed=signed)

    def read_long(self, signed: bool = True) -> int:
        return self.read_number(8, signed=signed)

    def read_bool(self) -> bool:
        value = self.read_int(signed=False)
        if value == 0x997275b5:
            return True
        elif value == 0xbc799737:
            return False
        raise BufferError(f'Unexpected byte value: {value}.')

    def read_byte_array(self) -> bytes:
        sl = 1
        length = self.read_number(1, signed=False)
        if length >= 254:
            length = self.read_number(3, signed=False)
            sl = 4

        addition = (length + sl) % 4
        if addition != 0:
            addition = 4 - addition

        result = self.read_bytes(length)
        self.read_bytes(addition)
        return result

    def read_string(self) -> str:
        return str(self.read_byte_array(), encoding='utf-8', errors='replace')

    def write_bytes(self, data: bytearray | bytes):
        self.stream.write(data)

    def write_number(self, number: int, length: int, signed: bool = True):
        self.write_bytes(number.to_bytes(length, byteorder='little', signed=signed))

    def write_int(self, number: int, signed: bool = True):
        self.write_number(number=number, length=4, signed=signed)

    def write_long(self, number: int, signed: bool = True):
        self.write_number(number=number, length=8, signed=signed)

    def write_bool(self, value: bool):
        if value is True:
            self.write_int(0x997275b5, signed=False)
        else:
            self.write_int(0xbc799737, signed=False)

    def write_byte_array(self, data: bytearray | bytes):
        length = len(data)
        if length < 254: # 1byte(len) + data
            self.write_number(length, 1, signed=False)
        else: # 1byte(len) + 3bytes(lenMore254) + data
            self.write_number(254, 1, signed=False)
            self.write_number(length, 3, signed=False)

        self.write_bytes(data)

        # calculate padding
        sl = 1 if length < 254 else 4
        total_length = length + sl
        padding = (4 - (total_length % 4)) % 4

        # write padding bytes
        if padding:
            self.write_bytes(b'\x00' * padding)

    def write_string(self, value: str):
        self.write_byte_array(value.encode())

    def _write_front_headers(self, headers: android.Headers):
        self.write_int(headers.version)
        self.write_bool(headers.is_test)

        if headers.version >= 3:
            self.write_bool(headers.client_blocked)
        if headers.version >= 4:
            self.write_string(headers.last_init_system_langcode)
        self.write_bool(True)
        self.write_int(headers.dc_id)
        self.write_int(headers.time_difference)
        self.write_int(headers.last_dc_update_time)
        self.write_long(headers.push_session_id)

        if headers.version >= 2:
            self.write_bool(headers.registered_for_internal_push)
        if headers.version >= 5:
            self.write_int(headers.last_server_time)

        self.write_int(0) # writing sessions_to_destroy is not implemented

    def _write_auth_key(self, auth_key: bytes, auth_key_id: int):
        if auth_key:
            self.write_int(len(auth_key), signed=False)
            self.write_bytes(auth_key)
            self.write_long(auth_key_id)
        else:
            self.write_int(0)
            self.write_long(0)

    def _write_datacenters(self, datacenters: list[android.Datacenter]):
        self.write_int(len(datacenters))
        for datacenter in datacenters:
            self.write_int(datacenter.current_version)
            self.write_int(datacenter.dc_id)
            self.write_int(datacenter.last_init_version)

            if datacenter.current_version > 10:
                self.write_int(datacenter.last_init_media_version)

            # writing ips
            for address_group in datacenter.ips:
                self.write_int(len(datacenter.ips[address_group]))

                for ip in datacenter.ips[address_group]:
                    self.write_string(ip.address)
                    self.write_int(ip.port)

                    if datacenter.current_version >= 7:
                        self.write_int(ip.flags)

                    if datacenter.current_version >= 11:
                        self.write_byte_array(ip.secret)
                    elif datacenter.current_version >= 9:
                        raise NotImplementedError('Writing sessions with Datacenter\'s versions 9 and 10 is not supported, please use another version.')

            if datacenter.current_version >= 6:
                self.write_bool(datacenter.is_cdn)

            # writing auth credentials
            if datacenter.auth.auth_key_perm:
                self.write_int(len(datacenter.auth.auth_key_perm), signed=False)
                self.write_bytes(datacenter.auth.auth_key_perm)
            else:
                self.write_int(0)

            if datacenter.current_version >= 4:
                self.write_long(datacenter.auth.auth_key_perm_id)
            else:
                raise NotImplementedError('Datacenters below version 4 are not supported')

            if datacenter.current_version >= 8:
                self._write_auth_key(datacenter.auth.auth_key_temp, datacenter.auth.auth_key_temp_id)
            if datacenter.current_version >= 12:
                self._write_auth_key(datacenter.auth.auth_key_media_temp, datacenter.auth.auth_key_media_temp_id)

            self.write_int(datacenter.auth.authorized)

            # writing salt info
            self.write_int(0)
            if datacenter.current_version >= 13:
                self.write_int(0) # writing salts in session is not implemented

    def _write_buffer_length(self):
        buffer_with_length = NativeByteBuffer()
        buffer_with_length.write_int(len(self))
        buffer_with_length.write_bytes(self.get_value())
        self.stream.seek(0)
        self.write_bytes(buffer_with_length.get_value())

    def _read_headers(self) -> android.Headers:
        self.read_int()
        headers = android.Headers(
            version=self.read_int(),
            is_test=self.read_bool()
        )
        if headers.version >= 3:
            client_blocked = self.read_bool()
            headers.client_blocked = client_blocked
        if headers.version >= 4:
            last_init_system_langcode = self.read_string()
            headers.last_init_system_langcode = last_init_system_langcode

        if self.read_bool(): # will be False if session is empty
            headers.dc_id = self.read_int(signed=False)
            headers.time_difference = self.read_int()
            headers.last_dc_update_time = self.read_int()
            headers.push_session_id = self.read_long()

            if headers.version >= 2:
                headers.registered_for_internal_push = self.read_bool()
            if headers.version >= 5:
                headers.last_server_time = self.read_int()
                headers.current_time = int(time.time())

                if headers.time_difference < headers.current_time < headers.last_server_time:
                    headers.time_difference += (headers.last_server_time - headers.current_time)

            count = self.read_int(signed=False)
            for _ in range(count):
                headers.sessions_to_destroy.append(self.read_long())
        return headers

    def _get_ip(self,
        current_version: int,
        ip_type: Literal['Ipv4', 'Ipv6', 'Ipv4Download', 'Ipv6Download']
    ) -> IP:
        ip = IP(ip_type, self.read_string(), self.read_int())

        if current_version >= 7:
            ip.flags = self.read_int()

        if current_version >= 11:
            ip.secret = self.read_byte_array()
        elif current_version >= 9:
            ip.secret = self.read_byte_array()
            if ip.secret:
                ip.secret = binascii.unhexlify(ip.secret)
        return ip

    def _read_datacenters(self) -> list[android.Datacenter]:
        datacenters = []
        datacenter_count = self.read_int()

        for _ in range(datacenter_count):
            datacenter = android.Datacenter(
                current_version=self.read_int(),
                dc_id=self.read_int(),
                last_init_version=self.read_int()
            )

            if datacenter.current_version > 10:
                datacenter.last_init_media_version = self.read_int()

            count = 4 if datacenter.current_version >= 5 else 1
            for i in range(count):
                type = {
                    0: 'Ipv4',
                    1: 'Ipv6',
                    2: 'Ipv4Download',
                    3: 'Ipv6Download'
                }.get(i)

                if type:
                    ip_count = self.read_int()
                    for _ in range(ip_count):
                        ip = self._get_ip(datacenter.current_version, type)
                        datacenter.ips[type].append(ip)

            if datacenter.current_version >= 6:
                datacenter.is_cdn = self.read_bool()

            datacenter.auth = self._auth(datacenter.current_version)
            datacenter.salt = self._salt_info(datacenter.current_version)
            datacenters.append(datacenter)

        return datacenters

    def _auth(self, current_version: int) -> android.Auth:
        auth = android.Auth()
        len_of_bytes = self.read_int(signed=False)
        if len_of_bytes != 0:
            auth.auth_key_perm = self.read_bytes(len_of_bytes)

        if current_version >= 4:
            auth.auth_key_perm_id = self.read_long()

        else:
            len_of_bytes = self.read_int(signed=False)
            if len_of_bytes != 0:
                auth.auth_key_perm_id = self.read_long()

        if current_version >= 8:
            len_of_bytes = self.read_int(signed=False)
            if len_of_bytes != 0:
                auth.auth_key_temp = self.read_bytes(len_of_bytes)
            auth.auth_key_temp_id = self.read_long()

        if current_version >= 12:
            len_of_bytes = self.read_int(signed=False)
            if len_of_bytes != 0:
                auth.auth_key_media_temp = self.read_bytes(len_of_bytes)
            auth.auth_key_media_temp_id = self.read_long()
        auth.authorized = self.read_int()
        return auth

    def _read_salt(self, salts: list['android.Salt']):
        bytes_len = self.read_int()
        for x in range(bytes_len):
            salt = android.Salt()
            salt.salt_valid_since = self.read_int()
            salt.salt_valid_until = self.read_int()
            salt.salt = self.read_long()
            salts.append(salt)

    def _salt_info(self, current_version: int) -> list['android.Salt']:
        salts = []
        self._read_salt(salts)

        if current_version >= 13:
            self._read_salt(salts)

        return salts
