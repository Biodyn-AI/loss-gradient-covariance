"""Literal, RNG-free contracts for portable recorded-data reanalysis."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

try:
    import numpy as np
except ImportError:
    np = None

from loss_gradient_covariance.recorded import matrix_table, reproduce_tables


NATIVE = Path('results/q2_matrix_validation_20261117/run')
ANALYSIS = Path('results/q2_matrix_analysis_20261117/run')


def artifact(path):
    return {'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def literal_record(root):
    """Four literal replicas: independent risks 1,4,9,16; coupled 4x.

    Each bootstrap row repeats a single replica, so the two percentile
    endpoints are 1.225 and 15.475 and every paired ratio is exactly four.
    This tiny fixture tests the archived layout without simulating a model.
    """
    native, analysis = root / NATIVE, root / ANALYSIS
    native.mkdir(parents=True)
    analysis.mkdir(parents=True)
    samples = np.zeros((12, 3, 3, 2, 3, 2, 4))
    for cell in range(12):
        scale = 2 if cell % 4 == 1 else 1
        samples[cell, :, :, :, 0, 0, :] = np.array([1., 2., 3., 4.]) * scale
        if cell % 4 == 2:
            samples[cell, :, :, :, 0, 0, :] = 1
            samples[cell, :, :, :, 0, 1, :] = 2
    indices = np.array([[0, 0, 0, 0], [1, 1, 1, 1],
                        [2, 2, 2, 2], [3, 3, 3, 3]], dtype=np.uint16)
    risks = np.tile([1., 4., 9., 16.], (108, 1))
    for cell in (1, 5, 9):
        risks[cell * 9:cell * 9 + 9] *= 4
    for cell in (2, 6, 10):
        # The cross term is essential: (1,2)^T Hbar (1,2)/2 = 7.5.
        risks[cell * 9:cell * 9 + 9] = 7.5
    rows = np.zeros((432, 4))
    rows[:108] = risks
    estimates = np.zeros((4, 648))
    estimates[:, :108] = risks.T
    ratios = np.full((4, 27), 4.)
    labels = [f'risk:cell{c}:start{s}:window{w}'
              for c in range(12) for s in range(3) for w in range(3)]
    labels += [f'copula:rate{r}:method{m}:start{s}:window{w}:coupled-independent'
               for r in range(3) for m in range(2) for s in range(3) for w in range(3)]
    labels += [f'sgd:cell{c}:start{s}:window{w}:minus-exact-nominal'
               for c in (2, 3, 6, 7, 10, 11) for s in range(3) for w in range(3)]
    labels += [f'start:cell{c}:window{w}:{s}-zero'
               for c in range(12) for w in range(3) for s in ('plus', 'minus')]
    labels += [f'window:cell{c}:start{s}:{w}'
               for c in range(12) for s in range(3) for w in ('middle-early', 'late-middle')]
    labels += [f'rate:mode{m}:start{s}:window{w}:rate{r+1}-rate{r}'
               for m in range(4) for s in range(3) for w in range(3) for r in range(2)]
    point = rows.mean(axis=1)
    se = rows.std(axis=1, ddof=1) / 2
    bands = np.column_stack((point - 2 * se, point + 2 * se))
    # Deliberately retain finite-clock failures in each diagnostic family.
    for index in (108, 135, 162, 216, 288, 360):
        bands[index] = [1, 2]
    np.savez(native / 'samples_and_terminal.npz', samples=samples,
             observed=np.ones((12, 3, 2), dtype=bool),
             failure_code=np.zeros((12, 3, 4), dtype=np.uint8))
    np.savez(analysis / 'bootstrap_and_rows.npz', indices=indices,
             risk_rows=risks, primary_rows=rows,
             bootstrap_estimates=estimates, bootstrap_ratios=ratios)
    native_summary = {'status': 'finished', 'study_complete': True,
        'failed_trajectories': 0, 'settings': {'replicas': 4,
            'eta_values': [.001, .0002, .00004],
            'matrices': [[[1, 1.25], [1.25, 3]], [[3, 1.25], [1.25, 1]]]},
        'artifacts': {'samples_and_terminal.npz': artifact(native / 'samples_and_terminal.npz')}}
    report = {'status': 'finished', 'analysis_complete': True,
        'finite_remainder_certified': False,
        'primary': {'labels': labels, 'point_estimates': point.tolist(),
            'replica_standard_errors': se.tolist(), 'simultaneous_95': bands.tolist(),
            'max_deviation_critical_value': 2.,
            'percentile_95': np.quantile(estimates[:, :432], [.025, .975], axis=0).T.tolist()},
        'artifacts': {'bootstrap_and_rows.npz': artifact(analysis / 'bootstrap_and_rows.npz')},
        'coordinate_diagnostics': {'labels': ['literal-coordinate'] * 216,
                                   'scope': 'Descriptive only.'},
        'exact_nominal_sgd_controls': [{'eta': e, 'scope': 'Nominal only.'}
                                      for e in [.001, .0002, .00004]]}
    (native / 'summary.json').write_text(json.dumps(native_summary))
    (analysis / 'summary.json').write_text(json.dumps(report))


@unittest.skipIf(np is None, 'recorded-data extra (NumPy) is not installed')
class RecordedTableTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        literal_record(self.root)

    def test_literal_quadratic_percentiles_pairing_and_se(self):
        with patch.object(np.random, 'default_rng', side_effect=AssertionError('no RNG')):
            report = matrix_table(self.root)
        self.assertEqual(len(report['table']), 3)
        for row in report['table']:
            independent = row['methods']['AdamW']['independent']
            self.assertEqual(independent['risk'], 7.5)
            self.assertAlmostEqual(independent['replica_se'], math.sqrt(43) / 2)
            np.testing.assert_allclose(independent['percentile_95'], [1.225, 15.475])
            self.assertEqual(row['methods']['AdamW']['coupled']['risk'], 30.)
            ratio = row['methods']['AdamW']['coupled_over_independent']
            self.assertEqual(ratio['point'], 4.)
            self.assertEqual(ratio['percentile_95'], [4., 4.])
            self.assertEqual(row['methods']['SGD']['independent']['risk'], 7.5)
            self.assertEqual(row['methods']['SGD']['independent']['replica_se'], 0.)
        self.assertEqual(report['validation']['saved_resamples_reused'], 4)
        self.assertFalse(report['finite_remainder_certified'])

    def test_all_frozen_diagnostic_families_and_flagged_labels_retained(self):
        report = matrix_table(self.root)
        families = report['finite_clock_diagnostics']['families']
        expected = {'adamw_copula': 27, 'sgd_copula': 27,
                    'sgd_exact_control': 54, 'start': 72, 'window': 72, 'rate': 72}
        self.assertEqual({k: v['total'] for k, v in families.items()}, expected)
        self.assertTrue(all(v['excludes_zero'] == 1 for v in families.values()))
        self.assertEqual(len(report['finite_clock_diagnostics']['flagged']), 6)

    def test_exclusive_json_output_and_deterministic_content(self):
        output = self.root / 'table.json'
        returned = reproduce_tables(self.root, output)
        self.assertEqual(json.loads(output.read_text()), returned)
        self.assertEqual(returned, reproduce_tables(self.root, self.root / 'second.json'))
        with self.assertRaises(FileExistsError):
            reproduce_tables(self.root, output)

    def test_refuses_artifact_digest_mismatch(self):
        with (self.root / NATIVE / 'samples_and_terminal.npz').open('ab') as stream:
            stream.write(b'changed')
        with self.assertRaisesRegex(ValueError, 'artifact'):
            matrix_table(self.root)

    def test_refuses_a_persisted_risk_row_inconsistent_with_snapshots(self):
        path = self.root / ANALYSIS / 'bootstrap_and_rows.npz'
        with np.load(path, allow_pickle=False) as saved:
            arrays = {key: saved[key] for key in saved.files}
        arrays['risk_rows'][0, 0] = 2
        np.savez(path, **arrays)
        summary_path = path.with_name('summary.json')
        summary = json.loads(summary_path.read_text())
        summary['artifacts'][path.name] = artifact(path)
        summary_path.write_text(json.dumps(summary))
        with self.assertRaisesRegex(ValueError, 'risk rows'):
            matrix_table(self.root)


class OptionalDependencyTests(unittest.TestCase):
    def test_module_import_without_numpy(self):
        source = str(Path(__file__).resolve().parents[1] / 'src')
        program = """import builtins, sys
sys.path.insert(0, sys.argv[1])
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == 'numpy' or name.startswith('numpy.'):
        raise ImportError('NumPy intentionally blocked')
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
from loss_gradient_covariance.recorded import matrix_table
assert 'numpy' not in sys.modules
try:
    matrix_table('.')
except ImportError as error:
    assert 'NumPy' in str(error)
else:
    raise AssertionError('missing optional dependency was not reported')
"""
        subprocess.run([sys.executable, '-B', '-I', '-c', program, source], check=True)


if __name__ == '__main__':
    unittest.main()
