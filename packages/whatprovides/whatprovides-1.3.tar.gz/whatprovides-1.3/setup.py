"""
whatprovides setup.py
"""

import os
from setuptools import setup, find_packages
from whatprovides.version import VERSION

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

with open('README.rst') as f:
    long_description: str = f.read()

setup(
    name='whatprovides',
    version=VERSION,
    packages=find_packages(),
    author='shmakovpn',
    author_email='shmakovpn@yandex.ru',
    url='https://github.com/shmakovpn/whatprovides',
    download_url='https://github.com/shmakovpn/whatprovides/archive/%s.zip' % (VERSION, ),
    long_description=long_description,
    long_description_content_type='text/x-rst',
    entry_points={
        'console_scripts': ['whatprovides=whatprovides:main'],
    },
    install_requires=[
        'chardet',
    ],
    include_package_data=True,
    test_suite='whatprovides.tests',
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
