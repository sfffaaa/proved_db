#!/usr/bin/env python3
# encoding: utf-8

import my_config
from register_onchain_handler import RegisterOnChainHandler


class Register():

    def __init__(self, config=my_config.CONFIG_PATH):
        self._onchain_handler = RegisterOnChainHandler(config)

    def set_register(self, name, address):
        self._onchain_handler.set_register(name, address)

    def set_multiple_register(self, name_dict):
        self._onchain_handler.set_multiple_register(name_dict)

    def get_register(self, name):
        return self._onchain_handler.get_register(name)

    def set_whitelist(self, address):
        self._onchain_handler.set_whitelist(address)

    def set_multiple_whitelist(self, addresses):
        self._onchain_handler.set_multiple_whitelist(addresses)


if __name__ == '__main__':
    Register()
