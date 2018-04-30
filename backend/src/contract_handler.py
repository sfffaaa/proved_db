import my_config
from web3 import Web3
from web3.contract import ConciseContract
from config_handler import ConfigHandler
import os
import json


class ContractHandler():

    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._config_handler = ConfigHandler(config_path)
        file_ipc = self._config_handler.get_chain_config('Ethereum', 'file_ipc')
        self._w3 = Web3(Web3.IPCProvider(file_ipc))

        contract_info = self._get_contract_info()
        contract_abi = contract_info['abi']
        contract_address = contract_info['address']
        self._contract_inst = self._w3.eth.contract(contract_address,
                                                    abi=contract_abi,
                                                    ContractFactoryClass=ConciseContract)

    def get_w3(self):
        return self._w3

    def get_contract(self):
        return self._contract_inst

    def _get_contract_info(self):
        file_path = self._config_handler.get_chain_config('Output', 'file_path')
        file_path = os.path.abspath(file_path)
        with open(file_path) as f:
            contract_info = json.load(f)
        return contract_info
