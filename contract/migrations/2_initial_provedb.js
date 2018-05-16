var ProvedDB = artifacts.require("./ProvedDB");
var ProvedCRUD = artifacts.require("./ProvedCRUD");
var KeysRecord = artifacts.require("./KeysRecord");
var FinaliseRecord = artifacts.require("./FinaliseRecord");
var EventEmitter = artifacts.require("./EventEmitter");
var RecordHash = artifacts.require("./RecordHash");
var RecordHashStorageV0 = artifacts.require("./RecordHashStorageV0");

module.exports = function(deployer) {
    deployer.deploy(KeysRecord).then(function() {
        return deployer.deploy(ProvedCRUD);
    }).then(function() {
        return deployer.deploy(EventEmitter);
    }).then(function() {
        return deployer.deploy(FinaliseRecord,
                               2,
                               EventEmitter.address);
    }).then(function() {
        return deployer.deploy(ProvedDB,
                               KeysRecord.address,
                               ProvedCRUD.address,
                               FinaliseRecord.address);
    }).then(function() {
        return deployer.deploy(RecordHashStorageV0);
    }).then(function() {
        return deployer.deploy(RecordHash,
                               EventEmitter.address,
                               RecordHashStorageV0.address);
    });
};
