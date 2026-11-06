"""
Tokenizer Module
Responsibility: Break raw text strings into discrete tokens (words).
Does NOT perform case folding or normalization.
"""

import re
from typing import List


class Tokenizer:
    """
    Component responsible solely for lexical analysis (tokenization):
    splitting text into tokens by separating words and discarding punctuation/whitespace.
    """

    def __init__(self) -> None:
        # Regex pattern matching alphanumeric word sequences
        # This strips out punctuation and whitespace naturally.
        self._pattern = re.compile(r"\b\w+\b")

    def tokenize(self, text: str) -> List[str]:
        """
        Convert an input text string into a list of word tokens.

        Preserves original casing (casing is handled later by Normalizer).
        Filters out empty tokens, punctuation, and extraneous whitespace.

        :param text: Raw input string.
        :return: List of extracted token strings.

        Example:
            >>> tokenizer = Tokenizer()
            >>> tokenizer.tokenize("Apple is a very useful fruit.")
            ['Apple', 'is', 'a', 'very', 'useful', 'fruit']
        """
        if not text:
            return []

        # Find all word matches based on word boundaries
        tokens = self._pattern.findall(text)

        # Ensure no empty or whitespace-only tokens exist
        return [tok for tok in tokens if tok.strip()]
