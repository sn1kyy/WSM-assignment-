"""
Query Processor Module
Responsibility: Parse and evaluate user search queries (single-term, AND, OR).
Executes set-based operations (intersection and union) against the Inverted Index.
"""

import re
from typing import List, Optional, Set

from src.inverted_index import InvertedIndex
from src.normalizer import Normalizer


class QueryProcessor:
    """
    Component responsible for processing search queries against the Inverted Index.
    Supports single-term lookups and boolean AND / OR queries with set operations.
    """

    def __init__(
        self,
        inverted_index: InvertedIndex,
        normalizer: Optional[Normalizer] = None,
    ) -> None:
        """
        Initialize QueryProcessor.

        :param inverted_index: The pre-built InvertedIndex instance.
        :param normalizer: Normalizer instance (defaults to index's normalizer or new Normalizer).
        """
        self.inverted_index = inverted_index
        self.normalizer = normalizer if normalizer is not None else (
            inverted_index.normalizer if hasattr(inverted_index, "normalizer") else Normalizer()
        )

    def process_query(self, query: str) -> Set[str]:
        """
        Process a user query string and return the set of matching document IDs.

        Supports:
        - Single term queries: "apple"
        - Boolean AND queries: "apple AND banana", "machine and learning"
        - Boolean OR queries: "apple OR banana", "database or network"
        - Multiple space-separated terms: treated as implicit AND queries

        Set operations:
        - AND -> Set intersection
        - OR  -> Set union

        :param query: Raw search query string from user.
        :return: Set of matching document IDs.
        """
        if not query or not str(query).strip():
            return set()

        raw_query = str(query).strip()

        # Clean dangling boolean operators at start or end (e.g. "apple AND", "OR apple")
        raw_query = re.sub(r"^\s*\b(AND|OR)\b\s*", "", raw_query, flags=re.IGNORECASE).strip()
        raw_query = re.sub(r"\s*\b(AND|OR)\b\s*$", "", raw_query, flags=re.IGNORECASE).strip()

        if not raw_query:
            return set()

        # Check for explicit OR operations first (lowest boolean precedence)
        # Regex splits on standalone "OR" / "or" with word boundaries
        or_clauses = re.split(r"\s+\bOR\b\s+", raw_query, flags=re.IGNORECASE)

        if len(or_clauses) > 1:
            return self._evaluate_or_clauses(or_clauses)

        # Check for explicit AND operations
        and_clauses = re.split(r"\s+\bAND\b\s+", raw_query, flags=re.IGNORECASE)

        if len(and_clauses) > 1:
            return self._evaluate_and_clauses(and_clauses)

        # Multi-term query without explicit operator: default to AND logic
        terms = raw_query.split()
        if len(terms) > 1:
            return self._evaluate_and_clauses(terms)

        # Single term query
        return self._evaluate_single_term(raw_query)

    def _evaluate_single_term(self, term: str) -> Set[str]:
        """
        Evaluate a single search term against the inverted index.

        :param term: Single word term.
        :return: Set of matching document IDs.
        """
        clean_term = self.normalizer.normalize_token(term)
        if not clean_term:
            return set()
        return self.inverted_index.search_term(clean_term)

    def _evaluate_and_clauses(self, clauses: List[str]) -> Set[str]:
        """
        Evaluate AND clauses using set intersection.

        :param clauses: List of terms/clauses that must ALL match.
        :return: Intersection of matching document sets.
        """
        result_set: Optional[Set[str]] = None

        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue

            # In case an inner clause has spaces (e.g. subterms), evaluate each
            subterms = clause.split()
            for st in subterms:
                term_docs = self._evaluate_single_term(st)

                if result_set is None:
                    result_set = set(term_docs)
                else:
                    result_set.intersection_update(term_docs)

                # Short-circuit: if intersection becomes empty, result is empty
                if not result_set:
                    return set()

        return result_set if result_set is not None else set()

    def _evaluate_or_clauses(self, clauses: List[str]) -> Set[str]:
        """
        Evaluate OR clauses using set union.

        :param clauses: List of terms/clauses where AT LEAST ONE must match.
        :return: Union of matching document sets.
        """
        result_set: Set[str] = set()

        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue

            # If an OR operand contains AND, evaluate it as AND first
            if re.search(r"\bAND\b", clause, flags=re.IGNORECASE):
                and_parts = re.split(r"\s+\bAND\b\s+", clause, flags=re.IGNORECASE)
                clause_docs = self._evaluate_and_clauses(and_parts)
            else:
                # Sub-terms in an OR branch without AND are evaluated
                subterms = clause.split()
                if len(subterms) > 1:
                    clause_docs = self._evaluate_and_clauses(subterms)
                else:
                    clause_docs = self._evaluate_single_term(clause)

            result_set.update(clause_docs)

        return result_set
