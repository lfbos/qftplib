import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='qftplib',
    version='1.0',
    author='Luis Boscan',
    author_email='lboscannava@gmail.com',
    description=(
        'Simple library to connect and interact to FTP/SFTP servers'
    ),
    license='MIT',
    url='https://github.com/lfbos/qftplib',
    packages=['qftplib', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_reqs=[
        'paramiko==2.7.1'
    ]
)
