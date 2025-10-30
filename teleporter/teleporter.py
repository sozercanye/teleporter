from __future__ import annotations

from .android import Android
from .android_x import AndroidX
from .desktop import Desktop, AUTH_KEY_SIZE
from .pyrogram import Pyrogram
from .telethon import Telethon
from .web import Web

class Teleporter(Android, AndroidX, Desktop, Pyrogram, Telethon, Web):
    __slots__ = ('dc_id', 'auth_key', 'user_id')

    def __init__(self,
        dc_id: int,
        auth_key: bytes | str | int,
        user_id: int = 0
    ):
        self.dc_id = dc_id
        self.auth_key = bytes.fromhex(auth_key) if isinstance(auth_key, str) else (auth_key.to_bytes(AUTH_KEY_SIZE) if isinstance(auth_key, int) else auth_key)
        assert len(self.auth_key) == AUTH_KEY_SIZE
        self.user_id = user_id
