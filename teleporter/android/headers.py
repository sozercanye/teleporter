import time

class Headers:
    __slots__ = (
        'dc_id', 'client_blocked', 'last_init_system_langcode', 'is_test', 'version', 'time_difference',
        'last_dc_update_time', 'push_session_id', 'registered_for_internal_push', 'last_server_time',
        'current_time', 'sessions_to_destroy'
    )

    def __init__(self,
        dc_id: int = None,
        is_test: bool = False,
        version: int = 5
    ):
        self.is_test = is_test
        self.client_blocked = False
        self.last_init_system_langcode = 'en-us'
        self.dc_id = dc_id
        self.version = version
        self.time_difference = 0
        self.last_dc_update_time = 0
        self.push_session_id = 0
        self.registered_for_internal_push = True
        self.last_server_time = 0
        self.current_time = int(time.time())
        self.sessions_to_destroy = []
