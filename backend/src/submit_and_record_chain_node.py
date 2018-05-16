#!/usr/bin/env python3
# encoding: utf-8

from base_chain_node import BaseChainNode
import my_config
from record_hash import RecordHash
from proved_db import ProvedDB


class SubmitAndRecordChainNode(BaseChainNode):

    def __init__(self,
                 config_path=my_config.CONFIG_PATH,
                 submit_hash_callback_objs=[],
                 record_over_callback_objs=[],
                 wait_time=3):
        self._record_hash_mgr = RecordHash(config_path)
        self._proved_db_mgr = ProvedDB(config_path, 'json')
        submit_hash_callback_objs = [self] + submit_hash_callback_objs
        record_over_callback_objs = [self] + record_over_callback_objs
        super(SubmitAndRecordChainNode, self).__init__(config_path,
                                                       submit_hash_callback_objs,
                                                       record_over_callback_objs,
                                                       wait_time)

    def submitHashEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._record_hash_mgr.record(event_finalise_hash)

    def recordOverEventCallback(self, node, event):
        event_finalise_hash = event['args']['finalise_hash']
        self._proved_db_mgr.finalise(event_finalise_hash)


if __name__ == '__main__':
    chain_node = SubmitAndRecordChainNode()
    chain_node.start()
    chain_node.join()
