from django.test import SimpleTestCase

from common.utils import calculate_emi


class LoanUtilityTests(SimpleTestCase):
    def test_calculates_standard_emi(self):
        self.assertEqual(calculate_emi(100_000, 12, 12), 8884.88)

    def test_zero_interest_splits_principal_across_tenure(self):
        self.assertEqual(calculate_emi(120_000, 0, 12), 10000.0)

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_emi(0, 12, 12)
        with self.assertRaises(ValueError):
            calculate_emi(100_000, 12, 0)
