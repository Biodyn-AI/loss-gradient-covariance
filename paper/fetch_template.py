"""Fetch only the two unmodified, hash-pinned JOTA publisher class files.

These files remain publisher material, with their original headers and terms;
the repository's code license does not extend to them. They are downloaded
locally into ignored paper paths, rather than redistributed in this repository.
This script needs only Python's standard library and works with ``python -I``.
"""
import hashlib
import io
from pathlib import Path, PurePosixPath
import stat
import urllib.parse
import urllib.request
import zipfile


TEMPLATE_URL = ('https://media.springer.com/full/springer-instructions-for-authors-assets/'
                'zip/1705114_LaTeX%20JOTA.zip')
ARCHIVE_BYTES = 358412
ARCHIVE_SHA256 = '763064cc0e2fed79a75d2623dddda4824683b6dd1cb51638064374e817d9d6b2'
# Independently read from the same pinned official ZIP, without normalization
# of line endings or alteration of the publisher's copyright/license headers.
CLASS_SHA256 = {
    'svjour3.cls': '877b71c10bdf2075cbb70ae5ce50e41692f97015e04f7abeee878d6598c2dbea',
    'svglov3.clo': 'a0b9f3522e6ef83f3dd8d5901c74745d515355ccd61f0a148668283aabdb5467',
}


class _HTTPSOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).scheme != 'https':
            raise ValueError('publisher template redirects must use HTTPS')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _download():
    if urllib.parse.urlsplit(TEMPLATE_URL).scheme != 'https':
        raise ValueError('publisher template URL must use HTTPS')
    opener = urllib.request.build_opener(_HTTPSOnlyRedirect())
    with opener.open(TEMPLATE_URL, timeout=30) as response:
        if urllib.parse.urlsplit(response.geturl()).scheme != 'https':
            raise ValueError('publisher template response must use HTTPS')
        # Read at most the pinned archive size plus one sentinel byte. A wrong
        # Content-Length header cannot bypass this actual byte limit.
        payload = bytearray()
        while len(payload) <= ARCHIVE_BYTES:
            block = response.read(min(64 * 1024, ARCHIVE_BYTES + 1 - len(payload)))
            if not block:
                break
            payload.extend(block)
    if len(payload) != ARCHIVE_BYTES:
        raise ValueError('publisher template archive size differs from the pinned size')
    if hashlib.sha256(payload).hexdigest() != ARCHIVE_SHA256:
        raise ValueError('publisher template archive SHA256 differs from the pinned digest')
    return bytes(payload)


def _components(payload):
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = archive.infolist()
        names = [member.filename for member in members]
        if len(names) != len(set(names)):
            raise ValueError('duplicate publisher template archive paths')
        for member in members:
            name = member.filename
            path = PurePosixPath(name)
            if (not name or path.is_absolute() or '..' in path.parts
                    or '\\' in name or ':' in name or stat.S_ISLNK(member.external_attr >> 16)):
                raise ValueError('unsafe publisher template archive path')
        files = {}
        for name, digest in CLASS_SHA256.items():
            if name not in names or archive.getinfo(name).file_size > 64 * 1024:
                raise ValueError('missing or oversized publisher template component')
            value = archive.read(name)
            if hashlib.sha256(value).hexdigest() != digest:
                raise ValueError('publisher template component SHA256 differs from its pinned digest')
            files[name] = value
    return files


def ensure_template(directory=None):
    """Verify existing classes, or fetch the missing ones without overwriting.

    An existing class with different bytes, or an existing symlink/directory,
    is an error requiring the caller to resolve it. A verified pair requires
    no network. Both downloaded components are validated before any writes.
    Returns the pinned class-name-to-SHA256 mapping.
    """
    destination = Path(directory) if directory is not None else Path(__file__).resolve().parent
    missing = []
    for name, digest in CLASS_SHA256.items():
        path = destination / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f'unsafe existing publisher class path: {path}')
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError(f'existing publisher class differs from its pinned digest: {path}')
        else:
            missing.append(name)
    if missing:
        files = _components(_download())
        destination.mkdir(parents=True, exist_ok=True)
        for name in missing:
            # Exclusive creation also prevents a concurrent writer from being
            # silently overwritten between the initial check and this write.
            with (destination / name).open('xb') as stream:
                stream.write(files[name])
    return dict(CLASS_SHA256)


if __name__ == '__main__':
    ensure_template()
    print('Verified the two unmodified JOTA publisher class files.')
