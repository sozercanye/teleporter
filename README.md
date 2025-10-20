# teleporter [![pypi package](https://img.shields.io/pypi/v/teleporter.svg)](https://pypi.python.org/pypi/teleporter/)

Serializer and deserializer for Telegram Android sessions.

### Description

This tool can be used to serialize and deserialize sessions on Telegram Android. And remove pin code.

It can extract any information stored in files/tgnet.dat and all needed information from shared_prefs/userconfing.xml

It also can deserialize existing session into object and convert it into other session formats (currently supported tdata, telethon and tgnet)

And you can serialize session manually into mobile tgnet format, all you need is just auth key, datacenter id and user id, it is minimum information needed for almost any session format

### Installation

You can easily set up this package as it is available on pypi by running the following command
```bash
pip install teleporter
```

### Usage

#### Converting existing android session into other format
```python
from teleporter import Teleporter

# both tgnet.dat and userconfing.xml are stored in /data/data/org.telegram.messenger directory
# if you have more than 1 account you would need to use tgnet.dat from /files/account(account_number)/tgnet.dat
# and corresponding userconfig.xml file from /shared_prefs/userconfig(account_number).xml

teleporter = await Teleporter.android('tgnet.dat', 'userconfing.xml')
teleporter.dc_id, teleporter.auth_key, teleporter.id
```

#### Creating android session from dc id, auth key and user id
```python
teleporter = Teleporter(dc_id, auth_key, user_id)
await teleporter.to_android('result/tgnet.dat', 'result/userconfing.xml')
```

#### Creating android session from desktop session
```python
teleporters = await Teleporter.desktop('tdata')
for teleporter in teleporters:
    await teleporter.to_android(f'result/{teleporter.id}/tgnet.dat', f'result/{teleporter.id}/userconfing.xml')
```
