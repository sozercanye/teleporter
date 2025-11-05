## teleporter

#### Setup

```bash
pip install --upgrade teleporter
```

If you want to import from/export to Android X or Desktop, also required:

```bash
pip install TgCrypto==1.2.5
```

#### Create an instance

```python
from teleporter import Teleporter

# Import from raw
teleporter = Teleporter(dc_id=1, auth_key='a916b5302b76209b6920bf6d9bd0e29a5e7b3aa2d2d61ebe69f31d246ffcd7336fd916f1dae14ab54c0b6d1b4e4864bf7ae11aa64087227ca3a891586832a40ef5bd51be05fb920da14a2377b85184d6dfae9a7c9526173e04df5ecafe32670a8a1c4771546e4422e4510f07e0eda050349b60f53426a8c02857943b954135a49d1ac37ed9e2e036f227db152b986b8ae51fce9fe6e23a036f7e4e383b72063455301f01fa869a0b10e587d6a00ec30c6defff68984792d940de7d83e63554d94cdb2404b1a80591ce6fbccfefd4de7079045e305f8839795fac572760f87fae5c9707c46a18b15982f4ff29541e073b9e6ea15ff4cfe64e0c8a536ced5d141c', user_id=0)

# Import from Android
# Located in /data/data/org.telegram.messenger/files
# and /data/data/org.telegram.messenger/shared_prefs
teleporter = Teleporter.android('tgnet.dat', 'userconfing.xml')

# Import from Android X
# Located in /data/data/org.thunderdog.challegram/files/tdlib
teleporter = Teleporter.android_x('td.binlog')

# Import from Desktop tdata directory
teleporters = Teleporter.desktop('tdata')

# Import from web.telegram.org local storage
teleporter = Teleporter.web({"dcId":1,"dc1_auth_key":'a916b5302b76209b6920bf6d9bd0e29a5e7b3aa2d2d61ebe69f31d246ffcd7336fd916f1dae14ab54c0b6d1b4e4864bf7ae11aa64087227ca3a891586832a40ef5bd51be05fb920da14a2377b85184d6dfae9a7c9526173e04df5ecafe32670a8a1c4771546e4422e4510f07e0eda050349b60f53426a8c02857943b954135a49d1ac37ed9e2e036f227db152b986b8ae51fce9fe6e23a036f7e4e383b72063455301f01fa869a0b10e587d6a00ec30c6defff68984792d940de7d83e63554d94cdb2404b1a80591ce6fbccfefd4de7079045e305f8839795fac572760f87fae5c9707c46a18b15982f4ff29541e073b9e6ea15ff4cfe64e0c8a536ced5d141c','userId':0})

# Import from Telethon session
teleporter = Teleporter.telethon('telethon.session')

# Import from Pyrogram session
teleporter = Teleporter.pyrogram('pyrogram.session')
```

#### Use an instance

```python
# Access raw
teleporter.dc_id, teleporter.auth_key, teleporter.user_id

# Export to use on Android
teleporter.to_android('tgnet.dat', 'userconfing.xml')

# Export to use on Desktop
Teleporter.to_desktop([teleporter], 'tdata')

# Export in-memory to use on Desktop
zip_bytes = Teleporter.to_desktop([teleporter])
with open('tdata.zip', 'wb') as f:
    f.write(zip_bytes)

# Export to put into web.telegram.org local storage
account = teleporter.to_web()
print(account)

# Export to use in Telethon
teleporter.to_telethon('telethon.session')

# Export to use in Pyrogram
teleporter.to_pyrogram('pyrogram.session')
```

### Credits
#### to [batreller](https://github.com/batreller) for [AndroidTelePorter](https://github.com/batreller/AndroidTelePorter)
#### to [lplpqq](https://github.com/lplpqq) for [tdbinlog_reader](https://github.com/lplpqq/tdbinlog_reader)
#### to [thedemons](https://github.com/thedemons) for [opentele](https://github.com/thedemons/opentele)
#### to [delivrance](https://github.com/delivrance) for [tgcrypto](https://github.com/pyrogram/tgcrypto)
