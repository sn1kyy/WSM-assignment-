"""
Unit Tests for WildcardProcessor Module.
Tests prefix, suffix, infix wildcard patterns, regex escaping, and doc retrieval.
"""

import unittest
from src.inverted_index import InvertedIndex
from src.wildcard_processor import WildcardProcessor


class TestWildcardProcessor(unittest.TestCase):
    """Test suite for WildcardProcessor."""

    def setUp(self) -> None:
        self.index = InvertedIndex()
        self.sample_docs = {
            "doc1": "apple application applied fruit",
            "doc2": "information retrieval education classification",
            "doc3": "computer computation networks system",
            "doc4": "c++ programming language code",
        }
        self.index.build(self.sample_docs)
        self.wildcard_proc = WildcardProcessor(self.index)

    def test_prefix_wildcard_terms(self) -> None:
        # app* should match apple, application, applied
        matched = self.wildcard_proc.match_terms("app*")
        self.assertEqual(matched, ["apple", "application", "applied"])

    def test_prefix_wildcard_search(self) -> None:
        # doc1 has apple, application, applied
        results = self.wildcard_proc.search("app*")
        self.assertEqual(results, {"doc1"})

    def test_suffix_wildcard_terms(self) -> None:
        # *tion should match application, classification, computation, education, information
        matched = self.wildcard_proc.match_terms("*tion")
        self.assertIn("application", matched)
        self.assertIn("classification", matched)
        self.assertIn("computation", matched)
        self.assertIn("education", matched)
        self.assertIn("information", matched)

    def test_suffix_wildcard_search(self) -> None:
        results = self.wildcard_proc.search("*tion")
        # doc1 has application; doc2 has information, education, classification; doc3 has computation
        self.assertEqual(results, {"doc1", "doc2", "doc3"})

    def test_infix_wildcard_terms(self) -> None:
        # *app* should match apple, application, applied
        matched = self.wildcard_proc.match_terms("*app*")
        self.assertEqual(matched, ["apple", "application", "applied"])

    def test_internal_wildcard_terms(self) -> None:
        # comp*ter should match computer
        matched = self.wildcard_proc.match_terms("comp*ter")
        self.assertEqual(matched, ["computer"])
        self.assertEqual(self.wildcard_proc.search("comp*ter"), {"doc3"})

    def test_no_match_pattern(self) -> None:
        self.assertEqual(self.wildcard_proc.match_terms("xyz*"), [])
        self.assertEqual(self.wildcard_proc.search("xyz*"), set())

    def test_empty_pattern(self) -> None:
        self.assertEqual(self.wildcard_proc.match_terms(""), [])
        self.assertEqual(self.wildcard_proc.search(""), set())

    def test_case_insensitive_wildcard(self) -> None:
        # APP* should match apple, application, applied
        matched = self.wildcard_proc.match_terms("APP*")
        self.assertEqual(matched, ["apple", "application", "applied"])

    def test_escaped_regex_characters(self) -> None:
        # Ensure characters like '+' or '.' do not cause regex errors or arbitrary regex matching
        matched = self.wildcard_proc.match_terms("c++*")
        # In our vocabulary, "c" was tokenized from "c++" by \b\w+\b
        # The key assertion is that compiling and searching does not raise re.error
        self.assertIsInstance(matched, list)

    def test_is_wildcard_query_helper(self) -> None:
        self.assertTrue(WildcardProcessor.is_wildcard_query("app*"))
        self.assertTrue(WildcardProcessor.is_wildcard_query("*tion"))
        self.assertFalse(WildcardProcessor.is_wildcard_query("apple"))


if __name__ == "__main__":
    unittest.main()
