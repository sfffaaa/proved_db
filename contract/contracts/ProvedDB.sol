pragma solidity ^0.4.23;

import {Strings} from "./Strings.sol";
import {Register} from "./Register.sol";
import {KeysRecord} from "./KeysRecord.sol";
import {ProvedCRUD} from "./ProvedCRUD.sol";
import {FinaliseRecord} from "./FinaliseRecord.sol";


contract ProvedDB {

	Register _register;

    constructor(address register_address)
	public {
		_register = Register(register_address);
    }

	function GetKeyRecordInst()
		private
		view
		returns (KeysRecord)
	{
		return KeysRecord(_register.GetInst("KeysRecord"));
	}

	function GetProvedCRUDInst()
		private
		view
		returns (ProvedCRUD)
	{
		return ProvedCRUD(_register.GetInst("ProvedCRUD"));
	}

	function GetFinaliseRecordInst()
		private
		view
		returns (FinaliseRecord)
	{
		return FinaliseRecord(_register.GetInst("FinaliseRecord"));
	}

	function Finalise(bytes32 finalise_hash) public {
		GetFinaliseRecordInst().Finalise(finalise_hash);
	}

	function GetFinalisedGroupEntriesLength(bytes32 kv_hash) public view returns (bool, uint) {
		return GetFinaliseRecordInst().GetFinalisedGroupEntriesLength(kv_hash);
	}

	function GetFinalisedGroupEntry(bytes32 kv_hash, uint idx) public view returns (bytes32) {
		return GetFinaliseRecordInst().GetFinalisedGroupEntry(kv_hash, idx);
	}

	function GetFinaliseEntriesLength(bytes32 finalise_hash) public view returns (bool, bool, uint) {
		return GetFinaliseRecordInst().GetFinaliseEntriesLength(finalise_hash);
	}

	function GetFinaliseEntry(bytes32 finalise_hash, uint index) public view returns(bytes32) {
		return GetFinaliseRecordInst().GetFinaliseEntry(finalise_hash, index);
	}

    function Create(string input_key, string val) public {
		GetProvedCRUDInst().Create(input_key, val);
		GetKeyRecordInst().Create(input_key);
		GetFinaliseRecordInst().Create(input_key, val);
    }

    function Retrieve(string input_key) public constant returns (bool, bytes32) {
		KeysRecord keys_record_inst = GetKeyRecordInst();
		bool rexist;
		bytes32 rdata;
		(rexist, rdata) = GetProvedCRUDInst().Retrieve(input_key);
		if (true == rexist) {
			keys_record_inst.ExistedCheck(input_key);
		} else {
			keys_record_inst.NonExistedCheck(input_key);
		}
		return (rexist, rdata);
    }
    
    function Update(string input_key, string val) public {
		GetProvedCRUDInst().Update(input_key, val);
		GetKeyRecordInst().ExistedCheck(input_key);
		GetFinaliseRecordInst().Update(input_key, val);
    }

    function Delete(string input_key) public {
		if (true == GetProvedCRUDInst().Delete(input_key)) {
			GetKeyRecordInst().Delete(input_key);
		}
	}

	function CheckEntry(string input_key, string val) public constant returns (bool) {
		return GetProvedCRUDInst().CheckEntry(input_key, val);
	}

	function GetKeysLength() public view returns (uint) {
		return GetKeyRecordInst().GetKeysLength();
	}

	function GetKey(uint idx) public view returns (string) {
		return GetKeyRecordInst().GetKey(idx);
	}
}
