from io import BytesIO
from hashlib import sha1

from teleporter.core import Int
from teleporter.desktop import aes_decrypt_local

def decrypt_local(
    encrypted: bytes,
    local_key: bytes
) -> BytesIO:
    encrypted_size = len(encrypted)
    if (encrypted_size <= 16) or (encrypted_size & 15):
        raise ValueError(f'Bad encrypted part size: {encrypted_size}.')

    encrypted_key = encrypted[:16]
    decrypted = aes_decrypt_local(encrypted[16:], local_key, encrypted_key)
    check_hash = sha1(decrypted).digest()[:16]

    if check_hash != encrypted_key:
        raise ValueError('Bad decrypt key, data not decrypted — incorrect passcode?')

    full_len = encrypted_size - 16
    data_len = Int.read(decrypted[:Int.SIZE], 'little')

    if (data_len > len(decrypted)) or (data_len <= full_len - 16) or (data_len < 4):
        raise ValueError(f'Bad decrypted part size: {encrypted_size}, full_len: {full_len}, decrypted size: {len(decrypted)}.')
    return BytesIO(decrypted[Int.SIZE:data_len])
