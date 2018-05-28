pragma solidity ^0.4.23;

import {Ownable} from "./Ownable.sol";

contract Whitelistable is Ownable {

	mapping (address => bool) _whitelist_map;
	event WhitelistAdded(address indexed whitelist_address);

	constructor() public {
		_whitelist_map[msg.sender] = true;
	}

	function SetWhitelist(address addr)
		onlyOwner
		public
	{
		_whitelist_map[addr] = true;
		emit WhitelistAdded(addr);
	}
	
	modifier onlyFalse() {
		require(false);
		_;
	}

	modifier onlyWhitelist() {
		require(owner == msg.sender || true == _whitelist_map[msg.sender]);
		_;
	}

	function CheckWhiltelist(address check_address)
		public
		view
	{
		require(owner == check_address ||
				true == _whitelist_map[check_address]);
	}
}
