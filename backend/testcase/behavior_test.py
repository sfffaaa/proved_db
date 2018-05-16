import unittest
import sys
sys.path.append('src')
import deploy
from submit_and_record_chain_node import SubmitAndRecordChainNode
from proved_db import ProvedDB
from test_utils import get_db_path, unlink_silence, _TEST_CONFIG
from chain_utils import calculate_entry_hash
from web3 import Web3
import gevent


def calculate_submit_hash_from_group(vals):
    hash_sums = [Web3.toInt(hexstr=val) for val in vals]
    return Web3.toHex(Web3.toInt(Web3.sha3(sum(hash_sums) & (2 ** 256 - 1))))


class TestBehavior(unittest.TestCase):

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

    def testBehaior(self):
        private_node = SubmitAndRecordChainNode(config_path=_TEST_CONFIG,
                                                submit_hash_callback_objs=[],
                                                record_over_callback_objs=[],
                                                wait_time=1)
        private_node.start()
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        # setting key val
        test_db.create({'my_key1': 'key1_data_01'})
        test_db.create({'my_key2': 'key1_data_01'})

        test_db.create({'my_key3': 'key1_data_01'})
        test_db.create({'my_key4': 'key1_data_01'})

        test_db.create({'my_key5': 'key1_data_01'})
        # check all entry
        test_db.check_all_entries()
        val = test_db.retrieve('my_key2')
        self.assertEqual(True, test_db.check_entry('my_key2', val), 'should pass')

        gevent.sleep(1)
        # check finalised data
        check_hash = calculate_entry_hash(['my_key3', 'key1_data_01'])
        existed, entries_length = test_db.get_finalised_group_entries_length(check_hash)
        self.assertEqual(True, existed, 'should be pass')
        all_check_hash = [test_db.get_finalised_group_entry(check_hash, i) for i in range(entries_length)]
        self.assertEqual(True, check_hash in all_check_hash, 'should pass')

        check_hash_sum = calculate_submit_hash_from_group(all_check_hash)
        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        double_check_hashes = [test_db.get_finalise_entry(check_hash_sum, i)
                               for i in range(entries_length)]
        self.assertEqual(double_check_hashes, all_check_hash, 'should pass')

        check_hash = calculate_entry_hash(['my_key5', 'key1_data_01'])
        existed, entries_length = test_db.get_finalised_group_entries_length(check_hash)
        self.assertEqual(False, existed, 'should be pass')

        # Test again
        test_db.update({'my_key5': 'key1_data_02'})
        gevent.sleep(1)

        check_hash = calculate_entry_hash(['my_key5', 'key1_data_01'])
        existed, entries_length = test_db.get_finalised_group_entries_length(check_hash)
        self.assertEqual(True, existed, 'should be pass')

        all_check_hash = [test_db.get_finalised_group_entry(check_hash, i) for i in range(entries_length)]
        self.assertEqual(True, check_hash in all_check_hash, 'should pass')

        check_hash_sum = calculate_submit_hash_from_group(all_check_hash)
        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        double_check_hashes = [test_db.get_finalise_entry(check_hash_sum, i)
                               for i in range(entries_length)]
        self.assertEqual(double_check_hashes, all_check_hash, 'should pass')

#        # setting key val again
        test_db.delete('my_key2')
        test_db.create({'my_key6': 'key1_data_01'})
        # Test again
        test_db.update({'my_key6': 'key1_data_02'})

        gevent.sleep(1)
        check_hash = calculate_entry_hash(['my_key6', 'key1_data_01'])
        existed, entries_length = test_db.get_finalised_group_entries_length(check_hash)
        self.assertEqual(True, existed, 'should be pass')

        all_check_hash = [test_db.get_finalised_group_entry(check_hash, i) for i in range(entries_length)]
        self.assertEqual(True, check_hash in all_check_hash, 'should pass')

        check_hash_sum = calculate_submit_hash_from_group(all_check_hash)
        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        double_check_hashes = [test_db.get_finalise_entry(check_hash_sum, i)
                               for i in range(entries_length)]
        self.assertEqual(double_check_hashes, all_check_hash, 'should pass')

        private_node.kill()


if __name__ == '__main__':
    unittest.main()
