import pytest
from bin_lookup_indexer.parsers.redsys_parser import RedsysParser
from unittest.mock import patch, mock_open


@pytest.fixture
def sample_line():
    return "10" + "400002000000000000" + "400002000999999999" + " " * 160


@pytest.fixture
def redsys_parser():
    return RedsysParser()


def test_parse_fixed_width_line(redsys_parser, sample_line):
    # Mock the colspecs, translation_rules, and excluded_fields to test the function in isolation
    with (
        patch.object(
            redsys_parser,
            "colspecs",
            [
                (0, 2, "StructureCode"),
                (2, 20, "LowAccountRange"),
                (20, 40, "HighAccountRange"),
            ],
        ),
        patch.object(redsys_parser, "translation_rules", []),
        patch.object(redsys_parser, "excluded_fields", []),
    ):  # Ensure no fields are excluded

        parsed_data = redsys_parser.parse_fixed_width_line(sample_line)
        assert parsed_data["StructureCode"] == "10"
        assert parsed_data["LowAccountRange"] == "400002000000000000"
        assert parsed_data["HighAccountRange"] == "400002000999999999"


def test_apply_translation(redsys_parser):
    parsed_data = {"Group": "1", "IssuerCode": "5401"}

    # Mock translation rules: one for a regular dictionary lookup, one for a callable
    with patch.object(
        redsys_parser,
        "translation_rules",
        [
            (
                "Group",
                {"1": "VISA SPAIN (REDSYS INTERNAL)"},
            ),  # Regular dictionary translation
            (
                "IssuerCode",
                lambda data: f"Issuer-{data['IssuerCode']}",
            ),  # Callable translation
        ],
    ):
        translated_data = redsys_parser.apply_translation(parsed_data)

        # Check regular dictionary translation
        assert translated_data["Group"] == "VISA SPAIN (REDSYS INTERNAL)"

        # Check callable translation
        assert translated_data["IssuerCode"] == "Issuer-5401"


def test_group_issuer_fields(redsys_parser):
    data = {
        "IssuerType": "National",
        "IssuerCode": "5401",
        "IssuerName": "River Valley Credit Union",
    }
    grouped_data = redsys_parser.group_issuer_fields(data)
    assert "Issuer" in grouped_data
    assert grouped_data["Issuer"] == {
        "Code": "5401",
        "Name": "River Valley Credit Union",
        "Type": "National",
    }


def test_expand_currency_and_country(redsys_parser):
    data = {"Currency": "840", "Country": "840"}
    expanded_data = redsys_parser.expand_currency_and_country(data)
    assert expanded_data["Currency"]["Alpha3"] == "USD"
    assert expanded_data["Country"]["Alpha3"] == "USA"


def test_parse_file_handling(redsys_parser):
    sample_content = (
        "104000020000000000004000020009999999991616010101684011C1W555401River Valley Credit Union               55540110001201400002     400002                           00840C 00"
        + " " * 30
        + "\n"  # Valid BIN record
        "90BIN000050008202406071216230001001425"
        # Valid totalization record
    )

    with patch("builtins.open", mock_open(read_data=sample_content)) as mock_file:
        parsed_records = list(redsys_parser.parse("fake_path"))

        assert len(parsed_records) == 1  # Ensure one BIN record was parsed
        mock_file.assert_called_once_with("fake_path", "r", encoding="cp1252")


def test_parse_atm_only_record_handling(redsys_parser):
    sample_content = (
        "104765882100000000004765882199999999991616010101648452D1W571602                                        57160210001201711488     711488                           00484C 00"
        + " " * 30
        + "\n"  # ATM only BIN record
        "90BIN000050008202406071216230001001425"
        # Valid totalization record
    )

    with patch("builtins.open", mock_open(read_data=sample_content)) as mock_file:
        parsed_records = list(redsys_parser.parse("fake_path"))

        assert len(parsed_records) == 0  # Ensure ATM only record was skipped
        mock_file.assert_called_once_with("fake_path", "r", encoding="cp1252")


def test_parse_totalization_record(redsys_parser):
    sample_content = (
        "00" + " " * 198 + "\n"  # Valid BIN record
        "10" + " " * 198 + "\n"  # Valid BIN record
        "90" + " " * 26 + "000003" + " " * 166  # Valid totalization record
    )

    with (
        patch("builtins.open", mock_open(read_data=sample_content)),
        patch.object(
            redsys_parser,
            "apply_translation",
            return_value={
                "LowAccountRange": "400002000000000000",
                "HighAccountRange": "400002000999999999",
                "Usage": "PURCHASES",
                "IssuerCode": "5401",
                "IssuerType": "National",
            },
        ),
        patch(
            "bin_lookup_indexer.parsers.redsys_parser.logger.info"
        ) as mock_logger_info,
    ):
        parsed_records = list(redsys_parser.parse("fake_path"))

        # Verify that logger.info was called with the correct arguments
        mock_logger_info.assert_called_with(
            "All records have been processed successfully",
            processed=1,
            atm_only=0,
            stored=1,
        )


def test_parse_with_missing_records(redsys_parser):
    sample_content = (
        "00" + " " * 198 + "\n"  # Valid BIN record
        "10" + " " * 198 + "\n"  # Valid BIN record
        "90" + " " * 26 + "000004" + " " * 166  # Valid totalization record
        # Incorrect totalization record (4 expected -minus 2 for header and totalization-, only 3 provided)
    )

    with (
        patch("builtins.open", mock_open(read_data=sample_content)),
        patch.object(
            redsys_parser,
            "apply_translation",
            return_value={
                "LowAccountRange": "400002000000000000",
                "HighAccountRange": "400002000999999999",
                "Usage": "PURCHASES",
                "IssuerCode": "5401",
                "IssuerType": "National",
            },
        ),
        patch(
            "bin_lookup_indexer.parsers.redsys_parser.logger.error"
        ) as mock_logger_error,
    ):
        parsed_records = list(redsys_parser.parse("fake_path"))

        mock_logger_error.assert_called_with(
            "Some records could not be processed", records=2, processed=1
        )
