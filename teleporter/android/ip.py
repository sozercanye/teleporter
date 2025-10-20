from typing import Literal

class IP:
    __slots__ = ('type', 'address', 'port', 'flags', 'secret')

    def __init__(self,
        type: Literal['Ipv4', 'Ipv6', 'Ipv4Download', 'Ipv6Download'],
        address: str,
        port: int = 443,
        flags: int = 0,
        secret: str = ''
    ):
        self.type = type
        self.address = address
        self.port = port
        self.flags = flags
        self.secret = secret

    def __str__(self):
        return f'{self.address}:{self.port}'
