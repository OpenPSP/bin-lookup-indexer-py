import csv
from typing import Iterator, Dict, Any

import pycountry

from bin_lookup_indexer.parsers.base_parser import BaseParser
from bin_lookup_indexer.parsers.versions import mastercard_simplified


class MastercardParser(BaseParser):
    """
    A parser for processing Mastercard BIN files in simplified CSV format.

    This class is designed to parse and extract BIN range information
    from Mastercard's CSV-formatted Simplified BIN Account Range Table. The parsed
    data includes the company name, ICA, account ranges, product details, and country information.
    """

    def __init__(self, version="simplified"):
        """
        Initialize the MastercardParser with a specific version's configuration.

        Args:
            version (str): The version of the Mastercard BIN file format. Default is "simplified".
        """
        if version == "simplified":
            # Load the column names and rules specific to the provided version
            self.column_mappings = mastercard_simplified.column_mappings
            self.translation_rules = mastercard_simplified.translation_rules
            self.excluded_fields = mastercard_simplified.excluded_fields
            self.index_name = "mastercard.index"
            self.skip_header = True  # Indicate if we have to skip the header
        else:
            raise ValueError(f"Unsupported version: {version}")

    def parse(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """
        Parse a CSV formatted Mastercard BIN file line by line.

        This method reads the CSV file, applies any necessary translations,
        filters out unwanted fields, and yields the resulting data as dictionaries.

        Args:
            file_path (str): The path to the BIN file.

        Yields:
            dict: A dictionary containing the parsed data for each record.
        """
        # Open the CSV file for reading
        with open(file_path, "r", encoding="utf-8") as file:
            # Create a CSV reader with the specified column names
            reader = csv.DictReader(file, fieldnames=self.column_mappings)

            # Skip the header row
            if self.skip_header:
                next(reader)

            # Iterate over each row in the CSV file
            for parsed_data in reader:

                # Normalize field names
                renamed_data = self.rename_fields(parsed_data)

                # Apply the translation rules in the specified order
                translated_data = self.apply_translation(renamed_data)

                # Filter out the fields that are excluded in this version
                filtered_data = {
                    k: v
                    for k, v in translated_data.items()
                    if k not in self.excluded_fields
                }

                # Expand the country information
                expanded_data = self.expand_country(filtered_data)

                # Yield the fully processed and expanded data
                yield expanded_data

    def rename_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Rename fields in the parsed data according to the column mappings specified
        in the configuration.

        Args:
            data (Dict[str, Any]): The original parsed data with keys corresponding to the original CSV column names.

        Returns:
            Dict[str, Any]: A dictionary with the field names renamed according to the column mappings.
        """
        renamed_data = {}

        # Loop through each key in the original data
        for original_field, value in data.items():
            # Get the new field name from the column mappings, default to original if not found
            new_field = self.column_mappings.get(original_field, original_field)
            renamed_data[new_field] = value

        return renamed_data

    def apply_translation(self, parsed_data: dict) -> dict:
        """
        Apply translations to the parsed data according to the specified rules.

        Args:
            parsed_data (dict): The raw parsed data as a dictionary.

        Returns:
            dict: The translated data.
        """
        translated_data = parsed_data.copy()

        for column_name, translation in self.translation_rules:
            if callable(translation):
                translated_data[column_name] = translation(translated_data)
            else:
                translated_data[column_name] = translation.get(
                    translated_data[column_name], translated_data[column_name]
                )

        return translated_data

    def expand_country(self, data: dict) -> dict:
        """
        Expand the country information to include Code, Alpha3, and Name fields.

        Args:
            data (dict): The dictionary containing the initial parsed and translated data.

        Returns:
            dict: The dictionary with expanded country information.
        """
        country_alpha3 = data.pop("CountryAlpha3", "")
        if country_alpha3:
            country_info = pycountry.countries.get(alpha_3=country_alpha3)
            if country_info:
                data["Country"] = {
                    "Code": country_info.numeric,
                    "Alpha3": country_info.alpha_3,
                    "Name": country_info.name,
                }
            else:
                # If country code is invalid or not found, default to the original Alpha3 code
                data["Country"] = {
                    "Code": "",
                    "Alpha3": country_alpha3,
                    "Name": "Unknown Country",
                }

        return data
