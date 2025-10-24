from __future__ import annotations
from os import PathLike
import sqlite3

import teleporter
from teleporter.core import get_session_file_path

class Pyrogram:
    @classmethod
    def pyrogram(cls: type['teleporter.Teleporter'],
        session: str | PathLike[str]
    ) -> 'teleporter.Teleporter':
        with sqlite3.connect(get_session_file_path(session)) as conn:
            cursor = conn.execute(f'select dc_id, auth_key, user_id from sessions limit 1;')
            return cls(*cursor.fetchone())

    def to_pyrogram(self: 'teleporter.Teleporter',
        session: str | PathLike[str]
    ):
        with sqlite3.connect(get_session_file_path(session)) as conn:
            conn.execute('''create table version (
              number integer primary key
            );''')
            conn.execute('insert into version values (?);', (3,))

            conn.execute('''create table sessions (
              dc_id     integer primary key,
              api_id    integer,
              test_mode integer,
              auth_key  blob,
              date      integer not null,
              user_id   integer,
              is_bot    integer
            );''')
            conn.execute(
                'insert into sessions values (?, ?, ?, ?, ?, ?, ?);',
                (self.dc_id, 6, False, self.auth_key, 0, self.user_id, False)
            )

            conn.execute('''create table peers (
                id             integer primary key,
                access_hash    integer,
                type           integer not null,
                username       text,
                phone_number   text,
                last_update_on integer not null default (cast(strftime('%s', 'now') as integer))
            );''')

            conn.execute('create index idx_peers_id on peers (id);')
            conn.execute('create index idx_peers_phone_number on peers (phone_number);')
            conn.execute('create index idx_peers_username on peers (username);')
            conn.execute('''
              create trigger trg_peers_last_update_on after update on peers begin
                update peers set last_update_on = cast(strftime('%s', 'now') as integer)
                where id = NEW.id; end;
            ''')
