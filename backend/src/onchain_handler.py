#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
import my_config
import time
from contract_handler import ContractHandler


class OnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._contract_handler = ContractHandler(config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()

    def convert_to_bytes(self, val):
        if val.startswith('0x'):
            return Web3.toBytes(hexstr=val)
        else:
            return Web3.toBytes(text=val)

    def hash_entry(self, val):
        return Web3.toHex(Web3.sha3(text=str(val)))

    def create(self, key, val):
        print('==== create start ====')
        tx_hash = self._contract_inst.Create(str(key), str(val),
                                             transact={'from': self._w3.eth.accounts[0],
                                                       'gas': 1000000})

        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        self._w3.miner.start(1)
        retry_time = 0
        while not tx_receipt and retry_time < 10:
            print('    wait for miner!')
            time.sleep(my_config.MINER_WAIT_TIME)
            tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
            retry_time += 1

        self._w3.miner.stop()
        if not tx_receipt:
            raise IOError('still cannot get contract result')

        print(tx_receipt)
        print('==== create finish ====')

    def update(self, key, val):
        print('==== update start ====')
        tx_hash = self._contract_inst.Update(str(key), str(val),
                                             transact={'from': self._w3.eth.accounts[0],
                                                       'gas': 1000000})

        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        self._w3.miner.start(1)
        retry_time = 0
        while not tx_receipt and retry_time < 10:
            print('    wait for miner!')
            time.sleep(my_config.MINER_WAIT_TIME)
            tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
            retry_time += 1

        self._w3.miner.stop()
        if not tx_receipt:
            raise IOError('still cannot get contract result')

        print(tx_receipt)
        print('==== update finish ====')

    def retrieve(self, key):
        print('==== retrieve start ====')

        exist, data = self._contract_inst.Retrieve(str(key))
        print('==== retrieve end ====')
        return (exist, Web3.toHex(data))

    def delete(self, key):
        print('==== deletestart ====')
        tx_hash = self._contract_inst.Delete(str(key),
                                             transact={'from': self._w3.eth.accounts[0],
                                                       'gas': 1000000})

        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        self._w3.miner.start(1)
        retry_time = 0
        while not tx_receipt and retry_time < 10:
            print('    wait for miner!')
            time.sleep(my_config.MINER_WAIT_TIME)
            tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
            retry_time += 1

        self._w3.miner.stop()
        if not tx_receipt:
            raise IOError('still cannot get contract result')

        print(tx_receipt)
        print('==== delete finish ====')

    def check_entry(self, key, val):
        print('==== check_entry start ====')
        ret = self._contract_inst.CheckEntry(str(key), str(val))
        print('==== check_entry end ====')
        return ret

    def get_keys_length(self):
        print('==== get_keys_length start ====')
        ret = self._contract_inst.GetKeysLength()
        print('==== get_keys_length end ====')
        return ret

    def get_key(self, idx):
        print('==== get_key start ====')
        ret = self._contract_inst.GetKey(idx)
        print('==== get_key end ====')
        return ret

    def get_finalise_entries_length(self, hash_sum):
        print('==== get_finalise_entries_length start ====')
        hash_arg = self.convert_to_bytes(hash_sum)
        existed, finalised, length = self._contract_inst.GetFinaliseEntriesLength(hash_arg)
        print('==== get_finalise_entries_length end ====')
        return existed, finalised, length

    def get_finalise_entry(self, hash_sum, idx):
        print('==== get_finalise_entries_length start ====')
        hash_arg = self.convert_to_bytes(hash_sum)
        ret = self._contract_inst.GetFinaliseEntry(hash_arg, idx)
        print('==== get_finalise_entries_length end ====')
        return ret

    def finalise(self, hash_sum):
        print('==== finalise start ====')
        hash_arg = self.convert_to_bytes(hash_sum)
        tx_hash = self._contract_inst.Finalise(hash_arg,
                                               transact={'from': self._w3.eth.accounts[0],
                                                         'gas': 1000000})

        tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
        self._w3.miner.start(1)
        retry_time = 0
        while not tx_receipt and retry_time < 10:
            print('    wait for miner!')
            time.sleep(my_config.MINER_WAIT_TIME)
            tx_receipt = self._w3.eth.getTransactionReceipt(tx_hash)
            retry_time += 1

        self._w3.miner.stop()
        if not tx_receipt:
            raise IOError('still cannot get contract result')

        print(tx_receipt)
        print('==== dfinalise finish ====')

    def get_finalised_group_entries_length(self, hash_sum):
        print('==== get_finalised_group_entries_length start ====')
        hash_arg = self.convert_to_bytes(hash_sum)
        existed, length = self._contract_inst.GetFinalisedGroupEntriesLength(hash_arg)
        print('==== get_finalised_group_entries_length end ====')
        return existed, length

    def get_finalised_group_entry(self, hash_sum, idx):
        print('==== get_finalised_group_entry start ====')
        hash_arg = self.convert_to_bytes(hash_sum)
        ret = self._contract_inst.GetFinalisedGroupEntry(hash_arg, idx)
        print('==== get_finalised_group_entry end ====')
        return Web3.toHex(ret)


if __name__ == '__main__':
    pass
