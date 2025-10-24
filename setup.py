from pathlib import Path
import setuptools

from teleporter import __version__

directory = Path(__file__).parent
setuptools.setup(
    name='teleporter',
    version=__version__,
    author='sozercanye',
    description='tool with almost zero dependencies that allows you to switch Telegram session from/to Android, Android X, Desktop, Web, Telethon or Pyrogram client',
    long_description_content_type='text/markdown',
    long_description='\n' + open(directory / 'README.md').read(),
    url='https://github.com/sozercanye/teleporter',
    packages=setuptools.find_packages(),
    install_requires=open(directory / 'requirements.txt').read().splitlines(),
    python_requires='>=3.9'
)
