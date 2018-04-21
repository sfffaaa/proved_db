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
            'test03': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        },
        'testUpdateEntry': [{
            'test04': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }}, {
            'test04': {
                'mydata03': 'data03',
                'mydata04': 'data04'
            }}
        ],
        'testCheckEntryWithEntry': [{
            'test05': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        }]
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
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateEntry']
        test_db.create(data)
        # Don't use select check here, so assume create is success here
        # Call solidity select for find hash is already on smart contract

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        key, val = list(data)[0], onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val, 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testCreateNoIdEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateNoIdEntry']
        self.assertRaisesRegex(IOError, 'input key should not more than one', test_db.create, data)

    def testCreateDuplicateID(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateDuplicateID']

        test_db.create(data)
        self.assertRaisesRegex(IOError, 'unique key already exist', test_db.create, data)

    def testRetrieveNoEntry(self):
        onchain_handler = OnChainHandler(_TEST_CONFIG)
        exist, data = onchain_handler.retrieve('You should not exist!!!')
        self.assertEqual(exist, False, 'key not on chain')
        self.assertEqual(data, '', "data doesn't exist also!")

    def testRetrieveEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testRetrieveEntry']
        test_db.create(data)

        retrieve_data = test_db.retrieve(list(data)[0])
        check_data = data[list(data)[0]]
        self.assertEqual(retrieve_data, check_data,
                         'retrive should be the same data, {0} != {1}'.format(retrieve_data, check_data))

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        key, val = list(data)[0], onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val, 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testDeleteEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateEntry']
        test_db.create(data)

        key = list(data)[0]
        test_db.delete(key)

        data = test_db.retrieve(key)
        self.assertEqual(data, '', 'data is deleted!')

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        val = onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, False, 'key is on chain')
        self.assertEqual(data, '', 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testDeleteNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        data = self.TEST_DATA['testCreateEntry']
        key = list(data)[0]
        test_db.delete(key)

        data = test_db.retrieve(key)
        self.assertEqual(data, '', 'data is deleted!')

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        val = onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, False, 'key is on chain')
        self.assertEqual(data, '', 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testUpdateNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        self.assertRaisesRegex(IOError, 'unique key does not exist',
                               test_db.update, {'you should not pass': {'a': 'b'}})

    def testUpdateEntry(self):
        test_key = 'testUpdateEntry'
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        test_db.create(self.TEST_DATA[test_key][0])
        test_db.update(self.TEST_DATA[test_key][1])

        data = self.TEST_DATA[test_key][1]
        retrieve_data = test_db.retrieve(list(data)[0])
        check_data = data[list(data)[0]]
        self.assertEqual(retrieve_data, check_data,
                         'retrive should be the same data, {0} != {1}'.format(retrieve_data, check_data))

        onchain_handler = OnChainHandler(_TEST_CONFIG)
        key, val = list(data)[0], onchain_handler.hash_entry(data)
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val, 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testCheckEntryNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        check_data = test_db.check_entry('I should not pass', 'I should not pass')
        self.assertEqual(check_data, False, 'checking should not pass')

    def testCheckEntryWithEntry(self):
        test_key = 'testCheckEntryWithEntry'
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        test_db.create(self.TEST_DATA[test_key][0])

        now_key = list(self.TEST_DATA[test_key][0])[0]
        now_val = self.TEST_DATA[test_key][0][now_key]
        ret = test_db.check_entry(now_key, now_val)
        self.assertEqual(ret, True, 'checking should pass')


if __name__ == '__main__':
    unittest.main()
