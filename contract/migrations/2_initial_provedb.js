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


module.exports = function(deployer) {
    var register_inst;
    deployer.deploy(Register).then(function(inst) {
        register_inst = inst;
        return deployer.deploy(EventEmitter);
    }).then(function(inst) {
        return deployer.deploy(ProvedCRUDStorageV0);
    }).then(function() {
        return deployer.deploy(ProvedCRUD,
                               Register.address);
    }).then(function() {
        return deployer.deploy(KeysRecordStorageV0);
    }).then(function() {
        return deployer.deploy(KeysRecord,
                               Register.address);
    }).then(function() {
        return deployer.deploy(FinaliseRecordStorageV0);
    }).then(function() {
        return deployer.deploy(FinaliseRecord,
                               2,
                               Register.address);
    }).then(function() {
        return deployer.deploy(ProvedDB,
                               Register.address);
    }).then(function() {
        return deployer.deploy(RecordHashStorageV0);
    }).then(function() {
        return deployer.deploy(RecordHash,
                               Register.address);
    }).then(function() {
        return register_inst.SetInst("EventEmitter", EventEmitter.address);
    }).then(function() {
        return register_inst.SetInst("ProvedCRUDStorageInterface", ProvedCRUDStorageV0.address);
    }).then(function() {
        return register_inst.SetInst("KeysRecordStorageInterface", KeysRecordStorageV0.address);
    }).then(function() {
        return register_inst.SetInst("FinaliseRecordInterface", FinaliseRecordStorageV0.address);
    }).then(function() {
        return register_inst.SetInst("RecordHashStorageInterface", RecordHashStorageV0.address);
    }).then(function() {
        return register_inst.SetInst("KeysRecord", KeysRecord.address);
    }).then(function() {
        return register_inst.SetInst("ProvedCRUD", ProvedCRUD.address);
    }).then(function() {
        return register_inst.SetInst("FinaliseRecord", FinaliseRecord.address);
    });
};
