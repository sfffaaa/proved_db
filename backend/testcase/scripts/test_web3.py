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

    struct SubmitEntry {
        bool is_exist;
        Entry entry;
    }

    struct FinaliseEntry {
        bool is_exist;
        bool is_finalise;
        Entry[] entries;
    }

    struct Record {
        bool is_exist;
        Entry[] entries;
    }

    struct ReverseRecord {
        bool is_exist;
        string key;
        uint idx;
    }

    mapping(string => Record) _kv_hash_map;

    string[] _keys;
    mapping(string => uint) _key_idxa1_map;

    mapping(bytes32 => ReverseRecord) _kv_hash_reverse_map;

    //[TODO] let owner to change this
    uint _submit_period;
    mapping(bytes32 => FinaliseEntry) _finalize_hash_map;

    //reverse find finalise group
    mapping(bytes32 => bytes32) _kv_hash_to_finalised_hash_map;

    SubmitEntry[] _submit_list;
    event submit_hash(bytes32 finalise_hash);

    //[TODO] but right now I haven't upgrade my solc
    //function constuctor(uint submit_period) public {
    function ProvedDB() public {
        _submit_period = 2;
    }

    function strcmp(string target_str, string check_str) private pure returns (bool) {
        return keccak256(target_str) != keccak256(check_str);
    }

    function UpdateHashReverseMap(string input_key, bytes32 kv_hash) private {
        assert(false == _kv_hash_reverse_map[kv_hash].is_exist);
        _kv_hash_reverse_map[kv_hash] = ReverseRecord(true,
                                                   input_key,
                                                   _kv_hash_map[input_key].entries.length - 1);
    }

    function IsNeedSubmit() private view returns (bool) {
        return _submit_period <= _submit_list.length;
    }

    function Submit() private returns (bool) {
        uint hash = 0;
        for (uint i = 0; i < _submit_list.length; i++) {
            if (false == _submit_list[i].is_exist) {
                continue;
            }
            hash += uint(_submit_list[i].entry.hash_value);
        }
        bytes32 finalise_hash = keccak256(hash);
        _finalize_hash_map[finalise_hash].is_exist = true;
        _finalize_hash_map[finalise_hash].is_finalise = false;
        for (uint j = 0; j < _submit_list.length; j++) {
            if (false == _submit_list[j].is_exist) {
                continue;
            }
            _finalize_hash_map[finalise_hash].entries.push(_submit_list[j].entry);
        }

        _submit_list.length = 0;
        submit_hash(finalise_hash);
        return true;
    }

    function Finalise(bytes32 finalise_hash) public {
        assert(true == _finalize_hash_map[finalise_hash].is_exist);
        assert(false == _finalize_hash_map[finalise_hash].is_finalise);
        _finalize_hash_map[finalise_hash].is_finalise = true;
        for (uint i = 0; i < _finalize_hash_map[finalise_hash].entries.length; i++) {
            bytes32 kv_hash = _finalize_hash_map[finalise_hash].entries[i].hash_value;
            _kv_hash_to_finalised_hash_map[kv_hash] = finalise_hash;
        }
    }

    function GetFinalisedGroupEntriesLength(bytes32 kv_hash) public view returns (bool, uint) {
        if (0 == uint(_kv_hash_to_finalised_hash_map[kv_hash])) {
            return (false, 0);
        }
        bytes32 finalised_hash = _kv_hash_to_finalised_hash_map[kv_hash];
        assert(true == _finalize_hash_map[finalised_hash].is_exist);
        assert(0 != _finalize_hash_map[finalised_hash].entries.length);
        return (true, _finalize_hash_map[finalised_hash].entries.length);
    }

    function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
        bytes32 finalised_hash = _kv_hash_to_finalised_hash_map[kv_hash];
        assert(0 != uint(finalised_hash));
        assert(true == _finalize_hash_map[finalised_hash].is_exist);
        assert(0 != _finalize_hash_map[finalised_hash].entries.length);
        assert(idx < _finalize_hash_map[finalised_hash].entries.length);
        return _finalize_hash_map[finalised_hash].entries[idx].hash_value;
    }

    function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
        if (false == _finalize_hash_map[finalise_hash].is_exist) {
            return (false, false, 0);
        }
        if (false == _finalize_hash_map[finalise_hash].is_finalise) {
            return (true, false, _finalize_hash_map[finalise_hash].entries.length);
        }
        return (true, true, _finalize_hash_map[finalise_hash].entries.length);
    }

    function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
        assert(true == _finalize_hash_map[finalise_hash].is_exist);
        assert(index < _finalize_hash_map[finalise_hash].entries.length);
        return _finalize_hash_map[finalise_hash].entries[index].hash_value;
    }

    function Create(string input_key, string val) public {
        assert(false == _kv_hash_map[input_key].is_exist);
        assert(0 == _key_idxa1_map[input_key]);

        bytes32 hash = keccak256(val);
        Entry memory entry = Entry("create", hash);
        _kv_hash_map[input_key].is_exist = true;
        _kv_hash_map[input_key].entries.push(entry);
        UpdateHashReverseMap(input_key, hash);
        assert(true == CheckHash(hash));

        _keys.push(input_key);
        _key_idxa1_map[input_key] = _keys.length;

        _submit_list.push(SubmitEntry(true, entry));
        if (IsNeedSubmit()) {
            assert(true == Submit());
        }
    }

    function Retrieve(string input_key) public constant returns (bool exist, bytes32 data) {
        if (false == _kv_hash_map[input_key].is_exist) {
            assert(0 == _key_idxa1_map[input_key]);
            return;
        }

        assert(0 != _kv_hash_map[input_key].entries.length);
        assert(0 != _key_idxa1_map[input_key]);
        assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));

        uint entry_len = _kv_hash_map[input_key].entries.length - 1;
        return (true, _kv_hash_map[input_key].entries[entry_len].hash_value);
    }

    function Update(string input_key, string val) public {
        assert(true == _kv_hash_map[input_key].is_exist);
        assert(0 != _key_idxa1_map[input_key]);
        assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));


        bytes32 hash = keccak256(val);
        Entry memory entry = Entry("update", hash);
        _kv_hash_map[input_key].entries.push(entry);

        UpdateHashReverseMap(input_key, hash);
        assert(true == CheckHash(hash));

        _submit_list.push(SubmitEntry(true, entry));
        if (IsNeedSubmit()) {
            assert(true == Submit());
        }
    }

    function Delete(string input_key) public {
        if (false == _kv_hash_map[input_key].is_exist) {
            return;
        }
        _kv_hash_map[input_key].is_exist = false;
        _kv_hash_map[input_key].entries.push(Entry("delete", keccak256("")));

        // remove key
        assert(0 != _key_idxa1_map[input_key]);
        assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));
        uint remove_idx = _key_idxa1_map[input_key] - 1;
        uint last_idx = _keys.length - 1;
        if (remove_idx != last_idx) {
            string memory last_key = _keys[last_idx];
            _keys[remove_idx] = last_key;
            _key_idxa1_map[last_key] = remove_idx + 1;
        }
        _key_idxa1_map[input_key] = 0;
        _keys.length--;
    }

    function CheckHash(bytes32 kv_hash) public view returns (bool) {
        ReverseRecord storage reverse_record = _kv_hash_reverse_map[kv_hash];
        if (true != reverse_record.is_exist) {
            return false;
        }
        Record storage record = _kv_hash_map[reverse_record.key];
        if (kv_hash != record.entries[reverse_record.idx].hash_value) {
            return false;
        }
        return true;
    }

    function CheckEntry(string input_key, string val) public constant returns (bool) {
        bool exist = false;
        bytes32 hash = '';
        (exist, hash) = Retrieve(input_key);

        if (false == exist) {
            if (!strcmp('', val)) {
                return true;
            } else {
                return false;
            }
        }

        if (hash == keccak256(val)) {
            return true;
        }
        assert(true == CheckHash(hash));
        return false;
    }

    function GetKeysLength() public constant returns (uint) {
        return _keys.length;
    }

    function GetKey(uint idx) public constant returns (string) {
        return _keys[idx];
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
contract_instance = w3.eth.contract(abi=contract_interface['abi'],
                                    address=contract_address,
                                    ContractFactoryClass=ConciseContract)

# Getters + Setters for web3.eth.contract object
print('test')
tx_hash = contract_instance.Create('a', 'b', transact={'from': w3.eth.accounts[0]})
tx_hash = contract_instance.Create('c', 'd', transact={'from': w3.eth.accounts[0]})
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
