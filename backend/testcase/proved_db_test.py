#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')
from proved_db import ProvedDB
from proved_db_onchain_handler import ProvedDBOnChainHandler
import deploy
from test_utils import calculate_submit_hash, unlink_silence, get_db_path, ZERO_VALUE, _TEST_CONFIG
from test_utils import TEST_PAIR_LENGTH, TEST_PAIR_PERIOD
from chain_utils import calculate_entry_hash


class TestProvedDBSupportTypes(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testNotSupportTypes(self):
        self.assertRaisesRegex(OSError, 'type not in support_types', ProvedDB, _TEST_CONFIG, 'test')


class TestProvedDBJsonMethods(unittest.TestCase):
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
        }],
        'testCheckAllEntriesEntry': [{
            'test06': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        }, {
            'test07': {
                'mydata03': 'data03',
                'mydata04': 'data04'
            }
        }, {
            'test08': {
                'mydata05': 'data05',
                'mydata06': 'data06'
            }
        }],
        'testDeleteEntry': {
            'test09': {
                'mydata01': 'data01',
                'mydata02': 'data02'
            }
        },
        'testDeleteNoEntry': {
            'test10': {
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
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def tearDown(self):
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def testCreateEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testCreateEntry']
        test_db.create(data)
        # Don't use select check here, so assume create is success here
        # Call solidity select for find hash is already on smart contract

        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        key = list(data)[0]
        val = onchain_handler.hash_entry([key, data[key]])
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(data, val,
                         'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testCreateNoIdEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testCreateNoIdEntry']
        self.assertRaisesRegex(IOError, 'input key should not more than one', test_db.create, data)

    def testCreateDuplicateID(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testCreateDuplicateID']

        test_db.create(data)
        self.assertRaisesRegex(IOError, 'unique key already exist', test_db.create, data)

    def testRetrieveNoEntry(self):
        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        exist, data = onchain_handler.retrieve('You should not exist!!!')
        self.assertEqual(exist, False, 'key not on chain')
        self.assertEqual(data, ZERO_VALUE, "data doesn't exist also!")

    def testRetrieveEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testRetrieveEntry']
        test_db.create(data)

        retrieve_data = test_db.retrieve(list(data)[0])
        check_data = data[list(data)[0]]
        self.assertEqual(retrieve_data, check_data,
                         'retrive should be the same data, {0} != {1}'.format(retrieve_data, check_data))

        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        key = list(data)[0]
        onchain_hash = onchain_handler.hash_entry([key, data[key]])
        exist, retrieve_hash = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(retrieve_hash, onchain_hash,
                         'data on chain is inconsistent {0} != {1}'.format(retrieve_hash, onchain_hash))

    def testDeleteEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testDeleteEntry']
        test_db.create(data)

        key = list(data)[0]
        test_db.delete(key)

        data = test_db.retrieve(key)
        self.assertEqual(data, '', 'data is deleted!')

        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        val = onchain_handler.hash_entry([key, data])
        exist, data = onchain_handler.retrieve(key)
        self.assertEqual(exist, False, 'key is on chain')
        self.assertEqual(data, ZERO_VALUE, 'data on chain is inconsistent {0} != {1}'.format(data, val))

    def testDeleteNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        data = self.TEST_DATA['testDeleteNoEntry']
        key = list(data)[0]
        test_db.delete(key)

        data = test_db.retrieve(key)
        self.assertEqual(data, '', 'data is deleted!')

        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        exist, retrieve_hash = onchain_handler.retrieve(key)
        self.assertEqual(exist, False, 'key is not on chain')
        self.assertEqual(retrieve_hash, ZERO_VALUE,
                         'data on chain is inconsistent {0} != {1}'.format(retrieve_hash, ZERO_VALUE))

    def testUpdateNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        self.assertRaisesRegex(IOError, 'unique key does not exist',
                               test_db.update, {'you should not pass': {'a': 'b'}})

    def testUpdateEntry(self):
        test_key = 'testUpdateEntry'
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        test_db.create(self.TEST_DATA[test_key][0])
        test_db.update(self.TEST_DATA[test_key][1])

        data = self.TEST_DATA[test_key][1]
        retrieve_data = test_db.retrieve(list(data)[0])
        check_data = data[list(data)[0]]
        self.assertEqual(retrieve_data, check_data,
                         'retrive should be the same data, {0} != {1}'.format(retrieve_data, check_data))

        onchain_handler = ProvedDBOnChainHandler(_TEST_CONFIG)
        key = list(data)[0]
        check_hash = onchain_handler.hash_entry([key, data[key]])
        exist, retrieve_hash = onchain_handler.retrieve(key)
        self.assertEqual(exist, True, 'key is not on chain')
        self.assertEqual(retrieve_hash, check_hash,
                         'data on chain is inconsistent {0} != {1}'.format(retrieve_hash, check_hash))

    def testCheckEntryNoEntry(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        check_data = test_db.check_entry('I should not pass', 'I should not pass')
        self.assertEqual(check_data, False, 'checking should not pass')

    def testCheckEntryWithEntry(self):
        test_key = 'testCheckEntryWithEntry'
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        test_db.create(self.TEST_DATA[test_key][0])

        now_key = list(self.TEST_DATA[test_key][0])[0]
        now_val = self.TEST_DATA[test_key][0][now_key]
        ret = test_db.check_entry(now_key, now_val)
        self.assertEqual(ret, True, 'checking should pass')

    def testCheckAllEntriesNoEntry(self):
        deploy.deploy(_TEST_CONFIG)
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        self.assertEqual(test_db.check_all_entries(), True, 'There should no data to check')

    def testCheckAllEntriesEntry(self):
        deploy.deploy(_TEST_CONFIG)
        test_key = 'testCheckAllEntriesEntry'
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        for test_case in self.TEST_DATA[test_key]:
            test_db.create(test_case)
        self.assertEqual(test_db.check_all_entries(), True, 'There should pass the checking')

        test_db.delete(list(self.TEST_DATA[test_key][1])[0])
        self.assertEqual(test_db.check_all_entries(), True, 'There should pass the checking')


class TestSubmitChecking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        deploy.deploy(_TEST_CONFIG)

    @classmethod
    def tearDownClass(cls):
        deploy.undeploy(_TEST_CONFIG)

    def setUp(self):
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def tearDown(self):
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def testEmptySubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        key = 'You should not pass'
        existed, finalised, entries_length = test_db.get_finalise_entries_length(key)
        self.assertEqual(False, existed, 'hash doesnt exist')
        self.assertEqual(False, finalised, 'hash doesn finalise')
        self.assertEqual(0, entries_length, 'hash entry index should be zero')

    def testSingleSubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_key = 'Plz, show me the money'
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        check_hash_sum = calculate_submit_hash([[test_key, _] for _ in test_data])
        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(False, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(calculate_entry_hash([test_key, test_data[i]]),
                             entry_hash,
                             'hash should be the same')
        test_db.finalise(check_hash_sum)

        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(calculate_entry_hash([test_key, test_data[i]]),
                             entry_hash,
                             'hash should be the same')

    def testMultipleSubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            check_hash_sum = calculate_submit_hash([[str(i), str(i)],
                                                    [str(i + 1), str(i + 1)]])
            existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
            self.assertEqual(True, existed, 'hash does exist')
            self.assertEqual(False, finalised, 'hash doesn finalise')
            self.assertEqual(2, entries_length, 'hash entry index should not be zero')
            test_db.finalise(check_hash_sum)

            existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
            self.assertEqual(True, existed, 'hash does exist')
            self.assertEqual(True, finalised, 'hash doesn finalise')
            self.assertEqual(2, entries_length, 'hash entry index should not be zero')

            for j in range(entries_length):
                entry_hash = test_db.get_finalise_entry(check_hash_sum, j)
                self.assertEqual(calculate_entry_hash([str(i + j), str(i + j)]),
                                 entry_hash,
                                 'hash should be the same')


class TestFinaliseGroupChecking(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        deploy.deploy(_TEST_CONFIG)

    @classmethod
    def tearDownClass(cls):
        deploy.undeploy(_TEST_CONFIG)

    def setUp(self):
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def tearDown(self):
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def testEmptyFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        key = 'You should not pass'
        existed, entries_length = test_db.get_finalised_group_entries_length(key)
        self.assertEqual(False, existed, 'hash doesnt exist')
        self.assertEqual(0, entries_length, 'hash entry index should be zero')

    def testSingleFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        test_key = 'show me the money'
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        for check_val in test_data:
            check_group_hash = calculate_entry_hash([test_key, check_val])
            existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
            self.assertEqual(False, existed, 'hash does exist')
            self.assertEqual(0, entries_length, 'hash entry index should be zero')

        check_hash_sum = calculate_submit_hash([[test_key, _] for _ in test_data])
        test_db.finalise(check_hash_sum)

        for check_val in test_data:
            check_group_hash = calculate_entry_hash([test_key, check_val])
            existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
            self.assertEqual(True, existed, 'hash does exist')
            self.assertEqual(len(test_data), entries_length, 'hash entry index should not be zero')
            for i in range(entries_length):
                entry_hash = test_db.get_finalised_group_entry(check_group_hash, i)
                self.assertEqual(calculate_entry_hash([test_key, test_data[i]]),
                                 entry_hash,
                                 'hash should be the same')

    def testMultipleFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

            for j in range(TEST_PAIR_PERIOD):
                check_group_hash = calculate_entry_hash([str(i + j), str(i + j)])
                existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
                self.assertEqual(False, existed, 'hash does exist')
                self.assertEqual(0, entries_length, 'hash entry index should be zero')

            check_hash_sum = calculate_submit_hash([[str(i + j), str(i + j)] for j in range(TEST_PAIR_PERIOD)])
            test_db.finalise(check_hash_sum)

        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                check_group_hash = calculate_entry_hash([str(i + j), str(i + j)])
                existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
                self.assertEqual(True, existed, 'hash does exist')
                self.assertEqual(TEST_PAIR_PERIOD, entries_length, 'hash entry index should not be zero')
                for k in range(TEST_PAIR_PERIOD):
                    entry_hash = test_db.get_finalised_group_entry(check_group_hash, k)
                    self.assertEqual(calculate_entry_hash([str(i + k), str(i + k)]),
                                     entry_hash,
                                     'hash should be the same')


if __name__ == '__main__':
    unittest.main()
