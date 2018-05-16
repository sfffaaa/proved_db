pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";

contract ProvedCRUD {
	using Strings for string;

	struct Entry {
		string action;
		bytes32 hash_value;
	}
	struct Record {
		bool is_exist;
		Entry[] entries;
	}

    mapping(string => Record) _kv_hash_map;
	function Create(string input_key, string val) public {
		assert(false == _kv_hash_map[input_key].is_exist);

		bytes32 hash = input_key.hashPair(val);
		Entry memory entry = Entry("create", hash);
		_kv_hash_map[input_key].is_exist = true;
		_kv_hash_map[input_key].entries.push(entry);
    }
	function Retrieve(string input_key) public constant returns (bool exist, bytes32 data) {
		if (false == _kv_hash_map[input_key].is_exist) {
			return (false, 0);
		}

		assert(0 != _kv_hash_map[input_key].entries.length);

		uint entry_len = _kv_hash_map[input_key].entries.length - 1;
		return (true, _kv_hash_map[input_key].entries[entry_len].hash_value);
    }

    function Update(string input_key, string val) public {
		assert(true == _kv_hash_map[input_key].is_exist);

		bytes32 hash = input_key.hashPair(val);
		Entry memory entry = Entry("update", hash);
		_kv_hash_map[input_key].entries.push(entry);
    }

    function Delete(string input_key) public returns (bool) {
		if (false == _kv_hash_map[input_key].is_exist) {
			return false;
		}
		_kv_hash_map[input_key].is_exist = false;
		_kv_hash_map[input_key].entries.push(Entry("delete", keccak256("")));
		return true;
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		bool exist = false;
		bytes32 hash = '';
		(exist, hash) = Retrieve(input_key);

		if (false == exist) {
			if (true == val.compareTo('')) {
				return true;
			} else {
				return false;
			}
		}
		if (hash == input_key.hashPair(val)) {
			return true;
		}
		return false;
	}
}
