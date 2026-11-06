"""
Text Normalizer Module
Responsibility: Standardize tokens (case folding, trimming punctuation/accents).
Does NOT perform tokenization.
"""

import string
from typing import List


class Normalizer:
    """
    Component responsible for converting tokens into a canonical standard representation.
    Ensures search terms match regardless of casing or surrounding punctuation.
    """

    def __init__(self) -> None:
        # Punctuation characters to strip from individual tokens if needed
        self._punctuation_to_strip = string.punctuation

    def normalize_token(self, token: str) -> str:
        """
        Normalize a single token:
        1. Strip surrounding whitespace and residual punctuation characters.
        2. Perform case folding (lowercase conversion).

        :param token: The raw token string.
        :return: Normalized, lowercased token string.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.normalize_token("Apple")
            'apple'
            >>> normalizer.normalize_token("APPLE")
            'apple'
            >>> normalizer.normalize_token("ApPlE")
            'apple'
        """
        if not token:
            return ""

        # Strip surrounding punctuation and whitespace, then lowercase
        cleaned = token.strip(self._punctuation_to_strip + " \t\r\n")
        return cleaned.lower()

    def normalize_tokens(self, tokens: List[str]) -> List[str]:
        """
        Normalize a list of tokens, filtering out any that become empty.

        :param tokens: List of raw token strings.
        :return: List of normalized, lowercase token strings.
        """
        normalized_list: List[str] = []
        for tok in tokens:
            norm = self.normalize_token(tok)
            if norm:
                normalized_list.append(norm)
        return normalized_list
