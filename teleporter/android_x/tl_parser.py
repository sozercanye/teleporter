from io import BytesIO
from struct import unpack

from teleporter.core import Int, Long
from teleporter.android_x import BinlogEvent

# https://github.com/tdlib/td/blob/master/tdutils/td/utils/tl_parsers.h#L24
class TLParser:
    __slots__ = ('stream',)

    def __init__(self, content: bytes):
        self.stream = BytesIO(content)

    def read_byte(self) -> int:
        """Reads a single byte value."""
        return self.stream.read(1)[0]

    def read_int(self, signed: bool = True) -> int:
        """Reads an integer (4 bytes) value."""
        return Int.read(self.stream, byteorder='little', signed=signed)

    def read_long(self, signed: bool = True) -> int:
        """Reads a long integer (8 bytes) value."""
        return Long.read(self.stream, byteorder='little', signed=signed)

    def read_double(self) -> float:
        """Reads a real floating point (8 bytes) value."""
        return unpack('<d', self.stream.read(8))[0]

    def read_bytes(self) -> bytes:
        first_byte = self.read_byte()
        if first_byte == 254:
            length = self.read_byte() | (self.read_byte() << 8) | (
                self.read_byte() << 16)
            padding = length % 4
        else:
            length = first_byte
            padding = (length + 1) % 4

        data = self.stream.read(length)
        if padding > 0:
            padding = 4 - padding
            self.stream.read(padding)

        return data

    def read_string(self) -> str:
        return str(self.read_bytes(), encoding='utf-8', errors='replace')

    # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/Binlog.cpp#L112
    def read_next_event(self) -> BinlogEvent:
        size = self.read_int()
        self.stream.seek(-4, 1) # go back

        if size > BinlogEvent.MAX_SIZE:
            raise ValueError(f'Event is too big: {size}.')
        elif size < BinlogEvent.MIN_SIZE:
            raise ValueError(f'Event is too small: {size}.')
        elif size % 4 != 0:
            raise ValueError(f'Event size is not expected: {size}.')
        return BinlogEvent(self.stream.read(size))
