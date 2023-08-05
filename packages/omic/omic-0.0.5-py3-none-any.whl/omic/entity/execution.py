#!/usr/bin/env python3
# -.- coding: utf-8 -.-

import json

from munch import munchify, Munch
import requests

from omic.client import Client
from omic.util import strict_http_do

__copyright__ = 'Copyright © 2020 Omic'

class ExecutionClient(Client):

    def delete(self, _id: str):
        pass

    # def retrieve(self, _id: str = None, fulfill: bool = False, recurse: bool = False):
    #     endpoint = f'{self.config.endpoint}/execution'
    #     params = {
    #         'user': self.config.user,
    #         '_id': _id, 
    #         'fulfill': fulfill, 
    #         'recurse': recurse
    #     }
    #     return self._hit('get', endpoint=endpoint, qparams=params)

    def execute(self):
        # requests.post(f'{API_BASE}/execution', params={
        #     'user': user,
        #     '_id': _id, 
        #     'fulfill': fulfill, 
        #     'recurse': recurse
        # })
        pass

    def update_status(self, _id: str, status: str):
        endpoint = f'{self.config.endpoint}/execution/{_id}/status'
        return self._hit('post',
                         endpoint=endpoint, 
                         json_body=status)

    def add_trace(self, _id: str, tracepoint: str, struct: dict = None, 
                  status: str = None, input=None, output=None, log=None, 
                  depth: int = None, stage: int = None):
        endpoint = f'{self.config.endpoint}/execution/{_id}/trace'
        payload = {'tracepoint': tracepoint}
        if struct:
            payload.update({'struct': struct})
        if status:
            payload.update({'status': status})
        if input:
            payload.update({'input': input})
        if output:
            payload.update({'output': output})
        if log:
            payload.update({'log': log})
        if depth is not None:
            payload.update({'depth': depth})
        if stage is not None:
            payload.update({'stage': stage})
        qparams = {'user': self.config.user}
        return strict_http_do(lambda: requests.post(endpoint, \
                              json=payload, params=qparams, 
                              headers={'x-api-key': self.config.key}))

    def retrieve_traces(self, _id: str):
        qparams = {'user': self.config.user}
        endpoint = f'{self.config.endpoint}/execution/{_id}/trace' 
        return strict_http_do(lambda: requests.get(endpoint, \
                              params=qparams, 
                              headers={'x-api-key': self.config.key}))

    def transfer_inputs(self, data: str):
        qparams = {'user': self.config.user}
        endpoint = f'{self.config.endpoint}/execution/cromwell/transfer'
        return strict_http_do(lambda: requests.post(endpoint, \
                              json=data, params=qparams, 
                              headers={'x-api-key': self.config.key}))._id

    def retrieve_transferred_inputs(self, _id: str):
        qparams = {'user': self.config.user, '_id': _id}
        endpoint = f'{self.config.endpoint}/execution/cromwell/transfer'
        return strict_http_do(lambda: requests.get(endpoint,
                              params=qparams,
                              headers={'x-api-key': self.config.key}))

    """Other bioinformatics engines:"""

    def execute_wdl(self, fields: dict, inputs: str):
        return hit('post', 
                   endpoint=f'{self.config.endpoint}/execution/cromwell',
                   qparams={'user': self.config.user}, 
                   headers={'x-api-key': self.config.key},
                   json_body={'inputs': inputs, 'fields': fields})._id

    def retrieve_wdl(self, _id: str) -> Munch:
        """Get cromwell status, output, and logs."""
        results = Munch()
        qparams = {'user': self.config.user, '_id': _id}
        headers = {'x-api-key': self.config.key}
        endpoint = f'{self.config.endpoint}/execution/cromwell/status'
        results.status = hit('get',
                             endpoint=endpoint,
                             qparams=qparams, 
                             headers=headers).status.lower()
        endpoint = f'{self.config.endpoint}/execution/cromwell/output'
        results.output = hit('get',
                             endpoint=endpoint,
                             qparams=qparams, 
                             headers=headers).output
        endpoint = f'{self.config.endpoint}/execution/cromwell/log'
        results.log = hit('get',
                          endpoint=endpoint,
                          qparams=qparams, 
                          headers=headers)
        return results