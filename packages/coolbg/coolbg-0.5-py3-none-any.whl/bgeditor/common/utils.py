import requests
import os
import tempfile
import uuid
def download_file(url, root_dir=None, ext= None):
    rs = None
    try:
        r = requests.get(url)
        if ext:
            file_name = str(uuid.uuid4()) + "." + ext
        else:
            file_name = os.path.basename(url)
        if not root_dir:
            rs = get_dir('download') + file_name
        else:
            rs = root_dir + "/" + file_name
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs = None
        pass
    return rs
def cache_file(url):
    rs = None
    try:
        rs = get_dir('download') + os.path.basename(url)
        if os.path.exists(rs):
            return rs #cached
        r = requests.get(url)
        with open(rs, 'wb') as f:
            f.write(r.content)
    except:
        rs  = None
        pass
    return rs

def get_dir(dir):
    tmp_download_path = tempfile.gettempdir() + "/"+dir+"/"
    if not os.path.exists(tmp_download_path):
        os.makedirs(tmp_download_path)
    return tmp_download_path