import unittest

from utils.helpers import format_currency, format_percent, normalize_whitespace, safe_get


class HelpersTestCase(unittest.TestCase):
    def test_format_currency(self):
        self.assertEqual(format_currency(1234.5, "USD"), "USD 1,234.50")

    def test_format_percent(self):
        self.assertEqual(format_percent(0.1234), "0.12%")

    def test_normalize_whitespace(self):
        self.assertEqual(normalize_whitespace("a   b \n c"), "a b c")

    def test_safe_get(self):
        data = {"a": {"b": {"c": 1}}}
        self.assertEqual(safe_get(data, "a.b.c"), 1)
        self.assertIsNone(safe_get(data, "a.b.d"))


if __name__ == "__main__":
    unittest.main()

