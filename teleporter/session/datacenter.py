from teleporter import session
from teleporter.session.ip import IP

IPS = {
    1: {
        'Ipv4': [
            IP('Ipv4', '149.154.175.52', 443),
            IP('Ipv4', '149.154.175.54', 443, flags=16)
        ],
        'Ipv6': [IP('Ipv6', '2001:0b28:f23d:f001:0000:0000:0000:000a', 443, flags=1)],
        'Ipv4Download': [],
        'Ipv6Download': []
    },
    2: {
        'Ipv4': [IP('Ipv4', '149.154.167.41', 443)],
        'Ipv6': [IP('Ipv6', '2001:067c:04e8:f002:0000:0000:0000:000a', 443, flags=1)],
        'Ipv4Download': [IP('Ipv4Download', '149.154.167.151', 443, flags=2)],
        'Ipv6Download': [IP('Ipv6Download', '2001:067c:04e8:f002:0000:0000:0000:000b', 443, flags=3)]
    },
    3: {
        'Ipv4': [IP('Ipv4', '149.154.175.100', 443)],
        'Ipv6': [IP('Ipv6', '2001:0b28:f23d:f003:0000:0000:0000:000a', 443, flags=1)],
        'Ipv4Download': [],
        'Ipv6Download': []
    },
    4: {
        'Ipv4': [IP('Ipv4', '149.154.167.92', 443)],
        'Ipv6': [IP('Ipv6', '2001:067c:04e8:f004:0000:0000:0000:000a', 443, flags=1)],
        'Ipv4Download': [IP('Ipv4Download', '149.154.165.96', 443, flags=2)],
        'Ipv6Download': [IP('Ipv6Download', '2001:067c:04e8:f004:0000:0000:0000:000b', 443, flags=3)]
    },
    5: {
        'Ipv4': [IP('Ipv4', '91.108.56.197', 443)],
        'Ipv6': [IP('Ipv6', '2001:0b28:f23f:f005:0000:0000:0000:000a', 443, flags=1)],
        'Ipv4Download': [],
        'Ipv6Download': []
    }
}

class Datacenter:
    __slots__ = ('dc_id', 'is_cdn', 'auth', 'salt', 'current_version', 'last_init_version', 'last_init_media_version', 'ips')

    def __init__(self,
        dc_id: int,
        auth: session.Auth = None,
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
        # self.ips = IPS.get(dc_id, {
            # 'Ipv4': [],
            # 'Ipv6': [],
            # 'Ipv4Download': [],
            # 'Ipv6Download': []
        # })
