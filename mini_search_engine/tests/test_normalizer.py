"""
Unit Tests for Normalizer Module.
Tests case folding, lowercase conversion, and token standardization.
"""

import unittest
from src.normalizer import Normalizer


class TestNormalizer(unittest.TestCase):
    """Test suite for Normalizer."""

    def setUp(self) -> None:
        self.normalizer = Normalizer()

    def test_lowercase_conversion(self) -> None:
        self.assertEqual(self.normalizer.normalize_token("apple"), "apple")

    def test_uppercase_input(self) -> None:
        self.assertEqual(self.normalizer.normalize_token("APPLE"), "apple")

    def test_mixed_case_input(self) -> None:
        self.assertEqual(self.normalizer.normalize_token("ApPlE"), "apple")
        self.assertEqual(self.normalizer.normalize_token("Apple"), "apple")

    def test_token_with_punctuation(self) -> None:
        self.assertEqual(self.normalizer.normalize_token("...apple!"), "apple")
        self.assertEqual(self.normalizer.normalize_token("'database'"), "database")

    def test_empty_input(self) -> None:
        self.assertEqual(self.normalizer.normalize_token(""), "")
        self.assertEqual(self.normalizer.normalize_token("   "), "")

    def test_normalize_tokens_list(self) -> None:
        tokens = ["Apple", "BANANA", "Computer!", "..."]
        expected = ["apple", "banana", "computer"]
        self.assertEqual(self.normalizer.normalize_tokens(tokens), expected)

    def test_normalize_empty_list(self) -> None:
        self.assertEqual(self.normalizer.normalize_tokens([]), [])


if __name__ == "__main__":
    unittest.main()
