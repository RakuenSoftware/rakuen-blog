import os
from app.errors import Forbidden

UPLOAD_ROOT = "/srv/uploads"

def download_path(name):
    root = os.path.realpath(UPLOAD_ROOT)
    path = os.path.realpath(os.path.join(root, name))
    if os.path.commonpath((root, path)) != root:
        raise Forbidden("invalid download path")
    return path
