from __future__ import annotations
from pathlib import Path

try: import tgcrypto
except ImportError: tgcrypto = None

import teleporter
from teleporter.core import Int, Long
from teleporter.desktop import FileWriteDescriptor, Map, create_local_key, decrypt_local, file, generate_local_key, to_file_part

def ensure_input(tdata: str | Path, passcode: str | bytes) -> tuple[Path, bytes]:
    if isinstance(tdata, str):
        tdata = Path(tdata)
    if isinstance(passcode, str):
        passcode = passcode.encode('ascii')
    return tdata, passcode

class Desktop:
    APP_VERSION = 3004000
    TDF_MAGIC = b'TDF$'
    MT_PROTO_AUTHORIZATION = 75
    WIDE_IDS_TAG = -1
    KEY_FILE_SUFFIX = 'data'

    @staticmethod
    def _tgcrypto():
        if not tgcrypto:
            raise ImportError('TgCrypto library is required for desktop import/export. Please install it via "pip install TgCrypto==1.2.5".')

    @classmethod
    def desktop(cls: type['teleporter.Teleporter'],
        tdata: str | Path,
        passcode: str | bytes = b''
    ) -> list['teleporter.Teleporter']:
        cls._tgcrypto()
        tdata, passcode = ensure_input(tdata, passcode)

        b = file(tdata / f'key_{cls.KEY_FILE_SUFFIX}')
        passcode_key = create_local_key(b.read(Int.read(b)), passcode)

        local_key = decrypt_local(b.read(Int.read(b)), passcode_key).read(256)
        info = decrypt_local(b.read(Int.read(b)), local_key)

        accounts = []
        for _ in range(Int.read(info)):
            i = Int.read(info)
            if i >= 0:
                b = file(tdata / to_file_part(cls.KEY_FILE_SUFFIX))
                b = decrypt_local(b.read(Int.read(b)), local_key)

                assert Int.read(b) == cls.MT_PROTO_AUTHORIZATION
                b.seek(4, 1) # size

                user_id = Int.read(b, signed=True)
                dc_id = Int.read(b, signed=True)

                if ((user_id << 32) | dc_id) == cls.WIDE_IDS_TAG:
                    user_id = Long.read(b)
                    dc_id = Int.read(b, signed=True)

                auth_keys = [
                    (Int.read(b, signed=True), b.read(256))
                    for _ in range(Int.read(b, signed=True))
                ]
                accounts.append(cls(dc_id, next(auth_key for auth_key_dc_id, auth_key in auth_keys if auth_key_dc_id == dc_id), user_id))
        return accounts

    def to_desktop(self: 'teleporter.Teleporter',
        tdata: str | Path,
        passcode: str | bytes = b'',
        map: bytes = Map(),
        performance_mode: bool = True
    ):
        self._tgcrypto()
        tdata, passcode = ensure_input(tdata, passcode)

        path = tdata / to_file_part(self.KEY_FILE_SUFFIX)
        path.mkdir(parents=True, exist_ok=True)

        local_key, passcode_key_salt, passcode_key, passcode_key_encrypted = generate_local_key(performance_mode, passcode)

        map_ = FileWriteDescriptor()
        map_.write(b'')
        map_.write(b'')
        map_.encrypted(map, local_key)
        map_.eof(path / 'map')

        b = (
            Long(self.WIDE_IDS_TAG, signed=True)+
            Long(self.user_id, signed=True)+
            Int(self.dc_id, signed=True)+
            Int(1, signed=True)+ # auth key count
            Int(self.dc_id, signed=True)+
            self.auth_key+
            Int(0, signed=True) # auth key to destroy count
        )

        mt_proto = FileWriteDescriptor()
        mt_proto.encrypted(
            Int(self.MT_PROTO_AUTHORIZATION, signed=True)+
            Int(len(b)) + b
        , local_key)
        mt_proto.eof(path)

        key = FileWriteDescriptor()
        key.write(passcode_key_salt)
        key.write(passcode_key_encrypted)

        # account count, account index, active account index
        key.encrypted(Int(1) + Int(0) + Int(0), local_key)
        key.eof(tdata / f'key_{self.KEY_FILE_SUFFIX}')
