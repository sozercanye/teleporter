from __future__ import annotations

from .android import Android
from .desktop import Desktop, AUTH_KEY_SIZE
from .pyrogram import Pyrogram
from .session import Session
from .telethon import Telethon
from .web import Web

class Teleporter(Android, Desktop, Pyrogram, Session, Telethon, Web):
    __slots__ = ('dc_id', 'auth_key', 'user_id', 'constructor_id')

    def __init__(self,
        dc_id: int,
        auth_key: bytes | str,
        user_id: int = 0,
        constructor_id: int = 34280482
    ):
        self.dc_id = dc_id
        self.auth_key = bytes.fromhex(auth_key) if isinstance(auth_key, str) else auth_key
        assert len(self.auth_key) == AUTH_KEY_SIZE
        self.user_id = user_id

        self.constructor_id = constructor_id
