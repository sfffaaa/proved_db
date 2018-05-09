#!/usr/bin/env python3
# encoding: utf-8

import gevent
import my_config
from contract_handler import ContractHandler


class BaseChainNode(gevent.Greenlet):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 proved_db_callback_objs=[],
                 record_hash_callback_objs=[],
                 wait_time=3):
        super(BaseChainNode, self).__init__()
        self.wait_time = wait_time
        self._setup_proved_db(config_path, proved_db_callback_objs)
        self._setup_record_hash(config_path, record_hash_callback_objs)

    def _setup_proved_db(self, config_path, callback_objs):
        self._proved_db = {}
        self._proved_db['callback_objs'] = callback_objs
        self._proved_db['contract_handler'] = ContractHandler('ProvedDB', config_path)

        self._proved_db['submit_hash_event_filter'] = \
            self._proved_db['contract_handler']._contract_inst.events.submit_hash.createFilter(fromBlock='latest')

    def _setup_record_hash(self, config_path, callback_objs):
        self._record_hash = {}
        self._record_hash['callback_objs'] = callback_objs
        self._record_hash['contract_handler'] = ContractHandler('RecordHash', config_path)

        self._record_hash['record_over_event_filter'] = \
            self._record_hash['contract_handler']._contract_inst.events.record_over.createFilter(fromBlock='latest')

    def _run(self):
        while True:
            for event in self._proved_db['submit_hash_event_filter'].get_new_entries():
                for callback_obj in self._proved_db['callback_objs']:
                    callback_obj.submitHashEventCallback(self, event)

            for event in self._record_hash['record_over_event_filter'].get_new_entries():
                for callback_obj in self._record_hash['callback_objs']:
                    callback_obj.recordOverEventCallback(self, event)

            gevent.sleep(self.wait_time)


if __name__ == '__main__':
    base_chain_node = BaseChainNode()
    base_chain_node.start()
    base_chain_node.join()
