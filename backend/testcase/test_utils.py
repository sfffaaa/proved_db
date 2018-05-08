from config_handler import ConfigHandler
from web3 import Web3
import os
import errno

ZERO_VALUE = '0x' + '0' * 64
_TEST_CONFIG = 'testcase/etc/test_config.conf'


def get_db_path(config):
    config_handler = ConfigHandler(config)
    return config_handler.get_chain_config('DB', 'db_path')


def calculate_submit_hash(input_vals):
    compose_hash = []
    for vals in input_vals:
        hash_sums = [Web3.toInt(Web3.sha3(text=str(val)))
                     for val in vals]
        compose_hash.append(Web3.toInt(Web3.sha3(sum(hash_sums) & (2 ** 256 - 1))))

    return Web3.toHex(Web3.sha3(sum(compose_hash) & (2 ** 256 - 1)))


def unlink_silence(path):
    try:
        os.unlink(path)
        return True
    except OSError as e:
        if e.errno == errno.ENOENT:
            return True
    return False
