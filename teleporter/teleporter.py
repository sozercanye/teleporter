from __future__ import annotations

from teleporter.android import Android
from teleporter.desktop import Desktop_

class Teleporter(Android, Desktop_):
    __slots__ = ('dc_id', 'auth_key', 'id', 'constructor_id', 'flags', 'flags2')

    def __init__(self,
        dc_id: int,
        auth_key: bytes | str,
        id: int = 0,
        constructor_id: int = 34280482,
        flags: int = 0,
        flags2: int = 0
    ):
        self.dc_id = dc_id
        self.auth_key = bytes.fromhex(auth_key) if isinstance(auth_key, str) else auth_key
        self.id = id

        self.constructor_id = constructor_id
        self.flags = flags
        self.flags2 = flags2
