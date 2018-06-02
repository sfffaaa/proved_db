pragma solidity 0.4.24;

import {Register} from "./Register.sol";

contract ProvedCRUDStorageV0 {
	struct Entry {
		string action;
		bytes32 hash_value;
	}
	struct Record {
		bool is_exist;
		Entry[] entries;
	}

    mapping(string => Record) private _kv_hash_map;

	Register private _register;
	constructor(address register_addr)
		public
	{
		_register = Register(register_addr);
	}

	modifier onlyWhitelist() {
		_register.CheckWhiltelist(msg.sender);
		_;
	}

	function Create(string input_key, bytes32 hash)
		public
		onlyWhitelist
	{
		assert(false == _kv_hash_map[input_key].is_exist);

		Entry memory entry = Entry("create", hash);
		_kv_hash_map[input_key].is_exist = true;
		_kv_hash_map[input_key].entries.push(entry);
	}

	function Update(string input_key, bytes32 hash)
		public
		onlyWhitelist
	{
		assert(true == _kv_hash_map[input_key].is_exist);

		Entry memory entry = Entry("update", hash);
		_kv_hash_map[input_key].entries.push(entry);
    }

    function Delete(string input_key)
		public
		onlyWhitelist
		returns (bool)	
	{
		if (false == _kv_hash_map[input_key].is_exist) {
			return false;
		}
		_kv_hash_map[input_key].is_exist = false;
		_kv_hash_map[input_key].entries.push(Entry("delete", keccak256("")));
		return true;
	}

	function Retrieve(string input_key)
		public
		view
		onlyWhitelist
		returns (bool exist, bytes32 data)
	{
		if (false == _kv_hash_map[input_key].is_exist) {
			return (false, 0);
		}

		assert(0 != _kv_hash_map[input_key].entries.length);

		uint entry_len = _kv_hash_map[input_key].entries.length - 1;
		return (true, _kv_hash_map[input_key].entries[entry_len].hash_value);
    }
}
