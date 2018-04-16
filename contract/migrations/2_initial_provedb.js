var ProvedDB = artifacts.require("./ProvedDB");

module.exports = function(deployer) {
  deployer.deploy(ProvedDB);
};
