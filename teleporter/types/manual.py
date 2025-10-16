import teleporter
from teleporter.session import Session, Auth, Headers, Datacenter

class Manual:
    @classmethod
    def manual(cls: type['teleporter.Teleporter'],
        dc_id: int, auth_key: bytes | str, id: int,
        is_test: bool = False,
        version: int = 5,
        current_dc_version: int = 13,
        last_dc_init_version: int = 48502,
        last_dc_media_init_version: int = 48502
    ) -> 'teleporter.Teleporter':
        return cls(session=Session(
            headers=Headers(dc_id, is_test, version),
            datacenters=[Datacenter(
                dc_id, Auth(auth_key if not isinstance(auth_key, str) else bytes.fromhex(auth_key)),
                current_dc_version, last_dc_init_version, last_dc_media_init_version
            )]
        ), id=id)

    def to_manual(self: 'teleporter.Teleporter') -> tuple[int, bytes, int]:
        return self.session.headers.dc_id, self.session.datacenters[self.session.headers.dc_id].auth.auth_key_perm, self.id
