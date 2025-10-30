from hashlib import md5

from teleporter.core import Int

def to_file_part(key_file_suffix: str, i: int) -> str:
    if i > 1:
        key_file_suffix += f'#{i}'

    md5_hash = md5(key_file_suffix.encode()).digest()
    data_name_key = Int.read(md5_hash, 'little')

    account_key_file_part = ''
    for i in range(0, 16):
        v = data_name_key & 15
        if v < 10:
            account_key_file_part += chr(ord('0') + v)
        else:
            account_key_file_part += chr(ord('A') + (v - 10))
        data_name_key >>= 4
    return account_key_file_part
