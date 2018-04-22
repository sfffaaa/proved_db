#!/usr/bin/env python3
# encoding: utf-8

from web3 import Web3
from web3.contract import ConciseContract
import configparser
import json
import os
import my_config
import time


class OnChainHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._config_path = config_path
        file_ipc = self._get_chain_config('Ethereum', 'file_ipc')
        self._w3 = Web3(Web3.IPCProvider(file_ipc))

        contract_info = self._get_contract_info()
        contract_abi = contract_info['abi']
        contract_address = contract_info['address']
        self._contract_inst = self._w3.eth.contract(contract_address,
                                                    abi=contract_abi,
                                                    ContractFactoryClass=ConciseContract)

    def _get_chain_config(self, section, key):
        config = configparser.ConfigParser()
        config.read(self._config_path)
        return config.get(section, key)

    def _get_contract_info(self):
        file_path = self._get_chain_config('Output', 'file_path')
        file_path = os.path.abspath(file_path)
        with open(file_path) as f:
            contract_info = json.load(f)
        return contract_info

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

        exist, data = self._contract_inst.Retrieve(key)
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

if __name__ == '__main__':
    pass
