from __future__ import annotations
from os import PathLike
from pathlib import Path
from io import BytesIO

import teleporter
from teleporter.core import Int, Long, tgcrypto
from teleporter.desktop import FileWriteDescriptor, Map, create_local_key, decrypt_local, file, generate_local_key, to_file_part, AUTH_KEY_SIZE

def ensure_input(
    tdata: str | PathLike[str],
    passcode: str | bytes
) -> tuple[Path, bytes]:
    if isinstance(tdata, str):
        tdata = Path(tdata)
    if isinstance(passcode, str):
        passcode = passcode.encode()
    return tdata, passcode

class Desktop:
    APP_VERSION = 3004000
    TDF_MAGIC = b'TDF$'
    MT_PROTO_AUTHORIZATION = 75
    WIDE_IDS_TAG = -1
    KEY_FILE_SUFFIX = 'data'

    @classmethod
    def desktop(cls: type['teleporter.Teleporter'],
        tdata: str | PathLike[str],
        passcode: str | bytes = b''
    ) -> list['teleporter.Teleporter']:
        tgcrypto()
        tdata, passcode = ensure_input(tdata, passcode)

        b = file(tdata / f'key_{cls.KEY_FILE_SUFFIX}')
        passcode_key = create_local_key(b.read(Int.read(b)), passcode)

        local_key = decrypt_local(b.read(Int.read(b)), passcode_key).read(AUTH_KEY_SIZE)
        info = decrypt_local(b.read(Int.read(b)), local_key)

        accounts = []
        for i in range(Int.read(info)):
            index = Int.read(info)
            if index >= 0:
                b = file(tdata / to_file_part(cls.KEY_FILE_SUFFIX, i + 1))
                b = decrypt_local(b.read(Int.read(b)), local_key)

                assert Int.read(b) == cls.MT_PROTO_AUTHORIZATION
                b.seek(4, 1) # size

                user_id = Int.read(b, signed=True)
                dc_id = Int.read(b, signed=True)

                if ((user_id << 32) | dc_id) == cls.WIDE_IDS_TAG:
                    user_id = Long.read(b)
                    dc_id = Int.read(b, signed=True)

                auth_keys = [
                    (Int.read(b, signed=True), b.read(AUTH_KEY_SIZE))
                    for _ in range(Int.read(b, signed=True))
                ]

                auth_keys_to_destroy = [
                    (Int.read(b, signed=True), b.read(AUTH_KEY_SIZE))
                    for _ in range(Int.read(b, signed=True))
                ]

                accounts.append(cls(dc_id, next(auth_key for auth_key_dc_id, auth_key in auth_keys if auth_key_dc_id == dc_id), user_id))
        return accounts

    @classmethod
    def to_desktop(cls,
        teleporters: list['teleporter.Teleporter'],
        tdata: str | PathLike[str],
        passcode: str | bytes = b'',
        map: bytes = Map(),
        performance_mode: bool = True
    ):
        tgcrypto()
        tdata, passcode = ensure_input(tdata, passcode)

        local_key, passcode_key_salt, passcode_key, passcode_key_encrypted = generate_local_key(performance_mode, passcode)
        map_ = FileWriteDescriptor()
        map_.write(b'')
        map_.write(b'')
        map_.encrypted(map, local_key)

        key_b = BytesIO()
        key_b.write(Int(len(teleporters))) # account count

        for i, teleporter in enumerate(teleporters):
            key_b.write(Int(i)) # account index
            path = tdata / to_file_part(cls.KEY_FILE_SUFFIX, i + 1)
            path.mkdir(parents=True, exist_ok=True)
            map_.eof(path / 'map')

            b = (
                Long(cls.WIDE_IDS_TAG, signed=True)+
                Long(teleporter.user_id, signed=True)+
                Int(teleporter.dc_id, signed=True)+
                Int(1, signed=True)+ # auth key count
                Int(teleporter.dc_id, signed=True)+
                teleporter.auth_key+
                Int(0, signed=True) # auth key to destroy count
            )

            mt_proto = FileWriteDescriptor()
            mt_proto.encrypted(
                Int(cls.MT_PROTO_AUTHORIZATION, signed=True)+
                Int(len(b)) + b
            , local_key)
            mt_proto.eof(path)

        key = FileWriteDescriptor()
        key.write(passcode_key_salt)
        key.write(passcode_key_encrypted)
        key_b.write(Int(0)) # active account index
        key.encrypted(key_b.getvalue(), local_key)
        key.eof(tdata / f'key_{cls.KEY_FILE_SUFFIX}')
