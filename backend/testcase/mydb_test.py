#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')
from mydb import MyDB


class TestMyDBMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNotSupportTypes(self):
        pass_error = False
        try:
            MyDB('test')
        except Exception as e:
            if 'type not in support_types' in str(e):
                pass_error = True
        self.assertTrue(pass_error)

    def testJsonCreateEntry(self):
        self.assertTrue(False)

    def testJsonUpdateEntry(self):
        self.assertTrue(False)

    def testJsonDeleteEntry(self):
        self.assertTrue(False)

    def testJsonSelectEntry(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
