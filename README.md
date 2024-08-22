# BIN Lookup Indexer

## Overview

This project is designed to parse BIN (Bank Identification Number) range files, generate an AVL range tree index from
the parsed data, and store the indexed data in a Redis database for fast lookup operations. The project is highly
configurable and can be extended to support multiple BIN file formats and storage backends.

## Features

* BIN File Parsing: Supports parsing BIN files from some of the main providers in Spain.
* Indexing: Generates an AVL range tree index for efficient range queries.
* Storage: Stores indexed BIN data in Redis/DragonflyDB for fast retrieval.
* Flexible Configuration: Easily configurable via environment variables and configuration files.
* Logging: Integrated logging with loguru for detailed monitoring and troubleshooting.

## Setup

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/bin-lookup-indexer.git
    cd bin-lookup-indexer
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

This will install all required dependencies as specified in the `pyproject.toml` file.

## Configuration

1. Set up environment variables:

    * Create a `.env` file in the project root directory, and define the necessary environment variables:

        ```bash
        REDIS_HOST=localhost
        REDIS_PORT=6379
        REDIS_DB=0
        REDIS_PASSWORD=yourpassword
        ```

2. Update the configuration:

    * The Config class in app/setup/config.py reads from environment variables. Ensure all necessary variables are
      defined in
      your environment or .env file.

## Usage

### Generate Index and Store in Redis

To generate an index from a BIN file and store it in Redis, follow these steps:

1. Prepare the BIN file:

    * Ensure you have a BIN file in the Redsys format (or another supported format in the future).

2. Run the indexer:

    ```bash
    poetry run index_cli -f format_version -p /path/to/your/binfile.ext -s redis -i /path/to/your/indexfile.index
    ```

    * Replace `/path/to/your/binfile.ext` with the actual path to your BIN file.
    * Replace `format` by one that is supported in `/parsers/parser_factory.py` and a valid version, which can be found
      in `/parsers/versions/`
    * Replace `/path/to/your/indexfile.index` by the path where you want to place the index file. The recommendation is
      to use the provider as name and index as extension (`mastercard.index`).
    * The script will parse the BIN file, generate an AVL range tree, and store the indexed data in Redis.

## Logging

Logging is handled by loguru and is configured to output logs to `sys.stdout` for cloud deployment compliance. You can
customize logging behavior by modifying the loguru configuration in `main.py`.

## Extending the Project

### Adding Support for New BIN File Formats

1. Create a new parser:

    * Implement a new parser class by extending `BaseParser` in the `bin_lookup_indexer/parsers/` directory.

2. Update the ParserFactory:

    * Modify `parser_factory.py` to include the new parser for your format.

3. (Optional) If it's possible to have different versions of that format, because may be multiple sources with distinct
   amounts of detail or because you may need to support older versions when the format evolves, you can include them in
   the `bin_lookup_indexer/parsers/versions/ package.`

4. Test the new parser backend:

   * Write unit tests in the tests/ directory to ensure your storage backend works correctly.

### Adding Support for New Storage Backends

I want to remind you of the importance of top-tier performance in retrieving key values. Otherwise, the system may have
a significant impact. In that case, with a degraded performance, you may need to add a cache, where you link the bin to
the data. However, this will have implications for scalable/reliable deployments where you have several balanced
deployments every time you update the index. During a time window, you will have different versions of the data, and
managing the cache is something you have to address.

1. Create a new storage class:

   * Implement a new storage class by extending StorageBase in the app/storage/ directory.

2. Update the StorageFactory:

   * Modify `storage_factory.py` to include the new storage backend.

3. Test the new storage backend:

   * Write unit tests in the tests/ directory to ensure your storage backend works correctly.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
