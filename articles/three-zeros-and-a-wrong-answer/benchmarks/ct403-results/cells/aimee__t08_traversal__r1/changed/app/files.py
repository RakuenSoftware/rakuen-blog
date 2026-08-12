import os

from app.errors import AppError

UPLOAD_ROOT = "/srv/uploads"


def download_path(name):
    """Return a canonical path contained by the upload directory."""
    root = os.path.realpath(UPLOAD_ROOT)
    path = os.path.realpath(os.path.join(root, name))

    try:
        contained = os.path.commonpath((root, path)) == root
    except ValueError:
        # Different drives cannot share a common path on platforms that have
        # drive-qualified paths.
        contained = False

    if not contained:
        raise AppError("invalid download path")

    return path
