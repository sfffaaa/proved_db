#!/usr/bin/env python3
# encoding: utf-8

import gevent
import my_config
from web3 import Web3
from contract_handler import ContractHandler
from record_hash import RecordHash
from proved_db import ProvedDB


class ProvedDBPrivateChainNode(gevent.Greenlet):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 proved_db_callback_objs=[],
                 record_hash_callback_objs=[],
                 wait_time=3):
        super(ProvedDBPrivateChainNode, self).__init__()
        self.wait_time = wait_time
        self._setup_proved_db(config_path, proved_db_callback_objs)
        self._setup_record_hash(config_path, record_hash_callback_objs)

    # [TODO] Need to refine..
    def _setup_proved_db(self, config_path, callback_objs):
        self._proved_db = {}
        self._proved_db['callback_objs'] = callback_objs
        self._proved_db['contract_handler'] = ContractHandler('ProvedDB', config_path)
        self._proved_db['w3'] = self._proved_db['contract_handler'].get_w3()
        self._proved_db['contract_inst'] = self._proved_db['contract_handler'].get_contract()
        self._proved_db['contract_event_inst'] = self._proved_db['contract_handler']._contract_event_inst

        self._proved_db['submit_hash_event_filter'] = \
            self._proved_db['contract_event_inst'].events.submit_hash.createFilter(fromBlock='latest')

    def _setup_record_hash(self, config_path, callback_objs):
        self._record_hash = {}
        self._record_hash['callback_objs'] = callback_objs
        self._record_hash['contract_handler'] = ContractHandler('RecordHash', config_path)
        self._record_hash['w3'] = self._record_hash['contract_handler'].get_w3()
        self._record_hash['contract_inst'] = self._record_hash['contract_handler'].get_contract()
        self._record_hash['contract_event_inst'] = self._record_hash['contract_handler']._contract_event_inst

        self._record_hash['record_over_event_filter'] = \
            self._record_hash['contract_event_inst'].events.record_over.createFilter(fromBlock='latest')

    def _run(self):
        while True:
            for event in self._proved_db['submit_hash_event_filter'].get_new_entries():
                for callback_obj in self._proved_db['callback_objs']:
                    callback_obj.submitHashEventCallback(self, event)

            for event in self._record_hash['record_over_event_filter'].get_new_entries():
                for callback_obj in self._record_hash['callback_objs']:
                    callback_obj.recordOverEventCallback(self, event)

            gevent.sleep(self.wait_time)


class SubmitAndRecordChainNode(ProvedDBPrivateChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 proved_db_callback_objs=[],
                 record_hash_callback_objs=[],
                 wait_time=3):
        self._record_hash_mgr = RecordHash(config_path)
        self._proved_db_mgr = ProvedDB(config_path, 'json')
        proved_db_callback_objs = [self] + proved_db_callback_objs
        record_hash_callback_objs = [self] + record_hash_callback_objs
        super(SubmitAndRecordChainNode, self).__init__(config_path,
                                                       proved_db_callback_objs,
                                                       record_hash_callback_objs,
                                                       wait_time)

    def submitHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        # [TODO] should let record/finalise allow byte code...
        self._record_hash_mgr.record(Web3.toHex(event_finalise_hash))

    def recordOverEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._proved_db_mgr.finalise(Web3.toHex(event_finalise_hash))


if __name__ == '__main__':
    private_chain_node = ProvedDBPrivateChainNode()
    private_chain_node.start()
    private_chain_node.join()
