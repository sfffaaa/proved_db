#!/usr/bin/env python3
# encoding: utf-8

import my_config
import time
from contract_handler import ContractHandler
from chain_utils import convert_to_bytes

GAS_SPENT = 1000000


class RecordHashOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler('RecordHash', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def _check_transaction_meet_assert(self, tx_hash):
        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt:
            raise IOError('{0} receipt does not exist'.format(tx_receipt))
        if tx_receipt.gasUsed == GAS_SPENT:
            return True
        else:
            return False

    def record(self, input_hash):
        print('==== record start ====')
        tx_hash = self._contract_inst.functions.Record(convert_to_bytes(input_hash)) \
                                               .transact({'from': self._w3.eth.accounts[0],
                                                          'gas': GAS_SPENT})

        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        self._w3.miner.start(1)
        retry_time = 0
        while not tx_receipt and retry_time < 10:
            print('    wait for miner!')
            time.sleep(my_config.MINER_WAIT_TIME)
            tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
            retry_time += 1

        self._w3.miner.stop()
        if self._check_transaction_meet_assert(tx_hash):
            raise IOError('assert encounter..')
        print('==== record finish ====')

    def get(self, input_hash):
        print('==== get start ====')

        exist = self._contract_inst.functions.Get(convert_to_bytes(input_hash)).call()
        print('==== get end ====')
        return exist


if __name__ == '__main__':
    pass
