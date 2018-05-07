import unittest
import sys
sys.path.append('src')
from web3 import Web3
import deploy
from proved_db import ProvedDB
from proved_db_private_node import SubmitAndRecordChainNode
from test_utils import calculate_submit_hash, get_db_path, unlink_silence, _TEST_CONFIG

TEST_PAIR_LENGTH = 2
TEST_PAIR_PERIOD = 2


def show_log_data(node, event):
    print('-------------------------------------------------------')
    print(event)
    print('-------------------------------------------------------')
    node.kill()


class TestSubmitAndRecordChainNode(unittest.TestCase):

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

    def testSingleEvent(self):
        private_node = SubmitAndRecordChainNode(config_path=_TEST_CONFIG,
                                                proved_db_callback_objs=[],
                                                record_hash_callback_objs=[],
                                                wait_time=1)
        private_node.start()
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        test_data = [{
            'testaaa': 'hash1'
        }, {
            'testbbb': 'hash2'
        }]
        test_key = 'May the force be with you'
        test_db.create({test_key: test_data[0]})
        test_db.update({test_key: test_data[1]})

        private_node.join(10)
        check_hash_sum = calculate_submit_hash([_ for _ in test_data])

        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(Web3.sha3(text=str(test_data[i])),
                             entry_hash,
                             'hash should be the same')


if __name__ == '__main__':
    unittest.main()
