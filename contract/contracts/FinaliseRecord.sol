pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";
import {EventEmitter} from "./EventEmitter.sol";
import {FinaliseRecordStorageInterface} from "./FinaliseRecordStorageInterface.sol";

contract FinaliseRecord {
	using Strings for string;

	struct Entry {
		string action;
		bytes32 hash_value;
	}
	
	struct SubmitEntry {
		bool is_exist;
		Entry entry;
	}

	struct FinaliseEntry {
		bool is_exist;
		bool is_finalise;
		Entry[] entries;
	}

	uint _submit_period;
	mapping(bytes32 => FinaliseEntry) _finalize_hash_map;

	//reverse find finalise group
	mapping(bytes32 => bytes32) _kv_hash_to_finalised_hash_map;

	SubmitEntry[] _submit_list;
	EventEmitter _event_emitter;
	FinaliseRecordStorageInterface _finalise_record_storage;

    constructor(uint submit_period,
				address event_emitter_addr,
				address finalise_record_storage_addr)
		public {
		_submit_period = submit_period;
		_event_emitter = EventEmitter(event_emitter_addr);
		_finalise_record_storage = FinaliseRecordStorageInterface(finalise_record_storage_addr);
    }

	function IsNeedSubmit() private view returns (bool) {
		return _submit_period <= _finalise_record_storage.GetSubmitEntriesLength();
	}

	function Submit() private returns (bool) {
		uint hash = 0;
		bool is_exist;
		string memory action;
		bytes32 hash_data;

		for (uint i = 0; i < _finalise_record_storage.GetSubmitEntriesLength(); i++) {
			(is_exist, action, hash_data) = _finalise_record_storage.GetSubmitEntry(i);
			if (false == is_exist) {
				continue;
			}
			hash += uint(hash_data);
		}
		bytes32 finalise_hash = keccak256(hash);
		_finalise_record_storage.UpdateFinaliseHashMap(finalise_hash, true, false);
		for (i = 0; i < _finalise_record_storage.GetSubmitEntriesLength(); i++) {
			(is_exist, action, hash_data) = _finalise_record_storage.GetSubmitEntry(i);
			if (false == is_exist) {
				continue;
			}
			_finalise_record_storage.PushFinaliseHashMap(finalise_hash, action, hash_data);
		}

		_finalise_record_storage.ResetSubmitEntries();
		_event_emitter.emit_submit_hash(finalise_hash);
		return true;
	}

	function Finalise(bytes32 finalise_hash) public {
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = _finalise_record_storage.GetFinaliseHashMap(finalise_hash);
		assert(true == is_exist);
		assert(false == is_finalise);
		_finalise_record_storage.UpdateFinaliseHashMap(finalise_hash, true, true);

		string memory action;
		bytes32 kv_hash;
		for (uint i = 0; i < length; i++) {
			(action, kv_hash) = _finalise_record_storage.GetFinaliseHashEntry(finalise_hash, i);
			_finalise_record_storage.SetKV2FinaliseHashMap(kv_hash, finalise_hash);
		}
	}

	function GetFinalisedGroupEntriesLength(bytes32 kv_hash)
		public
		view
		returns (bool, uint) {
		bytes32 finalise_hash = _finalise_record_storage.GetKV2FinalisedHashMap(kv_hash);
		if (0 == uint(finalise_hash)) {
			return (false, 0);
		}
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = _finalise_record_storage.GetFinaliseHashMap(finalise_hash);

		assert(true == is_exist);
		assert(0 != length);
		return (true, length);
	}

	function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
		bytes32 finalise_hash = _finalise_record_storage.GetKV2FinalisedHashMap(kv_hash);
		assert(0 != uint(finalise_hash));

		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = _finalise_record_storage.GetFinaliseHashMap(finalise_hash);
		assert(true == is_exist);
		assert(0 != length);
		assert(idx < length);

		string memory action;
		bytes32 hash_value;
		(action, hash_value) = _finalise_record_storage.GetFinaliseHashEntry(finalise_hash, idx);
		return hash_value;
	}

	function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = _finalise_record_storage.GetFinaliseHashMap(finalise_hash);

		if (false == is_exist) {
			return (false, false, 0);
		} else if (false == is_finalise) {
			return (true, false, length);
		}
		return (true, true, length);
	}

	function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = _finalise_record_storage.GetFinaliseHashMap(finalise_hash);

		assert(true == is_exist);
		assert(index < length);
		string memory action;
		bytes32 hash_value;
		(action, hash_value) = _finalise_record_storage.GetFinaliseHashEntry(finalise_hash, index);
		return hash_value;
	}

	function CreateUpdateBaseAction(string input_key, string val, string action_type)
		private
		returns (bool, bytes32) {
		bytes32 hash = input_key.hashPair(val);
		_finalise_record_storage.PushSubmitEntry(action_type, hash);
		if (IsNeedSubmit()) {
			require(true == Submit());
		}
	}

    function Create(string input_key, string val) public {
		CreateUpdateBaseAction(input_key, val, "create");
    }

    function Update(string input_key, string val) public {
		CreateUpdateBaseAction(input_key, val, "update");
    }
}
