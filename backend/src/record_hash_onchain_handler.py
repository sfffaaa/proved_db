#!/usr/bin/env python3
# encoding: utf-8

import my_config
from contract_handler import ContractHandler
from chain_utils import convert_to_bytes, wait_miner, check_transaction_meet_assert

GAS_SPENT = 1000000


class RecordHashOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler('RecordHash', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def record(self, input_hash):
        print('==== record start ====')
        tx_hash = self._contract_inst.functions.Record(convert_to_bytes(input_hash)) \
                                               .transact({'from': self._w3.eth.accounts[0],
                                                          'gas': GAS_SPENT})

        wait_miner(self._w3, tx_hash)
        if check_transaction_meet_assert(self._w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== record finish ====')

    def get(self, input_hash):
        print('==== get start ====')

        exist = self._contract_inst.functions.Get(convert_to_bytes(input_hash)).call()
        print('==== get end ====')
        return exist


if __name__ == '__main__':
    pass
