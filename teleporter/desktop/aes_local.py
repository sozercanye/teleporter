from hashlib import sha1

X = 8

def prepare_aes_old_mt_proto(
    local_key: bytes,
    msg_key: bytes
) -> tuple[bytes, bytes]:
    sha1_a = sha1(msg_key[:16] + local_key[X: X + 32]).digest()

    sha1_b = sha1(
        local_key[X + 32: X + 32 + 16]
        + msg_key[:16]
        + local_key[X + 48: X + 48 + 16]
    ).digest()

    sha1_c = sha1(local_key[X + 64: X + 64 + 32] + msg_key[:16]).digest()
    sha1_d = sha1(msg_key[:16] + local_key[X + 96: X + 96 + 32]).digest()

    aes_key = sha1_a[:8] + sha1_b[8: 8 + 12] + sha1_c[4: 4 + 12]
    aes_iv = sha1_a[8: 8 + 12] + sha1_b[:8] + sha1_c[16: 16 + 4] + sha1_d[:8]
    return aes_key, aes_iv

def aes_encrypt_local(
    src: bytes,
    local_key: bytes,
    key128: bytes
) -> bytes:
    from tgcrypto import ige256_encrypt
    aes_key, aes_iv = prepare_aes_old_mt_proto(local_key, key128)
    return ige256_encrypt(src, aes_key, aes_iv)

def aes_decrypt_local(
    src: bytes,
    local_key: bytes,
    key128: bytes
) -> bytes:
    from tgcrypto import ige256_decrypt
    aes_key, aes_iv = prepare_aes_old_mt_proto(local_key, key128)
    return ige256_decrypt(src, aes_key, aes_iv)
