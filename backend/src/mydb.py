#!/usr/bin/env python3
# encoding: utf-8


class MyDB():
    _support_types = ['json']

    def __init__(self, mytype='json', path=''):
        if not any(mytype == _ for _ in self._support_types):
            raise IOError('{0} type not in support_types {1}'.format(mytype, self._support_types))
        pass

    def create(self, entry):
        pass

    def retrieve(self, my_filter):
        pass

    def update(self, entry):
        pass

    def delete(self, myid):
        pass


if __name__ == '__main__':
    MyDB(mytype='json')
