"""A fresh finite-horizon demo, separate from the archived scientific studies."""
import argparse
import json
from pathlib import Path
import platform
import random

from loss_gradient_covariance import fixture_law, simulate

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--steps', type=int, default=5000)
parser.add_argument('--seed', type=int, default=7)
parser.add_argument('--eta', type=float, default=.001)
parser.add_argument('--output', type=Path, required=True)
arguments = parser.parse_args()
if not 1 <= arguments.steps <= 100000:
    parser.error('Use 1 to 100000 steps for this bounded demonstration')
if arguments.output.exists():
    parser.error('Choose a new output path')
generator = random.Random(arguments.seed)  # Private demo stream; never an archived stream.
traces = {}
for coupling in ('independent', 'coupled'):
    law = fixture_law(coupling)
    tape = [generator.randrange(len(law)) for _ in range(arguments.steps)]
    traces[coupling] = {method: simulate(law, tape, method=method, eta=arguments.eta)
                        for method in ('adamw', 'sgd')}
arguments.output.parent.mkdir(parents=True, exist_ok=True)
record = {'scope': 'Fresh finite-horizon demo, not a stationary-risk estimate or paper replication.',
          'python': platform.python_version(), 'seed': arguments.seed,
          'steps': arguments.steps, 'eta': arguments.eta, 'traces': traces}
with arguments.output.open('x') as stream:
    json.dump(record, stream, allow_nan=False)
    stream.write('\n')
print(arguments.output)
