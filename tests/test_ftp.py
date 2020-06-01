import os
import tempfile
import time
import unittest

import pytest

from qftplib.client import FTPClient
from qftplib.exceptions import InvalidConnection


class FTPTest(unittest.TestCase):
    host = os.environ.get('FTP_HOST_TEST', 'localhost')
    user = os.environ.get('FTP_USER_TEST', 'testuser')
    password = os.environ.get('FTP_PASS_TEST', '123')
    dir = os.environ.get('FTP_DIR_TEST', '/pruebas_sftp')

    def setUp(self):
        print(self.host)
        print(self.dir)
        print(self.dir)

    def test_name(self):
        with FTPClient(self.host, self.user, self.password) as ftp:
            assert str(ftp) == f'<FTPClient({self.host}, {self.user}, xxxx, port = 21, protocol = ftp)>'

    def test_invalid_connection(self):
        with pytest.raises(InvalidConnection) as e_info:
            with FTPClient(self.host, self.user, '1111') as ftp:
                pass

    def test_listdir(self):
        with FTPClient(self.host, self.user, self.password) as ftp:
            directory_files = ftp.listdir(self.dir)

            assert len(directory_files) > 0

    def test_pwd_chdir(self):
        with FTPClient(self.host, self.user, self.password) as ftp:
            assert ftp.pwd() == '/'

            ftp.chdir(self.dir)

            assert ftp.pwd() == self.dir

    def test_rmdir_mkdir(self):
        with FTPClient(self.host, self.user, self.password) as ftp:
            ftp.chdir(self.dir)
            new_dir = str(int(time.time()))
            ftp.mkdir(new_dir)
            files = ftp.listdir(self.dir)

            assert f'{self.dir}/{new_dir}' in files

            ftp.rmdir(new_dir)

            files = ftp.listdir(self.dir)

            assert f'{self.dir}/{new_dir}' not in files

    def test_rename(self):
        with FTPClient(self.host, self.user, self.password) as ftp:
            ftp.chdir(self.dir)
            new_dir = str(int(time.time()))
            ftp.mkdir(new_dir)

            ftp.rename(new_dir, f'{new_dir}_renamed')

            files = ftp.listdir(self.dir)

            assert f'{self.dir}/{new_dir}_renamed' in files

            ftp.rmdir(f'{new_dir}_renamed')

    def test_put_delete(self):
        with FTPClient(self.host, self.user, self.password) as ftp, tempfile.NamedTemporaryFile() as f:
            remotepath = os.path.join(self.dir, os.path.basename(f.name))
            ftp.put(f.name, remotepath)

            ftp.delete(remotepath)

            files = ftp.listdir(self.dir)

            assert remotepath not in files

    def test_get(self):
        with FTPClient(self.host, self.user, self.password) as ftp, tempfile.NamedTemporaryFile(mode='w') as f:
            files = ftp.listdir(self.dir)

            remotepath = next((f for f in files if f.endswith('.csv') or f.endswith('.txt')), None)

            ftp.get(remotepath, f.name)

            assert os.path.exists(f.name)
            assert os.path.isfile(f.name)
