pragma solidity 0.4.24;

import {Register} from "./Register.sol";
import {EventEmitter} from "./EventEmitter.sol";
import {RecordHashStorageInterface} from "./RecordHashStorageInterface.sol";

contract RecordHash {

	Register private _register;

	constructor(address register_address)
		public
	{
		_register = Register(register_address);
	}

	function GetEventEmitter()
		private
		view
		returns (EventEmitter) {
		return EventEmitter(_register.GetInst("EventEmitter"));
	}

	function GetStorageInterface()
		private
		view
		returns (RecordHashStorageInterface) {
		return RecordHashStorageInterface(_register.GetInst("RecordHashStorageInterface"));
	}

	function Record(bytes32 record_hash)
		public
	{
		GetStorageInterface().Set(record_hash);
		GetEventEmitter().emit_record_over(record_hash);
	}

	function Get(bytes32 record_hash)
		public
		view
		returns(bool)
	{
		return GetStorageInterface().Get(record_hash);
	}
}
