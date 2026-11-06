"""
Unit Tests for QueryProcessor Module.
Tests single-term queries, AND logic (intersection), OR logic (union), and edge cases.
"""

import unittest
from src.inverted_index import InvertedIndex
from src.query_processor import QueryProcessor


class TestQueryProcessor(unittest.TestCase):
    """Test suite for QueryProcessor."""

    def setUp(self) -> None:
        self.index = InvertedIndex()
        self.sample_docs = {
            "doc1": "apple banana fruit",
            "doc2": "apple computer technology",
            "doc3": "banana database system",
            "doc4": "machine learning intelligence computer",
        }
        self.index.build(self.sample_docs)
        self.processor = QueryProcessor(self.index)

    def test_single_term_search(self) -> None:
        self.assertEqual(self.processor.process_query("apple"), {"doc1", "doc2"})
        self.assertEqual(self.processor.process_query("database"), {"doc3"})
        self.assertEqual(self.processor.process_query("computer"), {"doc2", "doc4"})

    def test_single_term_with_casing(self) -> None:
        self.assertEqual(self.processor.process_query("APPLE"), {"doc1", "doc2"})
        self.assertEqual(self.processor.process_query("CoMpUtEr"), {"doc2", "doc4"})

    def test_and_query(self) -> None:
        # Both apple AND banana only in doc1
        self.assertEqual(self.processor.process_query("apple AND banana"), {"doc1"})
        # Case insensitive operator
        self.assertEqual(self.processor.process_query("apple and banana"), {"doc1"})
        # apple AND computer only in doc2
        self.assertEqual(self.processor.process_query("apple AND computer"), {"doc2"})

    def test_multi_term_and_query(self) -> None:
        # 3-term AND
        self.assertEqual(
            self.processor.process_query("machine AND learning AND computer"),
            {"doc4"},
        )

    def test_implicit_and_query(self) -> None:
        # Space-separated terms without operator treated as AND
        self.assertEqual(self.processor.process_query("apple banana"), {"doc1"})

    def test_or_query(self) -> None:
        # apple in {doc1, doc2}, database in {doc3}
        self.assertEqual(
            self.processor.process_query("apple OR database"),
            {"doc1", "doc2", "doc3"},
        )
        # Case insensitive OR
        self.assertEqual(
            self.processor.process_query("apple or database"),
            {"doc1", "doc2", "doc3"},
        )

    def test_empty_query(self) -> None:
        self.assertEqual(self.processor.process_query(""), set())
        self.assertEqual(self.processor.process_query("   "), set())
        self.assertEqual(self.processor.process_query(None), set())

    def test_unknown_term(self) -> None:
        # Term not in index yields empty set
        self.assertEqual(self.processor.process_query("astronaut"), set())
        # AND with an unknown term yields empty set
        self.assertEqual(self.processor.process_query("apple AND astronaut"), set())
        # OR with an unknown term yields docs for the known term
        self.assertEqual(self.processor.process_query("apple OR astronaut"), {"doc1", "doc2"})

    def test_malformed_query_handling(self) -> None:
        # Dangling AND or OR operator
        self.assertEqual(self.processor.process_query("apple AND"), {"doc1", "doc2"})
        self.assertEqual(self.processor.process_query("OR apple"), {"doc1", "doc2"})


if __name__ == "__main__":
    unittest.main()
