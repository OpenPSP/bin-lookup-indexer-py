import orjson
import redis
from typing import Dict, Any
from redis.exceptions import RedisError

from bin_lookup_indexer.storage.storage_base import StorageBase


class RedisStorage(StorageBase):
    def __init__(self, host: str, port: int, db: int = 0, password: str = None):
        """
        Initialize the Redis storage connection.

        Args:
            host (str): Redis server host.
            port (int): Redis server port.
            db (int): Redis database index.
            password (str, optional): Password for Redis authentication. Defaults to None.
        """
        try:
            self.client = redis.Redis(host=host, port=port, db=db, password=password)
        except RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis: {e}")

    def store_parsed_data(self, key: str, parsed_data: Dict[str, Any]):
        """
        Args:
            key (str): The unique identifier for the record (e.g., KSUID).
            parsed_data (Dict[str, Any]): A dictionary representing the columns and their values.
        """
        try:
            self.client.set(key, orjson.dumps(parsed_data).decode("utf-8"))
        except RedisError as e:
            raise RuntimeError(f"Failed to write data to Redis: {e}")
