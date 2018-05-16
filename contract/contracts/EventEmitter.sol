pragma solidity ^0.4.23;

contract EventEmitter {

	event submit_hash(bytes32 finalise_hash);

	function emit_submit_hash(bytes32 finalise_hash) {
		emit submit_hash(finalise_hash);
	}
}
