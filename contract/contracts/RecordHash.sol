pragma solidity ^0.4.23;

contract RecordHash {
    mapping(bytes32 => bool) _record_map;
	event record_over(bytes32 finalise_hash);

	constructor() public {
	}

	function Record(bytes32 record_hash) public {
		_record_map[record_hash] = true;
		emit record_over(record_hash);
	}

	function Get(bytes32 record_hash) public view returns(bool) {
		return _record_map[record_hash];
	}
}
