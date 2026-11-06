"""
Inverted Index Module
Responsibility: Build and manage the inverted index mapping terms to document postings.
Uses Tokenizer and Normalizer modules without duplicating preprocessing logic.
"""

from collections import defaultdict
from typing import Dict, List, Optional, Set

from src.normalizer import Normalizer
from src.tokenizer import Tokenizer


class InvertedIndex:
    """
    Inverted Index data structure for Information Retrieval.
    Maps distinct vocabulary terms to the set of document IDs in which they occur.
    """

    def __init__(
        self,
        tokenizer: Optional[Tokenizer] = None,
        normalizer: Optional[Normalizer] = None,
    ) -> None:
        """
        Initialize the InvertedIndex with a tokenizer and normalizer.

        :param tokenizer: Tokenizer instance (defaults to Tokenizer()).
        :param normalizer: Normalizer instance (defaults to Normalizer()).
        """
        self.tokenizer = tokenizer if tokenizer is not None else Tokenizer()
        self.normalizer = normalizer if normalizer is not None else Normalizer()

        # Core index structure: term -> set of document_ids
        self._index: Dict[str, Set[str]] = defaultdict(set)

        # Store document count and document IDs for reference
        self._document_ids: Set[str] = set()

    def build(self, documents: Dict[str, str]) -> None:
        """
        Construct the inverted index from a dictionary of documents.

        Pipeline:
        Raw Document Text -> Tokenizer -> Normalizer -> Postings List

        :param documents: Mapping of {doc_id: raw_text}
        """
        self._index.clear()
        self._document_ids.clear()

        for doc_id, text in documents.items():
            self._document_ids.add(doc_id)

            # 1. Tokenize document text
            raw_tokens: List[str] = self.tokenizer.tokenize(text)

            # 2. Normalize tokens (case-folding, stripping residual punctuation)
            normalized_tokens: List[str] = self.normalizer.normalize_tokens(raw_tokens)

            # 3. Add to inverted index postings
            for term in normalized_tokens:
                self._index[term].add(doc_id)

    def search_term(self, term: str) -> Set[str]:
        """
        Search for a single term in the index.
        Normalizes the search term before looking up.

        :param term: Single search word.
        :return: Set of document IDs containing the term, or empty set if not found.
        """
        if not term:
            return set()

        normalized_term = self.normalizer.normalize_token(term)
        if not normalized_term:
            return set()

        # Return a copy of the posting set to prevent external mutation
        return set(self._index.get(normalized_term, set()))

    def get_vocabulary(self) -> Set[str]:
        """
        Retrieve all distinct terms indexed in the vocabulary.

        :return: Set of vocabulary terms.
        """
        return set(self._index.keys())

    def get_index(self) -> Dict[str, Set[str]]:
        """
        Retrieve the full inverted index dictionary.

        :return: Dictionary mapping terms to sets of document IDs.
        """
        return dict(self._index)

    def get_document_ids(self) -> Set[str]:
        """
        Retrieve all indexed document IDs.

        :return: Set of all document IDs.
        """
        return set(self._document_ids)

    @property
    def total_terms(self) -> int:
        """Return total unique vocabulary terms."""
        return len(self._index)

    @property
    def total_documents(self) -> int:
        """Return total indexed documents."""
        return len(self._document_ids)
