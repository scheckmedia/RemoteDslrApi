import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


config = {
    'description': 'control your DSLR Camera remote over HTTP',
    'long_description' : read('README.md'),
    'author': 'Tobias Scheck',
    'url': 'http://www.scheck-media.de',
    'download_url': 'Where to download it.',
    'author_email': 'tobias@scheck-media.de',
    'version': '0.1',
    'install_requires': ['nose', 'gphoto2', 'flask'],
    'packages': ['RemoteDslrApi'],
    'scripts': [],
    'name': 'RemoteDslrApi'
}

setup(**config)
