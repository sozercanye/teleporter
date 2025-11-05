from pathlib import Path
from io import BytesIO
from hashlib import sha1, md5

from teleporter.core import Int
from teleporter import desktop
from teleporter.desktop import aes_encrypt_local

class FileWriteDescriptor:
    LETTER = 's'

    __slots__ = ('buffer',)

    def __init__(self):
        self.buffer = BytesIO()

    def write(self, data: bytes):
        self.buffer.write(Int(len(data) if data else 2**32 - 1))
        self.buffer.write(data)

    def encrypted(self, data: bytes, local_key: bytes):
        data = Int(0) + data # future encrypted size

        size = len(data)
        if size & 15:
            data = data.ljust(size + 16 - (size & 15), b'\x00')
        data = Int(size, 'little') + data[Int.SIZE:]

        hash_data = sha1(data).digest()
        encrypted = hash_data[:16]

        encrypted_data = aes_encrypt_local(data, local_key, encrypted)
        self.write(encrypted + encrypted_data)

    def eof(self, file: str | Path = None) -> bytes | None:
        data = self.buffer.getvalue()
        data += md5(data + Int(len(data), 'little') + Int(desktop.Desktop.APP_VERSION, 'little') + desktop.Desktop.TDF_MAGIC).digest()

        with (BytesIO() if not file else open(f'{file}{self.LETTER}', 'wb')) as f:
            f.write(desktop.Desktop.TDF_MAGIC)
            f.write(Int(desktop.Desktop.APP_VERSION, 'little'))
            f.write(data)

            if isinstance(f, BytesIO):
                return f.getvalue()
