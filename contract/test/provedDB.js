var ProvedDB = artifacts.require("ProvedDB");
const BigNumber = require('bignumber.js');
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
    }]

};

function CheckNotExist(ret) {
    assert.equal(ret[0], false, "key not exist, so return the key not exist");
    assert.equal(ret[1].toString(),
                 0x0000000000000000000000000000000000000000000000000000000000000000,
                 "key not exist, so return empty data");
}

function CheckExist(ret, checkKey, checkValue) {
    assert.equal(ret[0], true, "key exist, so return the key exist " + checkKey);
    assert.equal(ret[1].toString(), web3.sha3(checkValue),
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


