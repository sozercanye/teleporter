from hashlib import sha1

def get_auth_key_id(auth_key: bytes) -> int:
    if not auth_key:
        return 0
    return int.from_bytes(sha1(auth_key).digest()[12:12 + 8], 'little', signed=True)

class Auth:
    __slots__ = (
        'auth_key_perm', 'auth_key_perm_id', 'auth_key_temp', 'auth_key_temp_id',
        'auth_key_media_temp', 'auth_key_media_temp_id', 'authorized'
    )

    def __init__(self,
        auth_key_perm: bytes = b''
    ):
        self.auth_key_perm = auth_key_perm
        self.auth_key_perm_id = get_auth_key_id(self.auth_key_perm)
        self.auth_key_temp = b''
        self.auth_key_temp_id = get_auth_key_id(self.auth_key_temp)
        self.auth_key_media_temp = b''
        self.auth_key_media_temp_id = get_auth_key_id(self.auth_key_media_temp)
        self.authorized = 1

    def __str__(self) -> str:
        return self.auth_key_perm.hex()
