from hashlib import sha1

def prepare_aes_old_mtp(
    auth_key: bytes,
    msg_key: bytes,
    send: bool
) -> tuple[bytes, bytes]:
    x = 0 if send else 8
    sha1_a = sha1(msg_key[:16] + auth_key[x: x + 32]).digest()

    sha1_b = sha1(
        auth_key[x + 32: x + 32 + 16]
        + msg_key[:16]
        + auth_key[x + 48: x + 48 + 16]
    ).digest()

    sha1_c = sha1(auth_key[x + 64: x + 64 + 32] + msg_key[:16]).digest()
    sha1_d = sha1(msg_key[:16] + auth_key[x + 96: x + 96 + 32]).digest()

    aes_key = sha1_a[:8] + sha1_b[8: 8 + 12] + sha1_c[4: 4 + 12]
    aes_iv = sha1_a[8: 8 + 12] + sha1_b[:8] + sha1_c[16: 16 + 4] + sha1_d[:8]

    return aes_key, aes_iv
