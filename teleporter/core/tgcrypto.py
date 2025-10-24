try: import tgcrypto
except ImportError: tgcrypto = None

def tgcrypto():
    if not tgcrypto:
        raise ImportError('TgCrypto library is required for Android X and Desktop import/export. Please install it via "pip install TgCrypto==1.2.5".')
