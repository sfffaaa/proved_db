pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";


contract KeysRecordStorageV0 {

	using Strings for string;

	string[] _keys;
	mapping(string => uint) _key_idxa1_map;

    function PushKeyRecord(string input_key) public {
		assert(0 == _key_idxa1_map[input_key]);
		_keys.push(input_key);
		_key_idxa1_map[input_key] = _keys.length;
	}

    function GetKeyIdx(string input_key)
		public
		view
		returns (bool, uint) {
		if (0 == _key_idxa1_map[input_key]) {
			return (false, 0);
		} else {
			assert(true == input_key.compareTo(_keys[_key_idxa1_map[input_key] - 1]));
			return (true, _key_idxa1_map[input_key] - 1);
		}
	}

    function DeleteKey(string input_key) public {
		if (0 == _key_idxa1_map[input_key]) {
			return;
		}
		assert(true == input_key.compareTo(_keys[_key_idxa1_map[input_key] - 1]));
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

	function GetKeysLength() external view returns (uint) {
		return _keys.length;
	}

	function GetKey(uint idx) external view returns (string) {
		return _keys[idx];
	}
}
