#!/usr/bin/env python3
# -.- coding: utf-8 -.-

import json

from munch import munchify
import requests

from ..util import strict_http_do 

__copyright__ = 'Copyright © 2020 Omic'

class GraphClient:
    def __init__(self, config: dict):
        self.config = config

    def get(self, _id: str, fulfill: bool = False, recurse: bool = False):
        return strict_http_do(lambda: requests.get(
            f'{self.config.endpoint}/graph', 
            params={
                'user': self.config.user,
                '_id': _id, 
                'fulfill': fulfill, 
                'recurse': recurse
            },
            headers={'x-api-key': self.config.key}
        ))

    # TODO
    def post_graph(user, graph):
        def _func():
            return requests.post(f'{API_BASE}/graph', params={'user': user}, \
                                json=graph)
        return strict_http_do(_func)