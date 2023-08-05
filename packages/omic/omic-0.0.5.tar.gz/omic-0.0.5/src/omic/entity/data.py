#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Handles all data-related features."""

from pathlib import Path
import functools
import json
import os

from munch import munchify, Munch
import requests

from omic.client import Client
from omic.global_ import GlobalClient
from omic.parallel import run_parallel 
from omic.util import strict_http_do, check_args, get_cloud, \
                      download_url, vfs_path_join

__copyright__ = 'Copyright © 2020 Omic'

class DataClient(Client):
    def __init__(self, config: dict):
        self.config = config

    def create_bundle(self: object, files: list, vpath: str, mode: str, 
                      project: str, safe: bool = False) -> str:
        workload = [functools.partial(self.mount_data, rpath, vpath, mode, 
                                      project, safe) for rpath in files]
        file_ids = run_parallel(workload, batch_size=15)
        return hit('post',
                   endpoint=f'{self.config.endpoint}/data/bundle',
                   qparams={
                       'user': self.config.user, 
                       'mode': mode, 
                       'project': project
                   },
                   json_body={'data': file_ids},
                   headers={'x-api-key': self.config.key})._id

    # NOTE:  Formally `mount_data`.
    def mount(self, rpath: str, vpath: str, mode: str, project: str, 
              safe: bool = False):
        # TODO:  Add a parameter to preserve structure of rpath 
        #        (under mount key).  Right now we have flattened `vpath`s.
        qparams = {
            'user': self.config.user, 
            'mode': mode,
            'project': project,
            'cmd': 'mount',
            'repr': 'file',
            'mode': mode,
            'vpath': vpath, 
            'rpath': rpath,
            'safe': safe
        }
        print('Mount data:', rpath, '->', vpath)
        return self._hit('post',
                         endpoint=f'{self.config.endpoint}/data',
                         qparams=qparams,
                         headers={'x-api-key': self.config.key}).id

    def ls(
        self, 
        vpath: str = './', 
        mode: str = 'public', 
        project: str = None,
        silent=False
    ):
        if not project:
            # Fetch current project from user if none exists.
            gclient = GlobalClient(self.config)
            project = gclient.retrieve_project().project._id
        files = self._hit(
            'get',
            endpoint=f'{self.config.endpoint}/data',
            qparams={
                'cmd': 'ls', 'vpath': vpath, 'mode': mode,
                'project': project,  
            }
        )
        print('files', files)
        for f in files:
            print(' >', f.vpath)
        return files

    # NOTE:  Formally `get_data`.
    def stat(self, **kwargs) -> Munch:
        return self._hit(
            'get',
            endpoint=f'{self.config.endpoint}/data',
            qparams={'cmd': 'stat', **kwargs}
        )

    def upload(self, *args, **kwargs):
        pass

    def _download_file(
        self, 
        _id: str = None, 
        vpath: str = '/', 
        mode: str = 'public', 
        project: str = None, 
        repr: str = 'file',
        download_dir: str = './', 
        silent=False
    ) -> None:
        # Stat the file
        s = self.stat(_id=_id)
        # Setup local path location
        lp = s.vpath[len(vpath):]
        lp = lp[1:] if lp.startswith('/') else lp
        lp = vfs_path_join(download_dir, lp) 
        lp = str(Path(lp).resolve())
        ldirs, filename = os.path.split(lp)
        Path(ldirs).mkdir(parents=True, exist_ok=True)
        # Download file in parallel
        download_url(s.url, lp, silent=silent, desc=filename)

    def download(
        self, 
        vpath: str = None, 
        _id: str = None, 
        mode: str = 'public', 
        project: str = None, 
        download_dir: str = './', 
        silent=False
    ) -> None:
        assert _id or vpath
        if _id:
            self._download_file(_id, download_dir=download_dir)
            print('File download complete.')
            return
        for f in self.ls(vpath=vpath, mode=mode, project=project):
            try:
                self._download_file(_id=f._id, download_dir=download_dir)
            except Exception as ex:
                print(f'Could not download {f.name}.', ex)
                return
        print('Download complete.')

    def get_bundle(self, user: str, _id: str, fulfill=False, recurse=False):
        def _func():
            return requests.get(
                f'{API_BASE}/data/bundle', params={
                '_id': _id,
                'user': user,
                'fulfill': fulfill, 
                'recurse': recurse
            })
        return strict_http_do(_func)

    def get_bundle_or_data(self, user: str, _id: str, fulfill=False, 
                           recurse=False):
        data = get_data(user, _id)
        if not data:
            return get_bundle(user, _id, fulfill, recurse) 
        return data 
