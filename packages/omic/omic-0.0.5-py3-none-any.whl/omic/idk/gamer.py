#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Omic's Genome And MEdical Record DataBase (GAMER-DB) clinical data interface.

TODO:  
    - Move this interface to the Omic client (and thus API).
"""

import pandas as pd

import gisaid

class Gamer(object):
    
    def __init__(self):
        pass
    
    def _fetch_data(self) -> tuple:
        data = pd.read_csv('data_results.csv')
        for col in data.columns:
            print(col)
        X, y = gisaid.tx(data)
        return X, y
    
    def fetch_training_data(self, n: int = None) -> tuple:
        # TODO:  Update this to pull directly from Redshift.
        X, y = self._fetch_data()
        return X, y
    
    def fetch_testing_data(self, n: int = None) -> tuple:
        X, y = self._fetch_data()
        return X, y