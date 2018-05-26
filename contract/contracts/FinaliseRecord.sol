pragma solidity ^0.4.23;

import {Strings} from "./Strings.sol";
import {Register} from "./Register.sol";
import {EventEmitter} from "./EventEmitter.sol";
import {FinaliseRecordStorageInterface} from "./FinaliseRecordStorageInterface.sol";

contract FinaliseRecord {
	using Strings for string;

	uint _submit_period;

	Register _register;

	constructor(uint submit_period,
				address register_address)
		public {
		_submit_period = submit_period;
		_register = Register(register_address);
	}

	function GetEventEmitter()
		private
		view
		returns (EventEmitter) {
		return EventEmitter(_register.GetInst("EventEmitter"));
	}

	function GetStorageInterface()
		private
		view
		returns (FinaliseRecordStorageInterface) {
		return FinaliseRecordStorageInterface(_register.GetInst("FinaliseRecordInterface"));
	}

	function IsNeedSubmit() private view returns (bool) {
		return _submit_period <= GetStorageInterface().GetSubmitEntriesLength();
	}

	function Submit() private returns (bool) {
		uint hash = 0;
		bool is_exist;
		string memory action;
		bytes32 hash_data;

		FinaliseRecordStorageInterface inst = GetStorageInterface();

		for (uint i = 0; i < inst.GetSubmitEntriesLength(); i++) {
			(is_exist, action, hash_data) = inst.GetSubmitEntry(i);
			if (false == is_exist) {
				continue;
			}
			hash += uint(hash_data);
		}
		bytes32 finalise_hash = keccak256(hash);
		inst.UpdateFinaliseHashMap(finalise_hash, true, false);
		for (i = 0; i < inst.GetSubmitEntriesLength(); i++) {
			(is_exist, action, hash_data) = inst.GetSubmitEntry(i);
			if (false == is_exist) {
				continue;
			}
			inst.PushFinaliseHashMap(finalise_hash, action, hash_data);
		}

		inst.ResetSubmitEntries();
		GetEventEmitter().emit_submit_hash(finalise_hash);
		return true;
	}

	function Finalise(bytes32 finalise_hash) public {
		bool is_exist;
		bool is_finalise;
		uint length;

		FinaliseRecordStorageInterface inst = GetStorageInterface();

		(is_exist, is_finalise, length) = inst.GetFinaliseHashMap(finalise_hash);
		assert(true == is_exist);
		assert(false == is_finalise);
		inst.UpdateFinaliseHashMap(finalise_hash, true, true);

		string memory action;
		bytes32 kv_hash;
		for (uint i = 0; i < length; i++) {
			(action, kv_hash) = inst.GetFinaliseHashEntry(finalise_hash, i);
			inst.SetKV2FinaliseHashMap(kv_hash, finalise_hash);
		}
	}

	function GetFinalisedGroupEntriesLength(bytes32 kv_hash)
		public
		view
		returns (bool, uint) {
		FinaliseRecordStorageInterface inst = GetStorageInterface();
		bytes32 finalise_hash = inst.GetKV2FinalisedHashMap(kv_hash);
		if (0 == uint(finalise_hash)) {
			return (false, 0);
		}
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = inst.GetFinaliseHashMap(finalise_hash);

		assert(true == is_exist);
		assert(0 != length);
		return (true, length);
	}

	function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
		FinaliseRecordStorageInterface inst = GetStorageInterface();
		bytes32 finalise_hash = inst.GetKV2FinalisedHashMap(kv_hash);
		assert(0 != uint(finalise_hash));

		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = inst.GetFinaliseHashMap(finalise_hash);
		assert(true == is_exist);
		assert(0 != length);
		assert(idx < length);

		string memory action;
		bytes32 hash_value;
		(action, hash_value) = inst.GetFinaliseHashEntry(finalise_hash, idx);
		return hash_value;
	}

	function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = GetStorageInterface().GetFinaliseHashMap(finalise_hash);

		if (false == is_exist) {
			return (false, false, 0);
		} else if (false == is_finalise) {
			return (true, false, length);
		}
		return (true, true, length);
	}

	function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
		FinaliseRecordStorageInterface inst = GetStorageInterface();
		bool is_exist;
		bool is_finalise;
		uint length;

		(is_exist, is_finalise, length) = inst.GetFinaliseHashMap(finalise_hash);

		assert(true == is_exist);
		assert(index < length);
		string memory action;
		bytes32 hash_value;
		(action, hash_value) = inst.GetFinaliseHashEntry(finalise_hash, index);
		return hash_value;
	}

	function CreateUpdateBaseAction(string input_key, string val, string action_type)
		private
		returns (bool, bytes32) {
		bytes32 hash = input_key.hashPair(val);
		GetStorageInterface().PushSubmitEntry(action_type, hash);
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
