import os
import pytest
from bin_lookup_indexer.config import Config


# Redis Host Tests
def test_redis_host_setenv(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "test_host")
    config = Config()
    assert config.get_redis_config()["host"] == "test_host"


def test_redis_host_default(monkeypatch):
    monkeypatch.delenv("REDIS_HOST", raising=False)
    config = Config()
    assert config.get_redis_config()["host"] == "localhost"


# Redis Port Tests
def test_redis_port_setenv(monkeypatch):
    monkeypatch.setenv("REDIS_PORT", "6380")
    config = Config()
    assert config.get_redis_config()["port"] == "6380"


def test_redis_port_default(monkeypatch):
    monkeypatch.delenv("REDIS_PORT", raising=False)
    config = Config()
    assert config.get_redis_config()["port"] == 6379


# Redis DB Tests
def test_redis_db_setenv(monkeypatch):
    monkeypatch.setenv("REDIS_DB", "2")
    config = Config()
    assert config.get_redis_config()["db"] == "2"


def test_redis_db_default(monkeypatch):
    monkeypatch.delenv("REDIS_DB", raising=False)
    config = Config()
    assert config.get_redis_config()["db"] == 0


# Redis Password Tests
def test_redis_password_setenv(monkeypatch):
    monkeypatch.setenv("REDIS_PASSWORD", "test_password")
    config = Config()
    assert config.get_redis_config()["password"] == "test_password"


def test_redis_password_default(monkeypatch):
    monkeypatch.delenv("REDIS_PASSWORD", raising=False)
    config = Config()
    assert config.get_redis_config()["password"] is None


# Combined Test for All Redis Configurations
def test_get_redis_config_setenv(monkeypatch):
    monkeypatch.setenv("REDIS_HOST", "test_host")
    monkeypatch.setenv("REDIS_PORT", "6380")
    monkeypatch.setenv("REDIS_DB", "2")
    monkeypatch.setenv("REDIS_PASSWORD", "test_password")

    config = Config()  # Instantiate Config after setting the environment variables
    expected_config = {
        "host": "test_host",
        "port": "6380",
        "db": "2",
        "password": "test_password",
    }
    assert config.get_redis_config() == expected_config


def test_get_redis_config_default(monkeypatch):
    monkeypatch.delenv("REDIS_HOST", raising=False)
    monkeypatch.delenv("REDIS_PORT", raising=False)
    monkeypatch.delenv("REDIS_DB", raising=False)
    monkeypatch.delenv("REDIS_PASSWORD", raising=False)

    config = Config()  # Re-instantiate Config after unsetting the environment variables
    expected_config = {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": None,
    }
    assert config.get_redis_config() == expected_config
