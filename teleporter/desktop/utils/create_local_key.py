from hashlib import sha512, pbkdf2_hmac

def create_local_key(
    salt: bytes,
    passcode: bytes = b''
) -> bytes:
    hash_key = sha512(salt)
    hash_key.update(passcode)
    hash_key.update(salt)

    iterations = 1 if not passcode else 100_000
    return pbkdf2_hmac('sha512', hash_key.digest(), salt, iterations, 256)
