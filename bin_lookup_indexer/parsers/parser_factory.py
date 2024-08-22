from bin_lookup_indexer.parsers.mastercard_parser import MastercardParser
from bin_lookup_indexer.parsers.redsys_parser import RedsysParser


class ParserFactory:
    @staticmethod
    def create_parser(format: str):
        """
        Factory method to create a parser instance based on the given format.

        Args:
            format (str): The format of the BIN file (e.g., 'Redsys', 'VISA').

        Returns:
            Parser: An instance of a parser corresponding to the format.

        Raises:
            ValueError: If the format is not supported or improperly formatted.
        """
        try:
            # Split the format into provider and version parts
            provider, version = format.lower().split("_", 1)
        except ValueError:
            raise ValueError(
                f"Format '{format}' is invalid. It should be in the form 'Provider_Version'."
            )

        if provider == "redsys":
            return RedsysParser(version)
        elif provider == "mastercard":
            return MastercardParser(version)
        elif provider == "visa":
            raise ValueError(f"Unsupported format: {provider}")
        else:
            raise ValueError(f"Unsupported format: {format}")
