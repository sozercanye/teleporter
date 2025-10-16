from teleporter.session import Datacenter, Headers

class Session:
    __slots__ = ('headers', 'datacenters')

    def __init__(self,
        headers: Headers,
        datacenters: list[Datacenter]
    ):
        self.headers = headers
        self.datacenters = {datacenter.dc_id: datacenter for datacenter in datacenters}
