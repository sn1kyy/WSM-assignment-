"""
Wildcard Processor Module
Responsibility: Handle wildcard pattern queries (prefix, suffix, infix)
by matching patterns against the vocabulary of the Inverted Index.

Information Retrieval Architecture:
Instead of scanning every document (which would be O(N * length)),
the wildcard processor matches patterns against the indexed vocabulary (O(V)),
and retrieves pre-computed document postings directly from the inverted index (O(1)).
"""

import re
from typing import List, Optional, Set

from src.inverted_index import InvertedIndex
from src.normalizer import Normalizer


class WildcardProcessor:
    """
    Component responsible for evaluating wildcard search queries (e.g. app*, *tion, *app*).
    
    Design Note:
    Matches against the unique vocabulary of the Inverted Index and merges postings.
    This design is modular: a Permuterm Index or k-gram index could be plugged in
    to replace or optimize `match_terms()` without changing the rest of the application.
    """

    def __init__(
        self,
        inverted_index: InvertedIndex,
        normalizer: Optional[Normalizer] = None,
    ) -> None:
        """
        Initialize WildcardProcessor.

        :param inverted_index: Pre-built InvertedIndex containing vocabulary and postings.
        :param normalizer: Normalizer for consistent pattern casing.
        """
        self.inverted_index = inverted_index
        self.normalizer = normalizer if normalizer is not None else (
            inverted_index.normalizer if hasattr(inverted_index, "normalizer") else Normalizer()
        )

    @staticmethod
    def is_wildcard_query(query: str) -> bool:
        """
        Check if a given query contains wildcard characters.

        :param query: Query string to inspect.
        :return: True if '*' is in query, False otherwise.
        """
        return "*" in query

    def pattern_to_regex(self, pattern: str) -> re.Pattern:
        """
        Convert a user wildcard pattern (e.g., 'app*', '*tion', '*app*')
        into a safe, compiled Python regular expression.

        Standard characters are properly escaped to prevent arbitrary regex injection,
        while '*' is translated to '.*'.

        :param pattern: Raw wildcard pattern string.
        :return: Compiled re.Pattern object.
        """
        cleaned_pattern = pattern.strip().lower()

        # Split on '*' wildcard characters
        parts = cleaned_pattern.split("*")

        # Safely escape each non-wildcard part
        escaped_parts = [re.escape(part) for part in parts]

        # Join parts with '.*' (representing 0 or more characters) anchored to start and end
        regex_string = f"^{'.*'.join(escaped_parts)}$"

        return re.compile(regex_string)

    def match_terms(self, pattern: str) -> List[str]:
        """
        Find all terms in the inverted index vocabulary that match the wildcard pattern.

        :param pattern: Wildcard pattern (e.g., 'app*', '*tion', '*app*').
        :return: Sorted list of matching vocabulary terms.
        """
        if not pattern or not pattern.strip():
            return []

        compiled_regex = self.pattern_to_regex(pattern)
        vocabulary = self.inverted_index.get_vocabulary()

        # Match against vocabulary terms
        matching_terms = [
            term for term in vocabulary if compiled_regex.match(term)
        ]

        # Return sorted for deterministic display
        return sorted(matching_terms)

    def search(self, pattern: str) -> Set[str]:
        """
        Execute a wildcard search against the index.

        Steps:
        1. Determine vocabulary terms matching the wildcard pattern.
        2. Retrieve document postings for each matching term from inverted index.
        3. Merge the resulting document sets (Union).

        :param pattern: Wildcard pattern string.
        :return: Union set of matching document IDs.
        """
        matched_terms = self.match_terms(pattern)

        if not matched_terms:
            return set()

        result_docs: Set[str] = set()
        for term in matched_terms:
            doc_ids = self.inverted_index.search_term(term)
            result_docs.update(doc_ids)

        return result_docs
