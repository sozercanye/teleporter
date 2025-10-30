import hmac
from hashlib import sha256, pbkdf2_hmac

from teleporter import android_x

# https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/Binlog.cpp#L31
class AesCtrEncryptionEvent:
    MIN_SALT_SIZE = 16 # it isn't used
    DEFAULT_SALT_SIZE = 32 # it isn't used
    KEY_SIZE = 32
    IV_SIZE = 16 # it isn't used
    HASH_SIZE = 32 # it isn't used
    KDF_ITERATION_COUNT = 60002 # it isn't used
    KDF_FAST_ITERATION_COUNT = 2

    DEFAULT_PASSCODE = b'cucumber'
    # https://github.com/tdlib/td/blob/97ded01095246a3a693bc85bef4bca5d1af177dd/td/telegram/Td.cpp#L2770

    __slots__ = ('key_salt', 'iv', 'key_hash')

    def __init__(self, content: bytes):
        parser = android_x.TLParser(content)
        # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/Binlog.cpp#L87
        parser.stream.seek(4) # BEGIN_PARSE_FLAGS function consumes 4 bytes, because of read_int()

        self.key_salt = parser.read_bytes() # KEY_SIZE = 32
        self.iv = parser.read_bytes() # IV_SIZE = 16
        self.key_hash = parser.read_bytes() # HASH_SIZE = 16

    def generate_key(self, passcode: bytes = DEFAULT_PASSCODE) -> bytes:
        # https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/Binlog.cpp#L62
        return pbkdf2_hmac('sha256', passcode, self.key_salt, self.KDF_FAST_ITERATION_COUNT if passcode == self.DEFAULT_PASSCODE else self.KDF_ITERATION_COUNT, dklen=self.KEY_SIZE)

    @staticmethod
    def generate_hash(key: bytes) -> bytes:
        return hmac.new(key, b'cucumbers everywhere', sha256).digest()
