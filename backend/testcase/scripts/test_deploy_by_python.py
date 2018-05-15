from web3 import Web3, IPCProvider
# from web3 import HTTPProvider
from solc import compile_source

# Solidity source code
with open('test.sol') as f:
    lines = f.readlines()
contract_source_code = ''.join(lines)

compiled_sol = compile_source(contract_source_code)  # Compiled source code
contract_interface = compiled_sol['<stdin>:KeysRecord']

# web3.py instance
# w3 = Web3(HTTPProvider('http://localhost:8545'))
w3 = Web3(IPCProvider('/Users/jaypan/private-eth/test3/datadir/geth.ipc'))

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0]})
w3.miner.start(1)

# Get tx receipt to get contract address
print('deploy')
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
import time
time.sleep(8)
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
w3.miner.stop()

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=contract_interface['abi'],
                                    address=contract_address)


contract_interface = compiled_sol['<stdin>:ProvedDB']

# Instantiate and deploy contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

print(contract_address)
# Get transaction hash from deployed contract
tx_hash = contract.constructor(contract_address).transact({'from': w3.eth.accounts[0]})
w3.miner.start(8)

# Get tx receipt to get contract address
print('deploy')
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
time.sleep(8)
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']
w3.miner.stop()

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=contract_interface['abi'],
                                    address=contract_address)


# Getters + Setters for web3.eth.contract object
print('test')
# tx_hash = contract_instance.functions.Create('a', 'b').transact({'from': w3.eth.accounts[0]})
# tx_hash = contract_instance.functions.Create('c', 'd').transact({'from': w3.eth.accounts[0]})
# print(tx_hash)
# w3.miner.start(1)
# time.sleep(10)
# w3.miner.stop()
# print(tx_receipt)
print(contract_instance.functions.GetKeysLength().call())
# print(Web3.toHex(data[1]))
# print(Web3.toHex(Web3.sha3(text='b')))
# # contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
# # print('Setting value to: Nihao')
# # time.sleep(30)
# # print('Contract value: {}'.format(contract_instance.greet()))
