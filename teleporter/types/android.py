from pathlib import Path
import re
from io import BytesIO
import base64

import aiofiles

import teleporter
from teleporter.session import Session, NativeByteBuffer

USER_ID_PATTERN = re.compile(rb'<string name="user">(.+)</string>')

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
    @classmethod
    async def android(cls: type['teleporter.Teleporter'],
        tgnet: bytes | str | Path,
        userconfig: bytes | str | Path
    ) -> 'teleporter.Teleporter':
        if isinstance(tgnet, bytes): content = tgnet
        else:
            async with aiofiles.open(tgnet, 'rb') as f:
                content = await f.read()

        buffer = NativeByteBuffer(content)
        session = Session(buffer._read_headers(), buffer._read_datacenters())

        if isinstance(userconfig, bytes): content = userconfig
        else:
            async with aiofiles.open(userconfig, 'rb') as f:
                content = await f.read()

        b = BytesIO(base64.b64decode(USER_ID_PATTERN.search(content).group(1).strip().replace(b'&#10;', b'')))
        return cls(session=session, constructor_id=int.from_bytes(b.read(4), 'little'), flags=Int._read(b), flags2=Int._read(b), id=Long._read(b))

    async def to_android(self: 'teleporter.Teleporter',
        tgnet: str | Path = None,
        userconfig: str | Path = None
    ) -> list[bytes, bytes] | bytes | None:
        buffer = NativeByteBuffer()
        buffer._write_front_headers(self.session.headers)
        buffer._write_datacenters(self.session.datacenters.values())
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

                async with aiofiles.open(path, 'wb') as f:
                    await f.write(value)
        return (result[0] if len(result) == 1 else result) if result else None
