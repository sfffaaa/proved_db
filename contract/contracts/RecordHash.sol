pragma solidity ^0.4.17;

contract RecordHash {
    mapping(bytes32 => bool) _record_map;
	event record_over(bytes32 finalise_hash);

	function RecordHash() public {
	}

	function Record(bytes32 record_hash) public {
		_record_map[record_hash] = true;
		record_over(record_hash);
	}
}
