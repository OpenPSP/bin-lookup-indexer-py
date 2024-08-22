import pytest
from bin_lookup_indexer.parsers.versions.redsys_v3_8 import (
    create_conditional_translation,
)


@pytest.fixture
def processing_entity_translation():
    processing_entity_types = {
        "<=10": "NATIONAL",
        "15": "NON-FINANCIAL",
        "20": "ANDORRAN",
        ">=50": "FOREIGN",
    }
    return create_conditional_translation(
        processing_entity_types, "ProcessingEntityType"
    )


@pytest.fixture
def issuer_type_translation():
    issuer_types = {
        "<10": "NATIONAL",
        "10": "NON-FINANCIAL",
        "20": "ANDORRAN",
        ">50": "FOREIGN",
    }
    return create_conditional_translation(issuer_types, "IssuerType")


@pytest.fixture
def regions_by_brand():
    return {
        0: {  # Unassigned
            "1": "UNITED STATES",
            "2": "CANADA",
        },
        1: {  # Visa
            "A": "ASIA AND PACIFIC",
        },
    }


@pytest.fixture
def brands():
    return {"01": "VISA", "02": "MASTERCARD"}


@pytest.fixture
def groups():
    return {
        1: "VISA SPAIN (REDSYS INTERNAL)",
        2: "SYSTEM 4B",
    }


@pytest.fixture
def translation_rules(regions_by_brand, brands, groups):
    return [
        (
            "Region",
            lambda parsed_data: regions_by_brand.get(int(parsed_data["Brand"]), {}).get(
                parsed_data["Region"], "Unknown"
            ),
        ),
        ("Brand", brands),
        ("Group", lambda parsed_data: groups.get(int(parsed_data["Group"]), "Unknown")),
    ]


def test_exact_match(processing_entity_translation):
    parsed_data = {"ProcessingEntityType": "15"}
    result = processing_entity_translation(parsed_data)
    assert result == "NON-FINANCIAL"


def test_no_match(processing_entity_translation):
    parsed_data = {"ProcessingEntityType": "12"}
    result = processing_entity_translation(parsed_data)
    assert result == "Unknown"  # No match found, returns "Unknown"


def test_greater_than_or_equal(processing_entity_translation):
    parsed_data = {"ProcessingEntityType": "55"}
    result = processing_entity_translation(parsed_data)
    assert result == "FOREIGN"


def test_less_than_or_equal(processing_entity_translation):
    parsed_data = {"ProcessingEntityType": "8"}
    result = processing_entity_translation(parsed_data)
    assert result == "NATIONAL"


def test_less_than(issuer_type_translation):
    parsed_data = {"IssuerType": "8"}
    result = issuer_type_translation(parsed_data)
    assert result == "NATIONAL"


def test_greater_than(issuer_type_translation):
    parsed_data = {"IssuerType": "75"}
    result = issuer_type_translation(parsed_data)
    assert result == "FOREIGN"


def test_region_translation(translation_rules):
    parsed_data = {"Brand": "1", "Region": "A"}
    region_rule = translation_rules[0][1]
    result = region_rule(parsed_data)
    assert result == "ASIA AND PACIFIC"


def test_brand_translation(translation_rules):
    parsed_data = {"Brand": "01"}
    brand_rule = translation_rules[1][1]
    result = brand_rule.get(parsed_data["Brand"], "Unknown")
    assert result == "VISA"


def test_group_translation(translation_rules):
    parsed_data = {"Group": "1"}
    group_rule = translation_rules[2][1]
    result = group_rule(parsed_data)
    assert result == "VISA SPAIN (REDSYS INTERNAL)"


def test_unknown_group(translation_rules):
    parsed_data = {"Group": "99"}
    group_rule = translation_rules[2][1]
    result = group_rule(parsed_data)
    assert result == "Unknown"
