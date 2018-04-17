from web3 import Web3, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.17;

contract ProvedDB {

    struct Entry {
        string action;
        string hash_value;
    }

    struct Record {
        bool is_exist;
        Entry[] entries;
    }

    mapping(string => Record) proved_map;

    function ProvedDB() public {
    }

    function Create(string id, string hash) public {
        assert(false == proved_map[id].is_exist);
        proved_map[id].is_exist = true;
        proved_map[id].entries.push(Entry("create", hash));
    }

//      function CheckEntry(string id, string hash) public constant returns (bool result) {
//      }
//
//      function GetCheckSegment(int idx) public constant returns (bool continued, string fragment) {
//      }

    function Retrieve(string id) public constant returns (bool exist, string data) {
        if (false == proved_map[id].is_exist) {
            return;
        }

        assert(0 != proved_map[id].entries.length);

        uint entry_len = proved_map[id].entries.length - 1;
        exist = true;
        data = proved_map[id].entries[entry_len].hash_value;
    }

    function Update(string id, string hash) public {
        assert(true == proved_map[id].is_exist);
        proved_map[id].entries.push(Entry("update", hash));
    }

    function Delete(string id) public {
        if (false == proved_map[id].is_exist) {
            return;
        }
        proved_map[id].is_exist = false;
        delete proved_map[id].entries;
    }
}
'''

compiled_sol = compile_source(contract_source_code)  # Compiled source code
contract_interface = compiled_sol['<stdin>:ProvedDB']

# web3.py instance
w3 = Web3(IPCProvider('/Users/jaypan/private-eth/test1/node1/geth.ipc'))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 10010000})
w3.miner.start(1)

# Get tx receipt to get contract address
print('deploy')
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
import time
time.sleep(30)
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
w3.miner.stop()

# Contract instance in concise mode
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('test')
tx_hash = contract_instance.Create('aaa', '1', transact={'from': w3.eth.accounts[0]})
print(tx_hash)
w3.miner.start(1)
time.sleep(30)
w3.miner.stop()
print('Contract value: {}'.format(contract_instance.Retrieve('aaa')))
print(tx_receipt)
# contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
# print('Setting value to: Nihao')
# time.sleep(30)
# print('Contract value: {}'.format(contract_instance.greet()))
