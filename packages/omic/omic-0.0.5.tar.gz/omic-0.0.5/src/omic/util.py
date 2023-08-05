#!/usr/bin/env python3
# -.- coding: utf-8 -.-

from urllib.parse import urlparse, quote
import json
import os
import requests
import sys
import time

from munch import munchify, Munch
from urllib.request import urlopen
import humps
import requests
import tqdm
import validators

from omic.const import *

__copyright__ = 'Copyright © 2020 Omic'

def retry(f, n=5, *args, **kwargs):
    """Basic exponential retry.  Throw exception after we've retried 
    sufficiently.
    """
    last_ex = None
    for i in range(n):
        try:
            response = f(*args, **kwargs)
            assert 200 <= response.status_code < 300, response.text
            return response
        except Exception as ex:
            last_ex = ex
            time.sleep(2 ** i)
    raise ValueError(f'Retry failed:  {repr(last_ex)}') 

def strict_http_do(f, n=5):
    """Ensure we retry the request and it eventually succeeds."""
    response = retry(f, n)
    if hasattr(response, 'text') and len(response.text.strip()) > 0:
        return munchify(json.loads(response.text))
    return None

def get_cloud(rpath):
    if rpath.strip().startswith('gs://'):
        return 'gcp'
    elif rpath.strip().startswith('s3://'):
        return 'aws'
    else:
        raise ValueError('Cloud address not recognized.')

def check_args(kwargs, args):
    kwargs_set = set(kwargs.keys())
    assert kwargs_set.issubset(args), \
           'Unsupported arguments "{}" found.'.format(args - kwargs_set)

def split_rpath(rpath):
    """Return rpath object bucket and key."""
    o = urlparse(rpath, allow_fragments=False)
    bucket, key = o.netloc, o.path[1:]
    return bucket, key

def vfs_path_join(*args):
    """A path join that works as expected."""
    if len(args) == 1:
        return args.pop()
    parent = args[0]
    rest = [arg[1:] if arg.startswith('/') else arg for arg in args[1:]] 
    return os.path.join(parent, *rest)

class FileDownloader(object):

    def get_url_filename(self, url):
        """
        Discover file name from HTTP URL, If none is discovered derive name from http redirect HTTP content header Location
        :param url: Url link to file to download
        :type url: str
        :return: Base filename
        :rtype: str
        """
        try:
            if not validators.url(url):
                raise ValueError('Invalid url')
            filename = os.path.basename(url)
            basename, ext = os.path.splitext(filename)
            if ext:
                return filename
            header = requests.head(url, allow_redirects=False).headers
            return os.path.basename(header.get('Location')) if 'Location' in header else filename
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            raise errh
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            raise errc
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            raise errt
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            raise err

    def download_file(self, url, filename=None, target_dir=None, desc=None):
        """
        Stream downloads files via HTTP
        :param url: Url link to file to download
        :type url: str
        :param filename: filename overrides filename defined in Url param
        :type filename: str
        :param target_dir: target destination directory to download file to
        :type target_dir: str
        :return: Absolute path to target destination where file has been downloaded to
        :rtype: str
        """
        if target_dir and not os.path.isdir(target_dir):
            raise ValueError('Invalid target_dir={} specified'.format(target_dir))
        local_filename = self.get_url_filename(url) if not filename else filename

        req = requests.get(url, stream=True)
        file_size = int(req.headers['Content-Length'])
        chunk_size = 1024  # 1 MB
        num_bars = int(file_size / chunk_size)

        base_path = os.path.abspath(os.path.dirname(__file__))
        target_dest_dir = os.path.join(base_path, local_filename) \
                          if not target_dir \
                          else os.path.join(target_dir, local_filename)
        desc = local_filename if not desc else desc
        with open(target_dest_dir, 'wb') as fp:
            for chunk in tqdm.tqdm(req.iter_content(chunk_size=chunk_size), 
                                   total=num_bars, unit='KB', 
                                   desc=desc, leave=True, 
                                   file=sys.stdout):
                fp.write(chunk)

        return target_dest_dir

def download_url(
    url: str, 
    dst: str, 
    desc: str = None, 
    silent: bool = False
) -> None:
    """
    @param: url to download file
    @param: dst place to put the file

    TODO:  Integrate some of the nuggets from here:
    https://medium.com/better-programming/python-progress-bars-with-tqdm-by-example-ce98dbbc9697
    """
    downloader = FileDownloader()
    downloader.download_file(url, dst, desc=desc)

# def download_url(url: str, output_file: str):
#     # TODO:  Add parallization. 
#     r = requests.get(url, stream=True)
#     with open(output_file, 'wb+') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             f.write(chunk)
    
def pythonify(obj):
    if isinstance(obj, str):
        obj = json.loads(obj)
    # return munchify(humps.decamelize(obj))
    return munchify(obj)