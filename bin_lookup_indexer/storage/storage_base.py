from abc import ABC, abstractmethod
from typing import Dict, Any


class StorageBase(ABC):
    """
    Abstract base class for all storage strategies.

    All specific storage strategies (e.g., RedisStorage, DynamoDBStorage) should inherit from this class
    and implement the required methods.
    """

    @abstractmethod
    def store_parsed_data(self, key: str, parsed_data: Dict[str, Any]):
        """
        Store a single parsed record in the storage backend.

        Args:
            key (str): The unique identifier for the record (e.g., KSUID).
            parsed_data (Dict[str, str]): A dictionary representing the columns and their values.
        """
        pass
