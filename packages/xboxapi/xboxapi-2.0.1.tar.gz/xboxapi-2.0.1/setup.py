import codecs
import os

from setuptools import setup

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
README_FILE = os.path.join(PROJECT_ROOT, 'README.md')
VERSION_FILE = os.path.join(PROJECT_ROOT, 'xboxapi', 'VERSION')


def read(path):
    with codecs.open(path, 'r') as fil:
        return fil.read()


LONG_DESCRIPTION = read(README_FILE)
VERSION = read(VERSION_FILE).strip()


setup(
    name='xboxapi',
    version=VERSION,
    url='https://github.com/mKeRix/xboxapi-python',
    download_url=f'https://github.com/mKeRix/xboxapi-python/tarball/{VERSION}',
    license='MIT License',
    author='xapi.us',
    install_requires=['requests'],
    description='XBOX One API',
    long_description=LONG_DESCRIPTION,
    packages=['xboxapi'],
    package_data={'': ['README.md', 'LICENSE']},
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment',
    ],
)
