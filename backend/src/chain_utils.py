from web3 import Web3


def convert_to_bytes(val):
    if bytes == type(val):
        return val
    elif val.startswith('0x'):
        return Web3.toBytes(hexstr=val)
    else:
        return Web3.toBytes(text=val)
