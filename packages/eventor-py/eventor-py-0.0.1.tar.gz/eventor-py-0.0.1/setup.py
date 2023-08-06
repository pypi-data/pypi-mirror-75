from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='eventor-py',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Eventorpy is a python library that makes it easier to use eventors apis.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests'],
    url='https://github.com/WIGRU/eventorpy',
    author='William Grunder',
    author_email='william.grunder@gmail.com'
)