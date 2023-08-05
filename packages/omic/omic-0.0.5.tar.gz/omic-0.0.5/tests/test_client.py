#!/usr/bin/env python3
# =.- coding: utf-8 -.-

import time

import pytest

from omic import omic

TEST_USER = '63be793a-6e1b-40cd-9f70-49dd73f470ab'

def setup():
    omic.configure({'user': TEST_USER})

# def test_new_method():
#     return
#     S3_ADDR = 's3://0tmp/1e6271fc9bc9e6c713ac19297c031baf'
#     import boto3
#     import requests
#     # Get the service client.
#     s3 = boto3.client('s3')
#     # Generate the URL to get 'key-name' from 'bucket-name'
#     url = s3.generate_presigned_url(
#         ClientMethod='get_object',
#         Params={
#             'Bucket': '0tmp',
#             'Key': '1e6271fc9bc9e6c713ac19297c031baf'
#         },
#         ExpiresIn=(1 * 60 * 60) # 1 hr
#     )
#     print('url', url)
#     r = requests.get(url, stream=True)
#     with open('testytest', 'wb+') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             f.write(chunk)


def test_data_public_download():
    setup()
    data = omic.client('data') 
    print('Starting download...') 
    files = data.download( 
        vpath='/MEDRECORDS/SYNTHETIC/SYNTHEA COVID-19 100K/',  
        mode='public', 
        #project='project-891663a3-2ad5-4df7-b494-e85c3c855b93', 
        #download_dir='.' 
    )

def test_data_project_download():
    setup()
    start = time.time()
    data = omic.client('data')
    files = data.download(
        vpath='/yessss', 
        mode='project',
        project='project-48de6638-6a99-40a6-bf2d-dbfa5c158f29',
        download_dir='/tmp/test_dl'
    )
    print(f'{time.time() - start} seconds elapsed')

# def test_data_project_download():
#     setup()
#     start = time.time()
#     data = omic.client('data')
#     files = data.download(_id='')
#     print(f'{time.time() - start} seconds elapsed')