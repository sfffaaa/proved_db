pragma solidity ^0.4.23;

import {KeysRecordStorageInterface} from "./KeysRecordStorageInterface.sol";
import {Register} from "./Register.sol";

contract KeysRecord {

	Register _register;

	constructor(address register_address)
		public
	{
		_register = Register(register_address);
	}

	function GetStorageInterface()
		private
		view
		returns (KeysRecordStorageInterface) {
		return KeysRecordStorageInterface(_register.GetInst('KeysRecordStorageInterface'));
	}

    function Create(string input_key) public {
		GetStorageInterface().PushKeyRecord(input_key);
	}

	function NonExistedCheck(string input_key) public view {
		bool success;
		uint idx;
		(success, idx) = GetStorageInterface().GetKeyIdx(input_key);
		assert(false == success);
	}

    function ExistedCheck(string input_key) public view {
		bool success;
		uint idx;
		(success, idx) = GetStorageInterface().GetKeyIdx(input_key);
		assert(true == success);
	}

    function Delete(string input_key) public {
		ExistedCheck(input_key);
		GetStorageInterface().DeleteKey(input_key);
	}

	function GetKeysLength() external view returns (uint) {
		return GetStorageInterface().GetKeysLength();
	}

	function GetKey(uint idx) external view returns (string) {
		return GetStorageInterface().GetKey(idx);
	}
}
