pragma solidity ^0.4.23;

import {Register} from "./Register.sol";

contract EventEmitter {

	Register _register;

	event submit_hash(bytes32 finalise_hash);
	event record_over(bytes32 finalise_hash);

	constructor(address register_address)
		public
	{
		_register = Register(register_address);
	}

	modifier onlyWhitelist() {
		_register.CheckWhiltelist(msg.sender);
		_;
	}

	function emit_submit_hash(bytes32 finalise_hash)
		public
		onlyWhitelist
	{
		emit submit_hash(finalise_hash);
	}

	function emit_record_over(bytes32 finalise_hash)
		public
		onlyWhitelist
	{
		emit record_over(finalise_hash);
	}
}
