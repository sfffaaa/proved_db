pragma solidity ^0.4.23;

contract EventEmitter {

	event submit_hash(bytes32 finalise_hash);
	event record_over(bytes32 finalise_hash);

	function emit_submit_hash(bytes32 finalise_hash) public {
		emit submit_hash(finalise_hash);
	}

	function emit_record_over(bytes32 finalise_hash) public {
		emit record_over(finalise_hash);
	}
}
