from __future__ import annotations
from pathlib import Path
from io import BytesIO
import hashlib

def file(
    key_file_path: str | Path,
    tdata: str | Path
) -> tuple[int, BytesIO]:
    key_file_path = Path(key_file_path)
    tdata = Path(tdata)

    for chr_suffix in ('s', '1', '0'):
        file_path = tdata / f'{key_file_path}{chr_suffix}'
        if not file_path.exists():
            continue

        with open(file_path, 'rb') as f:
            magic = f.read(4)
            if magic != b'TDF$':
                raise ValueError(f'Invalid magic {magic} in file {file_path}.')
            version = int.from_bytes(f.read(4), 'little')

            bytesdata = f.read()
        data_size = len(bytesdata) - 16

        check_md5 = bytesdata[:data_size]
        check_md5 += data_size.to_bytes(4, 'little')
        check_md5 += version.to_bytes(4, 'little')
        check_md5 += magic
        check_md5 = hashlib.md5(check_md5).digest()

        md5 = bytesdata[data_size:]
        if check_md5 != md5:
            raise ValueError(f'Invalid checksum in file {file_path}.')
        return version, BytesIO(bytesdata[:data_size])
    raise FileNotFoundError(f'Could not open {key_file_path} with any suffix.')
