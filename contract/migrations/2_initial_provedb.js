var ProvedDB = artifacts.require("./ProvedDB");
var KeysRecord = artifacts.require("./KeysRecord");

module.exports = function(deployer) {
    deployer.deploy(KeysRecord).then(function() {
        return deployer.deploy(ProvedDB, 2, KeysRecord.address);
    });
};
