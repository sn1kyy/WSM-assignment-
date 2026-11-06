"""
Unit Tests for InvertedIndex Module.
Tests index construction, posting retrieval, multi-document terms, and vocabulary.
"""

import unittest
from src.inverted_index import InvertedIndex


class TestInvertedIndex(unittest.TestCase):
    """Test suite for InvertedIndex."""

    def setUp(self) -> None:
        self.index = InvertedIndex()
        self.sample_docs = {
            "doc1": "apple banana",
            "doc2": "apple computer",
            "doc3": "banana database system",
            "doc4": "",  # Empty document test
        }
        self.index.build(self.sample_docs)

    def test_index_creation(self) -> None:
        raw_index = self.index.get_index()
        self.assertIn("apple", raw_index)
        self.assertIn("banana", raw_index)
        self.assertIn("computer", raw_index)
        self.assertIn("database", raw_index)
        self.assertIn("system", raw_index)

    def test_term_lookup(self) -> None:
        self.assertEqual(self.index.search_term("computer"), {"doc2"})
        self.assertEqual(self.index.search_term("database"), {"doc3"})

    def test_multiple_documents_containing_same_term(self) -> None:
        # "apple" appears in doc1 and doc2
        self.assertEqual(self.index.search_term("apple"), {"doc1", "doc2"})
        # "banana" appears in doc1 and doc3
        self.assertEqual(self.index.search_term("banana"), {"doc1", "doc3"})

    def test_term_lookup_case_insensitivity(self) -> None:
        # Querying with different casings should normalize and match
        self.assertEqual(self.index.search_term("APPLE"), {"doc1", "doc2"})
        self.assertEqual(self.index.search_term("Apple"), {"doc1", "doc2"})

    def test_unknown_term(self) -> None:
        self.assertEqual(self.index.search_term("nonexistent"), set())
        self.assertEqual(self.index.search_term(""), set())

    def test_vocabulary_retrieval(self) -> None:
        vocab = self.index.get_vocabulary()
        expected_vocab = {"apple", "banana", "computer", "database", "system"}
        self.assertTrue(expected_vocab.issubset(vocab))

    def test_total_counts(self) -> None:
        self.assertEqual(self.index.total_documents, 4)
        self.assertEqual(self.index.total_terms, 5)


if __name__ == "__main__":
    unittest.main()
