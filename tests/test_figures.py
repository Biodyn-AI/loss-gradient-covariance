"""Portable figure-wrapper contracts using only literal temporary files."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/reproduce_figures.py'
SPEC = importlib.util.spec_from_file_location('figure_wrapper_contracts', SCRIPT)
WRAPPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WRAPPER)


class FigureWrapperTests(unittest.TestCase):
    def test_preflight_import_needs_only_standard_library(self):
        # An isolated interpreter avoids dependence on other tests' imports.
        program = (
            'import importlib.util,sys; '
            f'spec=importlib.util.spec_from_file_location("wrapper",{str(SCRIPT)!r}); '
            'module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); '
            'assert "numpy" not in sys.modules; assert "matplotlib" not in sys.modules'
        )
        completed = subprocess.run([sys.executable, '-I', '-B', '-c', program],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_literal_input_verifies_then_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root / 'saved.txt'
            record.write_bytes(b'frozen literal record')
            pins = {'saved.txt': hashlib.sha256(record.read_bytes()).hexdigest()}
            with patch.dict(WRAPPER.PINS, pins, clear=True):
                self.assertEqual(WRAPPER.verify_inputs(root), pins)
                record.write_bytes(b'changed literal record')
                with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                    WRAPPER.verify_inputs(root)

    def test_existing_output_is_preserved_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'existing'
            output.mkdir()
            sentinel = output / 'keep.txt'
            sentinel.write_text('unchanged')
            with patch.object(WRAPPER, 'verify_inputs', side_effect=AssertionError('unexpected read')):
                with self.assertRaisesRegex(FileExistsError, 'refusing to overwrite'):
                    WRAPPER.reproduce(root / 'science', output)
            self.assertEqual(sentinel.read_text(), 'unchanged')

    def test_output_inside_scientific_workspace_is_refused_before_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'forbidden-output'
            with patch.object(WRAPPER, 'verify_inputs', side_effect=AssertionError('unexpected read')):
                with self.assertRaisesRegex(ValueError, 'outside the frozen scientific workspace'):
                    WRAPPER.reproduce(root, output)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
