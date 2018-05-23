pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";
import {ProvedCRUDStorageV0} from "./ProvedCRUDStorageV0.sol";

contract ProvedCRUD {
	using Strings for string;

	ProvedCRUDStorageV0 _proved_crud_storage;
	constructor(address proved_crud_storage_addr)
		public
	{
		_proved_crud_storage = ProvedCRUDStorageV0(proved_crud_storage_addr);
	}

	function Create(string input_key, string val) public {
		bytes32 hash = input_key.hashPair(val);
		_proved_crud_storage.Create(input_key, hash);
    }
	function Retrieve(string input_key) public constant returns (bool exist, bytes32 data) {
		return _proved_crud_storage.Retrieve(input_key);
    }

    function Update(string input_key, string val) public {
		bytes32 hash = input_key.hashPair(val);
		_proved_crud_storage.Update(input_key, hash);
    }

    function Delete(string input_key) public returns (bool) {
		return _proved_crud_storage.Delete(input_key);
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		bool exist = false;
		bytes32 hash = '';
		(exist, hash) = Retrieve(input_key);

		if (false == exist) {
			if (true == val.compareTo('')) {
				return true;
			} else {
				return false;
			}
		}
		if (hash == input_key.hashPair(val)) {
			return true;
		}
		return false;
	}
}
