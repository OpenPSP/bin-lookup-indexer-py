import pytest
from bin_lookup_indexer.parsers.mastercard_parser import MastercardParser
from unittest.mock import patch, mock_open


@pytest.fixture
def sample_row():
    return {
        "COMPANY_NAME": "Test Issuer",
        "ICA": "12345",
        "ACCOUNT_RANGE_FROM": "4000020000000000",
        "ACCOUNT_RANGE_TO": "4000029999999999",
        "BRAND_PRODUCT_CODE": "MCC",
        "BRAND_PRODUCT_NAME": "Mastercard Credit",
        "ACCEPTANCE_BRAND": "MCC",
        "COUNTRY": "USA",
    }


@pytest.fixture
def mastercard_parser():
    return MastercardParser()


def test_rename_fields(mastercard_parser, sample_row):
    # Mock the column mappings to test the rename function in isolation
    with patch.object(
        mastercard_parser,
        "column_mappings",
        {
            "COMPANY_NAME": "IssuerName",
            "ICA": "ICA",
            "ACCOUNT_RANGE_FROM": "LowAccountRange",
            "ACCOUNT_RANGE_TO": "HighAccountRange",
            "BRAND_PRODUCT_CODE": "CardName",
            "BRAND_PRODUCT_NAME": "CardDescription",
            "ACCEPTANCE_BRAND": "Brand",
            "COUNTRY": "CountryAlpha3",
        },
    ):
        renamed_data = mastercard_parser.rename_fields(sample_row)
        assert renamed_data["IssuerName"] == "Test Issuer"
        assert renamed_data["LowAccountRange"] == "4000020000000000"
        assert renamed_data["CardName"] == "MCC"
        assert renamed_data["CountryAlpha3"] == "USA"


def test_apply_translation(mastercard_parser):
    parsed_data = {"Brand": "MCC", "CardName": "MCC"}

    # Mock translation rules: one for a regular dictionary lookup
    with patch.object(
        mastercard_parser,
        "translation_rules",
        [
            ("Brand", {"MCC": "Mastercard Credit"}),  # Regular dictionary translation
            (
                "CardName",
                {"MCC": "Mastercard Credit Card"},
            ),  # Regular dictionary translation
        ],
    ):
        translated_data = mastercard_parser.apply_translation(parsed_data)

        # Check regular dictionary translation
        assert translated_data["Brand"] == "Mastercard Credit"
        assert translated_data["CardName"] == "Mastercard Credit Card"


def test_expand_country(mastercard_parser):
    data = {"CountryAlpha3": "USA"}
    expanded_data = mastercard_parser.expand_country(data)
    assert expanded_data["Country"]["Alpha3"] == "USA"
    assert expanded_data["Country"]["Code"] == "840"
    assert expanded_data["Country"]["Name"] == "United States"


def test_parse_csv_handling(mastercard_parser):
    sample_content = "Test Issuer,12345,4000020000000000,4000029999999999,MCC,Mastercard Credit,MCC,USA\n"

    with patch("builtins.open", mock_open(read_data=sample_content)) as mock_file:
        parsed_records = list(mastercard_parser.parse("fake_path"))

        assert len(parsed_records) == 1  # Ensure one record was parsed
        mock_file.assert_called_once_with("fake_path", "r", encoding="utf-8")


def test_parse_with_missing_country(mastercard_parser):
    sample_content = "Test Issuer,12345,4000020000000000,4000029999999999,MCC,Mastercard Credit,MCC,XYZ\n"

    with patch("builtins.open", mock_open(read_data=sample_content)) as mock_file:
        parsed_records = list(mastercard_parser.parse("fake_path"))

        assert len(parsed_records) == 1  # Ensure one record was parsed
        assert parsed_records[0]["Country"]["Name"] == "Unknown Country"
        mock_file.assert_called_once_with("fake_path", "r", encoding="utf-8")


def test_parse_multiple_records(mastercard_parser):
    sample_content = (
        "Test Issuer,12345,4000020000000000,4000029999999999,MCC,Mastercard Credit,MCC,USA\n"
        "Another Issuer,67890,5000020000000000,5000029999999999,DMC,Debit Mastercard,DMC,CAN\n"
    )

    with patch("builtins.open", mock_open(read_data=sample_content)) as mock_file:
        parsed_records = list(mastercard_parser.parse("fake_path"))

        assert len(parsed_records) == 2  # Ensure two records were parsed
        assert parsed_records[0]["IssuerName"] == "Test Issuer"
        assert parsed_records[1]["IssuerName"] == "Another Issuer"
        mock_file.assert_called_once_with("fake_path", "r", encoding="utf-8")


def test_parse_and_exclude_fields(mastercard_parser):
    sample_content = "Test Issuer,12345,4000020000000000,4000029999999999,MCC,Mastercard Credit,MCC,USA\n"

    with (
        patch("builtins.open", mock_open(read_data=sample_content)),
        patch.object(
            mastercard_parser, "excluded_fields", ["IssuerName", "CardDescription"]
        ),
    ):
        parsed_records = list(mastercard_parser.parse("fake_path"))

        assert len(parsed_records) == 1  # Ensure one record was parsed
        assert "IssuerName" not in parsed_records[0]
        assert "CardDescription" not in parsed_records[0]


def test_parse_with_translation(mastercard_parser):
    sample_content = "Test Issuer,12345,4000020000000000,4000029999999999,MCC,Mastercard Credit,MCC,USA"

    with (
        patch("builtins.open", mock_open(read_data=sample_content)),
        patch.object(
            mastercard_parser,
            "column_mappings",
            {
                "COMPANY_NAME": "IssuerName",
                "ICA": "ICA",
                "ACCOUNT_RANGE_FROM": "LowAccountRange",
                "ACCOUNT_RANGE_TO": "HighAccountRange",
                "BRAND_PRODUCT_CODE": "CardName",
                "BRAND_PRODUCT_NAME": "CardDescription",
                "ACCEPTANCE_BRAND": "Brand",
                "COUNTRY": "CountryAlpha3",
            },
        ),
        patch.object(
            mastercard_parser,
            "translation_rules",
            [
                ("Brand", {"MCC": "Mastercard Credit"}),
                ("CardName", {"MCC": "Mastercard Credit Card"}),
            ],
        ),
    ):
        parsed_records = list(mastercard_parser.parse("fake_path"))

        assert len(parsed_records) == 1  # Ensure one record was parsed
        assert parsed_records[0]["Brand"] == "Mastercard Credit"
        assert parsed_records[0]["CardName"] == "Mastercard Credit Card"
