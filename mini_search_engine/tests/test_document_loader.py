"""
Unit Tests for DocumentLoader Module.
Tests loading .txt files, missing directory handling, empty file handling.
"""

import tempfile
import unittest
from pathlib import Path
from src.document_loader import DocumentLoader


class TestDocumentLoader(unittest.TestCase):
    """Test suite for DocumentLoader."""

    def test_load_documents_from_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "doc1.txt").write_text("Hello world", encoding="utf-8")
            (tmppath / "doc2.txt").write_text("Information retrieval", encoding="utf-8")
            (tmppath / "ignore.csv").write_text("a,b,c", encoding="utf-8")

            loader = DocumentLoader(tmppath)
            docs = loader.load_documents()

            self.assertEqual(len(docs), 2)
            self.assertIn("doc1.txt", docs)
            self.assertIn("doc2.txt", docs)
            self.assertEqual(docs["doc1.txt"], "Hello world")
            self.assertEqual(docs["doc2.txt"], "Information retrieval")
            self.assertNotIn("ignore.csv", docs)

    def test_missing_directory_handled_gracefully(self) -> None:
        loader = DocumentLoader(Path("non_existent_directory_xyz_12345"))
        docs = loader.load_documents()
        self.assertEqual(docs, {})

    def test_empty_document_handled(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "empty.txt").write_text("", encoding="utf-8")

            loader = DocumentLoader(tmppath)
            docs = loader.load_documents()

            self.assertIn("empty.txt", docs)
            self.assertEqual(docs["empty.txt"], "")


if __name__ == "__main__":
    unittest.main()
