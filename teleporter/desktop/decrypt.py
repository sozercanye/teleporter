from io import BytesIO
from hashlib import sha1

from .prepare_aes_old_mtp import prepare_aes_old_mtp

def decrypt(
    encrypted: bytes,
    auth_key: bytes
) -> BytesIO:
    from tgcrypto import ige256_decrypt

    encrypted_size = len(encrypted)
    if (encrypted_size <= 16) or (encrypted_size & 0x0F):
        raise ValueError(f'Bad encrypted part size: {encrypted_size}.')

    full_len = encrypted_size - 16
    encrypted_key = encrypted[:16]
    encrypted_data = encrypted[16:]

    aes_key, aes_iv = prepare_aes_old_mtp(auth_key, encrypted_key, send=False)
    decrypted = ige256_decrypt(encrypted_data, aes_key, aes_iv)

    check_hash = sha1(decrypted).digest()[:16]
    if check_hash != encrypted_key:
        raise ValueError('Bad decrypt key, data not decrypted — incorrect password?')

    data_len = int.from_bytes(decrypted[:4], 'little')
    if (data_len > len(decrypted)) or (data_len <= full_len - 16) or (data_len < 4):
        raise ValueError(f'Bad decrypted part size: {encrypted_size}, full_len: {full_len}, decrypted size: {len(decrypted)}.')

    buffer = BytesIO(decrypted[:data_len])
    buffer.seek(4)
    return buffer
