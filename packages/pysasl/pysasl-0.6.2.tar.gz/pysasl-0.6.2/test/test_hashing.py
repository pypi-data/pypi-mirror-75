
from __future__ import absolute_import

import unittest

from pysasl import AuthenticationCredentials
from pysasl.hashing import BuiltinHash

builtin_hash = BuiltinHash(rounds=1000)
password_hash = '6f3b2db13d217e79d70d43d326a6e485756bcbe1b4e959f3e86c0d9eb62' \
    'fa40a352c178b1fc30896e7c484d74a78561d'


class TestHashing(unittest.TestCase):

    def test_builtin_good(self) -> None:
        creds = AuthenticationCredentials('username', 'password')
        self.assertTrue(creds.check_secret(password_hash, hash=builtin_hash))

    def test_builtin_invalid(self) -> None:
        creds = AuthenticationCredentials('username', 'invalid')
        self.assertFalse(creds.check_secret(password_hash, hash=builtin_hash))

    def test_cleartext_good(self) -> None:
        creds = AuthenticationCredentials('username', 'password')
        self.assertTrue(creds.check_secret('password'))

    def test_cleartext_invalid(self) -> None:
        creds = AuthenticationCredentials('username', 'invalid')
        self.assertFalse(creds.check_secret('password'))
