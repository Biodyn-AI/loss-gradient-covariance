"""Exact matched-law tools and finite-horizon toy simulations."""
from .core import (
    Atom, fixture_law, gradient_moments, load_fixture_certificate,
    matching_report, sgd_stationary_covariance, simulate,
)

__all__ = [
    'Atom', 'fixture_law', 'gradient_moments', 'matching_report',
    'sgd_stationary_covariance', 'load_fixture_certificate', 'simulate',
]
