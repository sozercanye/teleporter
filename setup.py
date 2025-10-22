from pathlib import Path
import setuptools

from teleporter import __version__

directory = Path(__file__).parent

with open(directory / 'README.md') as f:
    long_description = '\n' + f.read()

with open(directory / 'requirements.txt') as f:
    install_requires = f.read().splitlines()

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
    install_requires=install_requires,
    python_requires='>=3.9'
)
