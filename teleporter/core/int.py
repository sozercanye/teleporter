from typing import Literal, BinaryIO

class Int(bytes):
    SIZE = 4

    @classmethod
    def read(cls, data: bytes | BinaryIO, byteorder: Literal['little', 'big'] = 'big', signed: bool = False) -> int:
        return int.from_bytes(data if isinstance(data, bytes) else data.read(cls.SIZE), byteorder, signed=signed)

    def __new__(cls, value: int, byteorder: Literal['little', 'big'] = 'big', signed: bool = False) -> bytes:
        return value.to_bytes(cls.SIZE, byteorder, signed=signed)

class Long(Int):
    SIZE = 8
