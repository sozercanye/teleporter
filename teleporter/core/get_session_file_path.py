from __future__ import annotations
from os import PathLike
from pathlib import Path

def get_session_file_path(
    session: str | PathLike[str],
    suffix: str = 'session'
) -> Path:
    if not isinstance(session, Path):
        session = Path(session)
    return session.with_suffix(f'.{suffix}')
