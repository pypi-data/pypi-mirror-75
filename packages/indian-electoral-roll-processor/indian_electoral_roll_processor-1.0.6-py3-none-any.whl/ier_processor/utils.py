import boto3
import tempfile
import os
import re
import os.path
import shutil

from urllib.parse import urlparse


def create_working_directory(prefix, debug=False):
    working_dir_root = os.getcwd() if debug else None
    working_dir = tempfile.TemporaryDirectory(prefix=prefix, dir=working_dir_root).name
    os.makedirs(working_dir)
    return working_dir

def copy_across_file_systems(src, dest):

    def strip_starting_slash(s):
        return re.sub('^/*', '', s)

    src_url = urlparse(src)
    dest_url = urlparse(dest)

    src_aws = src_url.scheme == 's3'
    dest_aws = dest_url.scheme == 's3'

    if src_aws and dest_aws:
        src_params = {'Bucket': src_url.netloc, 'Key': strip_starting_slash(src_url.path)}
        boto3.resource('s3').meta.client.copy(src_params, dest_url.netloc, strip_starting_slash(dest_url.path))
    elif src_aws:
        boto3.resource('s3').Bucket(src_url.netloc).download_file(strip_starting_slash(src_url.path), dest)
    elif dest_aws:
        dest_path = strip_starting_slash(dest_url.path).replace('\\', "/")
        print(f'copying {src} to {dest_path}')
        boto3.resource('s3').Bucket(dest_url.netloc).upload_file(src, dest_path)
    else:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(src, dest)
