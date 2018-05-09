#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
import my_config
import time
from contract_handler import ContractHandler
from chain_utils import convert_to_bytes, calculate_entry_hash

GAS_SPENT = 1000000


class ProvedDBOnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler('ProvedDB', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def hash_entry(self, input_vals):
        return calculate_entry_hash(input_vals)

    def create(self, key, val):
        print('==== create start ====')
        tx_hash = self._contract_inst.functions.Create(str(key), str(val)) \
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

        print('==== create finish ====')

    def update(self, key, val):
        print('==== update start ====')
        tx_hash = self._contract_inst.functions.Update(str(key), str(val)) \
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

        print('==== update finish ====')

    def retrieve(self, key):
        print('==== retrieve start ====')

        exist, data = self._contract_inst.functions.Retrieve(str(key)).call()
        print('==== retrieve end ====')
        return (exist, Web3.toHex(data))

    def delete(self, key):
        print('==== deletestart ====')
        tx_hash = self._contract_inst.functions.Delete(str(key)) \
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

        print('==== delete finish ====')

    def check_entry(self, key, val):
        print('==== check_entry start ====')
        ret = self._contract_inst.functions.CheckEntry(str(key), str(val)).call()
        print('==== check_entry end ====')
        return ret

    def get_keys_length(self):
        print('==== get_keys_length start ====')
        ret = self._contract_inst.functions.GetKeysLength().call()
        print('==== get_keys_length end ====')
        return ret

    def get_key(self, idx):
        print('==== get_key start ====')
        ret = self._contract_inst.functions.GetKey(idx).call()
        print('==== get_key end ====')
        return ret

    def get_finalise_entries_length(self, hash_sum):
        print('==== get_finalise_entries_length start ====')
        hash_arg = convert_to_bytes(hash_sum)
        existed, finalised, length = self._contract_inst.functions.GetFinaliseEntriesLength(hash_arg).call()
        print('==== get_finalise_entries_length end ====')
        return existed, finalised, length

    def get_finalise_entry(self, hash_sum, idx):
        print('==== get_finalise_entries_length start ====')
        hash_arg = convert_to_bytes(hash_sum)
        ret = self._contract_inst.functions.GetFinaliseEntry(hash_arg, idx).call()
        print('==== get_finalise_entries_length end ====')
        return Web3.toHex(ret)

    def finalise(self, hash_sum):
        print('==== finalise start ====')
        hash_arg = convert_to_bytes(hash_sum)
        tx_hash = self._contract_inst.functions.Finalise(hash_arg) \
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

        print('==== dfinalise finish ====')

    def get_finalised_group_entries_length(self, hash_sum):
        print('==== get_finalised_group_entries_length start ====')
        hash_arg = convert_to_bytes(hash_sum)
        existed, length = self._contract_inst.functions.GetFinalisedGroupEntriesLength(hash_arg).call()
        print('==== get_finalised_group_entries_length end ====')
        return existed, length

    def get_finalised_group_entry(self, hash_sum, idx):
        print('==== get_finalised_group_entry start ====')
        hash_arg = convert_to_bytes(hash_sum)
        ret = self._contract_inst.functions.GetFinalisedGroupEntry(hash_arg, idx).call()
        print('==== get_finalised_group_entry end ====')
        return Web3.toHex(ret)

    def _check_transaction_meet_assert(self, tx_hash):
        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        if not tx_receipt:
            raise IOError('{0} receipt does not exist'.format(tx_receipt))
        if tx_receipt.gasUsed == GAS_SPENT:
            return True
        else:
            return False


if __name__ == '__main__':
    pass
