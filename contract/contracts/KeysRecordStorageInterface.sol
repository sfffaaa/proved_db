pragma solidity 0.4.24;


interface KeysRecordStorageInterface {

    function PushKeyRecord(string input_key) external;
    function GetKeyIdx(string input_key) external view returns (bool, uint);
    function DeleteKey(string input_key) external;
	function GetKeysLength() external view returns (uint);
	function GetKey(uint idx) external view returns (string);
}
