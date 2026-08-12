import os

from app.errors import Forbidden


UPLOAD_ROOT = "/srv/uploads"


class InvalidDownloadPath(Forbidden, ValueError):
    """Raised when a requested download path is not safely confined."""


def download_path(name):
    """Return the canonical path for a file confined to ``UPLOAD_ROOT``.

    Resolving both paths before comparing them prevents absolute paths,
    ``..`` components, and existing symlinks from escaping the upload root.
    """
    try:
        name = os.fspath(name)
        if not isinstance(name, str) or os.path.isabs(name):
            raise InvalidDownloadPath("invalid download path")

        root = os.path.realpath(UPLOAD_ROOT)
        candidate = os.path.realpath(os.path.join(root, name))
        if os.path.commonpath((root, candidate)) != root:
            raise InvalidDownloadPath("invalid download path")
    except (TypeError, ValueError, OSError) as exc:
        if isinstance(exc, InvalidDownloadPath):
            raise
        raise InvalidDownloadPath("invalid download path") from exc

    return candidate
