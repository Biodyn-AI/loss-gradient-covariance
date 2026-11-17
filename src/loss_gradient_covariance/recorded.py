"""Portable reanalysis of the released matrix study, with no random draws.

``data_root`` is the extracted scientific record's root, containing ``results/``.
Only the two matrix-study summaries and their two NPZ artifacts are read.  All
paths inside historical receipts are ignored.  NumPy is an optional dependency
loaded when a table is requested; importing this module needs only Python.

The twelve displayed risks are recomputed from recorded u snapshots.  Their
pointwise intervals and the three paired AdamW ratios reuse the saved whole-
replica bootstrap indices.  The simultaneous critical value, all finite-clock
diagnostic bands, and exact nominal SGD controls are explicitly frozen inputs,
not fresh estimates or new coverage/stationarity certificates.
"""
import hashlib
import json
import math
from pathlib import Path


_NATIVE = Path('results/q2_matrix_validation_20261117/run')
_ANALYSIS = Path('results/q2_matrix_analysis_20261117/run')
_SCOPE = ('Recorded atomic quadratic fixture only. Reused whole-replica bootstrap '
          'indices; approximate uncertainty, without finite-sample coverage, '
          'stationarity, full-chain mixing, or finite-rate asymptotic certificates. '
          'Ratios are descriptive pointwise comparisons, outside the primary '
          'simultaneous family. No random draws or new experimental trajectories.')


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _digest(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


def _artifact(directory, summary, name):
    path = directory / name
    actual = _digest(path)
    _require(actual == summary['artifacts'][name], f'artifact size/hash mismatch: {name}')
    return path, actual


def _close(np, actual, expected, message):
    _require(np.shape(actual) == np.shape(expected)
             and np.allclose(actual, expected, rtol=5e-12, atol=2e-15), message)


def _diagnostics(np, primary):
    """Report every predeclared diagnostic, including unfavorable flags."""
    labels = primary['labels']
    bands = np.asarray(primary['simultaneous_95'], dtype=float)
    _require(len(labels) == len(set(labels)) == 432 and bands.shape == (432, 2)
             and np.isfinite(bands).all() and (bands[:, 0] <= bands[:, 1]).all(),
             'complete finite 432-feature diagnostic family required')
    families = {name: {'total': 0, 'excludes_zero': 0, 'positive': 0, 'negative': 0}
                for name in ('adamw_copula', 'sgd_copula', 'sgd_exact_control',
                             'start', 'window', 'rate')}
    flagged = []
    for label, (lower, upper) in zip(labels, bands):
        if label.startswith('risk:'):
            continue
        if label.startswith('copula:'):
            _require(':method0:' in label or ':method1:' in label, 'unknown copula method')
            family = 'adamw_copula' if ':method0:' in label else 'sgd_copula'
        else:
            prefix = label.split(':', 1)[0]
            family = 'sgd_exact_control' if prefix == 'sgd' else prefix
        _require(family in families, f'unknown primary diagnostic: {label}')
        count = families[family]
        count['total'] += 1
        if lower > 0 or upper < 0:
            count['excludes_zero'] += 1
            count['positive' if lower > 0 else 'negative'] += 1
            flagged.append({'family': family, 'label': label,
                            'simultaneous_95': [float(lower), float(upper)]})
    _require([record['total'] for record in families.values()] == [27, 27, 54, 72, 72, 72],
             'incomplete predeclared diagnostic families')
    return {'source': 'Frozen full-432-family approximate simultaneous bands.',
            'families': families, 'flagged': flagged,
            'scope': 'Excluding zero is a diagnostic flag, not a mixing or asymptotic-order test.'}


def matrix_table(data_root):
    """Return the three-rate, zero-start, final-window matrix table as a dict.

    The root must contain the unchanged relative ``results/`` layout. Artifact
    sizes/hashes are checked against their summaries, then inputs are hashed
    again to detect modification during analysis. This is not verification of
    every member of the larger release; the archive downloader does that.
    """
    try:
        import numpy as np
    except ImportError as error:
        raise ImportError('Recorded-data reanalysis requires the optional NumPy dependency.') from error

    root = Path(data_root).expanduser().resolve()
    native_path, analysis_path = root / _NATIVE / 'summary.json', root / _ANALYSIS / 'summary.json'
    sources = {str(path.relative_to(root)): _digest(path) for path in (native_path, analysis_path)}
    native = json.loads(native_path.read_text())
    analysis = json.loads(analysis_path.read_text())
    _require(native.get('status') == 'finished' and native.get('study_complete') is True
             and native.get('failed_trajectories') == 0
             and analysis.get('status') == 'finished' and analysis.get('analysis_complete') is True
             and analysis.get('finite_remainder_certified') is False,
             'complete recorded studies with no finite-remainder certificate required')
    settings = native['settings']
    _require(settings['matrices'] == [[[1, 1.25], [1.25, 3]],
                                      [[3, 1.25], [1.25, 1]]],
             'matrix table requires the published conditioned fixture')
    etas = settings['eta_values']
    _require(etas == [.001, .0002, .00004], 'three published rates required')
    replicas = settings['replicas']
    _require(isinstance(replicas, int) and replicas > 1, 'at least two complete replicas required')
    sample_path, sample_hash = _artifact(native_path.parent, native, 'samples_and_terminal.npz')
    bootstrap_path, bootstrap_hash = _artifact(analysis_path.parent, analysis, 'bootstrap_and_rows.npz')
    sources[str(sample_path.relative_to(root))] = sample_hash
    sources[str(bootstrap_path.relative_to(root))] = bootstrap_hash
    with np.load(sample_path, allow_pickle=False) as saved:
        samples = saved['samples']
        _require(samples.dtype == np.float64 and samples.ndim == 7
                 and samples.shape[:3] == (12, 3, 3) and samples.shape[3] > 0
                 and samples.shape[4:] == (3, 2, replicas) and np.isfinite(samples).all()
                 and saved['observed'].shape == (12, 3, samples.shape[3])
                 and saved['observed'].all() and not saved['failure_code'].any(),
                 'all finite snapshots and no failed/missing trajectories required')
        x, y = samples[:, :, :, :, 0, 0, :], samples[:, :, :, :, 0, 1, :]
        # Hbar = [[2, 1.25], [1.25, 2]], so this is u^T Hbar u / 2.
        risk_rows = (x * x + y * y + 1.25 * x * y).mean(axis=3).reshape(108, replicas)
    primary = analysis['primary']
    expected_labels = [f'risk:cell{c}:start{s}:window{w}'
                       for c in range(12) for s in range(3) for w in range(3)]
    _require(primary['labels'][:108] == expected_labels, 'published risk-row order required')
    critical = float(primary['max_deviation_critical_value'])
    _require(math.isfinite(critical) and critical >= 0, 'finite frozen simultaneous critical value required')
    with np.load(bootstrap_path, allow_pickle=False) as saved:
        _close(np, risk_rows, saved['risk_rows'], 'saved risk rows disagree with raw snapshots')
        _close(np, risk_rows, saved['primary_rows'][:108], 'saved primary risk rows disagree with raw snapshots')
        indices = saved['indices']
        _require(indices.ndim == 2 and indices.shape[0] > 1 and indices.shape[1] == replicas
                 and indices.dtype.kind in 'ui' and (indices >= 0).all() and (indices < replicas).all(),
                 'complete saved whole-replica bootstrap indices required')
        # Only twelve displayed rows are reanalysed; the complete 648-feature
        # original bootstrap artifact and every diagnostic remain available.
        display_indices = np.arange(12) * 9 + 2
        display_rows = risk_rows[display_indices]
        bootstrap = np.empty((len(indices), 12), dtype=float)
        for offset in range(0, len(indices), 256):
            chunk = indices[offset:offset + 256]
            counts = np.stack([np.bincount(row, minlength=replicas) for row in chunk])
            bootstrap[offset:offset + len(chunk)] = (counts @ display_rows.T) / replicas
        _close(np, bootstrap, saved['bootstrap_estimates'][:, display_indices],
               'saved displayed bootstrap estimates disagree with reused indices')
        ratios = bootstrap[:, [1, 5, 9]] / bootstrap[:, [0, 4, 8]]
        _require(np.isfinite(ratios).all() and (bootstrap[:, [0, 4, 8]] > 0).all(),
                 'positive independent AdamW bootstrap denominators required')
        _close(np, ratios, saved['bootstrap_ratios'][:, [2, 11, 20]],
               'saved paired ratios disagree with reused indices')
    means = risk_rows.mean(axis=1)
    standard_errors = risk_rows.std(axis=1, ddof=1) / math.sqrt(replicas)
    _close(np, means, primary['point_estimates'][:108], 'saved risk means disagree with raw snapshots')
    _close(np, standard_errors, primary['replica_standard_errors'][:108],
           'saved replica standard errors disagree with raw snapshots')
    pointwise = np.quantile(bootstrap, [.025, .975], axis=0, method='linear').T
    _close(np, pointwise, np.asarray(primary['percentile_95'])[display_indices],
           'saved displayed percentile intervals disagree with reused indices')
    simultaneous = np.column_stack((means[display_indices] - critical * standard_errors[display_indices],
                                    means[display_indices] + critical * standard_errors[display_indices]))
    _close(np, simultaneous, np.asarray(primary['simultaneous_95'])[display_indices],
           'saved displayed simultaneous bands disagree with frozen critical value')
    ratio_bands = np.quantile(ratios, [.025, .975], axis=0, method='linear').T
    table = []
    for rate, eta in enumerate(etas):
        row = {'eta': eta, 'methods': {}}
        for method, method_name in enumerate(('AdamW', 'SGD')):
            arms = {}
            for law, copula in enumerate(('independent', 'coupled')):
                cell = rate * 4 + method * 2 + law
                index = cell * 9 + 2
                point = float(means[index])
                arms[copula] = {'risk': point, 'risk_per_eta': point / eta,
                    'order_normalization': 'raw risk' if method == 0 and law == 1 else 'risk/eta',
                    'order_normalized_value': point if method == 0 and law == 1 else point / eta,
                    'replica_se': float(standard_errors[index]),
                    'percentile_95': pointwise[cell].tolist(),
                    'simultaneous_95': simultaneous[cell].tolist()}
            if method == 0:
                arms['coupled_over_independent'] = {
                    'point': arms['coupled']['risk'] / arms['independent']['risk'],
                    'percentile_95': ratio_bands[rate].tolist(),
                    'scope': 'Descriptive paired ratio; approximate pointwise interval only.'}
            else:
                arms['exact_nominal_stationary_control'] = analysis['exact_nominal_sgd_controls'][rate]
            row['methods'][method_name] = arms
        table.append(row)
    diagnostics = _diagnostics(np, primary)
    _require(all(_digest(root / name) == digest for name, digest in sources.items()),
             'recorded inputs changed during reanalysis')
    return {'study': 'q2_matrix_20261117', 'start_index': 0, 'window_index': 2,
            'risk': 'u^T [[2,1.25],[1.25,2]] u / 2, averaged over saved snapshots then replicas',
            'table': table, 'finite_clock_diagnostics': diagnostics,
            'coordinate_mean_diagnostics': {
                'features_in_frozen_analysis': len(analysis['coordinate_diagnostics']['labels']),
                'scope': analysis['coordinate_diagnostics']['scope']},
            'finite_remainder_certified': False,
            'uncertainty': {'saved_full_family_critical_value': critical,
                            'primary_family_size': 432, 'ratio_family': 'descriptive pointwise only'},
            'validation': {'raw_risks_recomputed': 108, 'displayed_bootstrap_risks_recomputed': 12,
                           'saved_resamples_reused': int(len(indices)),
                           'random_draws': 0, 'inputs_unchanged': True},
            'input_files': sources, 'scope': _SCOPE}


def reproduce_tables(data_root, output):
    """Write deterministic JSON exclusively to a fresh caller-selected file.

    No source, recorded artifact, archive receipt, or existing output is changed.
    Parent directories must already exist; this function creates only ``output``.
    """
    output = Path(output).expanduser()
    if output.exists():
        raise FileExistsError(output)
    report = {'schema_version': 1, 'matrix': matrix_table(data_root)}
    encoded = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + '\n'
    with output.open('x', encoding='utf-8') as stream:
        stream.write(encoded)
    return report
