pragma solidity ^0.4.23;

library Strings {

	// copy from https://github.com/willitscale/solidity-util/blob/master/lib/Strings.sol
    function compareTo(string _base, string _value)
		pure
        internal 
        returns (bool) {
        bytes memory _baseBytes = bytes(_base);
        bytes memory _valueBytes = bytes(_value);

        if (_baseBytes.length != _valueBytes.length) {
            return false;
        }

        for(uint i = 0; i < _baseBytes.length; i++) {
            if (_baseBytes[i] != _valueBytes[i]) {
                return false;
            }
        }

        return true;
    }
}


