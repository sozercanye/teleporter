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
teleporter = Teleporter(dc_id=1, auth_key='a916b5302b76209b6920bf6d9bd0e29a5e7b3aa2d2d61ebe69f31d246ffcd7336fd916f1dae14ab54c0b6d1b4e4864bf7ae11aa64087227ca3a891586832a40ef5bd51be05fb920da14a2377b85184d6dfae9a7c9526173e04df5ecafe32670a8a1c4771546e4422e4510f07e0eda050349b60f53426a8c02857943b954135a49d1ac37ed9e2e036f227db152b986b8ae51fce9fe6e23a036f7e4e383b72063455301f01fa869a0b10e587d6a00ec30c6defff68984792d940de7d83e63554d94cdb2404b1a80591ce6fbccfefd4de7079045e305f8839795fac572760f87fae5c9707c46a18b15982f4ff29541e073b9e6ea15ff4cfe64e0c8a536ced5d141c', user_id=0)

# Load from Android session files
# Located in /data/data/org.telegram.messenger/files
# and /data/data/org.telegram.messenger/shared_prefs
teleporter = Teleporter.android('tgnet.dat', 'userconfig.xml')

# Load from Desktop tdata directory
teleporters = Teleporter.desktop('tdata')

# Load from web.telegram.org local storage
teleporter = Teleporter.web({"dcId":1,"dc1_auth_key":'a916b5302b76209b6920bf6d9bd0e29a5e7b3aa2d2d61ebe69f31d246ffcd7336fd916f1dae14ab54c0b6d1b4e4864bf7ae11aa64087227ca3a891586832a40ef5bd51be05fb920da14a2377b85184d6dfae9a7c9526173e04df5ecafe32670a8a1c4771546e4422e4510f07e0eda050349b60f53426a8c02857943b954135a49d1ac37ed9e2e036f227db152b986b8ae51fce9fe6e23a036f7e4e383b72063455301f01fa869a0b10e587d6a00ec30c6defff68984792d940de7d83e63554d94cdb2404b1a80591ce6fbccfefd4de7079045e305f8839795fac572760f87fae5c9707c46a18b15982f4ff29541e073b9e6ea15ff4cfe64e0c8a536ced5d141c','userId':0})

# Load from an existing session file
teleporter = Teleporter.session('pyrogram.session')
teleporter = Teleporter.session('telethon.session')
```

#### Use a Teleporter instance

```python
# Access session parameters
teleporter.dc_id
teleporter.auth_key
teleporter.user_id

# Serialize to Android format
teleporter.to_android('tgnet.dat', 'userconfig.xml')

# Serialize to web.telegram.org local storage format
value = teleporter.to_web()
```