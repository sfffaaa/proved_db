import gevent
import unittest
import sys
sys.path.append('src')
import deploy
from proved_db import ProvedDB
from submit_and_record_chain_node import SubmitAndRecordChainNode
from test_utils import calculate_submit_hash, get_db_path, unlink_silence, _TEST_CONFIG
from chain_utils import calculate_entry_hash


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
                                                submit_hash_callback_objs=[],
                                                record_over_callback_objs=[],
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

        gevent.sleep(1)
        check_hash_sum = calculate_submit_hash([[test_key, _] for _ in test_data])

        existed, finalised, entries_length = test_db.get_finalise_entries_length(check_hash_sum)
        self.assertEqual(True, existed, 'hash does exist')
        self.assertEqual(True, finalised, 'hash doesn finalise')
        self.assertEqual(2, entries_length, 'hash entry index should not be zero')

        for i in range(entries_length):
            entry_hash = test_db.get_finalise_entry(check_hash_sum, i)
            self.assertEqual(calculate_entry_hash([test_key, test_data[i]]),
                             entry_hash,
                             'hash should be the same')
        private_node.kill()


if __name__ == '__main__':
    unittest.main()
