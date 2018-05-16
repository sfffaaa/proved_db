var ProvedDB = artifacts.require("./ProvedDB");
var ProvedCRUD = artifacts.require("./ProvedCRUD");
var KeysRecord = artifacts.require("./KeysRecord");
var FinaliseRecord = artifacts.require("./FinaliseRecord");
var EventEmitter = artifacts.require("./EventEmitter");

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
    });
};
