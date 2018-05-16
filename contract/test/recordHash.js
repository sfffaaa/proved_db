var RecordHash = artifacts.require("RecordHash");
var EventEmitter = artifacts.require("EventEmitter");

contract("RecordHashBasicTest", function(accounts) {

    it("Record hash", async function() {
        var contract = await RecordHash.deployed();
        var hash = web3.sha3('show me the money');

        var eventEmitterContract = await EventEmitter.deployed();
        var checkEvent = eventEmitterContract.record_over({fromBlock: 0, toBlock: 'latest'});
        checkEvent.watch(function (error, resp) {
            assert.equal(resp.args.finalise_hash, hash, "event should be the same");
            checkEvent.stopWatching();
        });
        var result = await contract.Record(hash);
    });

    it("Record hash", async function() {
        var contract = await RecordHash.deployed();
        var hash = web3.sha3('show me the money, again');
        var checkResult = await contract.Get(hash);
        assert.equal(false, checkResult, 'Two result should not be the same');
        await contract.Record(hash);
        checkResult = await contract.Get(hash);
        assert.equal(true, checkResult, 'Two result should be the same');
    });

});
