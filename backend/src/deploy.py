#!/usr/bin/env python3
# encoding: utf-8

import os
import json
from web3 import Web3
import hexbytes
import time
from config_handler import ConfigHandler

CONFIG_PATH = 'etc/config.conf'


def _ComposeContractBuildPath(truffle_build_path, target_contract_name):
    json_filename = '{0}.json'.format(target_contract_name)
    target_path = os.path.join(*[truffle_build_path, 'contracts', json_filename])
    return target_path


def _GetBuildContractJsonFileAttribute(filepath, key):
    with open(filepath) as f:
        return json.load(f)[key]


def _DeploySmartContract(contract_path, file_ipc):
    w3 = Web3(Web3.IPCProvider(file_ipc))
    abi = _GetBuildContractJsonFileAttribute(contract_path, 'abi')
    bytecode = _GetBuildContractJsonFileAttribute(contract_path, 'bytecode')
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0], 'gas': 5000000})
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    w3.miner.start(1)
    retry_time = 0
    while not tx_receipt and retry_time < 10:
        print('    wait for miner!')
        time.sleep(2)
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        retry_time += 1

    w3.miner.stop()
    if not tx_receipt:
        raise IOError('still cannot get contract result')

    return tx_receipt, w3.eth.accounts[0]


def _DumpContractInfo(contract_path, contract_detail, contract_owner, file_path):
    file_path = os.path.abspath(file_path)
    dir_path = os.path.dirname(file_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    json_data = {
        'abi': _GetBuildContractJsonFileAttribute(contract_path, 'abi'),
        'address': contract_detail['contractAddress'],
        'owner': contract_owner,
        'detail': {k: Web3.toHex(v) if type(v) is hexbytes.main.HexBytes else v
                   for k, v in contract_detail.items()}
    }
    with open(file_path, 'w') as f:
        json.dump(json_data, f)


def deploy(config_path=CONFIG_PATH):

    config_handler = ConfigHandler(config_path)

    print('==== Compile smart contract ====')
    cmd = '(cd {0}; truffle compile)'.format(config_handler.get_chain_config('Deploy', 'truffle_path'))
    print('run command {0}'.format(cmd))
    os.system(cmd)

    print('==== Deploy started ====')
    contract_path = _ComposeContractBuildPath(config_handler.get_chain_config('Deploy', 'truffle_build_path'),
                                              config_handler.get_chain_config('Deploy', 'target_contract_name'))

    assert os.path.isfile(contract_path), 'file compiled path {0} doesn\'t exist'.format(contract_path)

    print('==== Deploy contract to private chain  ====')
    contract_detail, contract_owner = _DeploySmartContract(contract_path,
                                                           config_handler.get_chain_config('Ethereum', 'file_ipc'))

    _DumpContractInfo(contract_path,
                      contract_detail,
                      contract_owner,
                      config_handler.get_chain_config('Output', 'file_path'))

    print('==== Deploy finished ====')
    print('Contract detail:')
    for k, v in contract_detail.items():
        if type(v) is hexbytes.main.HexBytes:
            print('    {0}: {1}'.format(k, Web3.toHex(v)))
        else:
            print('    {0}: {1}'.format(k, v))
    print('Contract owner:')
    print('    owner: {0}'.format(contract_owner))


def undeploy(config_path=CONFIG_PATH):
    ''' Actually, smart contract cannot undeploy, but I need an function to remove unused intermediate file'''
    config_handler = ConfigHandler(config_path)
    os.unlink(config_handler.get_chain_config('Output', 'file_path'))


if __name__ == '__main__':
    deploy()
