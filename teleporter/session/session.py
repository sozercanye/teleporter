from __future__ import annotations
from pathlib import Path
import sqlite3

import teleporter
from teleporter.session import get_session_file_path

class Session:
    @classmethod
    def session(cls: type['teleporter.Teleporter'],
        session: str | Path
    ) -> 'teleporter.Teleporter':
        with sqlite3.connect(get_session_file_path(session)) as conn:
            info = conn.execute('pragma table_info(sessions);').fetchall()
            if any(column[1] == 'user_id' for column in info):
                cursor = conn.execute(f'select dc_id, auth_key, user_id from sessions limit 1;')
                dc_id, auth_key, user_id = cursor.fetchone()
            else:
                cursor = conn.execute(f'select dc_id, auth_key from sessions limit 1;')
                dc_id, auth_key = cursor.fetchone()

                cursor = conn.execute(f'select hash from entities where id = 0 limit 1;')
                user_id = result[0] if (result := cursor.fetchone()) else 0
        return cls(dc_id, auth_key, user_id)
