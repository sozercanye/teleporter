"""
Desktop is based on opentele
https://github.com/thedemons/opentele/tree/main/src/td
"""

from .aes_local import aes_encrypt_local, aes_decrypt_local
from .create_local_key import create_local_key
from .decrypt_local import decrypt_local
from .file import file
from .file_write_descriptor import FileWriteDescriptor
from .generate_local_key import generate_local_key, AUTH_KEY_SIZE
from .map import Map
from .to_file_part import to_file_part
from .desktop import Desktop
