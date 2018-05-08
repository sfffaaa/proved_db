var ProvedDB = artifacts.require("ProvedDB");
const BigNumber = require('bignumber.js');
require('truffle-test-utils').init();

var NON_EXIST_KEY = "aabbccddeeff";
var TEST_DATA = {
    'test01': ['hash1'],
    'test02': ['hash1', 'hash2', 'hash3'],
    'test03': ['hash1'],
    'test04': ['hash1'],
    'test05': [{
            'deleteLastEntry01': 'hash01'
        }, {
            'deleteLastEntry02': 'hash02'
        }, {
            'deleteLastEntry03': 'hash03'
    }],
    'test06': [{
            'deleteFirstEntry01': 'hash01'
        }, {
            'deleteFirstEntry02': 'hash02'
        }, {
            'deleteFirstEntry03': 'hash03'
    }],
    'test07': [{
            'deleteFirstEntry01': 'hash01'
        }, {
            'deleteFirstEntry02': 'hash02'
        }, {
            'deleteFirstEntry03': 'hash03'
        }, {
            'deleteFirstEntry04': 'hash04'
    }],
    'test08': ['hash1', 'hash2', 'hash3'],
    'test09': ['hash1', 'hash2'],
};

function GetCheckHashSum(testEntries) {
    //remove overflow part
    var hashSum = BigNumber(0);
    var threshold = BigNumber(2).exponentiatedBy(256);
    for (var i = 0; i < testEntries.length; i++) {
        var entryHash = BigNumber(web3.sha3(testEntries[i]));
        hashSum = hashSum.plus(entryHash);
        if (hashSum.isGreaterThanOrEqualTo(threshold)) {
            hashSum = hashSum.minus(threshold);
        }
    }

    //add right padding
    var oriHexStr = web3.toHex(hashSum.toString());
    var newHexStr = '';
    if (66 === oriHexStr.length) {
        newHexStr = oriHexStr;
    } else {
        newHexStr = '0x' + '0'.repeat(66 - oriHexStr.length) + oriHexStr.substring(2);
    }
    return web3.sha3(newHexStr, {encoding: 'hex'});
}

function GetSubmitHashSum(testEntries) {
    //remove overflow part
    var hashSum = BigNumber(0);
    var threshold = BigNumber(2).exponentiatedBy(256);
    for (var i = 0; i < testEntries.length; i++) {
        var entryHash = BigNumber(GetCheckHashSum(testEntries[i]));
        hashSum = hashSum.plus(entryHash);
        if (hashSum.isGreaterThanOrEqualTo(threshold)) {
            hashSum = hashSum.minus(threshold);
        }
    }

    //add right padding
    var oriHexStr = web3.toHex(hashSum.toString());
    var newHexStr = '';
    if (66 === oriHexStr.length) {
        newHexStr = oriHexStr;
    } else {
        newHexStr = '0x' + '0'.repeat(66 - oriHexStr.length) + oriHexStr.substring(2);
    }
    return web3.sha3(newHexStr, {encoding: 'hex'});
}

function CheckNotExist(ret) {
    assert.equal(ret[0], false, "key not exist, so return the key not exist");
    assert.equal(ret[1].toString(),
                 0x0000000000000000000000000000000000000000000000000000000000000000,
                 "key not exist, so return empty data");
}

function CheckExist(ret, checkKey, checkValue) {
    assert.equal(ret[0], true, "key exist, so return the key exist " + checkKey);
    assert.equal(ret[1].toString(), GetCheckHashSum([checkKey, checkValue]),
                 "key exist, so return value " + checkValue);
}

contract("ProvedDBBasic", function(accounts) {

    it("Create, Retrieve, Delete, Retrieve", function() {
        var contract;
        var testKey = "test01";
        return ProvedDB.deployed().then(function(instance) {
            contract = instance;
            return contract.Create(testKey, TEST_DATA[testKey][0]);
        }).then(function(result) {
            return contract.Retrieve.call(testKey);
        }).then(function(dbData) {
            CheckExist(dbData, testKey, TEST_DATA[testKey][0])
            return contract.Delete(testKey);
        }).then(function(result) {
            return contract.Retrieve.call(testKey);
        }).then(function(result) {
            CheckNotExist(result);
        });
    });
});

contract("ProvedDBBasic2", function(accounts) {

    it("Create, Update, Retrieve, Update, Retrieve, Delete, Retrieve", function() {
        var contract;
        var testKey = "test02";
        return ProvedDB.deployed().then(function(instance) {
            contract = instance;
            return contract.Create(testKey, TEST_DATA[testKey][0]);
        }).then(function(result) {
            return contract.Update(testKey, TEST_DATA[testKey][1]);
        }).then(function(result) {
            return contract.Retrieve.call(testKey);
        }).then(function(dbData) {
            CheckExist(dbData, testKey, TEST_DATA[testKey][1])
        }).then(function(result) {
            return contract.Update(testKey, TEST_DATA[testKey][2]);
        }).then(function(result) {
            return contract.Retrieve.call(testKey);
        }).then(function(dbData) {
            CheckExist(dbData, testKey, TEST_DATA[testKey][2])
            return contract.Delete(testKey);
        }).then(function(result) {
            return contract.Retrieve.call(testKey);
        }).then(function(result) {
            CheckNotExist(result);
        });
    });

    it("Retrieve but key not exist", async function() {
        var contract = await ProvedDB.deployed();
        var ret = await contract.Retrieve.call(NON_EXIST_KEY);
        CheckNotExist(ret);
    });

    it("Delete but key not exist + Retrieve", function() {
        var contract;
        return ProvedDB.deployed().then(function(instance) {
            contract = instance;
            return contract.Delete(NON_EXIST_KEY);
        }).then(function(result) {
            return contract.Retrieve.call(NON_EXIST_KEY);
        }).then(function(result) {
            CheckNotExist(result);
        });
    });
});

contract("ProvedDBBasic3", function(accounts) {

    it("Create but key exist", async function() {
        var contract = await ProvedDB.deployed();
        var testKey = 'test03';
        var retrieveData = await contract.Retrieve.call(testKey);
        if (false === retrieveData[0]) {
            await contract.Create(testKey, TEST_DATA[testKey][0]);
        }
        CheckExist(await contract.Retrieve.call(testKey),
                   testKey,
                   TEST_DATA[testKey][0]);
        var err = undefined;
        try {
            await contract.Create(testKey, 'you should not pass');
        } catch(error) {
            err = error;
        }
        assert.notEqual(err, undefined, "err should be occurs");
    });

    it("Update but key not exist", async function() {
        var contract = await ProvedDB.deployed();
        var ret = await contract.Retrieve.call(NON_EXIST_KEY);
        CheckNotExist(ret);
        var err = undefined;
        try {
            await contract.Update(NON_EXIST_KEY, "you should not pass");
        } catch(error) {
            err = error;
        }
        assert.notEqual(err, undefined, "err should be occurs");
    });

    it("Check without id", async function() {
        var contract = await ProvedDB.deployed();
        assert.equal(await contract.CheckEntry.call('you should not pass', ''),
                     true, 'Cannot find the key, but compare with empty data, so should pass');
        assert.equal(await contract.CheckEntry.call('you should not pass', 'you should no have data'),
                     false, 'Cannot find the key, but compare with different data, so should not pass');
    });
});

contract("ProvedDBBasic4", function(accounts) {

    it("Create, Check", async function() {
        var testKey = "test04";
        var contract = await ProvedDB.deployed();
        await contract.Create(testKey, TEST_DATA[testKey][0])
        assert.equal(await contract.CheckEntry.call(testKey, TEST_DATA[testKey][0]),
                     true, 'It should be pass due to the same data');
        assert.equal(await contract.CheckEntry.call(testKey, 'This is wrong data'),
                     false, 'It should not be pass due to the different data');
    });
});

function GetTestcaseKeyList(testKey) {
    var testKeys = [];
    for (var i = 0; i < TEST_DATA[testKey].length; i++) {
        var testElement = TEST_DATA[testKey][i];
        var key = Object.keys(testElement)[0];
        testKeys.push(key);
    }
    return testKeys;
};

function GetTestcaseKey(testcase) {
    return Object.keys(testcase)[0];
};

async function CheckOnchainKeyExist(contract, testKeys) {
    var keysLength = await contract.GetKeysLength.call();
    assert.equal(keysLength.toNumber(), testKeys.length, 'key should be the same');
    for (var j = 0; j < keysLength.toNumber(); j++) {
        var keyName = await contract.GetKey.call(j);
        assert.notEqual(testKeys.indexOf(keyName), -1, 'key should be found');
    }
}

async function RetrieveExistChecking(contract, retrieveTestcase) {
    var retrieveKey = GetTestcaseKey(retrieveTestcase);
    var retrieveVal = retrieveTestcase[retrieveKey];
    var retrieveExistData = await contract.Retrieve.call(retrieveKey);
    CheckExist(retrieveExistData, retrieveKey, retrieveVal);
}

async function RetrieveNotExistChecking(contract, testElement) {
    var key = Object.keys(testElement)[0];
    var retrieveNoExistData = await contract.Retrieve.call(key);
    CheckNotExist(retrieveNoExistData);
}

async function DeleteChecking(contract, key) {
    await contract.Delete(key);
    var retrieveNoExistData = await contract.Retrieve.call(key);
    assert.equal(retrieveNoExistData[0], false, 'key is deleted');
    assert.equal(await contract.CheckEntry.call(key, ''),
                 true, 'Cannot find the key, but compare with empty data, so should pass');
}

contract("ProvedDBDeleteFromEndCheck", function(accounts) {
    it("Delete all entry from end + check", async function() {
        var testKey = "test05";
        
        var testKeys = GetTestcaseKeyList(testKey);
        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = GetTestcaseKey(testElement);
            await contract.Create(key, testElement[key]);

            var keysLength = await contract.GetKeysLength.call();
            assert.equal(keysLength.toNumber(), i + 1,
                         'key length should be the same');
        }
        await CheckOnchainKeyExist(contract, testKeys);

        for (var i = TEST_DATA[testKey].length - 1; i >= 0; i--) {
            var key = GetTestcaseKey(TEST_DATA[testKey][i]);
            await DeleteChecking(contract, key);

            for (var j = 0; j < i; j++) {
                await RetrieveExistChecking(contract, TEST_DATA[testKey][j]);
            }
            testKeys.splice(testKeys.indexOf(key), 1);
            var keysLength = await contract.GetKeysLength.call();
            for (var j = 0; j < keysLength.toNumber(); j++) {
                var keyName = await contract.GetKey.call(j);
                assert.notEqual(testKeys.indexOf(keyName), -1, 'key should be found');
            }
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var key = GetTestcaseKey(TEST_DATA[testKey][i]);
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');

        }
        var keysLength = await contract.GetKeysLength.call();
        assert.equal(keysLength.toNumber(), 0,
                     'key length should be the same');
    });
});
 
contract("ProvedDBDeleteFromFrontCheck", function(accounts) {
    it("Delete all entry from front + check", async function() {
        var testKey = "test06";

        var testKeys = GetTestcaseKeyList(testKey);

        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = GetTestcaseKey(testElement);
            await contract.Create(key, testElement[key]);
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var key = GetTestcaseKey(TEST_DATA[testKey][i]);
            await DeleteChecking(contract, key);

            for (var j = TEST_DATA[testKey].length - 1; j > i; j--) {
                await RetrieveExistChecking(contract, TEST_DATA[testKey][j]);
            }
 
            testKeys.splice(testKeys.indexOf(key), 1);
            await CheckOnchainKeyExist(contract, testKeys);
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            await RetrieveNotExistChecking(contract, TEST_DATA[testKey][i]);
        }
    });
});

contract("ProvedDBDeleteFromMiddleCheck", function(accounts) {
    it("Delete all entry from middle + check", async function() {
        var testKey = "test07";

        var testKeys = GetTestcaseKeyList(testKey);
        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = GetTestcaseKey(TEST_DATA[testKey][i]);
            await contract.Create(key, testElement[key]);
        }
        for (var i = 1; i < TEST_DATA[testKey].length - 1; i++) {
            var key = GetTestcaseKey(TEST_DATA[testKey][i]);
            await DeleteChecking(contract, key);

            testKeys.splice(testKeys.indexOf(key), 1);
            await CheckOnchainKeyExist(contract, testKeys);
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            if (0 == i || 0 == TEST_DATA[testKey].length - 1) {
                await RetrieveExistChecking(contract, TEST_DATA[testKey][i]);
            }
        }
    });
});

contract("ProvedDBSubmit", function(accounts) {
    it("empty finalise submit", async function() {
        var contract = await ProvedDB.deployed();
        var err = undefined;
        try {
            await contract.Finalise('I dont have any hash here');
        } catch(error) {
            err = error;
        }
        assert.notEqual(err, undefined, "err should be occurs");
    });

    it("Create, Update submit", async function() {
        var testKey = "test09";
        var contract = await ProvedDB.deployed();
        var checkHash = GetSubmitHashSum([[testKey, TEST_DATA[testKey][0]],
                                          [testKey, TEST_DATA[testKey][1]]]);
        await contract.Create(testKey, TEST_DATA[testKey][0]);

        var result = await contract.Update(testKey, TEST_DATA[testKey][1]);
        assert.web3Event(result, {
            event: 'submit_hash',
            args: {
                finalise_hash: checkHash
            }
        }, 'The event is emitted');
        await contract.Finalise(checkHash);
    });

    it("Multiple create", async function() {
        const TEST_PAIR_LENGTH = 50;
        const TEST_PERIOD = 2;
        var testEntries = [];
        for (var i = 0; i < TEST_PAIR_LENGTH; i++) {
            var val = '' + (i + 0);
            testEntries.push(val);
        }
        var contract = await ProvedDB.deployed();
        for (var i = 0; i < testEntries.length; i += TEST_PERIOD) {
            var checkHash = GetSubmitHashSum([['' + (i + 0), testEntries[i]],
                                              ['' + (i + 1), testEntries[i + 1]]]);
            await contract.Create(testEntries[i], testEntries[i]);
            var result = await contract.Create(testEntries[i + 1], testEntries[i + 1]);
            assert.web3Event(result, {
                event: 'submit_hash',
                args: {
                    finalise_hash: checkHash
                }
            }, 'The event is emitted');
            await contract.Finalise(checkHash);
        }
    });
});

contract("ProvedDBSubmitChecking", function(accounts) {
    it("empty finalise submit", async function() {
        var contract = await ProvedDB.deployed();
        var nonExistKey = 'You should not pass';
        var finaliseData = await contract.GetFinaliseEntriesLength(nonExistKey);
        assert.equal(false, finaliseData[0], "hash doesn't exist");
        assert.equal(false, finaliseData[1], "hash doens't finalise");
        assert.equal(0, finaliseData[2].toNumber(), 'hash entry index should be zero');
    });

    it("Create, Update submit and finalise", async function() {
        var testKey = "test09";
        var contract = await ProvedDB.deployed();
        var checkHash = GetSubmitHashSum([[testKey, TEST_DATA[testKey][0]],
                                          [testKey, TEST_DATA[testKey][1]]
                                         ]);
        await contract.Create(testKey, TEST_DATA[testKey][0]);
        await contract.Update(testKey, TEST_DATA[testKey][1]);

        var finaliseData = await contract.GetFinaliseEntriesLength(checkHash);
        assert.equal(true, finaliseData[0], 'hash should exist');
        assert.equal(false, finaliseData[1], "hash doens't finalise");
        assert.equal(2, finaliseData[2].toNumber(), 'hash entry index should be zero');
        for (var i = 0; i < finaliseData[2].length; i++) {
            var entryHash = await contract.GetFinaliseEntry(checkHash, i);
            assert.equal(web3.sha(TEST_DATA[testKey][i]), entryHash, "hash should be the same");
        }
        await contract.Finalise(checkHash);
        var finaliseData = await contract.GetFinaliseEntriesLength(checkHash);
        assert.equal(true, finaliseData[0], 'hash should exist');
        assert.equal(true, finaliseData[1], "hash doens't finalise");
        assert.equal(2, finaliseData[2].toNumber(), 'hash entry index should be zero');
        for (var i = 0; i < finaliseData[2].length; i++) {
            var entryHash = await contract.GetFinaliseEntry(checkHash, i);
            assert.equal(web3.sha(TEST_DATA[testKey][i]), entryHash, "hash should be the same");
        }
    });

    it("Multiple create", async function() {
        const TEST_PAIR_LENGTH = 50;
        const TEST_PERIOD = 2;
        var testEntries = [];
        for (var i = 0; i < TEST_PAIR_LENGTH; i++) {
            var val = '' + (i + 0);
            testEntries.push(val);
        }
        var contract = await ProvedDB.deployed();
        for (var i = 0; i < testEntries.length; i+=TEST_PERIOD) {
            var checkHash = GetSubmitHashSum([['' + (i + 0), testEntries[i]],
                                             ['' + (i + 1), testEntries[i + 1]]
                                            ]);
            await contract.Create(testEntries[i], testEntries[i]);
            await contract.Create(testEntries[i + 1], testEntries[i + 1]);
            await contract.Finalise(checkHash);
            var finaliseData = await contract.GetFinaliseEntriesLength(checkHash);
            assert.equal(true, finaliseData[0], 'hash should exist');
            assert.equal(true, finaliseData[1], "hash doens't finalise");
            assert.equal(2, finaliseData[2].toNumber(), 'hash entry index should be zero');
            for (var j = 0; j < finaliseData[2].length; j++) {
                var entryHash = await contract.GetFinaliseEntry(checkHash, j);
                assert.equal(web3.sha(testEntries[i + j]), entryHash, "hash should be the same");
            }
        }
    });
});

contract("ProvedDBFinaliseGroupChecking", function(accounts) {
    it("empty finalise submit", async function() {
        var contract = await ProvedDB.deployed();
        var nonExistKey = 'You should not pass';
        var finaliseGroupData = await contract.GetFinalisedGroupEntriesLength(nonExistKey);
        assert.equal(false, finaliseGroupData[0], "hash doesn't exist");
        assert.equal(0, finaliseGroupData[1].toNumber(), 'hash entry index should be zero');
    });

    it("Create, Update + check finalise group", async function() {
        var testKey = "test09";
        var contract = await ProvedDB.deployed();
        var checkHash = GetSubmitHashSum([[testKey, TEST_DATA[testKey][0]],
                                          [testKey, TEST_DATA[testKey][1]]
                                         ]);
        await contract.Create(testKey, TEST_DATA[testKey][0]);
        await contract.Update(testKey, TEST_DATA[testKey][1]);
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var finaliseGroupData = await contract.GetFinalisedGroupEntriesLength(TEST_DATA[testKey][i]);
            assert.equal(false, finaliseGroupData[0], 'hash should not exist');
            assert.equal(0, finaliseGroupData[1].toNumber(), 'hash entry index should be zero');
        }
        await contract.Finalise(checkHash);
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var checkGroupHash = GetCheckHashSum([testKey, TEST_DATA[testKey][i]]);
            var finaliseGroupData = await contract.GetFinalisedGroupEntriesLength(checkGroupHash);
            assert.equal(true, finaliseGroupData[0], 'hash should exist');
            assert.equal(TEST_DATA[testKey].length,
                         finaliseGroupData[1].toNumber(),
                         'hash entry index should be zero');
            for (var j = 0; j < finaliseGroupData[1].length; j++) {
                var entryHash = await contract.GetFinalisedGroupEntry(checkGroupHash, j);
                assert.equal(GetCheckHashSum([testKey, TEST_DATA[testKey][j]]), entryHash, "hash should be the same");
            }
        }
    });

    it("Multiple create + check finalise group", async function() {
        const TEST_PAIR_LENGTH = 50;
        const TEST_PERIOD = 2;
        var testEntries = [];
        for (var i = 0; i < TEST_PAIR_LENGTH; i++) {
            var val = '' + (i + 0);
            testEntries.push(val);
        }
        var contract = await ProvedDB.deployed();
        for (var i = 0; i < testEntries.length; i+=TEST_PERIOD) {
            var checkHash = GetSubmitHashSum([['' + (i + 0), testEntries[i]],
                                             ['' + (i + 1), testEntries[i + 1]]
                                            ]);
            await contract.Create(testEntries[i], testEntries[i]);
            await contract.Create(testEntries[i + 1], testEntries[i + 1]);
            for (var j = 0; j < TEST_PERIOD; j++) {
                var finaliseGroupData = await contract.GetFinalisedGroupEntriesLength(testEntries[i + j]);
                assert.equal(false, finaliseGroupData[0], 'hash should not exist');
                assert.equal(0, finaliseGroupData[1].toNumber(), 'hash entry index should be zero');
            }
            await contract.Finalise(checkHash);
            for (var j = 0; j < TEST_PERIOD; j++) {
                var checkGroupHash = GetCheckHashSum(['' + (i + j), testEntries[i + j]]);
                var finaliseData = await contract.contract.GetFinalisedGroupEntriesLength(checkGroupHash);
                assert.equal(true, finaliseData[0], 'hash should exist');
                assert.equal(TEST_PERIOD, finaliseData[1].toNumber(), 'hash entry index should be zero');
                for (var k = 0; k < finaliseData[1].toNumber(); k++) {
                    var entryHash = await contract.GetFinalisedGroupEntry(checkGroupHash, k);
                    assert.equal(GetCheckHashSum(['' + (i + k), testEntries[i + k]]),
                                                 entryHash,
                                                 "hash should be the same");
                }
            }
        }
    });
});

contract("ProvedDBCheckValRepeatFail", function(accounts) {
    it("check value repeat", async function() {
        var contract = await ProvedDB.deployed();
        await contract.Create('test01', "{'mydata01': 'data01', 'mydata02': 'data02'}");
        await contract.Create('test02', "{'mydata01': 'data01', 'mydata02': 'data02'}");
    });
});
