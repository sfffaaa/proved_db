pragma solidity ^0.4.23;

import {Strings} from "./strings.sol";
import {KeysRecord} from "./KeysRecord.sol";
import {ProvedCRUD} from "./ProvedCRUD.sol";
import {FinaliseRecord} from "./FinaliseRecord.sol";


contract ProvedDB {

	KeysRecord _keys_record;
	ProvedCRUD _proved_crud;
	FinaliseRecord _finalise_record;

    constructor(address keys_record_addr,
				address proved_crud_addr,
				address finalise_record_addr)
	public {
		_keys_record = KeysRecord(keys_record_addr);
		_proved_crud = ProvedCRUD(proved_crud_addr);
		_finalise_record = FinaliseRecord(finalise_record_addr);
    }

	function Finalise(bytes32 finalise_hash) public {
		_finalise_record.Finalise(finalise_hash);
	}

	function GetFinalisedGroupEntriesLength(bytes32 kv_hash) public view returns (bool, uint) {
		return _finalise_record.GetFinalisedGroupEntriesLength(kv_hash);
	}

	function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
		return _finalise_record.GetFinalisedGroupEntry(kv_hash, idx);
	}

	function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
		return _finalise_record.GetFinaliseEntriesLength(finalise_hash);
	}

	function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
		return _finalise_record.GetFinaliseEntry(finalise_hash, index);
	}

    function Create(string input_key, string val) public {
		_proved_crud.Create(input_key, val);
		_keys_record.Create(input_key);
		_finalise_record.Create(input_key, val);
    }

    function Retrieve(string input_key) public constant returns (bool, bytes32) {
		bool rexist;
		bytes32 rdata;
		(rexist, rdata) = _proved_crud.Retrieve(input_key);
		if (true == rexist) {
			_keys_record.ExistedCheck(input_key);
		} else {
			_keys_record.NonExistedCheck(input_key);
		}
		return (rexist, rdata);
    }
    
    function Update(string input_key, string val) public {
		_proved_crud.Update(input_key, val);
		_keys_record.ExistedCheck(input_key);
		_finalise_record.Update(input_key, val);
    }

    function Delete(string input_key) public {
		if (true == _proved_crud.Delete(input_key)) {
			_keys_record.Delete(input_key);
		}
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		return _proved_crud.CheckEntry(input_key, val);
	}

	function GetKeysLength() public view returns (uint) {
		return _keys_record.GetKeysLength();
	}

	function GetKey(uint idx) public view returns (string) {
		return _keys_record.GetKey(idx);
	}
}
