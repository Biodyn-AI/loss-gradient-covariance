"""Mocked-network contracts for the publisher-template bootstrap."""
import hashlib
import io
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.request import Request
import zipfile


SOURCE = Path(__file__).resolve().parents[1] / 'paper' / 'fetch_template.py'


def literal_archive(extra=()):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        archive.writestr('svjour3.cls', b'% Publisher class header\nclass bytes\n')
        archive.writestr('svglov3.clo', b'% Publisher option header\noption bytes\n')
        archive.writestr('unneeded.tex', b'not installed')
        for name, value in extra:
            archive.writestr(name, value)
    return buffer.getvalue()


class Response(io.BytesIO):
    def geturl(self):
        return 'https://media.springer.com/mock.zip'


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.namespace = runpy.run_path(str(SOURCE))
        # Functions retain runpy's execution globals, not its returned copy.
        self.globals = self.namespace['ensure_template'].__globals__
        self.payload = literal_archive()
        self.files = {'svjour3.cls': b'% Publisher class header\nclass bytes\n',
                      'svglov3.clo': b'% Publisher option header\noption bytes\n'}
        self.globals.update(ARCHIVE_BYTES=len(self.payload),
            ARCHIVE_SHA256=hashlib.sha256(self.payload).hexdigest(),
            CLASS_SHA256={name: hashlib.sha256(value).hexdigest()
                          for name, value in self.files.items()})
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.destination = Path(self.directory.name) / 'paper'
        self.opener = Mock()
        self.opener.open.side_effect = lambda *args, **kwargs: Response(self.payload)
        self.patch = patch.object(self.globals['urllib'].request, 'build_opener',
                                  return_value=self.opener)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def install(self):
        return self.namespace['ensure_template'](self.destination)

    def test_installs_only_two_byte_exact_files_and_reuses_them(self):
        self.install()
        self.assertEqual({p.name for p in self.destination.iterdir()}, set(self.files))
        for name, content in self.files.items():
            self.assertEqual((self.destination / name).read_bytes(), content)
        self.opener.open.assert_called_once()
        self.assertTrue(self.opener.open.call_args.args[0].startswith('https://'))
        self.assertLessEqual(self.opener.open.call_args.kwargs['timeout'], 30)
        self.install()
        self.opener.open.assert_called_once()

    def test_keeps_a_matching_existing_class_and_fetches_the_missing_one(self):
        self.destination.mkdir()
        existing = self.destination / 'svjour3.cls'
        existing.write_bytes(self.files['svjour3.cls'])
        modified = existing.stat().st_mtime_ns
        self.install()
        self.assertEqual(existing.stat().st_mtime_ns, modified)
        self.assertEqual((self.destination / 'svglov3.clo').read_bytes(), self.files['svglov3.clo'])

    def test_wrong_existing_class_is_not_overwritten_or_downloaded(self):
        self.destination.mkdir()
        existing = self.destination / 'svjour3.cls'
        existing.write_bytes(b'locally changed class')
        with self.assertRaisesRegex(ValueError, 'existing'):
            self.install()
        self.assertEqual(existing.read_bytes(), b'locally changed class')
        self.opener.open.assert_not_called()

    def test_symlink_is_rejected_even_if_its_bytes_match(self):
        self.destination.mkdir()
        outside = self.destination.parent / 'outside.cls'
        outside.write_bytes(self.files['svjour3.cls'])
        (self.destination / 'svjour3.cls').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'existing'):
            self.install()
        self.opener.open.assert_not_called()

    def test_wrong_archive_digest_leaves_no_class_files(self):
        self.globals['ARCHIVE_SHA256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            self.install()
        self.assertFalse(self.destination.exists())

    def test_download_size_is_capped(self):
        self.opener.open.side_effect = lambda *args, **kwargs: Response(self.payload + b'x')
        with self.assertRaisesRegex(ValueError, 'size'):
            self.install()
        self.assertFalse(self.destination.exists())

    def test_unsafe_zip_path_is_rejected_before_any_write(self):
        self.payload = literal_archive([('../escape.cls', b'bad')])
        self.globals.update(ARCHIVE_BYTES=len(self.payload),
                            ARCHIVE_SHA256=hashlib.sha256(self.payload).hexdigest())
        with self.assertRaisesRegex(ValueError, 'path'):
            self.install()
        self.assertFalse(self.destination.exists())
        self.assertFalse((self.destination.parent / 'escape.cls').exists())

    def test_pinned_component_hash_prevents_modified_publisher_bytes(self):
        self.globals['CLASS_SHA256']['svglov3.clo'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'component'):
            self.install()
        self.assertFalse(self.destination.exists())

    def test_redirect_and_response_must_use_https(self):
        redirect = self.namespace['_HTTPSOnlyRedirect']()
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            redirect.redirect_request(Request('https://example.test/a'), None, 302,
                                      'redirect', {}, 'http://example.test/b')
        response = Response(self.payload)
        response.geturl = lambda: 'http://example.test/b'
        self.opener.open.side_effect = None
        self.opener.open.return_value = response
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            self.install()
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
