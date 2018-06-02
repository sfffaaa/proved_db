pragma solidity 0.4.24;

import {KeysRecordStorageInterface} from "./KeysRecordStorageInterface.sol";
import {Register} from "./Register.sol";

contract KeysRecord {

	Register private _register;

	constructor(address register_address)
		public
	{
		_register = Register(register_address);
	}

	modifier onlyWhitelist() {
		_register.CheckWhiltelist(msg.sender);
		_;
	}

	function GetStorageInterface()
		private
		view
		returns (KeysRecordStorageInterface) {
		return KeysRecordStorageInterface(_register.GetInst('KeysRecordStorageInterface'));
	}

    function Create(string input_key)
		public
		onlyWhitelist
	{
		GetStorageInterface().PushKeyRecord(input_key);
	}

	function NonExistedCheck(string input_key)
		public
		view
		onlyWhitelist
	{
		bool success;
		uint idx;
		(success, idx) = GetStorageInterface().GetKeyIdx(input_key);
		assert(false == success);
	}

    function ExistedCheck(string input_key)
		public
		view
		onlyWhitelist
	{
		bool success;
		uint idx;
		(success, idx) = GetStorageInterface().GetKeyIdx(input_key);
		assert(true == success);
	}

    function Delete(string input_key)
		public
		onlyWhitelist
	{
		ExistedCheck(input_key);
		GetStorageInterface().DeleteKey(input_key);
	}

	function GetKeysLength()
		external
		view
		onlyWhitelist
		returns (uint) {
		return GetStorageInterface().GetKeysLength();
	}

	function GetKey(uint idx)
		external
		view
		onlyWhitelist
		returns (string) {
		return GetStorageInterface().GetKey(idx);
	}
}
