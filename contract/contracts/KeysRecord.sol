pragma solidity ^0.4.23;

import {KeysRecordStorageV0} from "./KeysRecordStorageV0.sol";

contract KeysRecord {

	KeysRecordStorageV0 _keys_record_stroage;

	constructor(address keys_record_storage_addr)
		public
	{
		_keys_record_stroage = KeysRecordStorageV0(keys_record_storage_addr);
	}

    function Create(string input_key) public {
		_keys_record_stroage.PushKeyRecord(input_key);
	}

	function NonExistedCheck(string input_key) public view {
		bool success;
		uint idx;
		(success, idx) = _keys_record_stroage.GetKeyIdx(input_key);
		assert(false == success);
	}
    function ExistedCheck(string input_key) public view {
		bool success;
		uint idx;
		(success, idx) = _keys_record_stroage.GetKeyIdx(input_key);
		assert(true == success);
	}
    function Delete(string input_key) public {
		ExistedCheck(input_key);
		_keys_record_stroage.DeleteKey(input_key);
	}

	function GetKeysLength() external view returns (uint) {
		return _keys_record_stroage.GetKeysLength();
	}

	function GetKey(uint idx) external view returns (string) {
		return _keys_record_stroage.GetKey(idx);
	}
}
