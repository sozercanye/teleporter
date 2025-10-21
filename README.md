# teleporter [![pypi package](https://img.shields.io/pypi/v/teleporter.svg)](https://pypi.python.org/pypi/teleporter/)

Serializer and deserializer for Telegram Android and Desktop sessions.

### Description

**teleporter** allows you to serialize and deserialize Telegram session data from Android and Desktop clients.  
It can extract required data from `tgnet.dat`, `userconfig.xml`, or `tdata` folders, and convert sessions between supported formats (`tgnet`, `telethon`, and `pyrogram`).  
PIN code removal is supported only for Android sessions.

### Installation & Update

Install or update the package from PyPI:

```bash
pip install --upgrade teleporter
```

### Usage

#### Create a Teleporter instance

```python
from teleporter import Teleporter

# Create from raw session parameters
teleporter = Teleporter(dc_id, auth_key, user_id)

# Load from Android session files
# Located in /data/data/org.telegram.messenger/files
# and /data/data/org.telegram.messenger/shared_prefs
teleporter = Teleporter.android('tgnet.dat', 'userconfig.xml')

# Load from Desktop tdata directory
teleporters = Teleporter.desktop('tdata')

# Load from an existing session file
teleporter = Teleporter.session('pyrogram.session')
teleporter = Teleporter.session('telethon.session')
```

#### Use a Teleporter instance

```python
# Access session parameters
teleporter.dc_id
teleporter.auth_key
teleporter.id

# Serialize to Android format
teleporter.to_android('tgnet.dat', 'userconfig.xml')
```