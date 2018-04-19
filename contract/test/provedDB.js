var ProvedDB = artifacts.require("ProvedDB");
const Web3 = require("web3")
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

    it("Delete all entry from end", async function() {
        var testKey = "test05";
        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Create(key, testElement[key]);
        }
        for (var i = TEST_DATA[testKey].length - 1; i >= 0; i--) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Delete(key);
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');

            for (var j = 0; j < i; j++) {
                var retrieveTestCase = TEST_DATA[testKey][j];
                var retrieveKey = Object.keys(retrieveTestCase)[0];
                var retrieveExistData = await contract.Retrieve.call(retrieveKey);
                assert.equal(retrieveExistData[0], true, 'key should exist');
                assert.equal(retrieveExistData[1], retrieveTestCase[retrieveKey], 'key should exist');
            }
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');

        }
    });

    it("Delete all entry from front", async function() {
        var testKey = "test06";
        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Create(key, testElement[key]);
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Delete(key);
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');

            for (var j = TEST_DATA[testKey].length - 1; j > i; j--) {
                var retrieveTestCase = TEST_DATA[testKey][j];
                var retrieveKey = Object.keys(retrieveTestCase)[0];
                var retrieveExistData = await contract.Retrieve.call(retrieveKey);
                assert.equal(retrieveExistData[0], true, 'key should exist');
                assert.equal(retrieveExistData[1], retrieveTestCase[retrieveKey], 'key should exist');
            }
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');
        }
    });
    it("Delete all entry from middle", async function() {
        var testKey = "test07";
        var contract  = await ProvedDB.deployed();
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Create(key, testElement[key]);
        }
        for (var i = 1; i < TEST_DATA[testKey].length - 1; i++) {
            var testElement = TEST_DATA[testKey][i];
            var key = Object.keys(testElement)[0];
            await contract.Delete(key);
            var retrieveNoExistData = await contract.Retrieve.call(key);
            assert.equal(retrieveNoExistData[0], false, 'key is deleted');
            assert.equal(await contract.CheckEntry.call(key, ''),
                         true, 'Cannot find the key, but compare with empty data, so should pass');
        }
        for (var i = 0; i < TEST_DATA[testKey].length; i++) {
            if (0 == i || 0 == TEST_DATA[testKey].length - 1) {
                var retrieveTestCase = TEST_DATA[testKey][i];
                var retrieveKey = Object.keys(retrieveTestCase)[0];
                var retrieveExistData = await contract.Retrieve.call(retrieveKey);
                assert.equal(retrieveExistData[0], true, 'key should exist');
                assert.equal(retrieveExistData[1], retrieveTestCase[retrieveKey], 'key should exist');
            }
        }
    });
});
