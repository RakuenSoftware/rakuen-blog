import os

UPLOAD_ROOT = "/srv/uploads"


def download_path(name):
    """Return the absolute path for an upload, rejecting traversal attempts."""
    # realpath handles both ``..`` components and symlinks.  commonpath (unlike
    # a string-prefix check) keeps similarly named directories such as
    # /srv/uploads-private outside the upload root.
    root = os.path.realpath(UPLOAD_ROOT)
    candidate = os.path.realpath(os.path.join(root, os.fspath(name)))
    try:
        contained = os.path.commonpath((root, candidate)) == root
    except ValueError:
        # Paths on different drives (possible on Windows) cannot share a root.
        contained = False
    if not contained:
        raise ValueError("download path is outside upload root")
    return candidate
