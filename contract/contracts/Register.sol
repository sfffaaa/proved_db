pragma solidity ^0.4.23;

contract Register {
	mapping(string => address) _register_map;

	function GetInst(string name) public view returns (address) {
		return _register_map[name];
	}

	function SetInst(string name, address target_address) public {
		_register_map[name] = target_address;
	}
}
