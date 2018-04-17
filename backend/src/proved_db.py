#!/usr/bin/env python3
# encoding: utf-8

import os
import json
import my_config
from onchain_handler import OnChainHandler


class ProvedBaseDB():
    def create(self, entry):
        pass

    def retrieve(self, myid):
        pass

    def update(self, entry):
        pass

    def delete(self, myid):
        pass


class ProvedJsonDB(ProvedBaseDB):
    def __init__(self, path=''):
        self._path = path
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump({}, f)
            self._data = {}
        else:
            with open(path) as f:
                self._data = json.load(f)

    def create(self, entry):
        if 1 != len(list(entry)):
            raise IOError('input key should not more than one, {0}'.format(list(entry)))
        if list(entry)[0] in self._data:
            raise IOError('unique key already exist, {0}'.format(list(entry)))

        self._data.update(entry)
        with open(self._path, 'w') as f:
            json.dump(self._data, f)

    def retrieve(self, key):
        if key not in self._data:
            return ''
        else:
            return self._data[key]

    def update(self, entry):
        pass

    def delete(self, myid):
        pass


class ProvedDB():
    _support_types = {
        'json': ProvedJsonDB
    }

    def __init__(self, config=my_config.CONFIG_PATH, mytype='json', path=''):
        if not any(mytype == _ for _ in self._support_types.keys()):
            raise IOError('{0} type not in support_types {1}'.format(mytype, self._support_types))
        self._type_db = self._support_types[mytype](path)
        self._onchain_handler = OnChainHandler(config)

    def create(self, entry):
        self._type_db.create(entry)
        key, val = list(entry)[0], self._onchain_handler.hash_entry(entry)
        self._onchain_handler.create(key, val)

        # use retrive to check it
        retrieve_data = self.retrieve(key)
        if retrieve_data != entry[list(entry)[0]]:
            raise IOError('create fail...')

    def retrieve(self, key):
        db_data = self._type_db.retrieve(key)
        onchain_exist, onchain_data = self._onchain_handler.retrieve(key)
        if not onchain_exist:
            if db_data or onchain_data:
                raise IOError('key is not exist, shouldn\'t have any data, {0} v.s. {1}'.
                              format(onchain_data, db_data))
        else:
            db_hash = self._onchain_handler.hash_entry({key: db_data})
            if onchain_data != db_hash:
                raise IOError('hash value doens\'t consist, {0} v.s. {1}'.
                              format(onchain_data, db_hash))
        return db_data

    def update(self, entry):
        pass

    def delete(self, myid):
        pass


if __name__ == '__main__':
    ProvedDB(mytype='json')
