pragma solidity 0.4.24;

contract ProvedCRUDStorageInterface {
	function Create(string input_key, bytes32 hash) public;
	function Update(string input_key, bytes32 hash) public;
    function Delete(string input_key) public returns (bool);
	function Retrieve(string input_key) public view returns (bool exist, bytes32 data);
}
