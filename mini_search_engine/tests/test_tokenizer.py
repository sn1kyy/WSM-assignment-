"""
Unit Tests for Tokenizer Module.
Tests token extraction, punctuation handling, whitespace, and empty input.
"""

import unittest
from src.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    """Test suite for Tokenizer."""

    def setUp(self) -> None:
        self.tokenizer = Tokenizer()

    def test_normal_sentence(self) -> None:
        text = "Apple is a very useful fruit."
        expected = ["Apple", "is", "a", "very", "useful", "fruit"]
        self.assertEqual(self.tokenizer.tokenize(text), expected)

    def test_preserves_case(self) -> None:
        """Tokenizer should NOT case fold; casing belongs to Normalizer."""
        text = "Apple APPLE ApPlE"
        expected = ["Apple", "APPLE", "ApPlE"]
        self.assertEqual(self.tokenizer.tokenize(text), expected)

    def test_punctuation_handling(self) -> None:
        """Verify various punctuation marks are cleanly separated/stripped."""
        text = "Hello, world! Welcome to Information-Retrieval (IR); isn't it great?"
        tokens = self.tokenizer.tokenize(text)
        self.assertIn("Hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("Information", tokens)
        self.assertIn("Retrieval", tokens)
        self.assertIn("IR", tokens)
        # Ensure raw punctuation marks are not tokens themselves
        for p in [",", "!", ";", "(", ")", "?"]:
            self.assertNotIn(p, tokens)

    def test_empty_input(self) -> None:
        self.assertEqual(self.tokenizer.tokenize(""), [])
        self.assertEqual(self.tokenizer.tokenize(None), [])

    def test_whitespace_and_newlines(self) -> None:
        text = "   \n\t  token1   \t\n   token2   \n "
        expected = ["token1", "token2"]
        self.assertEqual(self.tokenizer.tokenize(text), expected)

    def test_punctuation_only_input(self) -> None:
        text = "... ,,, !!! ??? -- ()"
        self.assertEqual(self.tokenizer.tokenize(text), [])


if __name__ == "__main__":
    unittest.main()
