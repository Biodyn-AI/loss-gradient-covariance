"""Rebuild all four paper displays from byte-pinned saved scientific records.

Install requirements-reproduce.txt, then run from any working directory:
python scripts/reproduce_figures.py --scientific-root data/workspace --output outputs/figures
No trajectories, resamples, confidence intervals or fitted statistics are generated.
The output directory must be new and outside the frozen scientific workspace.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PINS = {
    'results/q2_matrix_analysis_20261117/run/summary.json':
        '93bfb6d29724b8a73bae260eb1627258313f14c744bce7897a2aee4843e33148',
    'results/q2_matrix_validation_20261117/run/summary.json':
        '33fff2e3897f3bd9be0134e34e98bb890b35e98eb2b45fd30809e8c738a12a17',
    'results/q2_quadratic_analysis_20261116/run/summary.json':
        '2cacd0b19a00c04cf2c3909f848023ca6e9923113bc7ceccf90d9431cda5499c',
    'results/q2_matrix_validation_20261117/run/samples_and_terminal.npz':
        'f1df66757c55324655df8eb9d4139ce28740742ad937ad835134bf5f57ec2115',
    'experiments/q2_phase_paper_figures_20261117.py':
        '9ff88d7c24ee3fa6710c13cb134ee35b44458b51bee77492ad968991e45d6e0f',
    'experiments/q2_stationary_figures.py':
        '702cac53e79a11f6148c5f72b0db1e68a2e303bbd22ca8d069312976a62bb888',
    'results/q2_decay_contrast_analysis_20261117/run/summary.json':
        'db1802a09c53214dc21e62f53829b7a1b9afb140ca717de83a04149aba3e201a',
    'experiments/q2_pairing_mechanism_figure_20261117.py':
        '110beda5ca28d5e23c36b457c648530694c1fc74be95b3cdb1ab9439070f0b9b',
    'results/q2_conditioned_matrix_fixture_20261117.json':
        '0069acf768524174571e5a729693e878527fd991282f60a3f7bb89cceedaa2a8',
}
PRODUCERS = (
    'figure_typography_20261117.py',
    'figure1_journal_typography_20261117.py',
    'decay_figure_typography_20261117.py',
)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_inputs(scientific_root):
    """Fail before importing scientific code if any held input differs."""
    root = Path(scientific_root).resolve()
    actual = {name: sha(root / name) for name in PINS}
    mismatches = [name for name, expected in PINS.items() if actual[name] != expected]
    if mismatches:
        raise ValueError('frozen scientific input SHA256 mismatch: ' + ', '.join(mismatches))
    return actual


def load_producer(filename):
    path = REPOSITORY / 'paper' / filename
    specification = importlib.util.spec_from_file_location('public_' + path.stem, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def reproduce(scientific_root, output):
    root, output = Path(scientific_root).resolve(), Path(output).resolve()
    if output.exists():
        raise FileExistsError('refusing to overwrite output directory: ' + str(output))
    if output == root or root in output.parents:
        raise ValueError('write figure output outside the frozen scientific workspace')
    before = verify_inputs(root)
    producer_before = {name: sha(REPOSITORY / 'paper' / name) for name in PRODUCERS}
    typography, mechanism, decay = [load_producer(name) for name in PRODUCERS]
    # These input identities remain the historical producers' exact PINS.
    if any(PINS.get(name) != digest for module in (typography, decay) for name, digest in module.PINS.items()):
        raise ValueError('public wrapper and original producer input pins disagree')
    matrix = json.loads((root / 'results/q2_matrix_analysis_20261117/run/summary.json').read_text())
    native = json.loads((root / 'results/q2_matrix_validation_20261117/run/summary.json').read_text())
    scalar = json.loads((root / 'results/q2_quadratic_analysis_20261116/run/summary.json').read_text())
    response = json.loads((root / 'results/q2_decay_contrast_analysis_20261117/run/summary.json').read_text())
    if not (matrix['analysis_complete'] and native['study_complete']
            and scalar['analysis_complete'] and response['analysis_complete']):
        raise ValueError('only complete frozen studies may supply figure displays')
    # Copy exactly the four complete zero-start terminal clouds used before.
    with typography.np.load(root / 'results/q2_matrix_validation_20261117/run/samples_and_terminal.npz',
                            allow_pickle=False) as saved:
        state = saved['state']
        if state.shape != (12, 3, 3, 2, 256):
            raise ValueError('unexpected frozen terminal-state layout')
        clouds = [state[cell, 0, 0].copy() for cell in (8, 9, 10, 11)]
    figures = [
        ('matrix_phases', typography.matrix_figure(matrix['zero_start_final_window_table'], clouds)[0]),
        ('scalar_couplings', typography.scalar_figure(scalar['zero_start_final_window_table'],
                                                    scalar['independent_99_oracle'])[0]),
        ('decay_contrast', decay.decay_figure(response['zero_start_final_window_table'])[0]),
    ]
    for _, figure in figures:
        typography.assert_fonts_and_bounds(figure)
    output.mkdir(parents=True, exist_ok=False)
    try:
        # Do not call typography.run() or decay.run(): those historical entry
        # points have fixed destinations and one-execution archival receipts.
        for name, figure in figures:
            figure.savefig(output / (name + '.pdf'), metadata={'CreationDate': None, 'ModDate': None})
            figure.savefig(output / (name + '.svg'), metadata={'Date': None})
            figure.savefig(output / (name + '.png'))
        mechanism.run(root, output)
    finally:
        for _, figure in figures:
            typography.plt.close(figure)
    after = verify_inputs(root)
    producer_after = {name: sha(REPOSITORY / 'paper' / name) for name in PRODUCERS}
    if producer_before != producer_after:
        raise ValueError('public figure producer changed during rendering')
    paths = [output / (name + '.' + extension)
             for name in ('pairing_mechanism', 'matrix_phases', 'scalar_couplings', 'decay_contrast')
             for extension in ('pdf', 'svg', 'png')]
    receipt = {
        'status': 'complete', 'scientific_random_draws': 0, 'fitted_parameters': 0,
        'new_scientific_statistics': 0, 'input_sha256_before': before, 'input_sha256_after': after,
        'scientific_inputs_unchanged': before == after,
        'wrapper_source_sha256': sha(Path(__file__)),
        'producer_sha256_before': producer_before, 'producer_sha256_after': producer_after,
        'retained_display': {
            'matrix_curves': 4, 'matrix_steps': 3, 'terminal_clouds': 4,
            'replicas_per_cloud': 256, 'scalar_curves': 4, 'scalar_ratio_curves': 2,
            'scalar_steps': 3, 'decay_points': 2,
        },
        'scope': 'Saved declared displays and certified local mechanism only. '
                 'No trajectories, resamples, fitted exponents or new uncertainty estimates. '
                 'Matrix intervals: approximate simultaneous 95%; scalar: approximate pointwise 95% '
                 'and separate joint 99% oracle; decay: approximate simultaneous 95% and separate '
                 'joint 98% functional enclosure. Unknown finite-step and equilibration errors '
                 'remain excluded. Regeneration does not prove stationarity or mixing.',
        'artifacts': {path.name: {'bytes': path.stat().st_size, 'sha256': sha(path)} for path in paths},
    }
    with (output / 'reproduction_receipt.json').open('x') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scientific-root', type=Path, default=REPOSITORY / 'data' / 'workspace')
    parser.add_argument('--output', type=Path, help='new output directory; existing paths are refused')
    parser.add_argument('--check-inputs', action='store_true', help='only verify all nine frozen inputs; write nothing')
    arguments = parser.parse_args()
    try:
        if arguments.check_inputs:
            pins = verify_inputs(arguments.scientific_root)
            print(json.dumps({'status': 'verified', 'pinned_inputs': len(pins), 'scientific_random_draws': 0}))
        else:
            if arguments.output is None:
                parser.error('--output is required unless --check-inputs is used')
            receipt = reproduce(arguments.scientific_root, arguments.output)
            print(json.dumps({'status': receipt['status'], 'figure_files': len(receipt['artifacts']),
                              'output': str(arguments.output), 'scientific_random_draws': 0}))
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
