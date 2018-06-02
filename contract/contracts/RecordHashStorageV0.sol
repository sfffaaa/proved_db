pragma solidity 0.4.24;

import {Register} from "./Register.sol";

contract RecordHashStorageV0 {
    mapping(bytes32 => bool) private _record_map;

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

	function Set(bytes32 record_hash)
		external
		onlyWhitelist
	{
		_record_map[record_hash] = true;
	}

	function Get(bytes32 record_hash)
		external
		view
		onlyWhitelist
		returns (bool)
	{
		return _record_map[record_hash];
	}
}
