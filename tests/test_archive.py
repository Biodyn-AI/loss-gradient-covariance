"""Literal integrity and extraction contracts; no network or scientific draws."""
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from loss_gradient_covariance.archive import download_data, extract_data, verify_data
from loss_gradient_covariance import archive as archive_module


def fixture(path, *, name='data/value.txt', content=b'abc', recorded=b'abc', symlink=False):
    record = {'bytes': len(content), 'sha256': hashlib.sha256(recorded).hexdigest()}
    manifest = {'members': {name: record}}
    with zipfile.ZipFile(path, 'x') as archive:
        archive.writestr('MANIFEST.json', json.dumps(manifest))
        info = zipfile.ZipInfo(name)
        if symlink:
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(info, content)
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_known_bytes_and_fresh_extraction(self):
        path = self.root / 'record.zip'
        sha = fixture(path)
        self.assertEqual(verify_data(path, expected_sha256=sha)['member_count'], 1)
        destination = self.root / 'workspace'
        extract_data(path, destination, expected_sha256=sha)
        self.assertEqual((destination / 'data/value.txt').read_bytes(), b'abc')
        with self.assertRaises(FileExistsError):
            extract_data(path, destination, expected_sha256=sha)

    def test_outer_and_inner_tampering_rejected(self):
        path = self.root / 'tampered.zip'
        sha = fixture(path, content=b'xyz')
        with self.assertRaises(ValueError):
            verify_data(path, expected_sha256='0' * 64)
        with self.assertRaises(ValueError):
            verify_data(path, expected_sha256=sha)

    def test_traversal_and_symlinks_rejected_without_extraction(self):
        for index, arguments in enumerate([{'name': '../outside'}, {'symlink': True}]):
            path = self.root / ('bad' + str(index) + '.zip')
            sha = fixture(path, **arguments)
            with self.assertRaises(ValueError):
                extract_data(path, self.root / ('output' + str(index)), expected_sha256=sha)
        self.assertFalse((self.root / 'outside').exists())

    @unittest.skipIf(os.name == 'nt', 'Windows blocks replacement of this open file')
    def test_pathname_replacement_cannot_change_verified_extraction(self):
        path = self.root / 'record.zip'
        sha = fixture(path)
        replacement = self.root / 'replacement.zip'
        fixture(replacement, name='../outside', content=b'replacement', recorded=b'replacement')
        digest = archive_module._digest
        swapped = False

        def replace_after_verified_member(stream):
            nonlocal swapped
            result = digest(stream)
            if isinstance(stream, zipfile.ZipExtFile) and not swapped:
                # The member digest belongs to the original open archive.
                # Replacing its pathname must not change subsequent extraction.
                replacement.replace(path)
                swapped = True
            return result

        destination = self.root / 'workspace'
        with patch.object(archive_module, '_digest', side_effect=replace_after_verified_member):
            extract_data(path, destination, expected_sha256=sha)
        self.assertTrue(swapped)
        self.assertFalse((self.root / 'outside').exists())
        self.assertEqual((destination / 'data/value.txt').read_bytes(), b'abc')

    def test_download_exact_known_digest_and_cache(self):
        release = {'url': 'https://example.test/data.zip', 'bytes': 3,
                   'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}
        path = self.root / 'download.zip'
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'abc')) as request:
            download_data(path, release=release)
            self.assertEqual(path.read_bytes(), b'abc')
            download_data(path, release=release)
            self.assertEqual(request.call_count, 1)
        with patch('urllib.request.urlopen', return_value=io.BytesIO(b'xyz')):
            with self.assertRaises(ValueError):
                download_data(self.root / 'wrong.zip', release=release)
        self.assertFalse((self.root / 'wrong.zip').exists())


if __name__ == '__main__':
    unittest.main()
