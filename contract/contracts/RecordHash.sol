pragma solidity ^0.4.23;

import {EventEmitter} from "./EventEmitter.sol";
// [TODO] Wait for registry contract
import {RecordHashStorageInterface} from "./RecordHashStorageInterface.sol";

contract RecordHash {

	EventEmitter _event_emitter;
	RecordHashStorageInterface _record_hash_stroage;

	constructor(address event_emitter_addr,
				address record_hash_storage_addr)
		public
	{
		_event_emitter = EventEmitter(event_emitter_addr);
		_record_hash_stroage = RecordHashStorageInterface(record_hash_storage_addr);
	}

	function Record(bytes32 record_hash)
		public
	{
		_record_hash_stroage.Set(record_hash);
		_event_emitter.emit_record_over(record_hash);
	}

	function Get(bytes32 record_hash)
		public
		view
		returns(bool)
	{
		return _record_hash_stroage.Get(record_hash);
	}
}
