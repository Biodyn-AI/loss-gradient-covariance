"""Short, explicit commands for exact checks and recorded-data reproduction."""
import argparse
from importlib.resources import as_file, files
import json
from pathlib import Path

from . import fixture_law, load_fixture_certificate, matching_report, sgd_stationary_covariance
from .archive import download_data, extract_data, verify_data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check', help='Exact matched-law and nominal SGD identities; no simulation')
    download = commands.add_parser('download-data', help='Download the hash-pinned v1.0.0 archive')
    download.add_argument('--output', type=Path, required=True)
    verify = commands.add_parser('verify-data', help='Verify the archive and all 721 file hashes')
    verify.add_argument('path', type=Path)
    extract = commands.add_parser('extract-data', help='Verify and extract into a NEW workspace')
    extract.add_argument('path', type=Path)
    extract.add_argument('--output', type=Path, required=True)
    tables = commands.add_parser('reproduce-tables', help='Recompute the matrix table from saved data')
    tables.add_argument('--data-root', type=Path, required=True)
    tables.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    try:
        if arguments.command == 'check':
            laws = [fixture_law(name) for name in ('independent', 'coupled')]
            matching = matching_report(*laws)
            if not matching['all_matched']:
                raise ValueError('Matched-law identity failed')
            controls = {}
            for eta in ('0.001', '0.0002', '0.00004'):
                left, right = [sgd_stationary_covariance(law, eta) for law in laws]
                if left != right:
                    raise ValueError('Exact nominal SGD equality failed')
                controls[eta] = left
            assets = files('loss_gradient_covariance').joinpath('certificates')
            with as_file(assets.joinpath('conditioned_matrix_fixture.json')) as fixture:
                with as_file(assets.joinpath('kernel_certificate.json')) as kernel:
                    certificate = load_fixture_certificate(fixture, kernel_path=kernel)
            result = {'matching': matching, 'nominal_rational_sgd': controls,
                      'saved_instability_certificate': certificate['instability_verified'],
                      'scientific_random_draws': 0,
                      'scope': 'Exact finite-example checks; not proof-assistant verification or a mixing bound.'}
        elif arguments.command == 'download-data':
            result = {'path': str(download_data(arguments.output))}
        elif arguments.command == 'verify-data':
            result = verify_data(arguments.path)
        elif arguments.command == 'extract-data':
            result = extract_data(arguments.path, arguments.output)
        else:
            from .recorded import reproduce_tables
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            report = reproduce_tables(arguments.data_root, arguments.output)
            result = {'path': str(arguments.output), 'validation': report['matrix']['validation']}
        print(json.dumps(result, indent=2, default=str, allow_nan=False))
    except (ValueError, OSError, ImportError) as error:
        parser.exit(2, 'error: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
