from pathlib import Path
import setuptools

from teleporter import __version__

directory = Path(__file__).parent
setuptools.setup(
    name='teleporter',
    version=__version__,
    author='sozercanye',
    description='Serializer and deserializer for Telegram Android and Desktop sessions.',
    long_description_content_type='text/markdown',
    long_description='\n' + open(directory / 'README.md').read(),
    url='https://github.com/sozercanye/teleporter',
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=open(directory / 'requirements.txt').read().splitlines(),
    python_requires='>=3.9'
)
