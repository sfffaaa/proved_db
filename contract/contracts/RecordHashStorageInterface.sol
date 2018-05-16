pragma solidity ^0.4.23;

contract RecordHashStorageInterface {
	function Set(bytes32 record_hash) public;
	function Get(bytes32 record_hash) public view returns (bool);
}
