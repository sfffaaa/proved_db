import unittest
import os
import sys
import errno
sys.path.append('src')
from proved_db import ProvedDB
import deploy
from proved_db_private_node import ProvedDBPrivateChainNode
from web3 import Web3

_TEST_CONFIG = 'testcase/etc/test_config.conf'
ZERO_VALUE = '0x' + '0' * 64

TEST_PAIR_LENGTH = 2
TEST_PAIR_PERIOD = 2


# [TODO] Extract to utils function
def calculate_submit_hash(input_vals):
    hash_sums = [Web3.toInt(Web3.sha3(text=str(val)))
                 for val in input_vals]
    return Web3.toHex(Web3.sha3(sum(hash_sums) & (2 ** 256 - 1)))


def _unlink_silence(path):
    try:
        os.unlink(path)
        return True
    except OSError as e:
        if e.errno == errno.ENOENT:
            return True
    return False


def show_log_data(node, event):
    print('-------------------------------------------------------')
    print(event)
    print('-------------------------------------------------------')
    node.kill()


class TestPrivateNodeMethods(unittest.TestCase):
    _JSON_PATH = 'testcase/etc/test.json'

    @classmethod
    def setUpClass(cls):
        deploy.deploy(_TEST_CONFIG)

    @classmethod
    def tearDownClass(cls):
        deploy.undeploy(_TEST_CONFIG)

    def setUp(self):
        setattr(self, 'submitHashEventCallback', None)
        self.assertTrue(_unlink_silence(self._JSON_PATH))

    def tearDown(self):
        setattr(self, 'submitHashEventCallback', None)
        self.assertTrue(_unlink_silence(self._JSON_PATH))

    def submitSingleHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._submit_single_hash_data = Web3.toHex(event_finalise_hash)
        node.kill()

    def submitMultipleHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._submit_multiple_hash_data.append(Web3.toHex(event_finalise_hash))
        print('-=-=-=-=-=-=-=-= {0}'.format(self._submit_multiple_hash_data[-1]))

    def testSingleEvent(self):
        setattr(self, 'submitHashEventCallback', self.submitSingleHashEventCallback)
        private_node = ProvedDBPrivateChainNode(config_path=_TEST_CONFIG,
                                                callback_objs=[self],
                                                wait_time=1)
        private_node.start()
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_key = 'May the force be with you'
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        private_node.join()
        check_hash_sum = calculate_submit_hash([_ for _ in test_data])
        self.assertEqual(self._submit_single_hash_data, check_hash_sum, 'should be the same')

    def testMultipleEvent(self):
        self._submit_multiple_hash_data = []
        setattr(self, 'submitHashEventCallback', self.submitMultipleHashEventCallback)
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        private_node = ProvedDBPrivateChainNode(config_path=_TEST_CONFIG,
                                                callback_objs=[self],
                                                wait_time=1)
        private_node.start()
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

        private_node.join(10)
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            check_hash_sum = calculate_submit_hash([str(i), str(i + 1)])
            self.assertEqual(self._submit_multiple_hash_data[int(i / TEST_PAIR_PERIOD)],
                             check_hash_sum, 'should be the same')


class TestSubmitChecking(unittest.TestCase):
    _JSON_PATH = 'testcase/etc/test.json'

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

    def testEmptySubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        key = 'You should not pass'
        existed, finalised, entries_length = test_db.get_finalise_entries_length(key)
        self.assertEqual(False, existed, 'hash doesnt exist')
        self.assertEqual(False, finalised, 'hash doesn finalise')
        self.assertEqual(0, entries_length, 'hash entry index should be zero')

    def testSingleSubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_key = 'Plz, show me the money'
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        check_hash_sum = calculate_submit_hash([_ for _ in test_data])
        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(False, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(Web3.sha3(text=str(test_data[i])),
                             entry_hash,
                             'hash should be the same')
        test_db.finalise(check_hash_sum)

        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(Web3.sha3(text=str(test_data[i])),
                             entry_hash,
                             'hash should be the same')

    def testMultipleSubmitChecking(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            check_hash_sum = calculate_submit_hash([str(i), str(i + 1)])
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
                self.assertEqual(Web3.sha3(text=str(i + j)),
                                 entry_hash,
                                 'hash should be the same')


class TestFinaliseGroupChecking(unittest.TestCase):
    _JSON_PATH = 'testcase/etc/test.json'

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

    def testEmptyFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        key = 'You should not pass'
        existed, entries_length = test_db.get_finalised_group_entries_length(key)
        self.assertEqual(False, existed, 'hash doesnt exist')
        self.assertEqual(0, entries_length, 'hash entry index should be zero')

    def testSingleFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        test_key = 'show me the money'
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        for check_val in test_data:
            check_group_hash = Web3.toHex(Web3.sha3(text=str(check_val)))
            existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
            self.assertEqual(False, existed, 'hash does exist')
            self.assertEqual(0, entries_length, 'hash entry index should be zero')

        check_hash_sum = calculate_submit_hash([_ for _ in test_data])
        test_db.finalise(check_hash_sum)

        for check_val in test_data:
            check_group_hash = Web3.toHex(Web3.sha3(text=str(check_val)))
            existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
            self.assertEqual(True, existed, 'hash does exist')
            self.assertEqual(len(test_data), entries_length, 'hash entry index should not be zero')
            for i in range(entries_length):
                entry_hash = test_db.get_finalised_group_entry(check_group_hash, i)
                self.assertEqual(Web3.toHex(Web3.sha3(text=str(test_data[i]))),
                                 entry_hash,
                                 'hash should be the same')

    def testMultipleFinaliseGroup(self):
        test_db = ProvedDB(_TEST_CONFIG, 'json', self._JSON_PATH)
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

            for j in range(TEST_PAIR_PERIOD):
                check_group_hash = Web3.toHex(Web3.sha3(text=str(i + j)))
                existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
                self.assertEqual(False, existed, 'hash does exist')
                self.assertEqual(0, entries_length, 'hash entry index should be zero')

            check_hash_sum = calculate_submit_hash([str(i + j) for j in range(TEST_PAIR_PERIOD)])
            test_db.finalise(check_hash_sum)

        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                check_group_hash = Web3.toHex(Web3.sha3(text=str(i + j)))
                existed, entries_length = test_db.get_finalised_group_entries_length(check_group_hash)
                self.assertEqual(True, existed, 'hash does exist')
                self.assertEqual(TEST_PAIR_PERIOD, entries_length, 'hash entry index should not be zero')
                for k in range(TEST_PAIR_PERIOD):
                    entry_hash = test_db.get_finalised_group_entry(check_group_hash, k)
                    self.assertEqual(Web3.toHex(Web3.sha3(text=str(i + k))),
                                     entry_hash,
                                     'hash should be the same')


if __name__ == '__main__':
    unittest.main()
