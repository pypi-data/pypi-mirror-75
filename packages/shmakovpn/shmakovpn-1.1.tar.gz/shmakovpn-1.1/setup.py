import os
from setuptools import setup, find_packages
from shmakovpn.version import VERSION

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

with open('README.md') as f:
    long_description: str = f.read()

setup(
    name='shmakovpn',
    version=VERSION,
    packages=find_packages(),
    author='shmakovpn',
    author_email='shmakovpn@yandex.ru',
    url='https://github.com/shmakovpn/shmakovpn_tools',
    download_url='https://github.com/shmakovpn/shmakovpn_tools/archive/%s.zip' % (VERSION, ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
    },
    install_requires=[
    ],
    include_package_data=True,
    test_suite='shmakovpn.tests',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
