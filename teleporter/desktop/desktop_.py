from __future__ import annotations
from pathlib import Path

import teleporter
from teleporter.desktop import Desktop

class Desktop_:
    @classmethod
    async def desktop(cls: type['teleporter.Teleporter'],
        tdata: str | Path,
        passcode: str | bytes = b'',
        key_file_path: str | Path = Desktop.default_key_file_path
    ) -> list['teleporter.Teleporter']:
        return [
            cls(dc_id=dc_id, auth_key=auth_key, id=id)
            for dc_id, auth_key, id in
            await Desktop(tdata, passcode, key_file_path)
        ]
