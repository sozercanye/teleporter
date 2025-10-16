from teleporter.session import Session
from teleporter.types import Types

class Teleporter(Types):
    __slots__ = ('session', 'constructor_id', 'flags', 'flags2', 'id')

    def __init__(self,
        session: Session,
        constructor_id: int = 34280482,
        flags: int = 0,
        flags2: int = 0,
        id: int = 0
    ):
        self.session = session
        self.constructor_id = constructor_id
        self.flags = flags
        self.flags2 = flags2
        self.id = id
