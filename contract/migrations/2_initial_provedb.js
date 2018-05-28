var ProvedDB = artifacts.require("./ProvedDB");
var ProvedCRUD = artifacts.require("./ProvedCRUD");
var KeysRecord = artifacts.require("./KeysRecord");
var FinaliseRecord = artifacts.require("./FinaliseRecord");
var EventEmitter = artifacts.require("./EventEmitter");
var RecordHash = artifacts.require("./RecordHash");
var RecordHashStorageV0 = artifacts.require("./RecordHashStorageV0");
var FinaliseRecordStorageV0 = artifacts.require("./FinaliseRecordStorageV0");
var KeysRecordStorageV0 = artifacts.require("./KeysRecordStorageV0");
var ProvedCRUDStorageV0 = artifacts.require("./ProvedCRUDStorageV0");
var Register = artifacts.require("./Register");

function SetRegisterEntry(instance, allEntries) {
    for (var i = 0; i < allEntries.length; i++) {
        instance.SetInst(allEntries[i][0], allEntries[i][1]);
    }
};

function SetRegisterWhitelist(instance, allowWhiteLists) {
    for (var i = 0; i < allowWhiteLists.length; i++) {
        instance.SetWhitelist(allowWhiteLists[i]);
    }
};

async function SetAllRegisterRelatedInfo(instance) {
    await SetRegisterEntry(instance,
                           [["EventEmitter", EventEmitter.address],
                            ["ProvedCRUDStorageInterface", ProvedCRUDStorageV0.address],
                            ["KeysRecordStorageInterface", KeysRecordStorageV0.address],
                            ["FinaliseRecordInterface", FinaliseRecordStorageV0.address],
                            ["RecordHashStorageInterface", RecordHashStorageV0.address],
                            ["KeysRecord", KeysRecord.address],
                            ["ProvedCRUD", ProvedCRUD.address],
                            ["FinaliseRecord", FinaliseRecord.address]]);

    await SetRegisterWhitelist(instance,
                               [RecordHash.address,
                                ProvedDB.address,
                                KeysRecord.address,
                                ProvedCRUD.address,
                                FinaliseRecord.address,
                                ProvedCRUDStorageV0.address,
                                KeysRecordStorageV0.address,
                                FinaliseRecordStorageV0.address,
                                RecordHashStorageV0.address]);
};

module.exports = function(deployer) {
    var register_inst;
    deployer.deploy(Register).then(function(inst) {
        register_inst = inst;
        return deployer.deploy(EventEmitter,
                               Register.address);
    }).then(function(inst) {
        return deployer.deploy(ProvedCRUDStorageV0,
                               Register.address);
    }).then(function() {
        return deployer.deploy(ProvedCRUD,
                               Register.address);
    }).then(function() {
        return deployer.deploy(KeysRecordStorageV0,
                               Register.address);
    }).then(function() {
        return deployer.deploy(KeysRecord,
                               Register.address);
    }).then(function() {
        return deployer.deploy(FinaliseRecordStorageV0,
                               Register.address);
    }).then(function() {
        return deployer.deploy(FinaliseRecord,
                               2,
                               Register.address);
    }).then(function() {
        return deployer.deploy(ProvedDB,
                               Register.address);
    }).then(function() {
        return deployer.deploy(RecordHashStorageV0,
                               Register.address);
    }).then(function() {
        return deployer.deploy(RecordHash,
                               Register.address);
    }).then(function() {
        SetAllRegisterRelatedInfo(register_inst);
    });
};
