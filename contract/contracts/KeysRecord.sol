pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";

contract KeysRecord {

	using Strings for string;

	string[] _keys;
	mapping(string => uint) _key_idxa1_map;

    function Create(string input_key) public {
		assert(0 == _key_idxa1_map[input_key]);
		_keys.push(input_key);
		_key_idxa1_map[input_key] = _keys.length;
	}
    function RetrieveCheck(string input_key, bool is_exist) public constant {
		if (false == is_exist) {
			assert(0 == _key_idxa1_map[input_key]);
		} else {
			assert(0 != _key_idxa1_map[input_key]);
			assert(true == input_key.compareTo(_keys[_key_idxa1_map[input_key] - 1]));
		}
	}
    function UpdateCheck(string input_key) public constant {
		assert(0 != _key_idxa1_map[input_key]);
		assert(true == input_key.compareTo(_keys[_key_idxa1_map[input_key] - 1]));
	}
    function Delete(string input_key) public {
		assert(0 != _key_idxa1_map[input_key]);
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

	function GetKeysLength() external constant returns (uint) {
		return _keys.length;
	}

	function GetKey(uint idx) external constant returns (string) {
		return _keys[idx];
	}
}
