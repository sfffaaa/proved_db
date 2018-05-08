from web3 import Web3


def calculate_entry_hash(input_vals):
    hash_sums = [Web3.toInt(Web3.sha3(text=str(val))) for val in input_vals]
    return Web3.toHex(Web3.sha3(sum(hash_sums) & (2 ** 256 - 1)))


def convert_to_bytes(val):
    if bytes == type(val):
        return val
    elif val.startswith('0x'):
        return Web3.toBytes(hexstr=val)
    else:
        return Web3.toBytes(text=val)
