#!/usr/bin/env python3
# encoding: utf-8

import my_config
from contract_handler import ContractHandler
from chain_utils import check_transaction_meet_assert, wait_miner


class RegisterOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler('Register', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def set_register(self, name, address):
        print('==== record start ====')
        tx_hash = self._contract_inst.functions.SetInst(name, address) \
                                               .transact({'from': self._w3.eth.accounts[0],
                                                          'gas': my_config.GAS_SPENT})
        wait_miner(self._w3, tx_hash)
        if check_transaction_meet_assert(self._w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== record finish ====')

    def set_multiple_register(self, name_dict):
        print('==== record start ====')
        tx_hashs = []
        for name, address in name_dict.items():
            tx_hash = self._contract_inst.functions.SetInst(name, address) \
                                                   .transact({'from': self._w3.eth.accounts[0],
                                                              'gas': my_config.GAS_SPENT})
            tx_hashs.append(tx_hash)

        wait_miner(self._w3, tx_hashs)
        if check_transaction_meet_assert(self._w3, tx_hashs):
            raise IOError('assert encounter..')
        print('==== record finish ====')

    def get_register(self, name):
        print('==== get start ====')

        address = self._contract_inst.functions.GetInst(name).call()
        print('==== get end ====')
        return address

    def set_whitelist(self, address):
        print('==== record start ====')
        tx_hash = self._contract_inst.functions.SetWhitelist(address) \
                                               .transact({'from': self._w3.eth.accounts[0],
                                                          'gas': my_config.GAS_SPENT})
        wait_miner(self._w3, tx_hash)
        if check_transaction_meet_assert(self._w3, tx_hash):
            raise IOError('assert encounter..')
        print('==== record finish ====')

    def set_multiple_whitelist(self, addresses):
        print('==== record start ====')
        tx_hashs = []
        for address in addresses:
            tx_hash = self._contract_inst.functions.SetWhitelist(address) \
                                                   .transact({'from': self._w3.eth.accounts[0],
                                                              'gas': my_config.GAS_SPENT})
            tx_hashs.append(tx_hash)

        wait_miner(self._w3, tx_hashs)
        if check_transaction_meet_assert(self._w3, tx_hashs):
            raise IOError('assert encounter..')
        print('==== record finish ====')


if __name__ == '__main__':
    pass
