#!/usr/bin/env python3
# encoding: utf-8

import my_config
from record_hash_onchain_handler import RecordHashOnChainHandler


class RecordHash():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = RecordHashOnChainHandler(config)

    def record(self, input_hash):
        self._onchain_handler.record(input_hash)

    def get(self, input_hash):
        return self._onchain_handler.get(input_hash)


if __name__ == '__main__':
    RecordHash()
