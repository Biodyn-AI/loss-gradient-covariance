"""Small exact tools for the paper's atomic matched-curvature examples.

Exact functions accept integers, ``Fraction`` values and decimal strings;
floats are rejected to distinguish nominal decimals from binary64 numbers.
For example, ``sgd_stationary_covariance(fixture_law('coupled'), '0.001')``
returns exact rational covariance and risk. ``simulate`` intentionally uses
floating-point arithmetic and a caller-supplied atom-index tape, never an RNG.
Its complete finite-horizon trace is not a stationary or mixing certificate.
"""
from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import islice
import json
import math
from pathlib import Path
from typing import NamedTuple


class Atom(NamedTuple):
    """One finite-law atom; nested tuples make fixture laws immutable."""
    probability: Fraction
    hessian: tuple
    noise: tuple


_FIXTURE_SHA = '0069acf768524174571e5a729693e878527fd991282f60a3f7bb89cceedaa2a8'
_KERNEL_SHA = '50c12257117198e4c3c523e07a06807d10fc5fcbab0cc4add86b914f24ddf0d4'
_ZERO = (Fraction(0), Fraction(0))
_BASIS = (_ZERO, (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))


def _fraction(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise TypeError('exact values require int, Fraction or decimal string; floats are ambiguous')
    return Fraction(value)


def _vector(values):
    vector = tuple(_fraction(value) for value in values)
    if len(vector) != 2:
        raise ValueError('a vector must have two coordinates')
    return vector


def _law(atoms):
    normalized = []
    for atom in atoms:
        probability, hessian, noise = atom
        matrix = tuple(_vector(row) for row in hessian)
        if len(matrix) != 2 or matrix[0][1] != matrix[1][0]:
            raise ValueError('sample Hessians must be symmetric 2x2 matrices')
        normalized.append(Atom(_fraction(probability), matrix, _vector(noise)))
    if not normalized or any(atom.probability <= 0 for atom in normalized):
        raise ValueError('a nonempty law needs positive atom probabilities')
    if sum(atom.probability for atom in normalized) != 1:
        raise ValueError('atom probabilities must sum exactly to one')
    return tuple(normalized)


def fixture_law(coupling):
    """Return the exact eight-atom independent or four-atom coupled law.

    Hessians are [[1,5/4],[5/4,3]] and its coordinate exchange. Noise is
    equally likely to be either sign of either coordinate vector. Coupling
    pairs the first Hessian with noise in coordinate 1 (zero-based index).
    """
    if coupling not in ('independent', 'coupled'):
        raise ValueError("coupling must be 'independent' or 'coupled'")
    matrices = (((1, '1.25'), ('1.25', 3)), ((3, '1.25'), ('1.25', 1)))
    atoms = []
    for hessian_index, hessian in enumerate(matrices):
        for active in range(2):
            if coupling == 'coupled' and hessian_index == active:
                continue
            for sign in (-1, 1):
                noise = tuple(sign if coordinate == active else 0 for coordinate in range(2))
                atoms.append(Atom(Fraction(1, 8 if coupling == 'independent' else 4), hessian, noise))
    return _law(atoms)


def _gradient(atom, u):
    return tuple(sum(atom.hessian[i][j] * u[j] for j in range(2)) + atom.noise[i] for i in range(2))


def _moments(law, u, v):
    gradients = [(atom.probability, _gradient(atom, u), _gradient(atom, v)) for atom in law]
    mean_u = tuple(sum(p * left[i] for p, left, _ in gradients) for i in range(2))
    mean_v = tuple(sum(p * right[i] for p, _, right in gradients) for i in range(2))
    covariance = tuple(tuple(sum(p * (left[i] - mean_u[i]) * (right[j] - mean_v[j])
                                 for p, left, right in gradients) for j in range(2)) for i in range(2))
    return {'mean_u': mean_u, 'mean_v': mean_v, 'covariance': covariance}


def gradient_moments(law, u, v):
    """Exact means and same-sample cross covariance at two rational parameters.

    The covariance need not be symmetric when u and v differ. Parameters
    and every law entry follow the exact input convention in the module docstring.
    """
    return _moments(_law(law), _vector(u), _vector(v))


def matching_report(left, right):
    """Check complete marginals and equality of means/covariance for ALL u,v.

    Covariance is affine in each argument separately. Its values at the
    nine pairs drawn from {0,(1,0),(0,1)} determine every polynomial
    coefficient exactly; this is an algebraic identity check, not sampling.
    """
    left, right = _law(left), _law(right)
    def marginal(law, field):
        weights = defaultdict(Fraction)
        for atom in law:
            weights[getattr(atom, field)] += atom.probability
        return dict(weights)
    report = {field + '_marginal': marginal(left, field) == marginal(right, field)
              for field in ('hessian', 'noise')}
    report['mean_gradient'] = all(_moments(left, u, _ZERO)['mean_u'] == _moments(right, u, _ZERO)['mean_u']
                                  for u in _BASIS)
    report['covariance_kernel'] = all(
        _moments(left, u, v)['covariance'] == _moments(right, u, v)['covariance']
        for u in _BASIS for v in _BASIS)
    report['all_matched'] = all(report.values())
    return report


def _positive_definite(matrix):
    return matrix[0][0] > 0 and matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2 > 0


def _solve(matrix, rhs):
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for column in range(len(rhs)):
        pivot = next((row for row in range(column, len(rhs)) if augmented[row][column]), None)
        if pivot is None:
            raise ValueError('singular covariance equation')
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(len(rhs)):
            if row != column:
                factor = augmented[row][column]
                augmented[row] = [a - factor * b for a, b in zip(augmented[row], augmented[column])]
    return tuple(row[-1] for row in augmented)


def sgd_stationary_covariance(law, eta, decay='0.1'):
    """Exact nominal-rational stationary covariance and population risk.

    This restricted helper requires positive sample Hessians, centered
    noise and every mixed moment E[A_ij e_k]=0. For each atom it checks
    B=A+decay*I>0 and 2I-eta*B>0 exactly (uniform strict contraction).
    It then solves Sigma=E[T Sigma T^T]+eta^2 E[ee^T], T=I-eta*B.
    It is a real-arithmetic control, not a floating-point stationary identity.
    """
    law, eta, decay = _law(law), _fraction(eta), _fraction(decay)
    if eta <= 0 or decay < 0:
        raise ValueError('eta must be positive and decay nonnegative')
    if _moments(law, _ZERO, _ZERO)['mean_u'] != _ZERO:
        raise ValueError('stationary control requires centered noise')
    if any(sum(a.probability * a.hessian[i][j] * a.noise[k] for a in law)
           for i in range(2) for j in range(2) for k in range(2)):
        raise ValueError('stationary control requires all E[A_ij e_k]=0')
    transitions = []
    for atom in law:
        shifted = tuple(tuple(atom.hessian[i][j] + decay * (i == j) for j in range(2)) for i in range(2))
        upper = tuple(tuple(2 * (i == j) - eta * shifted[i][j] for j in range(2)) for i in range(2))
        if not all(_positive_definite(m) for m in (atom.hessian, shifted, upper)):
            raise ValueError('positive Hessians and uniformly contractive SGD steps are required')
        transitions.append(tuple(tuple((i == j) - eta * shifted[i][j] for j in range(2)) for i in range(2)))
    basis = (((1, 0), (0, 0)), ((0, 0), (0, 1)), ((0, 1), (1, 0)))
    positions = ((0, 0), (1, 1), (0, 1))
    columns = []
    for matrix in basis:
        columns.append([matrix[i][j] - sum(
            atom.probability * sum(t[i][k] * matrix[k][l] * t[j][l] for k in range(2) for l in range(2))
            for atom, t in zip(law, transitions)) for i, j in positions])
    operator = list(zip(*columns))
    rhs = [eta ** 2 * sum(a.probability * a.noise[i] * a.noise[j] for a in law) for i, j in positions]
    c00, c11, c01 = _solve(operator, rhs)
    covariance = ((c00, c01), (c01, c11))
    risk = sum(a.probability * sum(a.hessian[i][j] * covariance[j][i] for i in range(2) for j in range(2))
               for a in law) / 2
    return {'covariance': covariance, 'risk': risk}


def load_fixture_certificate(path, *, kernel_path=None):
    """Read the byte-verified saved fixture bounds; optionally verify their kernel.

    Supply paths inside this repository's certificates/ directory, or copies
    of those exact files. No old private filesystem path is consulted and no
    bound is recomputed. Returned decimal strings retain the original bounds.
    """
    def verified(path, digest):
        body = Path(path).read_bytes()
        if hashlib.sha256(body).hexdigest() != digest:
            raise ValueError('certificate SHA256 mismatch')
        return json.loads(body)
    fixture = verified(path, _FIXTURE_SHA)
    if kernel_path is not None:
        verified(kernel_path, _KERNEL_SHA)
    if fixture['source_kernel_certificate_sha256'] != _KERNEL_SHA:
        raise ValueError('unexpected kernel-certificate link')
    return fixture


def simulate(law, atom_indices, *, method, eta, alpha=.1, beta=.2,
             epsilon=.03, decay=.1, initial_u=(0., 0.), max_steps=100000):
    """Return a complete float AdamW/SGD trace for a supplied integer tape.

    No RNG is created. A caller may sample indices using atom probabilities,
    with a private generator. Entries 0..len(law)-1 select atoms; initial
    moments are zero, epsilon is outside sqrt, and bias correction is absent.
    Sample Hessians must be positive definite and noise centered, making
    risk=0.5*u^T E[A]*u the excess population loss. SGD moment traces stay zero.
    State/risk lists include step zero. Storage grows with the user horizon;
    max_steps bounds input consumption and trace size (default 100,000).
    These are fresh finite-horizon observations, not stationary samples.
    """
    law = _law(law)
    if (any(not _positive_definite(atom.hessian) for atom in law)
            or _moments(law, _ZERO, _ZERO)['mean_u'] != _ZERO):
        raise ValueError('simulation risk requires positive sample Hessians and centered noise')
    if type(max_steps) is not int or max_steps < 0:
        raise ValueError('max_steps must be a nonnegative integer')
    tape = tuple(islice(atom_indices, max_steps + 1))
    if len(tape) > max_steps or any(type(i) is not int or not 0 <= i < len(law) for i in tape):
        raise ValueError('tape exceeds the step limit or contains an invalid atom index')
    eta, alpha, beta, epsilon, decay = map(float, (eta, alpha, beta, epsilon, decay))
    if not all(map(math.isfinite, (eta, alpha, beta, epsilon, decay))):
        raise ValueError('optimizer parameters must be finite')
    if (method not in ('adamw', 'sgd') or eta <= 0 or decay < 0 or epsilon <= 0
            or not 0 <= alpha < math.sqrt(beta) < 1):
        raise ValueError('require adamw/sgd, eta>0, decay>=0, epsilon>0 and 0<=alpha<sqrt(beta)<1')
    u = tuple(map(float, initial_u))
    if len(u) != 2 or not all(map(math.isfinite, u)):
        raise ValueError('initial_u must contain two finite coordinates')
    matrices = [tuple(tuple(map(float, row)) for row in atom.hessian) for atom in law]
    noise = [tuple(map(float, atom.noise)) for atom in law]
    average = tuple(tuple(sum(float(a.probability) * h[i][j] for a, h in zip(law, matrices))
                          for j in range(2)) for i in range(2))
    def risk(vector):
        return .5 * sum(vector[i] * average[i][j] * vector[j] for i in range(2) for j in range(2))
    m = v = (0., 0.)
    initial_risk = risk(u)
    if not math.isfinite(initial_risk):
        raise FloatingPointError('nonfinite population risk at step 0')
    trace = {'steps': list(range(len(tape) + 1)), 'u': [u], 'm': [m], 'v': [v], 'risk': [initial_risk],
             'method': method, 'scope': 'finite-horizon trace; no stationarity or mixing guarantee'}
    for step, index in enumerate(tape, 1):
        gradient = tuple(sum(matrices[index][i][j] * u[j] for j in range(2)) + noise[index][i] for i in range(2))
        if method == 'adamw':
            m = tuple(alpha * m[i] + (1 - alpha) * gradient[i] for i in range(2))
            v = tuple(beta * v[i] + (1 - beta) * gradient[i] * gradient[i] for i in range(2))
            action = tuple(m[i] / (math.sqrt(v[i]) + epsilon) for i in range(2))
        else:
            action = gradient
        u = tuple((1 - eta * decay) * u[i] - eta * action[i] for i in range(2))
        loss = risk(u)
        if not all(map(math.isfinite, u + m + v + (loss,))):
            raise FloatingPointError(f'nonfinite simulation state at step {step}')
        for key, value in (('u', u), ('m', m), ('v', v), ('risk', loss)):
            trace[key].append(value)
    return trace
