var ProvedDB = artifacts.require("ProvedDB");
var EventEmitter = artifacts.require("EventEmitter");
var FinaliseRecord = artifacts.require("FinaliseRecord");
var FinaliseRecordStorageV0 = artifacts.require("FinaliseRecordStorageV0");
var KeysRecord = artifacts.require("KeysRecord");
var KeysRecordStorageV0 = artifacts.require("KeysRecordStorageV0");
var ProvedCRUD = artifacts.require("ProvedCRUD");
var ProvedCRUDStorageV0 = artifacts.require("ProvedCRUDStorageV0");
var RecordHashStorageV0 = artifacts.require("RecordHashStorageV0");
var Register = artifacts.require("Register");

const AssertRevert = require('./helper/assertRevert.js');
const AssertNoRevert = require('./helper/assertNoRevert.js');

contract("Onwer test", function(accounts) {

    it("execute EventEmitter on not owner", async function() {
        var eventEmitterContract = await EventEmitter.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]},
                                     {func: AssertNoRevert, from: accounts[0]}];
        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(eventEmitterContract.emit_submit_hash.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(eventEmitterContract.emit_record_over.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
        }

    });

    it("execute FinaliseRecord function on not owner", async function() {
        var finaliseRecordContract = await FinaliseRecord.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(finaliseRecordContract.Finalise.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.GetFinalisedGroupEntriesLength.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.GetFinalisedGroupEntry.call(
                web3.sha3('show me the money'), 1,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.GetFinaliseEntriesLength.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.GetFinaliseEntry.call(
                web3.sha3('show me the money'), 1,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.Create.call(
                'show me the money', 'it is money',
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordContract.Update.call(
                'show me the money', 'it is money',
                {from: fromAccount}
            ));
        }
    });

    it("execute FinaliseRecord function on not owner", async function() {
        var finaliseRecordStorageV0Contract = await FinaliseRecordStorageV0.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(finaliseRecordStorageV0Contract.GetSubmitEntriesLength.call(
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.ResetSubmitEntries.call(
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.PushSubmitEntry.call(
                'I want money', web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.GetSubmitEntry.call(
                1,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.UpdateFinaliseHashMap.call(
                web3.sha3('show me the money'), true, true,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.PushFinaliseHashMap.call(
                web3.sha3('show me the money'), true, true,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.GetFinaliseHashMap.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.GetFinaliseHashEntry.call(
                web3.sha3('show me the money'), 0,
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.GetKV2FinalisedHashMap.call(
                web3.sha3('show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(finaliseRecordStorageV0Contract.SetKV2FinaliseHashMap.call(
                web3.sha3('show me the money'), 'Give me money',
                {from: fromAccount}
            ));
        }
    });

    it("execute KeysRecord function on not owner", async function() {
        var keysRecordContract = await KeysRecord.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(keysRecordContract.Create.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordContract.NonExistedCheck.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordContract.ExistedCheck.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordContract.Delete.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordContract.GetKeysLength.call(
                {from: fromAccount}
            ));
            await checkFunc(keysRecordContract.GetKey.call(
                0,
                {from: fromAccount}
            ));
        }
    });

    it("execute KeysRecordStorageV0 function on not owner", async function() {
        var keysRecordStorageV0Contract = await KeysRecordStorageV0.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(keysRecordStorageV0Contract.PushKeyRecord.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordStorageV0Contract.GetKeyIdx.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordStorageV0Contract.DeleteKey.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(keysRecordStorageV0Contract.GetKeysLength.call(
                {from: fromAccount}
            ));
            await checkFunc(keysRecordStorageV0Contract.GetKey.call(
                0,
                {from: fromAccount}
            ));
        }
    });

    it("execute ProvedCRUD function on not owner", async function() {
        var provedCRUDContract = await ProvedCRUD.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(provedCRUDContract.Create.call(
                'Show me the money', 'again',
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDContract.Retrieve.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDContract.Update.call(
                'Show me the money', 'again',
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDContract.Delete.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDContract.CheckEntry.call(
                'Show me the money', 'again',
                {from: fromAccount}
            ));
        }
    });

    it("execute ProvedCRUDStorageV0 function on not owner", async function() {
        var provedCRUDStorageV0Contract = await ProvedCRUDStorageV0.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(provedCRUDStorageV0Contract.Create.call(
                'Show me the money', web3.sha3('again'),
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDStorageV0Contract.Update.call(
                'Show me the money', web3.sha3('again'),
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDStorageV0Contract.Delete.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(provedCRUDStorageV0Contract.Retrieve.call(
                'Show me the money',
                {from: fromAccount}
            ));
        }
    });

    it("execute RecordHashStorageV0 function on not owner", async function() {
        var recordHashStorageV0Contract = await RecordHashStorageV0.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(recordHashStorageV0Contract.Set.call(
                web3.sha3('Show me the money'),
                {from: fromAccount}
            ));
            await checkFunc(recordHashStorageV0Contract.Get.call(
                web3.sha3('Show me the money'),
                {from: fromAccount}
            ));
        }
    });

    it("execute Register function on not owner", async function() {
        var registerContract = await Register.deployed();
        var checkFuncWithAccounts = [{func: AssertRevert, from: accounts[1]}];

        for (var checkingIdx = 0;
            checkingIdx < checkFuncWithAccounts.length;
            checkingIdx++) {
            var checkFunc = checkFuncWithAccounts[checkingIdx]['func'];
            var fromAccount = checkFuncWithAccounts[checkingIdx]['from'];
            await checkFunc(registerContract.GetInst.call(
                'Show me the money',
                {from: fromAccount}
            ));
            await checkFunc(registerContract.SetInst.call(
                'Show me the money',
                fromAccount,
                {from: fromAccount}
            ));
            await checkFunc(registerContract.SetWhitelist.call(
                fromAccount,
                {from: fromAccount}
            ));
            await checkFunc(registerContract.CheckWhiltelist.call(
                fromAccount,
                {from: fromAccount}
            ));
        }
    });

});
