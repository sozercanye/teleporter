from pathlib import Path
import setuptools

from teleporter import __version__

with open(Path(__file__).parent / 'README.md') as f:
    long_description = '\n' + f.read()

setuptools.setup(
    name='teleporter',
    version=__version__,
    author='sozercanye',
    description='Serializer and deserializer for Telegram Android and Desktop sessions.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/sozercanye/teleporter',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['aiofiles~=25.1.0'],
    python_requires='>=3.9'
)
