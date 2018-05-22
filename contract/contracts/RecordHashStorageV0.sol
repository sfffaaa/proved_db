pragma solidity ^0.4.23;

contract RecordHashStorageV0 {
    mapping(bytes32 => bool) _record_map;

	function Set(bytes32 record_hash)
		external
	{
		_record_map[record_hash] = true;
	}

	function Get(bytes32 record_hash)
		external
		view
		returns (bool)
	{
		return _record_map[record_hash];
	}
}
