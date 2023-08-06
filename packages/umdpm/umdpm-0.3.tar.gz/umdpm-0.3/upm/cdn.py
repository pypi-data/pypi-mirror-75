"""
七牛云上传CDN
"""

from qiniu import Auth, put_file, etag
from os import path
from upm.config import config


def upload_cdn(filepath):
    access_key = config['access_key']
    secret_key = config['secret_key']
    bucket_name = config['bucket_name']
    if not access_key or not secret_key or not bucket_name:
        print('cdn配置不全，请执行 upm config set access_key [mykey]')
        exit(0)
        return
    q = Auth(access_key, secret_key)
    filename = path.basename(filepath)
    token = q.upload_token(bucket_name, filename, 3600)

    ret, info = put_file(token, filename, filepath)
    assert ret['key'] == filename
    assert ret['hash'] == etag(filepath)
