import zlib

from teleporter import android_x

# https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/BinlogEvent.h#L50
class BinlogEvent:
    MAX_SIZE = 1 << 24
    HEADER_SIZE = 4 + 8 + 4 + 4 + 8
    TAIL_SIZE = 4
    MIN_SIZE = HEADER_SIZE + TAIL_SIZE

    __slots__ = ('raw_event', 'event_data', 'size', 'id', 'type', 'flags', 'extra', 'crc32')

    # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/BinlogEvent.cpp#L17
    def __init__(self, content: bytes):
        parser = android_x.TLParser(content)
        self.raw_event = parser.stream.getvalue()

        self.size = parser.read_int(False)  # cast into uint32: 4 bytes
        self.id = parser.read_long(False)  # cast into uint64: 8 bytes
        self.type = parser.read_int(True)  # no cast: 4 bytes
        self.flags = parser.read_int(True)  # no cast: 4 bytes
        self.extra = parser.read_long(False)  # cast into uint64: 8 bytes

        # in original code it says "skip data". this was implemented, so inside method `get_data`
        # this content aka event_data would be read and returned. but we do it already in place
        # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/BinlogEvent.cpp#L26
        # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/BinlogEvent.cpp#L33
        # HEADER_SIZE = sum bytes of: size + id_ + type_ + flags + extra
        self.event_data = parser.stream.read(self.size - self.MIN_SIZE)

        self.crc32 = parser.read_int(False)  # cast into uint32: 4 bytes

    def validate(self):
        if len(self.raw_event) < self.MIN_SIZE:
            raise ValueError(f'Event is too small: {len(self.raw_event)}.')

        expected_binlog_event = BinlogEvent(self.raw_event)
        if self.size != expected_binlog_event.size or self.size != len(self.raw_event):
            raise ValueError(f'Size of event changed: was={self.size}, now={expected_binlog_event.size}, real_size={len(self.raw_event)}.')

        data = self.raw_event[:-self.TAIL_SIZE]
        calculated_crc = zlib.crc32(data)
        stored_crc = expected_binlog_event.crc32

        if calculated_crc != self.crc32 or calculated_crc != stored_crc:
            raise ValueError(f'CRC32 hash mismatch: actual={calculated_crc}, expected={self.crc32}.')
