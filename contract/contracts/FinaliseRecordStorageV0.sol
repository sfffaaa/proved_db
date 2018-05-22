pragma solidity ^0.4.23;

contract FinaliseRecordStorageV0 {

	struct Entry {
		string action;
		bytes32 hash_value;
	}
	struct SubmitEntry {
		bool is_exist;
		Entry entry;
	}
	SubmitEntry[] _submit_list;

	struct FinaliseEntry {
		bool is_exist;
		bool is_finalise;
		Entry[] entries;
	}

	mapping(bytes32 => FinaliseEntry) _finalize_hash_map;

	//reverse find finalise group
	mapping(bytes32 => bytes32) _kv_hash_to_finalised_hash_map;
	
	function GetSubmitEntriesLength()
		external
		view
		returns (uint) {
		return _submit_list.length;
	}
	function ResetSubmitEntries() external {
		_submit_list.length = 0;
	}
	function PushSubmitEntry(string action, bytes32 hash_value) external {
		Entry memory entry = Entry(action, hash_value);
		_submit_list.push(SubmitEntry(true, entry));
	}
	function GetSubmitEntry(uint idx)
		external
		view
		returns (bool, string, bytes32) {
		SubmitEntry memory data = _submit_list[idx];
		return (data.is_exist, data.entry.action, data.entry.hash_value);
	}
	function UpdateFinaliseHashMap(bytes32 key, bool existed, bool finalised) external {
		_finalize_hash_map[key].is_exist = existed;
		_finalize_hash_map[key].is_finalise = finalised;
	}
	function PushFinaliseHashMap(bytes32 key, string action, bytes32 hash_value) external {
		_finalize_hash_map[key].entries.push(Entry(action, hash_value));
	}
	function GetFinaliseHashMap(bytes32 key)
		external
		view
		returns (bool, bool, uint) {
		return (_finalize_hash_map[key].is_exist,
			    _finalize_hash_map[key].is_finalise,
			    _finalize_hash_map[key].entries.length);
	}
	function GetFinaliseHashEntry(bytes32 key, uint idx)
		external
		view
		returns (string, bytes32) {
		return (_finalize_hash_map[key].entries[idx].action,
				_finalize_hash_map[key].entries[idx].hash_value);
	}
	function GetKV2FinalisedHashMap(bytes32 key)
		external
		view
		returns (bytes32) {
		return _kv_hash_to_finalised_hash_map[key];
	}
	function SetKV2FinaliseHashMap(bytes32 key, bytes32 val) external {
		_kv_hash_to_finalised_hash_map[key] = val;
	}
}
