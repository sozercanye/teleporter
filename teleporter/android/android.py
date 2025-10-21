from __future__ import annotations
from pathlib import Path
import re
from io import BytesIO
import base64

import teleporter
from teleporter.android import NativeByteBuffer, Auth, Headers, Datacenter

class Int(bytes):
    SIZE = 4

    @classmethod
    def _read(cls, data: BytesIO, signed: bool = True) -> int:
        return int.from_bytes(data.read(cls.SIZE), 'little', signed=signed)

    def __new__(cls, value: int, signed: bool = True) -> bytes:
        return value.to_bytes(cls.SIZE, 'little', signed=signed)

class Long(Int):
    SIZE = 8

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

        kwargs = {}
        if userconfig:
            if isinstance(userconfig, bytes): content = userconfig
            else:
                with open(userconfig, 'rb') as f:
                    content = f.read()
            b = BytesIO(base64.b64decode(cls.USER_ID_PATTERN.search(content).group(1).strip().replace(b'&#10;', b'')))
            kwargs = {
                'constructor_id': int.from_bytes(b.read(4), 'little'),
                'flags': Int._read(b),
                'flags2': Int._read(b),
                'id': Long._read(b)
            }

        return cls(dc_id, auth_key, **kwargs)

    def to_android(self: 'teleporter.Teleporter',
        tgnet: str | Path = None,
        userconfig: str | Path = None,
        is_test: bool = False,
        version: int = 5,
        current_dc_version: int = 13,
        last_dc_init_version: int = 48502,
        last_dc_media_init_version: int = 48502
    ) -> list[bytes, bytes] | bytes | None:
        buffer = NativeByteBuffer()
        buffer._write_front_headers(Headers(self.dc_id, is_test, version))
        buffer._write_datacenters([Datacenter(
            self.dc_id, Auth(self.auth_key),
            current_dc_version, last_dc_init_version, last_dc_media_init_version
        )])
        buffer._write_buffer_length()
        tgnet_value = buffer.get_value()

        b = BytesIO()
        b.write(Int(self.constructor_id))
        b.write(Int(self.flags))
        b.write(Int(self.flags2))
        b.write(Long(self.id))
        userconfig_value = b'''<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<map>
    <string name="user">%s</string>
</map>''' % base64.b64encode(b.getvalue())

        result = []
        for path, value in (
            (tgnet, tgnet_value),
            (userconfig, userconfig_value)
        ):
            if not path: result.append(value)
            else:
                if not isinstance(path, Path):
                    path = Path(path)
                path.parent.mkdir(parents=True, exist_ok=True)

                with open(path, 'wb') as f:
                    f.write(value)
        return (result[0] if len(result) == 1 else result) if result else None
