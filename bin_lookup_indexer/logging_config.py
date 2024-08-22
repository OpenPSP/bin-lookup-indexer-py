from loguru import logger
import sys
import json
import orjson
import datetime


# Define a custom serializer for JSON
def json_serializer(message):
    return json.dumps(message, default=str)


# Custom serializer using orjson (better performance)
def orjson_serializer(message):
    return orjson.dumps(message, default=str).decode("utf-8")


def serialize(record):
    subset = {
        "timestamp": record["time"].timestamp(),
        "message": record["message"],
        "level": record["level"].name,
    }
    return orjson.dumps(subset, default=str).decode("utf-8")


def patching(record):
    record["extra"]["serialized"] = serialize(record)


# Configure loguru to use JSON serialization
logger.remove()  # Remove the default logger to avoid duplicate logs
# logger.add(sys.stdout, serialize=True, format=orjson_serializer, level="INFO")

logger.add(
    sys.stdout,
    format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}",
    serialize=True,
)

# logger = logger.patch(patching)
# logger.add(sys.stdout, format="{extra[serialized]}", level="INFO")
# logger.add(sys.stderr, format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message} | {extra}", serialize=True, level="ERROR")
