var ProvedDB = artifacts.require("ProvedDB");
const Web3 = require("web3")
var NON_EXIST_KEY = "aabbccddeeff";
var TEST_DATA = {
    'test01': ['hash1'],
    'test02': ['hash1', 'hash2', 'hash3'],
    'test03': ['hash1']
};

function CheckNotExist(ret) {
    assert.equal(ret[0], false, "key not exist, so return the key not exist");
    assert.equal(ret[1].toString(), "", "key not exist, so return empty data");
}

function CheckExist(ret, checkKey, checkValue) {
    assert.equal(ret[0], true, "key exist, so return the key exist " + checkKey);
    assert.equal(ret[1].toString(), checkValue, "key exist, so return value " + checkValue);
}


contract("ProvedDB", function(accounts) {

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
});
