from typing import Literal

class IP:
    __slots__ = ('type', 'address', 'port', 'flags', 'secret')

    def __init__(self,
        type: Literal['Ipv4', 'Ipv6', 'Ipv4Download', 'Ipv6Download'],
        address: str,
        port: int = 443,
        flags: int = 0,
        secret: bytes = b''
    ):
        self.type = type
        self.address = address
        self.port = port
        self.flags = flags
        self.secret = secret

    def __str__(self):
        return f'{self.address}:{self.port}'

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
