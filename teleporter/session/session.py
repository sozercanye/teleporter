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

        columns = 'dc_id, auth_key, user_id' if has_user_id else 'dc_id, auth_key'
        cursor = conn.execute(f'SELECT {columns} FROM sessions LIMIT 1;')

        return cls(*cursor.fetchone())
