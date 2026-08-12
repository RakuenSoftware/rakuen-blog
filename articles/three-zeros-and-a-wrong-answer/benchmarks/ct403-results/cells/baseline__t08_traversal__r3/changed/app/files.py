import os

from app.errors import Forbidden


UPLOAD_ROOT = "/srv/uploads"


def download_path(name):
    """Return a canonical path contained by the upload directory."""
    root = os.path.realpath(UPLOAD_ROOT)
    candidate = os.path.realpath(os.path.join(root, name))

    try:
        contained = os.path.commonpath((root, candidate)) == root
    except ValueError:
        # Different drives (on platforms that have them) cannot share a root.
        contained = False

    if not contained:
        raise Forbidden("invalid download path")
    return candidate
