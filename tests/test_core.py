"""Exact mathematical identities and literal, RNG-free update contracts."""
from fractions import Fraction as F
import itertools
import math
from pathlib import Path
import tempfile
import unittest

from loss_gradient_covariance import (
    Atom, fixture_law, gradient_moments, load_fixture_certificate,
    matching_report, sgd_stationary_covariance, simulate,
)


IDENTITY = ((F(1), F(0)), (F(0), F(1)))
ZERO = (0, 0)
CERTIFICATE = Path(__file__).resolve().parents[1] / 'certificates/conditioned_matrix_fixture.json'
KERNEL = CERTIFICATE.with_name('kernel_certificate.json')


class ExactLawTests(unittest.TestCase):
    def test_atomic_pair_matches_complete_marginals_and_covariance(self):
        independent, coupled = map(fixture_law, ('independent', 'coupled'))
        self.assertEqual((len(independent), len(coupled)), (8, 4))
        self.assertEqual(sum(a.probability for a in independent), 1)
        self.assertEqual(sum(a.probability for a in coupled), 1)
        self.assertTrue(all(matching_report(independent, coupled).values()))
        # A higher cross moment still differs, despite the matched summaries.
        moment = lambda law: sum(a.probability * a.hessian[0][0] * a.noise[0] ** 2 for a in law)
        self.assertEqual((moment(independent), moment(coupled)), (1, F(3, 2)))

    def test_cross_covariance_at_distinct_rational_parameters(self):
        for name in ('independent', 'coupled'):
            moments = gradient_moments(fixture_law(name), (1, -1), (2, 1))
            self.assertEqual(moments['mean_u'], (F(3, 4), F(-3, 4)))
            self.assertEqual(moments['mean_v'], (F(21, 4), F(9, 2)))
            self.assertEqual(moments['covariance'], ((F(5, 2), F(-1)), (F(2), F(-1, 2))))

    def test_full_marginal_matching_does_not_hide_changed_covariance(self):
        independent = fixture_law('independent')
        h1, h2 = independent[0].hessian, independent[-1].hessian
        changed = tuple(Atom(F(1, 4), h1 if sign == 1 else h2, noise)
                        for sign, noise in [(1, (1, 0)), (1, (0, 1)),
                                            (-1, (-1, 0)), (-1, (0, -1))])
        report = matching_report(independent, changed)
        self.assertTrue(report['hessian_marginal'])
        self.assertTrue(report['noise_marginal'])
        self.assertTrue(report['mean_gradient'])
        self.assertFalse(report['covariance_kernel'])
        self.assertFalse(report['all_matched'])

    def test_exact_interfaces_reject_float_ambiguity_and_bad_laws(self):
        law = fixture_law('independent')
        with self.assertRaises(TypeError):
            gradient_moments(law, (.1, 0), ZERO)
        with self.assertRaises(TypeError):
            sgd_stationary_covariance(law, .01)
        with self.assertRaises(ValueError):
            fixture_law('other')
        with self.assertRaises(ValueError):
            gradient_moments((Atom(F(1, 2), IDENTITY, ZERO),), ZERO, ZERO)


class StationarySGDTests(unittest.TestCase):
    def test_isotropic_case_has_literal_closed_form(self):
        law = tuple(Atom(F(1, 4), IDENTITY, e)
                    for e in [(1, 0), (-1, 0), (0, 1), (0, -1)])
        control = sgd_stationary_covariance(law, '0.1', decay='0.1')
        self.assertEqual(control['covariance'], ((F(50, 2079), F(0)), (F(0), F(50, 2079))))
        self.assertEqual(control['risk'], F(50, 2079))

    def test_fixture_controls_match_and_satisfy_exact_discrete_equation(self):
        eta, decay = F(1, 1000), F(1, 10)
        controls = [sgd_stationary_covariance(fixture_law(name), eta, decay)
                    for name in ('independent', 'coupled')]
        self.assertEqual(controls[0], controls[1])
        covariance = controls[0]['covariance']
        for i in range(2):
            for j in range(2):
                transformed = F(0)
                for atom in fixture_law('coupled'):
                    transition = tuple(tuple(F(k == l) - eta * (atom.hessian[k][l] + decay * (k == l))
                                             for l in range(2)) for k in range(2))
                    transformed += atom.probability * (
                        sum(transition[i][k] * covariance[k][l] * transition[j][l]
                            for k in range(2) for l in range(2))
                        + eta ** 2 * atom.noise[i] * atom.noise[j])
                self.assertEqual(covariance[i][j], transformed)

    def test_control_rejects_unproved_or_noncontractive_cases(self):
        with self.assertRaises(ValueError):
            sgd_stationary_covariance(fixture_law('coupled'), '1')
        with self.assertRaises(ValueError):
            sgd_stationary_covariance((Atom(F(1), IDENTITY, (1, 0)),), '0.1')
        bad_hessian = ((F(0), F(0)), (F(0), F(1)))
        with self.assertRaises(ValueError):
            sgd_stationary_covariance((Atom(F(1), bad_hessian, ZERO),), '0.1')

    def test_centered_noise_with_nonzero_mixed_moments_is_rejected(self):
        fixture = fixture_law('independent')
        law = (Atom(F(1, 2), fixture[0].hessian, (1, 0)),
               Atom(F(1, 2), fixture[-1].hessian, (-1, 0)))
        with self.assertRaises(ValueError):
            sgd_stationary_covariance(law, '0.01')

    def test_exact_contraction_allows_negative_transition_but_not_boundary(self):
        law = (Atom(F(1, 2), IDENTITY, (1, 0)), Atom(F(1, 2), IDENTITY, (-1, 0)))
        control = sgd_stationary_covariance(law, '1.5', decay=0)
        self.assertEqual(control['covariance'], ((F(3), F(0)), (F(0), F(0))))
        with self.assertRaises(ValueError):
            sgd_stationary_covariance(law, 2, decay=0)


class CertificateTests(unittest.TestCase):
    def test_saved_certificate_chain_and_strict_signs(self):
        certificate = load_fixture_certificate(CERTIFICATE, kernel_path=KERNEL)
        bounds = certificate['decay_plus_field_eigenvalue_bounds']
        self.assertLess(F(bounds['coupled_antisymmetric'][1]), 0)
        self.assertGreater(F(bounds['independent_antisymmetric'][0]), 0)

    def test_even_whitespace_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'changed.json'
            path.write_bytes(CERTIFICATE.read_bytes() + b'\n')
            with self.assertRaises(ValueError):
                load_fixture_certificate(path)


class LiteralSimulationTests(unittest.TestCase):
    def test_sgd_literal_two_step_recurrence_and_population_risk(self):
        law = (Atom(F(1, 2), IDENTITY, (1, -1)), Atom(F(1, 2), IDENTITY, (-1, 1)))
        trace = simulate(law, [0, 0], method='sgd', eta=.25, decay=.5, initial_u=(2., -3.))
        self.assertEqual(trace['u'], [(2., -3.), (1., -1.625), (.375, -.765625)])
        self.assertEqual(trace['steps'], [0, 1, 2])
        self.assertEqual(trace['m'], [(0., 0.)] * 3)
        self.assertEqual(trace['v'], [(0., 0.)] * 3)
        self.assertEqual(trace['risk'][1], .5 * (1 + 1.625 ** 2))
        self.assertIn('finite', trace['scope'])

    def test_adamw_literal_moments_offset_and_separate_decay(self):
        law = (Atom(F(1, 2), IDENTITY, (1, 0)), Atom(F(1, 2), IDENTITY, (-1, 0)))
        trace = simulate(law, [0, 0], method='adamw', eta=.1, alpha=0., beta=.25,
                         epsilon=.5, decay=.2, initial_u=(1., -1.))
        first = (.98 - .2 / (math.sqrt(3) + .5), -.98 + .1 / (math.sqrt(.75) + .5))
        self.assertEqual(trace['m'][1], (2., -1.))
        self.assertEqual(trace['v'][1], (3., .75))
        self.assertEqual(trace['u'][1], first)
        second_gradient = (first[0] + 1, first[1])
        second_variance = (.75 + .75 * second_gradient[0] ** 2,
                           .1875 + .75 * second_gradient[1] ** 2)
        self.assertEqual(trace['m'][2], second_gradient)
        self.assertEqual(trace['v'][2], second_variance)
        for i in range(2):
            expected = .98 * first[i] - .1 * second_gradient[i] / (math.sqrt(second_variance[i]) + .5)
            self.assertEqual(trace['u'][2][i], expected)

    def test_input_tape_is_not_mutated_and_empty_trace_keeps_initial_state(self):
        law, tape = fixture_law('coupled'), [0, 1]
        simulate(law, tape, method='sgd', eta=.001)
        self.assertEqual(tape, [0, 1])
        self.assertEqual(simulate(law, [], method='sgd', eta=.001)['u'], [(0., 0.)])

    def test_invalid_tapes_parameters_and_unbounded_iterators_are_rejected(self):
        law = fixture_law('coupled')
        for tape in ([4], [-1], [True]):
            with self.assertRaises(ValueError):
                simulate(law, tape, method='sgd', eta=.01)
        with self.assertRaises(ValueError):
            simulate(law, [], method='sgd', eta=float('nan'))
        with self.assertRaises(ValueError):
            simulate(law, itertools.repeat(0), method='sgd', eta=.01, max_steps=2)

    def test_nonfinite_initial_risk_is_detected_even_with_empty_tape(self):
        with self.assertRaises(FloatingPointError):
            simulate(fixture_law('coupled'), [], method='sgd', eta=.01, initial_u=(1e308, 1e308))

    def test_simulated_risk_requires_centered_noise_and_positive_hessians(self):
        with self.assertRaises(ValueError):
            simulate((Atom(F(1), IDENTITY, (1, 0)),), [0], method='sgd', eta=.01)
        indefinite = ((F(-1), F(0)), (F(0), F(1)))
        with self.assertRaises(ValueError):
            simulate((Atom(F(1), indefinite, ZERO),), [0], method='sgd', eta=.01)


if __name__ == '__main__':
    unittest.main()
