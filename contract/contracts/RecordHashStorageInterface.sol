pragma solidity ^0.4.23;

interface RecordHashStorageInterface {
	function Set(bytes32 record_hash) external;
	function Get(bytes32 record_hash) external view returns (bool);
}
