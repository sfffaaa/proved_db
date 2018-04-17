#!/usr/bin/env python3
# encoding: utf-8

import unittest
import os
import sys
import errno
sys.path.append('src')
from proved_db import ProvedDB
from onchain_handler import OnChainHandler
import deploy

_TEST_CONFIG = 'testcase/etc/test_config.conf'


def _unlink_silence(path):
    try:
        os.unlink(path)
        return True
    except OSError as e:
        if e.errno == errno.ENOENT:
            return True
    return False


class TestProvedDBSupportTypes(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNotSupportTypes(self):
        self.assertRaisesRegex(OSError, 'type not in support_types', ProvedDB, _TEST_CONFIG, 'test')


class TestProvedDBJsonMethods(unittest.TestCase):
    _JSON_PATH = 'testcase/etc/test.json'

    TEST_DATA = {
        'testCreateEntry': {
            'test01': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        },
        'testCreateNoIdEntry': {
        },
        'testCreateDuplicateID': {
            'test02': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        },
        'testRetrieveEntry': {
            'test01': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        },
    }

    @classmethod
    def setUpClass(cls):
        deploy.deploy(_TEST_CONFIG)

    @classmethod
    def tearDownClass(cls):
        deploy.undeploy(_TEST_CONFIG)

    def setUp(self):
        self.assertTrue(_unlink_silence(self._JSON_PATH))

    def tearDown(self):
        self.assertTrue(_unlink_silence(self._JSON_PATH))

    def testCreateEntry(self):
        testDB = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateEntry']
        testDB.create(data)
        # Don't use select check here, so assume create is success here
        # Call solidity select for find hash is already on smart contract

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        key, val = list(data)[0], onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val, 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testCreateNoIdEntry(self):
        testDB = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateNoIdEntry']
        self.assertRaisesRegex(IOError, 'input key should not more than one', testDB.create, data)

    def testCreateDuplicateID(self):
        testDB = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateDuplicateID']

        testDB.create(data)
        self.assertRaisesRegex(IOError, 'unique key already exist', testDB.create, data)

    def testRetrieveNoEntry(self):
        onchain_handler = OnChainHandler(_TEST_CONFIG)
        exist, data = onchain_handler.retrieve('You should not exist!!!')
        self.assertEqual(exist, False, 'key not on chain')
        self.assertEqual(data, '', "data doesn't exist also!")

    def testRetrieveEntry(self):
        testDB = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testRetrieveEntry']
        testDB.create(data)

        retrieve_data = testDB.retrieve(list(data)[0])
        check_data = data[list(data)[0]]
        self.assertEqual(retrieve_data, check_data,
                         'retrive should be the same data, {0} != {1}'.format(retrieve_data, check_data))

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        key, val = list(data)[0], onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val, 'data on chain is inconsistent {0} != {1}'.format(data, val))

#     def testUpdateEntry(self):
#         self.assertTrue(False)
#
#     def testDeleteEntry(self):
#         self.assertTrue(False)
#
#     def testSelectEntry(self):
#         self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
