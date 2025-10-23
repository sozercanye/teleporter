from teleporter.core import IPS
from teleporter.android import Auth

class Datacenter:
    __slots__ = ('dc_id', 'is_cdn', 'auth', 'salt', 'current_version', 'last_init_version', 'last_init_media_version', 'ips')

    def __init__(self,
        dc_id: int,
        auth: Auth = None,
        current_version: int = 13,
        last_init_version: int = 48502,
        last_init_media_version: int = 48502
    ):
        self.dc_id = dc_id
        self.is_cdn = False
        self.auth = auth
        self.salt = []
        self.current_version = current_version
        self.last_init_version = last_init_version
        self.last_init_media_version = last_init_media_version

        self.ips = IPS[dc_id]
