import hashlib

def create_local_key(
    salt: bytes,
    passcode: bytes = b''
) -> bytes:
    hash_key = hashlib.sha512(salt)
    hash_key.update(passcode)
    hash_key.update(salt)

    iterations = 1 if not passcode else 100_000
    return hashlib.pbkdf2_hmac('sha512', hash_key.digest(), salt, iterations, 256)
