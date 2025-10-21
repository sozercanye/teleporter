from __future__ import annotations
from pathlib import Path
import sqlite3

import teleporter

class Session:
    @classmethod
    def session(cls: type['teleporter.Teleporter'],
        session: str | Path
    ) -> 'teleporter.Teleporter':
        if not isinstance(session, Path):
            session = Path(session)
        conn = sqlite3.connect(session.with_suffix('.session'))

        info = conn.execute('PRAGMA table_info(sessions);').fetchall()
        has_user_id = any(col[1] == 'user_id' for col in info)

        if has_user_id:
            cursor = conn.execute(f'SELECT dc_id, auth_key, user_id FROM sessions LIMIT 1;')
            dc_id, auth_key, user_id = cursor.fetchone()
        else:
            cursor = conn.execute(f'SELECT dc_id, auth_key FROM sessions LIMIT 1;')
            dc_id, auth_key = cursor.fetchone()

            cursor = conn.execute(f'SELECT hash FROM entities WHERE id = 0 LIMIT 1;')
            user_id = result[0] if (result := cursor.fetchone()) else None

        return cls(dc_id, auth_key, user_id)
