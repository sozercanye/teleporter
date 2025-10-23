from __future__ import annotations
from pathlib import Path
from io import BytesIO
import hashlib

from teleporter.core import Int
from teleporter import desktop

def file(key_file_path: str | Path) -> BytesIO:
    for chr_suffix in ('s', '1', '0'):
        file_path = Path(f'{key_file_path}{chr_suffix}')
        if not file_path.exists():
            continue

        with open(file_path, 'rb') as f:
            magic = f.read(4)
            if magic != desktop.Desktop.TDF_MAGIC:
                raise ValueError(f'Invalid magic {magic} in file {file_path}.')
            version = Int.read(f, 'little')
            data = f.read()
        data_size = len(data) - 16 # md5

        check_md5 = data[:data_size]
        check_md5 += Int(data_size, 'little')
        check_md5 += Int(version, 'little')
        check_md5 += magic
        check_md5 = hashlib.md5(check_md5).digest()

        md5 = data[data_size:]
        if check_md5 != md5:
            raise ValueError(f'Invalid checksum in file {file_path}.')
        return BytesIO(data[:data_size])
    raise FileNotFoundError(f'Could not open {key_file_path} with any suffix.')
