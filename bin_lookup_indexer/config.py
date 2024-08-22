import os


class Config:
    def __init__(self):
        # Redis configuration
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = os.getenv("REDIS_PORT", 6379)
        self.redis_db = os.getenv("REDIS_DB", 0)
        self.redis_password = os.getenv("REDIS_PASSWORD", None)

        # DynamoDB configuration
        self.dynamodb_region = os.getenv("DYNAMODB_REGION", "us-west-2")
        self.dynamodb_table_name = os.getenv("DYNAMODB_TABLE_NAME", "BinRanges")
        self.dynamodb_access_key = os.getenv("DYNAMODB_ACCESS_KEY", "")
        self.dynamodb_secret_key = os.getenv("DYNAMODB_SECRET_KEY", "")

        # Other configurations can go here as needed

    def get_redis_config(self):
        return {
            "host": self.redis_host,
            "port": self.redis_port,
            "db": self.redis_db,
            "password": self.redis_password,
        }

    def get_dynamodb_config(self):
        return {
            "region": self.dynamodb_region,
            "table_name": self.dynamodb_table_name,
            "access_key": self.dynamodb_access_key,
            "secret_key": self.dynamodb_secret_key,
        }
