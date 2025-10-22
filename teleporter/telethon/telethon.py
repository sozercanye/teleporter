from __future__ import annotations
from pathlib import Path
import sqlite3

import teleporter
from teleporter.session import get_session_file_path

class Telethon:
    def to_telethon(self: 'teleporter.Teleporter',
        session: str | Path
    ):
        with sqlite3.connect(get_session_file_path(session)) as conn:
            conn.execute('''create table version (
              version integer primary key
            );''')
            conn.execute('insert into version values (?);', (7,))

            conn.execute('''create table update_state (
              id   integer primary key,
              pts  integer,
              qts  integer,
              date integer,
              seq  integer
            );''')

            conn.execute('''create table sessions (
              dc_id          integer primary key,
              server_address text,
              port           integer,
              auth_key       blob,
              takeout_id     integer
            );''')
            conn.execute('insert into sessions (dc_id, auth_key) values (?, ?);', (self.dc_id, self.auth_key))

            conn.execute('''create table sent_files (
              md5_digest blob,
              file_size  integer,
              type       integer,
              id         integer,
              hash       integer,
              primary key (md5_digest, file_size, type)
            );''')

            conn.execute('''create table entities (
              id       integer primary key,
              hash     integer not null,
              username text,
              phone    integer,
              name     text,
              date     integer
            );''')
            conn.execute('insert into entities (id, hash) values (?, ?)', (0, self.user_id))
