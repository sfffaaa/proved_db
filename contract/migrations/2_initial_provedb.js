var ProvedDB = artifacts.require("./ProvedDB");
var ProvedCRUD = artifacts.require("./ProvedCRUD");
var KeysRecord = artifacts.require("./KeysRecord");
var FinaliseRecord = artifacts.require("./FinaliseRecord");

module.exports = function(deployer) {
    deployer.deploy(KeysRecord).then(function() {
        return deployer.deploy(ProvedCRUD);
    }).then(function() {
        return deployer.deploy(FinaliseRecord, 2);
    }).then(function() {
        return deployer.deploy(ProvedDB,
                               KeysRecord.address,
                               ProvedCRUD.address,
                               FinaliseRecord.address);
    });
};
