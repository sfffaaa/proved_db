pragma solidity ^0.4.17;

contract ProvedDB {

	struct Entry {
		string action;
		bytes32 hash_value;
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

    function ProvedDB() public {
    }

	function strcmp(string s1, string s2) private pure returns (bool) {
		return keccak256(s1) != keccak256(s2);
	}

	function UpdateHashReverseMap(string key, bytes32 hash) private {
		assert(false == _hash_reverse_map[hash].is_exist);
		_hash_reverse_map[hash] = ReverseRecord(true, key, _proved_map[key].entries.length - 1);
	}

    function Create(string key, string val) public {
		assert(false == _proved_map[key].is_exist);
		assert(0 == _key_idxa1_map[key]);

		bytes32 hash = keccak256(val);
		_proved_map[key].is_exist = true;
		_proved_map[key].entries.push(Entry("create", hash));
		UpdateHashReverseMap(key, hash);

		_keys.push(key);
		_key_idxa1_map[key] = _keys.length;

		assert(true == CheckHash(hash));
    }

    function Retrieve(string key) public constant returns (bool exist, bytes32 data) {
		if (false == _proved_map[key].is_exist) {
			assert(0 == _key_idxa1_map[key]);
			return;
		}

		assert(0 != _proved_map[key].entries.length);
		assert(0 != _key_idxa1_map[key]);
		assert(!strcmp(_keys[_key_idxa1_map[key] - 1], key));

		uint entry_len = _proved_map[key].entries.length - 1;
		return (true, _proved_map[key].entries[entry_len].hash_value);
    }
    
    function Update(string key, string val) public {
		assert(true == _proved_map[key].is_exist);
		assert(0 != _key_idxa1_map[key]);
		assert(!strcmp(_keys[_key_idxa1_map[key] - 1], key));

		bytes32 hash = keccak256(val);
		_proved_map[key].entries.push(Entry("update", hash));

		UpdateHashReverseMap(key, hash);
		assert(true == CheckHash(hash));
    }

    function Delete(string key) public {
		if (false == _proved_map[key].is_exist) {
			return;
		}
		_proved_map[key].is_exist = false;
		_proved_map[key].entries.push(Entry("delete", keccak256("")));

		// remove key
		assert(0 != _key_idxa1_map[key]);
		assert(!strcmp(_keys[_key_idxa1_map[key] - 1], key));
		uint remove_idx = _key_idxa1_map[key] - 1;
		uint last_idx = _keys.length - 1;
		if (remove_idx != last_idx) {
			string memory last_key = _keys[last_idx];
			_keys[remove_idx] = last_key;
			_key_idxa1_map[last_key] = remove_idx + 1;
		}
		_key_idxa1_map[key] = 0;
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

	function CheckEntry(string key, string val) public constant returns (bool) {
		bool exist = false;
		bytes32 hash = '';
		(exist, hash) = Retrieve(key);

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
