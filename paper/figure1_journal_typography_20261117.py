"""Reformat the existing certified mechanism at its final journal size.

Only typography and verbal labels change. The original scientific producer
supplies all conditional responses, exact bounds and outward-rounded labels.
This script draws no random values, fits nothing, and preserves the original
9.5:4.3 aspect ratio at a physical width of 119 mm. All text is at least 8 pt.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


DIRECTORY = Path(__file__).resolve().parent
ROOT = DIRECTORY.parent / 'data' / 'workspace'
ORIGINAL_SHA = '110beda5ca28d5e23c36b457c648530694c1fc74be95b3cdb1ab9439070f0b9b'
WIDTH_MM = 119.0
ASPECT = 4.3 / 9.5


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(scientific_root=ROOT, output_directory=DIRECTORY / 'figures'):
    original = Path(scientific_root) / 'experiments/q2_pairing_mechanism_figure_20261117.py'
    output_directory = Path(output_directory)
    assert output_directory.is_dir()
    # Loading the held producer executes no plotting or numerical experiment.
    specification = importlib.util.spec_from_file_location('held_mechanism', original)
    held = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(held)
    certificate, response = held.read_certificate()
    certificate_before = sha(held.CERTIFICATE)
    original_before = sha(original)
    assert original_before == ORIGINAL_SHA
    colors = {'independent': '#1767a6', 'coupled': '#b63c39'}
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 8,
        'axes.titlesize': 8, 'axes.labelsize': 8,
        'xtick.labelsize': 8, 'ytick.labelsize': 8,
        'legend.fontsize': 8, 'svg.fonttype': 'none',
        'pdf.fonttype': 42, 'axes.spines.top': False,
        'axes.spines.right': False,
    })
    width = WIDTH_MM / 25.4
    figure = plt.figure(figsize=(width, width * ASPECT))
    left = figure.add_axes([.070, .240, .250, .590])
    middle = figure.add_axes([.415, .240, .225, .590])
    right = figure.add_axes([.700, .195, .290, .690])

    # a: ordinary conditional responses. The original exact enumeration
    # verifies that both coordinate rows agree and both means are 3/4.
    for name, offset in (('independent', -.17), ('coupled', .17)):
        heights = [float(value) for value in response[name][0]]
        positions = [offset, 1 + offset]
        left.bar(positions, heights, width=.30, color=colors[name])
        for position, height in zip(positions, heights):
            label = {Fraction(3, 4): '.75', Fraction(-1, 4): '-.25',
                     Fraction(7, 4): '1.75'}[Fraction(height)]
            left.text(position, height + (.045 if height >= 0 else -.045),
                      label, ha='center',
                      va='bottom' if height >= 0 else 'top', fontsize=8)
    left.axhline(0, color='#555555', linewidth=.6)
    left.set(xticks=[0, 1], xticklabels=['Quiet', 'Noisy'],
             yticks=[0, 1, 2], xlim=(-.50, 1.52), ylim=(-.57, 2.24))
    left.tick_params(axis='both', pad=2, length=2)
    left.set_xlabel('Mean = .75 in both', labelpad=2)
    figure.text(.066, .967, 'a  Row response', fontsize=8.5,
                ha='left', va='top', weight='bold')
    # This color key also identifies the two local-drift rows in panel c.
    handles = [Line2D([0], [0], color=colors[name], lw=3)
               for name in ('independent', 'coupled')]
    figure.legend(handles, ['Independent', 'Coupled'],
                  loc='lower left', bbox_to_anchor=(.010, -.008),
                  frameon=False, ncol=2, handlelength=.9,
                  handletextpad=.35, columnspacing=.85, borderaxespad=0)

    # b: the same full-history susceptibility in both laws. Each label is
    # an outward-rounded enclosure, inherited without recomputation/fitting.
    displayed_kernel = {}
    for position, key in enumerate(('quiet', 'noisy')):
        interval = tuple(Fraction(value) for value in certificate['kernel_bounds'][key])
        lower, upper = map(float, interval)
        middle.bar(position, lower, width=.48, color='#d2a13c', alpha=.35)
        middle.vlines(position, lower, upper, color='#986b17', linewidth=4)
        middle.hlines([lower, upper], position - .14, position + .14,
                      color='#986b17', linewidth=.8)
        labels = held.outward_label(interval)
        displayed_kernel[key] = labels
        middle.text(position, upper + .16, labels[0] + '-' + labels[1],
                    ha='center', va='bottom', fontsize=8)
    middle.set(xticks=[0, 1], xticklabels=[r'$\Psi(0)$', r'$\Psi(1)$'],
               yticks=[0, 2, 4, 6], xlim=(-.58, 1.58), ylim=(0, 7.10))
    middle.tick_params(axis='both', pad=2, length=2)
    middle.set_xlabel('Same in both', labelpad=2)
    figure.text(.403, .967, 'b  AdamW weight', fontsize=8.5,
                ha='left', va='top', weight='bold')

    # c: arrows encode signs only, not magnitudes, finite-radius fields,
    # simulated trajectories or a stationarity assertion.
    right.set(xlim=(0, 1), ylim=(0, 1))
    right.axis('off')
    figure.text(.702, .967, 'c  Local motion', fontsize=8.5,
                ha='left', va='top', weight='bold')
    right.text(.5, .990, r'$u=(x,-x),\ \dot{x}=-kx$',
               ha='center', va='top', fontsize=8)
    displayed_rates = {}
    for name, height in (('independent', .570), ('coupled', .030)):
        interval = tuple(Fraction(value) for value in certificate[
            'decay_plus_field_eigenvalue_bounds'][name + '_antisymmetric'])
        labels = held.outward_label(interval)
        displayed_rates[name] = labels
        right.text(.5, height + .270, name.capitalize(), ha='center',
                   va='top', color=colors[name], fontsize=8)
        right.text(.5, height + .155,
                   r'$k\in[' + labels[0] + ',' + labels[1] + ']$',
                   ha='center', va='top', color=colors[name], fontsize=8)
        right.plot([.06, .94], [height, height], color='#dddddd', linewidth=.7)
        for start, end in ((.08, .44), (.92, .56)):
            if name == 'coupled':
                start, end = end, start
            right.annotate('', xy=(end, height), xytext=(start, height),
                           arrowprops={'arrowstyle': '-|>', 'color': colors[name],
                                       'lw': 1.5, 'mutation_scale': 9})
        right.plot(.5, height, 'o', color='#222222', markersize=2.2)
        right.text(.5, height - .040, '0', ha='center', va='top', fontsize=8)
        right.text(.5, height - .155,
                   'Inward' if name == 'independent' else 'Outward',
                   ha='center', va='top', color=colors[name], fontsize=8)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    all_text = [artist for artist in figure.findobj(matplotlib.text.Text)
                if artist.get_visible() and artist.get_text()]
    assert all(artist.get_fontsize() >= 8 for artist in all_text)
    canvas_box = figure.bbox
    # Every visible text bounding box must be entirely on the fixed canvas.
    # No tight-crop resizing is used, preserving the exact journal aspect.
    for artist in all_text:
        box = artist.get_window_extent(renderer)
        assert (box.x0 >= canvas_box.x0 - .5 and box.y0 >= canvas_box.y0 - .5
                and box.x1 <= canvas_box.x1 + .5 and box.y1 <= canvas_box.y1 + .5), (
                    artist.get_text(), tuple(box.bounds), tuple(canvas_box.bounds))
    right_text = [artist for artist in right.texts if artist.get_visible()]
    for position, first in enumerate(right_text):
        for second in right_text[position + 1:]:
            assert not first.get_window_extent(renderer).overlaps(
                second.get_window_extent(renderer)), (first.get_text(), second.get_text())
    paths = [output_directory / ('pairing_mechanism.' + suffix)
             for suffix in ('pdf', 'svg', 'png')]
    for path in paths:
        figure.savefig(path, dpi=300)
    plt.close(figure)
    assert sha(held.CERTIFICATE) == certificate_before
    assert sha(original) == original_before
    metrics = {
        'source_sha256': sha(Path(__file__)),
        'original_producer_sha256': original_before,
        'certificate_sha256': certificate_before,
        'width_mm': WIDTH_MM, 'height_mm': WIDTH_MM * ASPECT,
        'minimum_text_size_pt': min(artist.get_fontsize() for artist in all_text),
        'scientific_random_draws': 0, 'fitted_parameters': 0,
        'conditional_coordinate_responses': {
            name: [[str(value) for value in row] for row in rows]
            for name, rows in response.items()},
        'kernel_bounds': certificate['kernel_bounds'],
        'local_rate_bounds': {name: certificate['decay_plus_field_eigenvalue_bounds'][
            name + '_antisymmetric'] for name in response},
        'displayed_outward_kernel_enclosures': displayed_kernel,
        'displayed_outward_rate_enclosures': displayed_rates,
        'scope': 'Unchanged certified atomic example; local averaged drift signs only. '
                 'Bounds are deterministic, not confidence intervals. '
                 'Full-history weights, not instantaneous inverse-noise factors. '
                 'No trajectories or stationarity conclusion is inferred from arrows.',
        'artifacts': {path.name: {'sha256': sha(path), 'bytes': path.stat().st_size}
                      for path in paths},
    }
    (output_directory / 'pairing_mechanism_journal_typography_metrics.json').write_text(
        json.dumps(metrics, indent=2) + '\n')
    print(json.dumps({'width_mm': WIDTH_MM, 'height_mm': WIDTH_MM * ASPECT,
                      'minimum_font_pt': metrics['minimum_text_size_pt'],
                      'scientific_random_draws': 0, 'fitted_parameters': 0}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scientific-root', type=Path, default=ROOT,
                        help='Scientific archive root containing experiments/ and results/.')
    parser.add_argument('--output-dir', type=Path, default=DIRECTORY / 'figures')
    arguments = parser.parse_args()
    run(arguments.scientific_root, arguments.output_dir)
