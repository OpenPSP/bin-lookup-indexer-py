import argparse
import os
from typing import Dict, Any

import orjson
from avl_range_tree.avl_tree import RangeTree
from ksuid import Ksuid

from bin_lookup_indexer.config import Config
from bin_lookup_indexer.parsers.parser_factory import ParserFactory
from bin_lookup_indexer.storage.storage_factory import StorageFactory


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process BIN Account Range Tables.")

    parser.add_argument(
        "-f",
        "--format",
        type=str,
        required=True,
        choices=["redsys_3.8", "mastercard_simplified"],
        help="The format of the BIN file (e.g., 'redsys_version', 'mastercard_version' , 'visa_version').",
    )

    parser.add_argument(
        "-p",
        "--file-path",
        type=str,
        required=True,
        help="The file path to the BIN file, either local or an S3 URL.",
    )

    parser.add_argument(
        "-s",
        "--storage",
        type=str,
        choices=["redis"],
        default="redis",
        help="The storage type to use (e.g., 'Redis', 'DynamoDB').",
    )

    parser.add_argument(
        "-i",
        "--index",
        type=str,
        required=True,
        help="The output file path to the index tree, either local or an S3 URL.",
    )

    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load configuration
    config = Config()

    # Create the appropriate parser
    parser = ParserFactory.create_parser(args.format)
    # Create the appropriate storage strategy
    storage = StorageFactory.create_storage(args.storage, config)

    # Create index
    index = RangeTree()

    # Process the BIN file line by line
    for record in parser.parse(args.file_path):
        key = str(Ksuid())  # Generate a unique KSUID for the storage key

        # Build the index tree
        index.insert(record["LowAccountRange"], record["HighAccountRange"], key)

        # store the data
        storage.store_parsed_data(key, record)

    # store index
    def json_serializer(data: Dict[str, Any]) -> str:
        return orjson.dumps(data).decode("utf-8")

    json_index = index.serialize(json_serializer)

    # Determine the correct index file path
    index_file_path = args.index
    if os.path.isdir(index_file_path):
        index_file_path = os.path.join(index_file_path, parser.index_name)

    with open(index_file_path, "w") as file:
        file.write(json_index)


if __name__ == "__main__":
    main()
