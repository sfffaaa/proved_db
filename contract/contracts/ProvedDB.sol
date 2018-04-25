pragma solidity ^0.4.17;

contract ProvedDB {

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

	struct Record {
		bool is_exist;
		Entry[] entries;
	}

	struct ReverseRecord {
		bool is_exist;
		string key;
		uint idx;
	}

    mapping(string => Record) _proved_map;

	string[] _keys;
	mapping(string => uint) _key_idxa1_map;

	mapping(bytes32 => ReverseRecord) _hash_reverse_map;

	//[TODO] let owner to change this
	uint _submit_period;
	mapping(bytes32 => FinaliseEntry) _finalize_map;

	SubmitEntry[] _submit_list;
	event submit_hash(bytes32 hash);

	//[TODO] Need to check...
    //function constuctor(uint submit_period) public {
    function ProvedDB() public {
		_submit_period = 2;
    }

	function strcmp(string target_str, string check_str) private pure returns (bool) {
		return keccak256(target_str) != keccak256(check_str);
	}

	function UpdateHashReverseMap(string input_key, bytes32 hash) private {
		assert(false == _hash_reverse_map[hash].is_exist);
		_hash_reverse_map[hash] = ReverseRecord(true,
											    input_key,
												_proved_map[input_key].entries.length - 1);
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
		bytes32 final_hash = keccak256(hash);
		_finalize_map[final_hash].is_exist = true;
		_finalize_map[final_hash].is_finalise = false;
		for (uint j = 0; j < _submit_list.length; j++) {
			if (false == _submit_list[j].is_exist) {
				continue;
			}
			_finalize_map[final_hash].entries.push(_submit_list[j].entry);
		}

		_submit_list.length = 0;
		submit_hash(final_hash);
		return true;
	}

	function Finalise(bytes32 hash) public {
		assert(true == _finalize_map[hash].is_exist);
		assert(false == _finalize_map[hash].is_finalise);
		_finalize_map[hash].is_finalise = true;
	}

	function GetFinaliseEntriesLength(bytes32 hash) public view returns (bool, bool, uint) {
		if (false == _finalize_map[hash].is_exist) {
			return (false, false, 0);
		}
		if (false == _finalize_map[hash].is_finalise) {
			return (true, false, _finalize_map[hash].entries.length);
		}
		return (true, true, _finalize_map[hash].entries.length);
	}

	function GetFinaliseEntry(bytes32 hash, uint index) public view returns(bytes32) {
		assert(true == _finalize_map[hash].is_exist);
		assert(index < _finalize_map[hash].entries.length);
		return _finalize_map[hash].entries[index].hash_value;
	}

    function Create(string input_key, string val) public {
		assert(false == _proved_map[input_key].is_exist);
		assert(0 == _key_idxa1_map[input_key]);

		bytes32 hash = keccak256(val);
		Entry memory entry = Entry("create", hash);
		_proved_map[input_key].is_exist = true;
		_proved_map[input_key].entries.push(entry);
		UpdateHashReverseMap(input_key, hash);
		assert(true == CheckHash(hash));

		_keys.push(input_key);
		_key_idxa1_map[input_key] = _keys.length;

		_submit_list.push(SubmitEntry(true, entry));
		if (IsNeedSubmit()) {
			assert(true == Submit());
		}
    }

    function Retrieve(string input_key) public constant returns (bool exist, bytes32 data) {
		if (false == _proved_map[input_key].is_exist) {
			assert(0 == _key_idxa1_map[input_key]);
			return;
		}

		assert(0 != _proved_map[input_key].entries.length);
		assert(0 != _key_idxa1_map[input_key]);
		assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));

		uint entry_len = _proved_map[input_key].entries.length - 1;
		return (true, _proved_map[input_key].entries[entry_len].hash_value);
    }
    
    function Update(string input_key, string val) public {
		assert(true == _proved_map[input_key].is_exist);
		assert(0 != _key_idxa1_map[input_key]);
		assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));

		
		bytes32 hash = keccak256(val);
		Entry memory entry = Entry("update", hash);
		_proved_map[input_key].entries.push(entry);

		UpdateHashReverseMap(input_key, hash);
		assert(true == CheckHash(hash));

		_submit_list.push(SubmitEntry(true, entry));
		if (IsNeedSubmit()) {
			assert(true == Submit());
		}
    }

    function Delete(string input_key) public {
		if (false == _proved_map[input_key].is_exist) {
			return;
		}
		_proved_map[input_key].is_exist = false;
		_proved_map[input_key].entries.push(Entry("delete", keccak256("")));

		// remove key
		assert(0 != _key_idxa1_map[input_key]);
		assert(!strcmp(_keys[_key_idxa1_map[input_key] - 1], input_key));
		uint remove_idx = _key_idxa1_map[input_key] - 1;
		uint last_idx = _keys.length - 1;
		if (remove_idx != last_idx) {
			string memory last_key = _keys[last_idx];
			_keys[remove_idx] = last_key;
			_key_idxa1_map[last_key] = remove_idx + 1;
		}
		_key_idxa1_map[input_key] = 0;
		_keys.length--;
	}

	function CheckHash(bytes32 hash) public view returns (bool) {
		ReverseRecord storage reverse_record = _hash_reverse_map[hash];
		if (true != reverse_record.is_exist) {
			return false;
		}
		Record storage record = _proved_map[reverse_record.key];
		if (hash != record.entries[reverse_record.idx].hash_value) {
			return false;
		}
		return true;
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		bool exist = false;
		bytes32 hash = '';
		(exist, hash) = Retrieve(input_key);

		if (false == exist) {
			if (!strcmp('', val)) {
				return true;
			} else {
				return false;
			}
		}
		
		if (hash == keccak256(val)) {
			return true;
		}
		assert(true == CheckHash(hash));
		return false;
	}

	function GetKeysLength() public constant returns (uint) {
		return _keys.length;
	}

	function GetKey(uint idx) public constant returns (string) {
		return _keys[idx];
	}
}
