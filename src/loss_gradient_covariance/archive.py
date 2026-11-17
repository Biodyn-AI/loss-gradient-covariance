"""Download and verify the recorded study without executing archived code."""
from contextlib import contextmanager
import hashlib
from importlib.resources import files
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import urllib.request
import zipfile

RELEASE = json.loads(files('loss_gradient_covariance').joinpath('release.json').read_text())
BLOCK = 1024 * 1024


def sha256_file(path):
    """Hash a file with bounded memory."""
    with Path(path).open('rb') as stream:
        return _digest(stream)


def _digest(stream):
    checksum = hashlib.sha256()
    for block in iter(lambda: stream.read(BLOCK), b''):
        checksum.update(block)
    return checksum.hexdigest()


def download_data(destination, *, release=RELEASE):
    """Download the pinned release asset, verifying size and SHA before publishing.

    A matching existing file is reused. An existing different file is never
    overwritten. This function downloads bytes; it does not execute them.
    """
    destination = Path(destination)
    if destination.exists():
        if sha256_file(destination) != release['sha256']:
            raise ValueError('Existing destination has a different SHA-256')
        return destination
    if not release['url'].startswith('https://'):
        raise ValueError('Release URL must use HTTPS')
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix='.download-', dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        checksum, count = hashlib.sha256(), 0
        with os.fdopen(handle, 'wb') as target:
            with urllib.request.urlopen(release['url'], timeout=60) as response:
                for block in iter(lambda: response.read(BLOCK), b''):
                    count += len(block)
                    if count > release['bytes']:
                        raise ValueError('Download exceeds the pinned size')
                    target.write(block)
                    checksum.update(block)
        if count != release['bytes'] or checksum.hexdigest() != release['sha256']:
            raise ValueError('Downloaded size or SHA-256 differs from the release record')
        # A hard link publishes the complete verified file without overwriting
        # another process's destination. Both names are on the same filesystem.
        os.link(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def _manifest(archive):
    names = archive.namelist()
    if len(names) != len(set(names)):
        raise ValueError('Duplicate archive names')
    if archive.getinfo('MANIFEST.json').file_size > 8 * BLOCK:
        raise ValueError('Manifest is unexpectedly large')
    manifest = json.loads(archive.read('MANIFEST.json'))
    members = manifest['members']
    if set(names) != set(members) | {'MANIFEST.json'}:
        raise ValueError('Archive inventory differs from its manifest')
    total = 0
    for name, record in members.items():
        relative = PurePosixPath(name)
        if (relative.is_absolute() or '..' in relative.parts or ':' in name
                or '\\' in name or name != relative.as_posix()
                or name == 'MANIFEST.json'):
            raise ValueError('Unsafe archive path: ' + name)
        info = archive.getinfo(name)
        if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16):
            raise ValueError('Only regular scientific files are accepted: ' + name)
        if info.file_size != record['bytes'] or record['bytes'] < 0:
            raise ValueError('Member size mismatch: ' + name)
        total += info.file_size
    if total > 1024**3:
        raise ValueError('Scientific record exceeds the one-GiB extraction bound')
    return members, total


@contextmanager
def _verify_archive(path, expected_sha256):
    """Keep one open file from the outer hash through any caller extraction.

    A replacement of the pathname cannot substitute a different archive
    after verification. Member checks and extraction use this same handle.
    """
    with Path(path).open('rb') as source:
        if _digest(source) != expected_sha256:
            raise ValueError('Archive SHA-256 mismatch')
        source.seek(0)
        with zipfile.ZipFile(source) as archive:
            members, total = _manifest(archive)
            for name, record in members.items():
                with archive.open(name) as stream:
                    if _digest(stream) != record['sha256']:
                        raise ValueError('Member SHA-256 mismatch: ' + name)
            report = {'sha256': expected_sha256, 'member_count': len(members),
                      'uncompressed_bytes': total, 'scientific_random_draws': 0}
            yield archive, report


def verify_data(path, *, expected_sha256=RELEASE['sha256']):
    """Verify the outer archive and every member against the embedded manifest."""
    with _verify_archive(path, expected_sha256) as (_, report):
        return report


def extract_data(path, destination, *, expected_sha256=RELEASE['sha256']):
    """Verify first, then extract into a new workspace without overwriting data."""
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError('Choose a new extraction directory')
    with _verify_archive(path, expected_sha256) as (archive, report):
        destination.parent.mkdir(parents=True, exist_ok=True)
        if shutil.disk_usage(destination.parent).free < report['uncompressed_bytes'] + 512 * BLOCK:
            raise OSError('Extraction requires the recorded size plus a 512-MiB reserve')
        destination.mkdir()
        marker = destination / '.incomplete'
        marker.write_text('Extraction has not completed. Do not use this workspace yet.\n')
        for name in archive.namelist():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as source, target.open('xb') as output:
                shutil.copyfileobj(source, output, BLOCK)
        marker.unlink()
    return report
