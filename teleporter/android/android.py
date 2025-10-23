from __future__ import annotations
from pathlib import Path
import re
from io import BytesIO
import base64

import teleporter
from teleporter.core import Int, Long
from teleporter.android import NativeByteBuffer, Auth, Headers, Datacenter

class Android:
    USER_ID_PATTERN = re.compile(rb'<string name="user">(.+)</string>')

    @classmethod
    def android(cls: type['teleporter.Teleporter'],
        tgnet: bytes | str | Path,
        userconfig: bytes | str | Path = None
    ) -> 'teleporter.Teleporter':
        if isinstance(tgnet, bytes): content = tgnet
        else:
            with open(tgnet, 'rb') as f:
                content = f.read()

        buffer = NativeByteBuffer(content)
        dc_id = buffer._read_headers().dc_id
        auth_key = next(datacenter.auth.auth_key_perm for datacenter in buffer._read_datacenters() if datacenter.dc_id == dc_id)

        if userconfig:
            if isinstance(userconfig, bytes): content = userconfig
            else:
                with open(userconfig, 'rb') as f:
                    content = f.read()
            b = BytesIO(base64.b64decode(cls.USER_ID_PATTERN.search(content).group(1).strip().replace(b'&#10;', b'')))

            constructor_id = Int.read(b, byteorder='little', signed=True)
            b.seek(2 * Int.SIZE, 1) # flags1 & flags2
            user_id = Long.read(b, byteorder='little', signed=True)
            return cls(dc_id, auth_key, user_id, constructor_id)
        return cls(dc_id, auth_key)

    def to_android(self: 'teleporter.Teleporter',
        tgnet: str | Path = 'tgnet.dat',
        userconfig: str | Path = 'userconfing.xml',
        is_test: bool = False,
        version: int = 5,
        current_dc_version: int = 13,
        last_dc_init_version: int = 48502,
        last_dc_media_init_version: int = 48502
    ):
        buffer = NativeByteBuffer()
        buffer._write_front_headers(Headers(self.dc_id, is_test, version))
        buffer._write_datacenters([Datacenter(
            self.dc_id, Auth(self.auth_key),
            current_dc_version, last_dc_init_version, last_dc_media_init_version
        )])
        buffer._write_buffer_length()
        tgnet_value = buffer.get_value()

        b = BytesIO()
        b.write(Int(self.constructor_id, byteorder='little', signed=True))
        b.write(Int(0, byteorder='little', signed=True))
        b.write(Int(0, byteorder='little', signed=True))
        b.write(Long(self.user_id, byteorder='little', signed=True))
        userconfig_value = b'''<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<map>
    <string name="user">%s</string>
</map>''' % base64.b64encode(b.getvalue())

        for path, value in (
            (tgnet, tgnet_value),
            (userconfig, userconfig_value)
        ):
            if not isinstance(path, Path):
                path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'wb') as f:
                f.write(value)
