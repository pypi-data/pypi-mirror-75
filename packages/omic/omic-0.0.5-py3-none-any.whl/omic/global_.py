#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Undifferentiated client; mainly user and util functionality."""

import json

from munch import munchify
import requests

from omic.client import Client
from omic.util import strict_http_do

__copyright__ = 'Copyright © 2020 Omic'

class GlobalClient(Client):

    def retrieve_project(self):
        return self._hit(
            'get',
            endpoint=f'{self.config.endpoint}/user/project'
        )

    def fulfill(self, obj):
        return self._hit('post',
                          endpoint=f'{self.config.endpoint}/util/fulfill', 
                          json_body=obj,
                          qparams={'user': self.config.user},
                          headers={'x-api-key': self.config.key})