from io import BytesIO

def read(b: BytesIO) -> bytes:
    size = int.from_bytes(b.read(4))
    return b.read(size)
