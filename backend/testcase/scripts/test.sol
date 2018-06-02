pragma solidity 0.4.24;                                                                                                       

contract KeysRecord {

    function GetKeysLength() external pure returns (uint result) {
       return 10;
    }   
}
contract ProvedDB {

    address _address;
    KeysRecord _keys_record;

    constructor(address keys_record_addr) public {
        _address = keys_record_addr;
       _keys_record = KeysRecord(keys_record_addr);
    }   

    function GetAddr() public view returns (address addr) {
        return _address;
    }   
    function GetKeysLength() public view returns (uint result) {
        return _keys_record.GetKeysLength();
    }   
}

