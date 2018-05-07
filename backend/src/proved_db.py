#!/usr/bin/env python3
# encoding: utf-8

import os
import json
import my_config
from proved_db_onchain_handler import ProvedDBOnChainHandler
from config_handler import ConfigHandler
ZERO_VALUE = '0x' + '0' * 64


class ProvedBaseDB():
    def create(self, entry):
        pass

    def retrieve(self, myid):
        pass

    def update(self, entry):
        pass

    def delete(self, myid):
        pass

    def get_keys(self):
        pass

    def check_entry(self, key, val):
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
        if 1 != len(list(entry)):
            raise IOError('input key should not more than one, {0}'.format(list(entry)))
        if list(entry)[0] not in self._data:
            raise IOError('unique key does not exist, {0}'.format(list(entry)))
        self._data.update(entry)
        with open(self._path, 'w') as f:
            json.dump(self._data, f)

    def delete(self, key):
        if key not in self._data:
            return
        del self._data[key]
        with open(self._path, 'w') as f:
            json.dump(self._data, f)

    def check_entry(self, key, val):
        if key not in self._data:
            return False
        if self._data[key] != val:
            return False
        return True

    def get_keys(self):
        return list(self._data.keys())


class ProvedDB():
    _support_types = {
        'json': ProvedJsonDB
    }

    def __init__(self, config=my_config.CONFIG_PATH, mytype='json', path=''):
        if not any(mytype == _ for _ in self._support_types.keys()):
            raise IOError('{0} type not in support_types {1}'.format(mytype, self._support_types))
        if not path:
            config_handler = ConfigHandler(config)
            path = config_handler.get_chain_config('DB', 'db_path')
        self._type_db = self._support_types[mytype](path)
        self._onchain_handler = ProvedDBOnChainHandler(config)

    def create(self, entry):
        self._type_db.create(entry)
        key = list(entry)[0]
        val = entry[key]
        self._onchain_handler.create(key, val)

        # use retrive to check it
        retrieve_data = self.retrieve(key)
        if retrieve_data != entry[list(entry)[0]]:
            raise IOError('create fail...')

    def retrieve(self, key):
        db_data = self._type_db.retrieve(key)
        onchain_exist, onchain_hash = self._onchain_handler.retrieve(key)
        if not onchain_exist:
            if db_data or onchain_hash != ZERO_VALUE:
                raise IOError('key "{0}" is not exist, shouldn\'t have any data, {1} v.s. {2}'.
                              format(key, onchain_hash, db_data))
        else:
            db_hash = self._onchain_handler.hash_entry(db_data)
            if onchain_hash != db_hash:
                raise IOError('hash value doens\'t consist, {0} v.s. {1}'.
                              format(onchain_hash, db_hash))
        return db_data

    def update(self, entry):
        self._type_db.update(entry)

        key = list(entry)[0]
        val = entry[key]
        self._onchain_handler.update(key, val)

        retrieve_data = self.retrieve(key)
        if retrieve_data != val:
            raise IOError('update fail...')

    def delete(self, key):
        self._type_db.delete(key)
        self._onchain_handler.delete(key)

    def check_entry(self, key, val):
        if not self._type_db.check_entry(key, val):
            return False
        if not self._onchain_handler.check_entry(key, val):
            return False
        return True

    def check_all_entries(self):
        data_keys = [_ for _ in self._type_db.get_keys()]
        online_keys = [self._onchain_handler.get_key(idx)
                       for idx in range(self._onchain_handler.get_keys_length())]

        if set(data_keys) != set(online_keys):
            return False

        for key in data_keys:
            data_val = self._type_db.retrieve(key)
            if not self._onchain_handler.check_entry(key, data_val):
                return False

        return True

    def get_finalise_entries_length(self, hash_sum):
        return self._onchain_handler.get_finalise_entries_length(hash_sum)

    def get_finalise_entry(self, hash_sum, idx):
        return self._onchain_handler.get_finalise_entry(hash_sum, idx)

    def finalise(self, hash_sum):
        self._onchain_handler.finalise(hash_sum)

    def get_finalised_group_entries_length(self, hash_sum):
        return self._onchain_handler.get_finalised_group_entries_length(hash_sum)

    def get_finalised_group_entry(self, hash_sum, idx):
        return self._onchain_handler.get_finalised_group_entry(hash_sum, idx)


if __name__ == '__main__':
    ProvedDB(mytype='json')
