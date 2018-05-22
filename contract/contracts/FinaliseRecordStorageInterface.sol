pragma solidity ^0.4.23;

interface FinaliseRecordStorageInterface {

	function GetSubmitEntriesLength() external view returns (uint);
	function ResetSubmitEntries() external;
	function PushSubmitEntry(string action, bytes32 hash_value) external;
	function GetSubmitEntry(uint idx) external view returns (bool, string, bytes32);
	function UpdateFinaliseHashMap(bytes32 key, bool existed, bool finalised) external;
	function PushFinaliseHashMap(bytes32 key, string action, bytes32 hash_value) external;
	function GetFinaliseHashMap(bytes32 key) external view returns (bool, bool, uint);
	function GetFinaliseHashEntry(bytes32 key, uint idx) external view returns (string, bytes32);
	function GetKV2FinalisedHashMap(bytes32 key) external view returns (bytes32);
	function SetKV2FinaliseHashMap(bytes32 key, bytes32 val) external;
}
