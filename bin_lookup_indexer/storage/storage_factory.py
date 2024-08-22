from bin_lookup_indexer.storage.redis_storage import RedisStorage

# from bin_lookup_indexer.storage.dynamodb_storage import DynamoDBStorage
from bin_lookup_indexer.config import Config


class StorageFactory:
    @staticmethod
    def create_storage(storage_type: str, config: Config):
        """
        Factory method to create a storage instance based on the given storage type.

        Args:
            storage_type (str): The type of storage to use (e.g., 'Redis', 'DynamoDB').
            config (Config): The configuration object containing necessary settings for the storage.

        Returns:
            An instance of the selected storage strategy.

        Raises:
            ValueError: If the storage type is not supported.
        """
        storage_type = storage_type.lower()

        if storage_type == "redis":
            redis_config = config.get_redis_config()
            return RedisStorage(
                host=redis_config["host"],
                port=redis_config["port"],
                db=redis_config["db"],
                password=redis_config["password"],
            )
        elif storage_type == "dynamodb":
            # dynamodb_config = config.get_dynamodb_config()
            # return DynamoDBStorage(
            #     region=dynamodb_config["region"],
            #     table_name=dynamodb_config["table_name"],
            #     access_key=dynamodb_config["access_key"],
            #     secret_key=dynamodb_config["secret_key"]
            # )
            raise ValueError(f"Unsupported storage type: {storage_type}")
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")
