pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";
import {KeysRecord} from "./KeysRecord.sol";
import {ProvedCRUD} from "./ProvedCRUD.sol";


contract ProvedDB {

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
	event submit_hash(bytes32 finalise_hash);

	KeysRecord _keys_record;
	ProvedCRUD _proved_crud;

    constructor(uint submit_period, address keys_record_addr, address proved_crud_addr) public {
		_submit_period = submit_period;
		_keys_record = KeysRecord(keys_record_addr);
		_proved_crud = ProvedCRUD(proved_crud_addr);
    }


	function IsNeedSubmit() private view returns (bool) {
		return _submit_period <= _submit_list.length;
	}

	function Submit() private returns (bool) {
		uint hash = 0;
		for (uint i = 0; i < _submit_list.length; i++) {
			if (false == _submit_list[i].is_exist) {
				continue;
			}
			hash += uint(_submit_list[i].entry.hash_value);
		}
		bytes32 finalise_hash = keccak256(hash);
		_finalize_hash_map[finalise_hash].is_exist = true;
		_finalize_hash_map[finalise_hash].is_finalise = false;
		for (uint j = 0; j < _submit_list.length; j++) {
			if (false == _submit_list[j].is_exist) {
				continue;
			}
			_finalize_hash_map[finalise_hash].entries.push(_submit_list[j].entry);
		}

		_submit_list.length = 0;
		emit submit_hash(finalise_hash);
		return true;
	}

	function Finalise(bytes32 finalise_hash) public {
		assert(true == _finalize_hash_map[finalise_hash].is_exist);
		assert(false == _finalize_hash_map[finalise_hash].is_finalise);
		_finalize_hash_map[finalise_hash].is_finalise = true;
		for (uint i = 0; i < _finalize_hash_map[finalise_hash].entries.length; i++) {
			bytes32 kv_hash = _finalize_hash_map[finalise_hash].entries[i].hash_value;
			_kv_hash_to_finalised_hash_map[kv_hash] = finalise_hash;
		}
	}

	function GetFinalisedGroupEntriesLength(bytes32 kv_hash) public view returns (bool, uint) {
		if (0 == uint(_kv_hash_to_finalised_hash_map[kv_hash])) {
			return (false, 0);
		}
		bytes32 finalised_hash = _kv_hash_to_finalised_hash_map[kv_hash];
		assert(true == _finalize_hash_map[finalised_hash].is_exist);
		assert(0 != _finalize_hash_map[finalised_hash].entries.length);
		return (true, _finalize_hash_map[finalised_hash].entries.length);
	}

	function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
		bytes32 finalised_hash = _kv_hash_to_finalised_hash_map[kv_hash];
		assert(0 != uint(finalised_hash));
		assert(true == _finalize_hash_map[finalised_hash].is_exist);
		assert(0 != _finalize_hash_map[finalised_hash].entries.length);
		assert(idx < _finalize_hash_map[finalised_hash].entries.length);
		return _finalize_hash_map[finalised_hash].entries[idx].hash_value;
	}

	function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
		if (false == _finalize_hash_map[finalise_hash].is_exist) {
			return (false, false, 0);
		}
		if (false == _finalize_hash_map[finalise_hash].is_finalise) {
			return (true, false, _finalize_hash_map[finalise_hash].entries.length);
		}
		return (true, true, _finalize_hash_map[finalise_hash].entries.length);
	}

	function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
		assert(true == _finalize_hash_map[finalise_hash].is_exist);
		assert(index < _finalize_hash_map[finalise_hash].entries.length);
		return _finalize_hash_map[finalise_hash].entries[index].hash_value;
	}

    function Create(string input_key, string val) public {
		_proved_crud.Create(input_key, val);
		_keys_record.Create(input_key);

		bytes32 hash = input_key.hashPair(val);
		Entry memory entry = Entry("create", hash);


		_submit_list.push(SubmitEntry(true, entry));
		if (IsNeedSubmit()) {
			assert(true == Submit());
		}
    }

    function Retrieve(string input_key) public constant returns (bool, bytes32) {
		bool rexist;
		bytes32 rdata;
		(rexist, rdata) = _proved_crud.Retrieve(input_key);
		_keys_record.RetrieveCheck(input_key, rexist);
		return (rexist, rdata);
    }
    
    function Update(string input_key, string val) public {
		_proved_crud.Update(input_key, val);
		_keys_record.UpdateCheck(input_key);

		bytes32 hash = input_key.hashPair(val);
		Entry memory entry = Entry("update", hash);

		_submit_list.push(SubmitEntry(true, entry));
		if (IsNeedSubmit()) {
			assert(true == Submit());
		}
    }

    function Delete(string input_key) public {
		if (true == _proved_crud.Delete(input_key)) {
			_keys_record.Delete(input_key);
		}
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		return _proved_crud.CheckEntry(input_key, val);
	}

	function GetKeysLength() public constant returns (uint) {
		return _keys_record.GetKeysLength();
	}

	function GetKey(uint idx) public constant returns (string) {
		return _keys_record.GetKey(idx);
	}
}
