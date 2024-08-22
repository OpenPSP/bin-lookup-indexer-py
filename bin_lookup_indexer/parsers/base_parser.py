from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any


class BaseParser(ABC):
    """
    Abstract base class for BIN file parsers.

    All specific parsers (e.g., RedsysParser, VisaParser) should inherit from this class
    and implement the parse_line method for line-by-line processing.
    """

    @abstractmethod
    def parse(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """
        Parse the BIN file line by line and yield each parsed record.

        Args:
            file_path (str): The path to the BIN file, which can be a local path or an S3 URL.

        Yields:
            dict: A dictionary with keys 'StartRange' and 'EndRange' for each BIN range.
        """
        pass
