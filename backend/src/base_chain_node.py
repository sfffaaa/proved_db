#!/usr/bin/env python3
# encoding: utf-8

import gevent
import my_config
from contract_handler import ContractHandler


class BaseChainNode(gevent.Greenlet):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 submit_hash_callback_objs=[],
                 record_over_callback_objs=[],
                 wait_time=3):
        super(BaseChainNode, self).__init__()
        self.wait_time = wait_time
        self._setup_event_emitter(config_path, submit_hash_callback_objs, record_over_callback_objs)

    def _setup_event_emitter(self, config_path, submit_hash_callback_objs, record_over_callback_objs):
        self._event_emitter = {}
        self._event_emitter['submit_hash_callback_objs'] = submit_hash_callback_objs
        self._event_emitter['record_over_callback_objs'] = record_over_callback_objs
        self._event_emitter['contract_handler'] = ContractHandler('EventEmitter', config_path)

        self._event_emitter['submit_hash_event_filter'] = \
            self._event_emitter['contract_handler']._contract_inst.events.submit_hash.createFilter(fromBlock='latest')

        self._event_emitter['record_over_event_filter'] = \
            self._event_emitter['contract_handler']._contract_inst.events.record_over.createFilter(fromBlock='latest')

    def _run(self):
        while True:
            for event in self._event_emitter['submit_hash_event_filter'].get_new_entries():
                for callback_obj in self._event_emitter['submit_hash_callback_objs']:
                    callback_obj.submitHashEventCallback(self, event)

            for event in self._event_emitter['record_over_event_filter'].get_new_entries():
                for callback_obj in self._event_emitter['record_over_callback_objs']:
                    callback_obj.recordOverEventCallback(self, event)

            gevent.sleep(self.wait_time)


if __name__ == '__main__':
    base_chain_node = BaseChainNode()
    base_chain_node.start()
    base_chain_node.join()
