pragma solidity ^0.4.17;

contract ProvedDB {

	struct Entry {
		string action;
		string hash_value;
	}

	struct Record {
		bool is_exist;
		Entry[] entries;
	}

    mapping(string => Record) proved_map;

    function ProvedDB() public {
    }

    function Create(string id, string hash) public {
		assert(false == proved_map[id].is_exist);
		proved_map[id].is_exist = true;
		proved_map[id].entries.push(Entry("create", hash));
    }

	function CheckEntry(string id, string hash) public constant returns (bool) {

		bytes32 hashHash = keccak256(hash);

		bool exist = false;
		string memory data = '';
		(exist, data) = Retrieve(id);

		if (false == exist) {
			if (keccak256('') == hashHash) {
				return true;
			} else {
				return false;
			}
		}
		
		if (keccak256(data) == hashHash) {
			return true;
		}
		return false;
	}
//
//	  function GetCheckSegment(int idx) public constant returns (bool continued, string fragment) {
//	  }

    function Retrieve(string id) public constant returns (bool exist, string data) {
		if (false == proved_map[id].is_exist) {
			return;
		}

		assert(0 != proved_map[id].entries.length);

		uint entry_len = proved_map[id].entries.length - 1;
		exist = true;
		data = proved_map[id].entries[entry_len].hash_value;
    }
    
    function Update(string id, string hash) public {
		assert(true == proved_map[id].is_exist);
		proved_map[id].entries.push(Entry("update", hash));
    }

    function Delete(string id) public {
		if (false == proved_map[id].is_exist) {
			return;
		}
		proved_map[id].is_exist = false;
		delete proved_map[id].entries;
    }
}
