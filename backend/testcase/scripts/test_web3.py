from web3 import Web3, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.17;

contract ProvedDB {

    struct Entry {
        string action;
        bytes32 hash_value;
    }

    struct Record {
        bool is_exist;
        Entry[] entries;
    }

    mapping(string => Record) proved_map;
    string[] keys;
    mapping(string => uint) key_idxa1_map;

    function ProvedDB() public {
    }

    function strcmp(string s1, string s2) private pure returns (bool) {
        return keccak256(s1) == keccak256(s2);
    }

    function Create(string key, string val) public {
        assert(false == proved_map[key].is_exist);
        assert(0 == key_idxa1_map[key]);

        proved_map[key].is_exist = true;
        proved_map[key].entries.push(Entry("create", keccak256(val)));

        keys.push(key);
        key_idxa1_map[key] = keys.length;
    }

    function Retrieve(string key) public constant returns (bool exist, bytes32 data) {
        if (false == proved_map[key].is_exist) {
            assert(0 == key_idxa1_map[key]);
            return;
        }

        assert(0 != proved_map[key].entries.length);
        assert(0 != key_idxa1_map[key]);
        assert(strcmp(keys[key_idxa1_map[key] - 1], key));

        uint entry_len = proved_map[key].entries.length - 1;
        return (true, proved_map[key].entries[entry_len].hash_value);
    }

    function Update(string key, string val) public {
        assert(true == proved_map[key].is_exist);
        assert(0 != key_idxa1_map[key]);
        assert(strcmp(keys[key_idxa1_map[key] - 1], key));

        proved_map[key].entries.push(Entry("update", keccak256(val)));
    }

    function Delete(string key) public {
        if (false == proved_map[key].is_exist) {
            assert(0 == key_idxa1_map[key]);
            return;
        }
        proved_map[key].is_exist = false;
        delete proved_map[key].entries;

        assert(0 != key_idxa1_map[key]);
        assert(strcmp(keys[key_idxa1_map[key] - 1], key));
        uint remove_idx = key_idxa1_map[key] - 1;
        uint last_idx = keys.length - 1;
        if (remove_idx != last_idx) {
            string memory last_key = keys[last_idx];
            keys[remove_idx] = last_key;
            key_idxa1_map[last_key] = remove_idx + 1;
        }
        key_idxa1_map[key] = 0;
        keys.length--;
    }

    function CheckEntry(string key, string val) public constant returns (bool) {
        bool exist = false;
        bytes32 hash = '';
        (exist, hash) = Retrieve(key);

        if (false == exist) {
            if (strcmp('', val)) {
                return true;
            } else {
                return false;
            }
        }

        if (hash == keccak256(val)) {
            return true;
        }
        return false;
    }

    function GetKeysLength() public constant returns (uint) {
        return keys.length;
    }

    function GetKey(uint idx) public constant returns (string) {
        return keys[idx];
    }
}'''

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
contract_instance = w3.eth.contract(abi=contract_interface['abi'],
                                    address=contract_address,
                                    ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('test')
tx_hash = contract_instance.Create('a', 'b', transact={'from': w3.eth.accounts[0]})
print(tx_hash)
w3.miner.start(1)
time.sleep(10)
w3.miner.stop()
print('Contract value: {}'.format(contract_instance.Retrieve('a')))
print(tx_receipt)
data = contract_instance.Retrieve('a')
print(Web3.toHex(data[1]))
print(Web3.toHex(Web3.sha3(text='b')))
# contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
# print('Setting value to: Nihao')
# time.sleep(30)
# print('Contract value: {}'.format(contract_instance.greet()))
