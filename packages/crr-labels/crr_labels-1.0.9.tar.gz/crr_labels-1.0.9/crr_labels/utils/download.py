from encodeproject import download as encodedownload
import os

def download(url:str, root:str, filename:str=None):
    os.makedirs(root, exist_ok=True)
    path = "{root}/{filename}".format(
        root=root,
        filename=url.split("/")[-1] if filename is None else filename
    )
    if not os.path.exists(path):
        encodedownload(url, path)