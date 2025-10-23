from hashlib import sha512, pbkdf2_hmac

from teleporter import desktop

def create_local_key(
    salt: bytes,
    passcode: bytes
) -> bytes:
    return pbkdf2_hmac('sha512', sha512(salt + passcode + salt).digest(), salt, 1 if not passcode else 100_000, desktop.AUTH_KEY_SIZE)
