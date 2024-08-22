import pytest
from bin_lookup_indexer.parsers.parser_factory import ParserFactory
from bin_lookup_indexer.parsers.redsys_parser import RedsysParser
from bin_lookup_indexer.parsers.mastercard_parser import MastercardParser


def test_create_parser_redsys_v3_8():
    # Test with provider and version for Redsys
    parser = ParserFactory.create_parser("redsys_3.8")
    assert isinstance(parser, RedsysParser)


def test_create_parser_mastercard_simplified():
    # Test with provider and version for Mastercard
    parser = ParserFactory.create_parser("mastercard_simplified")
    assert isinstance(parser, MastercardParser)


def test_create_parser_invalid_format():
    # Test with an invalid format (unsupported provider)
    with pytest.raises(ValueError) as exc_info:
        ParserFactory.create_parser("invalid_format")
    assert str(exc_info.value) == "Unsupported format: invalid_format"


def test_create_parser_invalid_version_format():
    # Test with an invalid format where version is missing
    with pytest.raises(ValueError) as exc_info:
        ParserFactory.create_parser("redsys_")
    assert str(exc_info.value) == "Unsupported version: "


def test_create_parser_no_version():
    # Test with only the provider, no version (assuming this is invalid)
    with pytest.raises(ValueError) as exc_info:
        ParserFactory.create_parser("redsys")
    assert (
        str(exc_info.value)
        == "Format 'redsys' is invalid. It should be in the form 'Provider_Version'."
    )
