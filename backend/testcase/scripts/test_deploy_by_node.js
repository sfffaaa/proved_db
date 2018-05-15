const fs = require('fs');
const solc = require('solc');
const Web3 = require('web3');
const net = require('net');
//const web3Admin = require('web3admin');

// const web3 = new Web3(new Web3.providers.IpcProvider('/Users/jaypan/private-eth/test2/node1/blockchainData/geth.ipc', net));
const web3 = new Web3(new Web3.providers.IpcProvider('/Users/jaypan/private-eth/test3/datadir/geth.ipc', net));
// const web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8545'));
// const web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:8042'));

const input = fs.readFileSync('test.sol');
const output = solc.compile(input.toString(), 0);

const keysRecordBytecode = output.contracts[':KeysRecord'].bytecode;
const keysRecordABI = JSON.parse(output.contracts[':KeysRecord'].interface);

const provedDBBytecode = output.contracts[':ProvedDB'].bytecode;
const provedDBABI = JSON.parse(output.contracts[':ProvedDB'].interface);

web3.extend({
    property: 'miner',
    methods:
    [{
        name: 'start',
        call: 'miner_start',
        params: 1,
        inputFormatter: [web3.extend.formatters.formatInputInt],
        outputFormatter: web3.extend.formatters.formatOutputBool
    }, {
        name: 'stop',
        call: 'miner_stop',
        params: 1,
        inputFormatter: [web3.extend.formatters.formatInputInt],
        outputFormatter: web3.extend.formatters.formatOutputBool
    }]
});


async function Deploy() {
    console.log('----------- KeysRecord -----------');
    var coinbase = await web3.eth.getCoinbase();
    var keysRecordContract = new web3.eth.Contract(keysRecordABI, null, {from: coinbase});
    web3.miner.start();
    var error, transactionHash = await keysRecordContract.deploy({
        data: '0x' + keysRecordBytecode,
    }).send({
        from: coinbase,
        gas: 265543
    }, function(error, transactionHash){
        console.log(transactionHash);
    });
    console.log(error);
    console.log(transactionHash.options.address);
    keysRecordContract = new web3.eth.Contract(keysRecordABI, transactionHash.options.address, {from: coinbase});
    data = await keysRecordContract.methods.GetKeysLength().call({from: coinbase});
    console.log(data);

    console.log('----------- ProvedDB -----------');
    var provedDBContract = new web3.eth.Contract(provedDBABI, null, {from: coinbase});
    error, transactionHash = await provedDBContract.deploy({
        arguments: [transactionHash.options.address],
        data: '0x' + provedDBBytecode,
    }).send({
        from: coinbase,
        gas: 265543
    }, function(error, transactionHash){
        console.log(transactionHash);
    });

    web3.miner.stop();

    console.log(error);
    console.log(transactionHash.options.address);
    provedDBContract = new web3.eth.Contract(provedDBABI, transactionHash.options.address, {from: coinbase});

    console.log('----------- Delopy over -----------');
    console.log(await provedDBContract.methods.GetAddr().call({from: coinbase, gas: 90000*3}))
    var lengthData = await provedDBContract.methods.GetKeysLength().call({from: coinbase, gas: 90000*3})
    console.log(lengthData);
}

Deploy();
