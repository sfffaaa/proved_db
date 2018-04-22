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

    mapping(string => Record) proved_map;
	string[] keys;
	mapping(string => uint) key_idxa1_map;

    function ProvedDB() public {
    }

	function strcmp(string s1, string s2) private pure returns (bool) {
		return keccak256(s1) == keccak256(s2);
	}

    function Create(string key, string val) public {
		assert(false == proved_map[key].is_exist);
		assert(0 == key_idxa1_map[key]);

		proved_map[key].is_exist = true;
		proved_map[key].entries.push(Entry("create", keccak256(val)));

		keys.push(key);
		key_idxa1_map[key] = keys.length;
    }

    function Retrieve(string key) public constant returns (bool exist, bytes32 data) {
		if (false == proved_map[key].is_exist) {
			assert(0 == key_idxa1_map[key]);
			return;
		}

		assert(0 != proved_map[key].entries.length);
		assert(0 != key_idxa1_map[key]);
		assert(strcmp(keys[key_idxa1_map[key] - 1], key));

		uint entry_len = proved_map[key].entries.length - 1;
		return (true, proved_map[key].entries[entry_len].hash_value);
    }
    
    function Update(string key, string val) public {
		assert(true == proved_map[key].is_exist);
		assert(0 != key_idxa1_map[key]);
		assert(strcmp(keys[key_idxa1_map[key] - 1], key));

		proved_map[key].entries.push(Entry("update", keccak256(val)));
    }

    function Delete(string key) public {
		if (false == proved_map[key].is_exist) {
			assert(0 == key_idxa1_map[key]);
			return;
		}
		proved_map[key].is_exist = false;
		delete proved_map[key].entries;

		assert(0 != key_idxa1_map[key]);
		assert(strcmp(keys[key_idxa1_map[key] - 1], key));
		uint remove_idx = key_idxa1_map[key] - 1;
		uint last_idx = keys.length - 1;
		if (remove_idx != last_idx) {
			string memory last_key = keys[last_idx];
			keys[remove_idx] = last_key;
			key_idxa1_map[last_key] = remove_idx + 1;
		}
		key_idxa1_map[key] = 0;
		keys.length--;
	}

	function CheckEntry(string key, string val) public constant returns (bool) {
		bool exist = false;
		bytes32 hash = '';
		(exist, hash) = Retrieve(key);

		if (false == exist) {
			if (strcmp('', val)) {
				return true;
			} else {
				return false;
			}
		}
		
		if (hash == keccak256(val)) {
			return true;
		}
		return false;
	}

	function GetKeysLength() public constant returns (uint) {
		return keys.length;
	}

	function GetKey(uint idx) public constant returns (string) {
		return keys[idx];
	}
}
