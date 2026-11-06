"""
Document Loader Module
Responsibility: Load plain-text documents from disk into memory.
This module does NOT perform tokenization or normalization.
"""

from pathlib import Path
from typing import Dict, Union
import logging

logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Component responsible solely for discovering and reading text documents
    from a specified directory.
    """

    def __init__(self, directory: Union[str, Path]) -> None:
        """
        Initialize DocumentLoader with a target directory path.

        :param directory: Path to directory containing document files.
        """
        self.directory = Path(directory)

    def load_documents(self) -> Dict[str, str]:
        """
        Read all '.txt' files from the configured directory.

        Returns:
            Dict[str, str]: Mapping of document IDs (filenames) to raw text content.
            Returns an empty dictionary if the directory does not exist or contains no text files.
        """
        documents: Dict[str, str] = {}

        if not self.directory.exists():
            logger.warning("Directory does not exist: %s", self.directory)
            return documents

        if not self.directory.is_dir():
            logger.warning("Specified path is not a directory: %s", self.directory)
            return documents

        # Find all .txt files, sorted by name for deterministic ordering
        txt_files = sorted(self.directory.glob("*.txt"))

        for file_path in txt_files:
            try:
                # Read document using UTF-8 encoding; ignore/replace non-decodable bytes if any
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()

                # Use file name as stable document identifier
                doc_id = file_path.name
                documents[doc_id] = content

            except Exception as e:
                logger.error("Failed to read file %s: %s", file_path, e)

        return documents
