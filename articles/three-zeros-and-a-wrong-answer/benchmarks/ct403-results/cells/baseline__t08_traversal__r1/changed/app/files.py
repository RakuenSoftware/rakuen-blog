import os

UPLOAD_ROOT = "/srv/uploads"


def download_path(name):
    """Return the canonical path for a file contained by ``UPLOAD_ROOT``."""
    upload_root = os.path.realpath(UPLOAD_ROOT)
    candidate = os.path.realpath(os.path.join(upload_root, name))

    try:
        contained = os.path.commonpath((upload_root, candidate)) == upload_root
    except ValueError:
        # Paths on different drives have no common path on Windows.
        contained = False

    if not contained:
        raise ValueError("download path is outside the upload root")

    return candidate
