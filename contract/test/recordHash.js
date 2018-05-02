var RecordHash = artifacts.require("RecordHash");
require('truffle-test-utils').init();

contract("RecordHashBasicTest", function(accounts) {

    it("Record hash", async function() {
        var contract = await RecordHash.deployed();
        var hash = web3.sha3('show me the money');
        var result = await contract.Record(hash);
        assert.web3Event(result, {
            event: 'record_over',
            args: {
                finalise_hash: hash
            }
        }, 'The event is emitted');
    });
});
