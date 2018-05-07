#!/usr/bin/env python3
# encoding: utf-8

import unittest
import sys
sys.path.append('src')
from record_hash import RecordHash
from record_hash_onchain_handler import RecordHashOnChainHandler
import deploy
from web3 import Web3
from test_utils import _TEST_CONFIG


class TestRecordHashJsonMethods(unittest.TestCase):
    TEST_DATA = {
        'testRecordEntry': Web3.toHex(Web3.sha3(text=str('Show my money'))),
        'testGetEntry': Web3.toHex(Web3.sha3(text=str('Yoooo man~')))
    }

    @classmethod
    def setUpClass(cls):
        deploy.deploy(_TEST_CONFIG)

    @classmethod
    def tearDownClass(cls):
        deploy.undeploy(_TEST_CONFIG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRecordEntry(self):
        test_hash_mgr = RecordHash(_TEST_CONFIG)
        data = self.TEST_DATA['testRecordEntry']
        test_hash_mgr.record(data)
        # Don't use select check here, so assume create is success here
        # Call solidity select for find hash is already on smart contract

        onchain_handler = RecordHashOnChainHandler(_TEST_CONFIG)
        exist = onchain_handler.get(data)
        self.assertEqual(exist, True, 'key is not on chain')

    def testGetEntry(self):
        test_hash_mgr = RecordHash(_TEST_CONFIG)
        data = self.TEST_DATA['testGetEntry']
        exist = test_hash_mgr.get(data)
        self.assertEqual(exist, False, 'key should on chain')

        test_hash_mgr.record(data)

        exist = test_hash_mgr.get(data)
        self.assertEqual(exist, True, 'key should on chain')


if __name__ == '__main__':
    unittest.main()
