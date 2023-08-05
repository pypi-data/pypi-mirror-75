#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Client base class."""

import json

from munch import munchify, Munch
import requests

from .util import strict_http_do

__copyright__ = 'Copyright © 2020 Omic'

class Client:
    def __init__(self, config: dict):
        self.config = config

    def _hit(self, method: str, endpoint: str, qparams: dict = {}, 
             headers: dict = {}, json_body: dict = None, retry_count: int = 2,
             silent: bool = True) -> Munch:
        """Abstraction on all HTTP methods with our API."""
        qparams.update({'user': self.config.user})
        headers.update({'x-api-key': self.config.key})
        method_map = {
            'get': requests.get,
            'post': requests.post,
        }
        methodf = method_map[method.lower()]
        if not silent:
            print('—' * 100)
            print(f'Hitting {endpoint} ({method}):')
            print('Parameters:', json.dumps(qparams, indent=4))
            print('Body:', json.dumps(json_body, indent=4))
            print('—' * 100)
        return strict_http_do(lambda: methodf(endpoint, params=qparams, 
                                              headers=headers, json=json_body),
                              n=retry_count)
