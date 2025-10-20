from teleporter import android
from teleporter.android.ip import IP

class Datacenter:
    IPS = {
        1: {
            'Ipv4': [
                IP('Ipv4', '149.154.175.52'),
                IP('Ipv4', '149.154.175.54', flags=16)
            ],
            'Ipv6': [IP('Ipv6', '2001:0b28:f23d:f001:0000:0000:0000:000a', flags=1)],
            'Ipv4Download': [],
            'Ipv6Download': []
        },
        2: {
            'Ipv4': [IP('Ipv4', '149.154.167.41')],
            'Ipv6': [IP('Ipv6', '2001:067c:04e8:f002:0000:0000:0000:000a', flags=1)],
            'Ipv4Download': [IP('Ipv4Download', '149.154.167.151', flags=2)],
            'Ipv6Download': [IP('Ipv6Download', '2001:067c:04e8:f002:0000:0000:0000:000b', flags=3)]
        },
        3: {
            'Ipv4': [IP('Ipv4', '149.154.175.100')],
            'Ipv6': [IP('Ipv6', '2001:0b28:f23d:f003:0000:0000:0000:000a', flags=1)],
            'Ipv4Download': [],
            'Ipv6Download': []
        },
        4: {
            'Ipv4': [IP('Ipv4', '149.154.167.92')],
            'Ipv6': [IP('Ipv6', '2001:067c:04e8:f004:0000:0000:0000:000a', flags=1)],
            'Ipv4Download': [IP('Ipv4Download', '149.154.165.96', flags=2)],
            'Ipv6Download': [IP('Ipv6Download', '2001:067c:04e8:f004:0000:0000:0000:000b', flags=3)]
        },
        5: {
            'Ipv4': [IP('Ipv4', '91.108.56.197')],
            'Ipv6': [IP('Ipv6', '2001:0b28:f23f:f005:0000:0000:0000:000a', flags=1)],
            'Ipv4Download': [],
            'Ipv6Download': []
        },
        203: {
            'Ipv4': [IP('Ipv4', '91.105.192.100')],
            'Ipv6': [IP('Ipv6', '2a0a:f280:0203:000a:5000:0000:0000:0100', flags=1)],
            'Ipv4Download': [],
            'Ipv6Download': []
        }
    }

    __slots__ = ('dc_id', 'is_cdn', 'auth', 'salt', 'current_version', 'last_init_version', 'last_init_media_version', 'ips')

    def __init__(self,
        dc_id: int,
        auth: android.Auth = None,
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

        self.ips = self.IPS[dc_id]
