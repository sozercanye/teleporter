from __future__ import annotations
from os import PathLike

import teleporter
from teleporter.core import Int, Long, tgcrypto
from teleporter.android_x import TLParser, AesCtrEncryptionEvent, HandlerType

def to_int(data: bytes) -> int:
    if data.startswith(b'I'):
        data = data[1:]
    return int(data.decode())

# https://github.com/tdlib/td/blob/cb164927417f22811c74cd8678ed4a5ab7cb80ba/tddb/td/db/binlog/Binlog.cpp#L95
class AndroidX:
    @classmethod
    def android_x(cls: type['teleporter.Teleporter'],
        td: str | PathLike[str]
    ) -> 'teleporter.Teleporter':
        tgcrypto()
        from tgcrypto import ctr256_encrypt

        with open(td, 'rb') as f:
            content = f.read()

        parser = TLParser(content)
        event = parser.read_next_event()
        event.validate()
        aes_encryption_event = AesCtrEncryptionEvent(event.event_data)
        secret_key = aes_encryption_event.generate_key()

        if aes_encryption_event.generate_hash(secret_key) != aes_encryption_event.key_hash:
            raise ValueError('Bad decrypt key, data not decrypted — incorrect passcode?')

        data = parser.stream.read()
        # https://github.com/tdlib/td/blob/81dc2e242b6c3ea358dba6b5a750727c378dc098/tddb/td/db/binlog/Binlog.cpp#L472
        decrypted_buffer = ctr256_encrypt(data, secret_key, aes_encryption_event.iv, bytes(1))

        # https://github.com/tdlib/td/blob/81dc2e242b6c3ea358dba6b5a750727c378dc098/tddb/td/db/binlog/Binlog.cpp#L478
        parser = TLParser(decrypted_buffer)

        length = len(parser.stream.getvalue())
        map = {}

        while parser.stream.tell() != length:
            event = parser.read_next_event()
            event.validate()

            if event.type in {HandlerType.config_pmc_magic, HandlerType.binlog_pmc_magic}:
                event_parser = TLParser(event.event_data)
                key = event_parser.read_string()
                map[key] = event_parser.read_bytes()

        assert map['auth'] == b'ok'

        dc_id = to_int(map.get('main_dc_id', map['webfile_dc_id']))

        raw_auth_key = map[f'auth{dc_id}']
        parser = TLParser(raw_auth_key)
        parser.stream.seek(Long.SIZE) # auth_key_id
        parser.stream.seek(Int.SIZE, 1) # flags
        auth_key = parser.read_bytes()

        user_id = to_int(map['my_id'])

        return cls(dc_id, auth_key,  user_id)
