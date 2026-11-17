"""Build the main paper and supplement with their cross-file references.

Requires pdflatex and bibtex on PATH. No experiment or random-number
generator is run. Output goes to a separate build directory.
"""
import argparse
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=Path('build'))
args = parser.parse_args()
source = Path(__file__).resolve().parent
# Load by exact path so isolated Python (-I) does not need the paper directory
# on sys.path. Verified existing publisher files make this a network-free check.
runpy.run_path(str(source / 'fetch_template.py'))['ensure_template'](source)
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=True)
environment = os.environ.copy()
# xr-hyper must find the other document's auxiliary file during each pass.
environment['TEXINPUTS'] = str(output) + os.pathsep + str(source) + os.pathsep
environment['BIBINPUTS'] = str(source) + os.pathsep
environment['BSTINPUTS'] = str(source) + os.pathsep
latex = shutil.which('pdflatex') or '/Library/TeX/texbin/pdflatex'
bibtex = shutil.which('bibtex') or '/Library/TeX/texbin/bibtex'

def run(command, cwd):
    completed = subprocess.run(command, cwd=cwd, env=environment,
                               text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    if completed.returncode:
        raise SystemExit(completed.stdout)

def typeset(stem):
    run([latex, '-halt-on-error', '-interaction=nonstopmode',
         '-output-directory=' + str(output), stem + '.tex'], source)

# First establish both documents, then resolve the bibliography and the
# circular main/supplement references. Extra passes handle counter changes.
typeset('manuscript')
run([bibtex, 'manuscript'], output)
# JOTA's current rule orders three-or-more-author entries with the same
# first author chronologically. Its legacy style instead compares every
# coauthor name. Reorder complete rendered entries; retain their contents.
bbl_path = output / 'manuscript.bbl'
bbl = bbl_path.read_text()
entries = {match.group(1): match.group(0) for match in re.finditer(
    r'\\bibitem\{([^}]+)\}.*?(?=\\bibitem|\\end\{thebibliography\})', bbl, re.S)}
order = json.loads((source / 'reference_order.json').read_text())['keys']
if len(order) != len(set(order)) or set(order) != set(entries):
    raise SystemExit('Reference inventory differs from the validated order')
bbl_path.write_text(bbl[:bbl.index('\\bibitem')] + ''.join(entries[key] for key in order)
                    + bbl[bbl.index('\\end{thebibliography}'):])
typeset('ESM_1')
for _ in range(3):
    typeset('manuscript')
    typeset('ESM_1')
for stem in ('manuscript', 'ESM_1'):
    log = (output / (stem + '.log')).read_text()
    if re.search(r'undefined|Rerun to get|Label\(s\) may have changed', log):
        raise SystemExit(stem + ': unresolved references or unstable labels')
    print(stem + ': ' + str(output / (stem + '.pdf')))
