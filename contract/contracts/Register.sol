pragma solidity 0.4.24;

import {Whitelistable} from "./Whitelistable.sol";

contract Register is Whitelistable {
	mapping(string => address) _register_map;

	function GetInst(string name)
		public
		view
		onlyWhitelist
		returns (address) {
		return _register_map[name];
	}

	function SetInst(string name, address target_address)
		public
		onlyOwner
	{
		_register_map[name] = target_address;
	}
}
