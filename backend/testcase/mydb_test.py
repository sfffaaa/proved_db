#!/usr/bin/env python3
# encoding: utf-8

import unittest
import os
import sys
import errno
sys.path.append('src')
from mydb import MyDB


def _unlink_silence(path):
    try:
        os.unlink(path)
        return True
    except OSError as e:
        if e.errno == errno.ENOENT:
            return True
    return False


class TestMyDBSupportTypes(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNotSupportTypes(self):
        self.assertRaisesRegex(OSError, 'type not in support_types', MyDB, 'test')


class TestMyDBJsonMethods(unittest.TestCase):
    _JSON_PATH = 'test.json'

    def setUp(self):
        _unlink_silence(self._JSON_PATH)

    def tearDown(self):
        _unlink_silence(self._JSON_PATH)

    def testCreateEntry(self):
        self.assertTrue(False)

    def testUpdateEntry(self):
        self.assertTrue(False)

    def testDeleteEntry(self):
        self.assertTrue(False)

    def testSelectEntry(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
