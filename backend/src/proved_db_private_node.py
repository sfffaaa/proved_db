#!/usr/bin/env python3
# encoding: utf-8

import gevent
import my_config
from contract_handler import ContractHandler


class ProvedDBPrivateChainNode(gevent.Greenlet):

    def __init__(self, config_path=my_config.CONFIG_PATH, callback_objs=[], wait_time=3):
        super(ProvedDBPrivateChainNode, self).__init__()
        self.callback_objs = callback_objs
        self.wait_time = wait_time

        self._contract_handler = ContractHandler('ProvedDB', config_path)
        self._w3 = self._contract_handler.get_w3()
        self._contract_inst = self._contract_handler.get_contract()
        self._contract_event_inst = self._contract_handler._contract_event_inst

        self.smart_hash_event_filter = self._contract_event_inst.events.submit_hash.createFilter(fromBlock='latest')

    def _run(self):
        while True:
            for event in self.smart_hash_event_filter.get_new_entries():
                for callback_obj in self.callback_objs:
                    callback_obj.submitHashEventCallback(self, event)
            gevent.sleep(self.wait_time)


if __name__ == '__main__':
    private_chain_node = ProvedDBPrivateChainNode()
    private_chain_node.start()
    private_chain_node.join()
