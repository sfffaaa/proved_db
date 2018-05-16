pragma solidity ^0.4.23;

import {EventEmitter} from "./EventEmitter.sol";

contract RecordHash {
    mapping(bytes32 => bool) _record_map;

	EventEmitter _event_emitter;
	constructor(address event_emitter_addr) public {
		_event_emitter = EventEmitter(event_emitter_addr);
	}

	function Record(bytes32 record_hash) public {
		_record_map[record_hash] = true;
		_event_emitter.emit_record_over(record_hash);
	}

	function Get(bytes32 record_hash) public view returns(bool) {
		return _record_map[record_hash];
	}
}
