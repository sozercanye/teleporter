from __future__ import annotations
from typing import Awaitable
from pathlib import Path
from hashlib import md5

from .utils import create_local_key, decrypt, file, read

class Desktop:
    max_accounts = 3
    """The maximum amount of accounts a client can have"""

    default_key_file_path = 'data'
    """See `TDesktop.key_file`"""

    performance_mode = True
    """
    When enabled, `write()` will be 5000x faster.
    - What it does is using a constant `local_key` rather than generating it everytime when saving tdata.
    - The average time for generating `local_key` is about `250` to `350` ms, depend on your CPU.
    - When in performance mode, the average time to generate `local_key` is `0.0628` ms. Which is 5000x faster
    - Of course this comes with a catch, your `tdata files` will always use a same constant `local_key`. Basicly no protection at all, but who cares?

    ### Notes:
        Note: Performance mode will be disabled if `passcode` is set.
    """

    wide_ids_tag: int = 2**32 - 1

    @classmethod
    async def _read(cls,
        tdata: str | Path,
        passcode: str | bytes = b'',
        key_file_path: str | Path = default_key_file_path
    ) -> list[tuple[int, bytes, int]]:
        if isinstance(passcode, str):
            passcode = passcode.encode('ascii')
        if isinstance(key_file_path, Path):
            key_file_path = str(key_file_path)

        accounts = []

        version, b = await file('key_' + key_file_path, tdata)
        salt = read(b)
        key_encrypted = read(b)
        info_encrypted = read(b)

        passcode_key = create_local_key(salt, passcode)
        key_inner_data = decrypt(key_encrypted, passcode_key)
        local_key = key_inner_data.read(256)

        info = decrypt(info_encrypted, local_key)
        count = int.from_bytes(info.read(4))

        for _ in range(count):
            i = int.from_bytes(info.read(4))
            if (i >= 0) and (i < cls.max_accounts):
                md5_hash = md5(key_file_path.encode()).digest()
                data_name_key = int.from_bytes(md5_hash, 'little')

                account_key_file_path = ''
                for i in range(0, 0x10):
                    v = data_name_key & 0xF
                    if v < 0x0A:
                        account_key_file_path += chr(ord('0') + v)
                    else:
                        account_key_file_path += chr(ord('A') + (v - 0x0A))
                    data_name_key >>= 4

                _, b = await file(account_key_file_path, tdata)
                b = decrypt(read(b), local_key)
                b.seek(b.tell())

                b.seek(4, 1) # block_id = int.from_bytes(b.read(4))
                b.seek(4, 1)

                id = int.from_bytes(b.read(4))
                dc_id = int.from_bytes(b.read(4))

                if (id or dc_id) == cls.wide_ids_tag:
                    id = int.from_bytes(b.read(8))
                    dc_id = int.from_bytes(b.read(4))

                auth_key_count = int.from_bytes(b.read(4))
                auth_keys = [
                    (int.from_bytes(b.read(4)), b.read(256))
                    for _ in range(auth_key_count)
                ]
                auth_key = next(auth_key for auth_key_dc_id, auth_key in auth_keys if auth_key_dc_id == dc_id)

                accounts.append((dc_id, auth_key, id))

        return accounts

    def __new__(cls,
        tdata: str | Path,
        passcode: str | bytes = b'',
        key_file_path: str | Path = default_key_file_path
    ) -> Awaitable[list[tuple[int, bytes, int]]]:
        return cls._read(tdata, passcode, key_file_path)
