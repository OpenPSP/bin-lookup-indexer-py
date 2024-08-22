from typing import Iterator, Dict, Any

import orjson
import pycountry

from bin_lookup_indexer.logging_config import logger
from bin_lookup_indexer.parsers.base_parser import BaseParser
from bin_lookup_indexer.parsers.versions import redsys_v3_8


class RedsysParser(BaseParser):
    def __init__(self, version="3.8"):
        # Load the specific version's configuration
        if version == "3.8":
            self.colspecs = redsys_v3_8.colspecs
            self.translation_rules = redsys_v3_8.translation_rules
            self.excluded_fields = redsys_v3_8.excluded_fields
            self.index_name = "redsys.index"
        else:
            raise ValueError(f"Unsupported version: {version}")

    def parse_fixed_width_line(self, line: str) -> dict:
        """
        Parse a fixed-width formatted line according to the colspecs.

        Args:
            line (str): The line of text to parse.

        Returns:
            dict: A dictionary containing the parsed data.
        """
        parsed_data = {}

        # Apply the column specifications to extract data
        for start, end, column_name in self.colspecs:
            parsed_data[column_name] = line[start:end].strip()

        # Apply the translation rules in the specified order
        translated_data = self.apply_translation(parsed_data)

        # Filter out the excluded fields
        filtered_data = {
            k: v for k, v in translated_data.items() if k not in self.excluded_fields
        }

        # Group Issuer-related fields into a single dictionary
        issuer_grouped_data = self.group_issuer_fields(filtered_data)

        # Expand currency and country information
        expanded_data = self.expand_currency_and_country(issuer_grouped_data)

        return expanded_data

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

    def group_issuer_fields(self, data: dict) -> dict:
        """
        Group IssuerType, IssuerCode, and IssuerName into a single Issuer dictionary.
        Remove the individual IssuerType, IssuerCode, and IssuerName fields from the data.
        """
        issuer_type = data.pop("IssuerType", "")
        issuer_code = data.pop("IssuerCode", "")
        issuer_name = data.pop("IssuerName", "")

        if issuer_type or issuer_code or issuer_name:
            data["Issuer"] = {
                "Code": issuer_code,
                "Name": issuer_name,
                "Type": issuer_type,
            }

        return data

    def expand_currency_and_country(self, data: dict) -> dict:
        """
        Expand the currency and country fields into detailed information.

        Args:
            data (dict): The dictionary containing the initial parsed and translated data.

        Returns:
            dict: The dictionary with expanded currency and country information.
        """
        # Expand currency information
        currency_code = data.get("Currency")
        if currency_code:
            currency_info = pycountry.currencies.get(numeric=currency_code)
            if currency_info:
                data["Currency"] = {
                    "Code": currency_code,
                    "Alpha3": currency_info.alpha_3,
                    "Name": currency_info.name,
                }

        # Expand country information
        country_code = data.get("Country")
        if country_code:
            country_info = pycountry.countries.get(numeric=country_code)
            if country_info:
                data["Country"] = {
                    "Code": country_code,
                    "Alpha3": country_info.alpha_3,
                    "Name": country_info.name,
                }

        return data

    def parse(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """
        Parse a fixed-width formatted Redsys BIN file line by line.
        This parser is for version 3.8

        Args:
            file_path (str): The path to the BIN file, which can be a local path or an S3 URL.

        Yields:
            dict: A dictionary with keys 'StartRange' and 'EndRange' for each BIN range.
        """

        with open(file_path, "r", encoding="cp1252") as file:
            records = 0
            atm_only_records = 0
            for line in file:

                if line[0:2] == "10":  # Structure code 10 means it's a BIN record
                    records += 1

                    parsed_data = self.parse_fixed_width_line(line)

                    # For our purposes, we can remove the ATM only to avoid conflicts and reduce the file
                    # size improving performance in queries
                    if parsed_data["Usage"] == "ATM":
                        atm_only_records += 1
                        continue
                    else:
                        del parsed_data["Usage"]

                    yield parsed_data
                elif (
                    line[0:2] == "90"
                ):  # Structure code 90 means it's a totalization record
                    lines_to_process = int(line[28:38]) - 2
                    if lines_to_process == records:
                        logger.info(
                            "All records have been processed successfully",
                            processed=records,
                            atm_only=atm_only_records,
                            stored=records - atm_only_records,
                        )
                    else:
                        logger.error(
                            "Some records could not be processed",
                            records=lines_to_process,
                            processed=records,
                        )
