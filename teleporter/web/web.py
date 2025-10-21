from __future__ import annotations
import json

import teleporter

class Web:
    @classmethod
    def web(cls: type['teleporter.Teleporter'],
        account: str | dict[str, str | int]
    ) -> 'teleporter.Teleporter':
        if not isinstance(account, dict):
            account = json.loads(account)

        dc_id = account['dcId']
        return cls(dc_id, account[f'dc{dc_id}_auth_key'], account['userId'])

    def to_web(self: 'teleporter.Teleporter'
    ) -> str:
        return json.dumps({
            'dcId': self.dc_id,
            f'dc{self.dc_id}_auth_key': self.auth_key.hex(),
            'userId': self.user_id
        }, separators=(',', ':'))
