from django.test import SimpleTestCase

from customers.services import calculate_approved_limit


class CustomerServiceTests(SimpleTestCase):
    def test_approved_limit_is_rounded_to_nearest_lakh(self):
        self.assertEqual(calculate_approved_limit(50_000), 1_800_000)
        self.assertEqual(calculate_approved_limit(48_500), 1_700_000)

