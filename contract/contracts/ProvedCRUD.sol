pragma solidity ^0.4.23;

import {Strings} from "./Strings.sol";
import {Register} from "./Register.sol";
import {ProvedCRUDStorageInterface} from "./ProvedCRUDStorageInterface.sol";

contract ProvedCRUD {
	using Strings for string;

	Register _register;
	constructor(address register_addr)
		public
	{
		_register = Register(register_addr);
	}

	modifier onlyWhitelist() {
		_register.CheckWhiltelist(msg.sender);
		_;
	}

	function GetStorageInterface()
		private
		view
		returns (ProvedCRUDStorageInterface) {
		return ProvedCRUDStorageInterface(_register.GetInst("ProvedCRUDStorageInterface"));
	}

	function Create(string input_key, string val)
		public
		onlyWhitelist
	{
		bytes32 hash = input_key.hashPair(val);
		GetStorageInterface().Create(input_key, hash);
    }
	function Retrieve(string input_key)
		public
		constant
		onlyWhitelist
		returns (bool exist, bytes32 data) {
		return GetStorageInterface().Retrieve(input_key);
    }

    function Update(string input_key, string val)
		public
		onlyWhitelist
	{
		bytes32 hash = input_key.hashPair(val);
		GetStorageInterface().Update(input_key, hash);
    }

    function Delete(string input_key)
		public
		onlyWhitelist
		returns (bool)
	{
		return GetStorageInterface().Delete(input_key);
	}

	function CheckEntry(string input_key, string val)
		public
		constant
		onlyWhitelist
		returns (bool)
	{
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
