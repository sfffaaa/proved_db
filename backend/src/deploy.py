#!/usr/bin/env python3
# encoding: utf-8

import os
import json
from web3 import Web3
import hexbytes
import time
from config_handler import ConfigHandler
from register import Register

CONFIG_PATH = 'etc/config.conf'
RETRY_TIME = 60


def _ComposeContractBuildPath(truffle_build_path, target_contract_name):
    json_filename = '{0}.json'.format(target_contract_name)
    target_path = os.path.join(*[truffle_build_path, 'contracts', json_filename])
    return target_path


def _GetBuildContractJsonFileAttribute(filepath, key):
    with open(filepath) as f:
        return json.load(f)[key]


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


def _StartMultipleDeployToChain(config_handler, contract_dict):
    file_ipc = config_handler.get_chain_config('Ethereum', 'file_ipc')
    w3 = Web3(Web3.IPCProvider(file_ipc))

    contract_tx_hash = {}
    for contract_name, contract_inst in contract_dict.items():
        tx_hash = contract_inst.transact({'from': w3.eth.accounts[0]})
        contract_tx_hash[contract_name] = tx_hash

    tx_receipts = {contract_name: w3.eth.getTransactionReceipt(tx_hash)
                   for contract_name, tx_hash in contract_tx_hash.items()}
    w3.miner.start(1)
    retry_time = 0
    while None in tx_receipts.values() and retry_time < RETRY_TIME:
        print('    wait for miner!')
        time.sleep(2)
        tx_receipts = {contract_name: w3.eth.getTransactionReceipt(tx_hash)
                       for contract_name, tx_hash in contract_tx_hash.items()}
        retry_time += 1
        print("wait...")

    w3.miner.stop()
    if None in tx_receipts.values():
        raise IOError('still cannot get contract result')

    return tx_receipts, w3.eth.accounts[0]


def _GetContractInstance(config_handler, contract_name):
    file_ipc = config_handler.get_chain_config('Ethereum', 'file_ipc')
    w3 = Web3(Web3.IPCProvider(file_ipc))

    print('==== Deploy started {0} ===='.format(contract_name))
    contract_path = _ComposeContractBuildPath(config_handler.get_chain_config('Deploy', 'truffle_build_path'),
                                              contract_name)
    assert os.path.isfile(contract_path), 'file compiled path {0} doesn\'t exist'.format(contract_path)

    abi = _GetBuildContractJsonFileAttribute(contract_path, 'abi')
    bytecode = _GetBuildContractJsonFileAttribute(contract_path, 'bytecode')

    return w3.eth.contract(abi=abi, bytecode=bytecode)


def _DumpMultipleSmartContract(config_handler, contract_detail_dict, contract_owner):
    for contract_name, contract_detail in contract_detail_dict.items():
        contract_path = _ComposeContractBuildPath(config_handler.get_chain_config('Deploy', 'truffle_build_path'),
                                                  contract_name)
        assert os.path.isfile(contract_path), 'file compiled path {0} doesn\'t exist'.format(contract_path)

        output_path = os.path.join(config_handler.get_chain_config('Output', 'file_path'),
                                   '{0}.json'.format(contract_name))

        _DumpContractInfo(contract_path,
                          contract_detail,
                          contract_owner,
                          output_path)


def _ComposeSmartContractArgs(config_handler, contract_name, my_args):
    if contract_name == 'ProvedDB':
        return [my_args['Register']['contractAddress']]
    elif contract_name == 'FinaliseRecord':
        raw_args = config_handler.get_chain_config(contract_name, 'args')
        return [int(raw_args.split()[0].strip()),
                my_args['Register']['contractAddress']]
    elif contract_name == 'Register':
        return []
    elif contract_name == 'ProvedCRUDStorageV0':
        return []
    elif contract_name == 'KeysRecordStorageV0':
        return []
    elif contract_name == 'RecordHashStorageV0':
        return []
    elif contract_name == 'EventEmitter':
        return []
    elif contract_name == 'ProvedCRUD':
        return [my_args['Register']['contractAddress']]
    elif contract_name == 'FinaliseRecordStorageV0':
        return []
    elif contract_name == 'RecordHash':
        return [my_args['Register']['contractAddress']]
    elif contract_name == 'KeysRecord':
        return [my_args['Register']['contractAddress']]
    else:
        raise IOError('Wrong contract name {0}'.format(contract_name))


def _ShowMultipleSmartContractDetail(contract_detail_dict, contract_owner):
    for contract_name, contract_detail in contract_detail_dict.items():
        print('==== Deploy finished {0} ===='.format(contract_name))
        print('Contract detail:')
        for k, v in contract_detail.items():
            if type(v) is hexbytes.main.HexBytes:
                print('    {0}: {1}'.format(k, Web3.toHex(v)))
            else:
                print('    {0}: {1}'.format(k, v))
        print('Contract owner:')
        print('    owner: {0}'.format(contract_owner))


def _DeployMultipleSmartContractV0(config_handler, infos):
    contract_insts = {}
    for contract_name, my_args in infos.items():
        print('==== Deploy started {0} ===='.format(contract_name))
        my_args = _ComposeSmartContractArgs(config_handler, contract_name, my_args)

        contract_inst = _GetContractInstance(config_handler, contract_name)
        contract_inst = contract_inst.constructor(*my_args)
        contract_insts[contract_name] = contract_inst

    contract_detail_dict, contract_owner = _StartMultipleDeployToChain(config_handler, contract_insts)
    _DumpMultipleSmartContract(config_handler, contract_detail_dict, contract_owner)

    _ShowMultipleSmartContractDetail(contract_detail_dict, contract_owner)
    return contract_detail_dict


def deploy(config_path=CONFIG_PATH):

    config_handler = ConfigHandler(config_path)

    print('==== Compile smart contract ====')
    cmd = '(cd {0}; truffle compile)'.format(config_handler.get_chain_config('Deploy', 'truffle_path'))
    print('run command {0}'.format(cmd))
    os.system(cmd)

    # step 1
    step_one_info = _DeployMultipleSmartContractV0(config_handler, {
        'Register': {}
    })

    # step 2
    register_info = step_one_info['Register']
    infos = _DeployMultipleSmartContractV0(config_handler, {
        'KeysRecordStorageV0': {},
        'KeysRecord': {'Register': register_info},
        'ProvedCRUDStorageV0': {},
        'ProvedCRUD': {'Register': register_info},
        'EventEmitter': {},
        'FinaliseRecordStorageV0': {},
        'FinaliseRecord': {'Register': register_info},
        'ProvedDB': {'Register': register_info},
        'RecordHashStorageV0': {},
        'RecordHash': {'Register': register_info}
    })

    # step 3
    register = Register(config_path)
    register.set_multiple_register({
        'EventEmitter': infos['EventEmitter']['contractAddress'],
        'ProvedCRUDStorageInterface': infos['ProvedCRUDStorageV0']['contractAddress'],
        'KeysRecordStorageInterface': infos['KeysRecordStorageV0']['contractAddress'],
        'FinaliseRecordInterface': infos['FinaliseRecordStorageV0']['contractAddress'],
        'RecordHashStorageInterface': infos['RecordHashStorageV0']['contractAddress'],
        'KeysRecord': infos['KeysRecord']['contractAddress'],
        'ProvedCRUD': infos['ProvedCRUD']['contractAddress'],
        'FinaliseRecord': infos['FinaliseRecord']['contractAddress']
    })

    # step 4
    register.set_multiple_whitelist([infos['RecordHash']['contractAddress'],
                                     infos['ProvedDB']['contractAddress'],
                                     infos['KeysRecord']['contractAddress'],
                                     infos['ProvedCRUD']['contractAddress'],
                                     infos['FinaliseRecord']['contractAddress']])


def undeploy(config_path=CONFIG_PATH):
    ''' Actually, smart contract cannot undeploy, but I need an function to remove unused intermediate file'''
    config_handler = ConfigHandler(config_path)
    contract_names = config_handler.get_chain_config('Deploy', 'target_contract_name')
    for contract_name in contract_names.split(','):
        contract_path = os.path.join(config_handler.get_chain_config('Output', 'file_path'),
                                     '{0}.json'.format(contract_name))
        os.unlink(contract_path)


if __name__ == '__main__':
    deploy()
