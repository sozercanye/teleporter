from __future__ import annotations

from .android import Android
from .desktop import Desktop
from .session import Session
from .web import Web

class Teleporter(Android, Desktop, Session, Web):
    __slots__ = ('dc_id', 'auth_key', 'id', 'constructor_id')

    def __init__(self,
        dc_id: int,
        auth_key: bytes | str,
        id: int = 0,
        constructor_id: int = 34280482
    ):
        self.dc_id = dc_id
        self.auth_key = bytes.fromhex(auth_key) if isinstance(auth_key, str) else auth_key
        self.id = id

        self.constructor_id = constructor_id
