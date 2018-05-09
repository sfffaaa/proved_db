import unittest
import sys
sys.path.append('src')
from proved_db import ProvedDB
from record_hash import RecordHash
import deploy
from base_chain_node import BaseChainNode
from web3 import Web3
from test_utils import calculate_submit_hash, get_db_path, unlink_silence, _TEST_CONFIG
from chain_utils import calculate_entry_hash
from test_utils import TEST_PAIR_LENGTH, TEST_PAIR_PERIOD


def show_log_data(node, event):
    print('-------------------------------------------------------')
    print(event)
    print('-------------------------------------------------------')
    node.kill()


class TestPrivateNodeSingleMethods(unittest.TestCase):

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

    def submitHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._submit_single_hash_data = Web3.toHex(event_finalise_hash)
        node.kill()

    def testSingleEvent(self):
        private_node = BaseChainNode(config_path=_TEST_CONFIG,
                                     proved_db_callback_objs=[self],
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

        private_node.join()
        check_hash_sum = calculate_submit_hash([[test_key, _] for _ in test_data])
        self.assertEqual(self._submit_single_hash_data, check_hash_sum, 'should be the same')


class TestPrivateNodeMultipleMethods(unittest.TestCase):

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
        setattr(self, 'submitHashEventCallback', None)
        path = get_db_path(_TEST_CONFIG)
        self.assertTrue(unlink_silence(path))

    def submitHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._submit_multiple_hash_data.append(Web3.toHex(event_finalise_hash))
        print('-=-=-=-=-=-=-=-= {0}'.format(self._submit_multiple_hash_data[-1]))

    def testMultipleEvent(self):
        self._submit_multiple_hash_data = []
        test_db = ProvedDB(_TEST_CONFIG, 'json')
        private_node = BaseChainNode(config_path=_TEST_CONFIG,
                                     proved_db_callback_objs=[self],
                                     record_hash_callback_objs=[],
                                     wait_time=1)
        private_node.start()
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                test_db.create({val: val})

        private_node.join(10)
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            check_hash_sum = calculate_submit_hash([[str(i), str(i)],
                                                    [str(i + 1), str(i + 1)]])
            self.assertEqual(self._submit_multiple_hash_data[int(i / TEST_PAIR_PERIOD)],
                             check_hash_sum, 'should be the same')


class TestPrivateNodeRecordHashMethods(unittest.TestCase):

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

    def recordOverEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._record_over_hashes.append(Web3.toHex(event_finalise_hash))
        print('-=-=-=-=-=-=-=-= {0}'.format(self._record_over_hashes[-1]))

    def testMultipleEvent(self):
        self._record_over_hashes = []
        test_hash_mgr = RecordHash(_TEST_CONFIG)
        private_node = BaseChainNode(config_path=_TEST_CONFIG,
                                     proved_db_callback_objs=[],
                                     record_hash_callback_objs=[self],
                                     wait_time=1)
        private_node.start()
        check_hashes = []
        for i in range(0, TEST_PAIR_PERIOD * TEST_PAIR_LENGTH, TEST_PAIR_PERIOD):
            for j in range(TEST_PAIR_PERIOD):
                val = str(i + j)
                hash_val = calculate_entry_hash([val, val])
                test_hash_mgr.record(hash_val)
                check_hashes.append(hash_val)

        private_node.join(4)
        self.assertEqual(check_hashes, self._record_over_hashes, 'data should be the same')


if __name__ == '__main__':
    unittest.main()
