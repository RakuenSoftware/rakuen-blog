import os
UPLOAD_ROOT = "/srv/uploads"

def download_path(name):
    """Return the requested upload path, rejecting paths outside the root."""
    root = os.path.realpath(UPLOAD_ROOT)
    path = os.path.realpath(os.path.join(root, name))

    if os.path.commonpath((root, path)) != root:
        raise ValueError("download path escapes upload root")

    return path
