from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'forechotest',
    version = '0.0.1',
    keywords = ['simple', 'test'],
    description = 'just a simple test',
    license = 'MIT License',

    author = 'zwy',
    author_email = '2181778692@qq.com',

    packages = find_packages(),
    platforms = 'any',
)