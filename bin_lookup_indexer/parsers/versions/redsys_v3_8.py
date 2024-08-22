"""
 REDSYS FILE PARSER - VERSION 3.8
 --------------------------------
 This module defines the column specifications and
 translation dictionaries for Redsys format version 3.8.
"""
from typing import Dict, Any, Callable

# Define the column specifications for this version
colspecs = [
    (0, 2, "StructureCode"),
    (2, 20, "LowAccountRange"),
    (20, 38, "HighAccountRange"),
    (38, 40, "MinimumLength"),
    (40, 42, "MaximumLength"),
    (42, 44, "Brand"),
    (44, 46, "CardName"),
    (46, 49, "CardDescription"),
    (49, 52, "Country"),
    (52, 53, "Region"),
    (53, 54, "Usage"),
    (54, 55, "FundingSource"),
    (55, 56, "CheckDigit"),
    (56, 57, "UsageScope"),
    (57, 59, "IssuerType"),
    (59, 63, "IssuerCode"),
    (63, 103, "IssuerName"),
    (103, 105, "ProcessingEntityType"),
    (105, 109, "ProcessorCode"),
    (109, 111, "GroupType"),
    (111, 115, "Group"),
    (115, 117, "Organism"),
    (117, 128, "BINPrefix"),
    (128, 139, "BINProcessorPrefix"),
    (139, 150, "ICA"),
    (150, 161, "ICAProcessor"),
    (161, 162, "ChipTechnology"),
    (162, 163, "Prepaid"),
    (163, 166, "Currency"),
    (166, 168, "CardType"),
    (168, 169, "Contactless"),
    (169, 170, "Token"),
]

brands = {
    "00": "UNASSIGNED",
    "01": "VISA",
    "02": "MASTERCARD",
    "04": "4B CARD",
    "05": "EURO6000 CARD",
    "06": "DINERS CLUB",
    "07": "PRIVATE",
    "08": "AMERICAN EXPRESS",
    "09": "JCB",
    "10": "CITICORP",
    "11": "CLAU",
    "13": "DIESEL FUEL",
    "15": "MULTIBANCO PORTUGAL",
    "16": "TRANSPONDERS",
    "22": "CHINA UNION PAY 99 OTHERS",
    "99": "OTHER",
}

card_names = {
    "01": "VISA CLASSIC",
    "02": "VISA ELECTRON",
    "03": "VISA GOLD",
    "04": "MASTERCARD",
    "05": "MASTERCARD EU",
    "06": "ACCESS CARD",
    "07": "MASTER B2B",
    "08": "4B CARD",
    "09": "ALIPAY QR",
    "10": "PLUS",
    "11": "CIRRUS",
    "12": "DINERS",
    "14": "EURO6000 CARD",
    "15": "WECHAT",
    "16": "VISA CORPORATE GOLD",
    "17": "AMERICAN EXPRESS",
    "18": "MAESTRO",
    "19": "JCB CONSUMPTION",
    "20": "CITICORP",
    "21": "CLAU",
    "22": "VISA B2B",
    "23": "DISCOUNTED DIESEL",
    "24": "VISA CORPORATE T&E CARD",
    "25": "VISA PURCHASING CARD",
    "26": "VISA BUSINESS SILVER",
    "27": "VISA BUSINESS GENERIC",
    "28": "VISA BUSINESS GOLD",
    "29": "DIPLOMATIC DIESEL",
    "30": "VISA AFFINITY CLASSIC",
    "31": "VISA AFFINITY GOLD",
    "32": "VISA ATM",
    "33": "TRAVEL VOUCHER",
    "34": "VISA CASH",
    "35": "MASTERCARD ATM",
    "36": "MULTIBANCO SIBS",
    "37": "PRIVATE LEADER (L)",
    "38": "VISA AFFINITY ELECTRON",
    "39": "VISA CASH AFFINITY",
    "40": "VISA CASH-ELECTRON",
    "41": "VISA CASH-CLASSIC",
    "42": "VISA CASH-PREMIER",
    "43": "ANONYMOUS 4B WALLET",
    "44": "DUMMY CASH PAYMENT",
    "45": "S4B CASH MIXED",
    "46": "CAIXA PHONE WALLET",
    "47": "VISA PROPRIETARY",
    "48": "MASTER DEBIT CASH S4B",
    "49": "ANONYMOUS VISA CASH",
    "50": "MAESTRO EURO6000",
    "51": "MASTER BUSINESS CORPORATE",
    "52": "MASTER PURCHASING",
    "53": "VISA TRAVEL MONEY",
    "54": "VISA CASH ELECTRON AFFINITY",
    "55": "MASTER EU BUSINESS",
    "56": "MASTER EU PURCHASING",
    "57": "MAESTRO ATM",
    "58": "MASTERCARD EU GOLD",
    "59": "MASTER EU PLATINUM",
    "60": "MASTERCARD GOLD",
    "61": "MASTER PLATINUM WORLD",
    "62": "VISA PLATINUM",
    "63": "PRIVATE",
    "64": "MASTER EU CORPORATE",
    "65": "MASTER EU WORLDSIGN",
    "66": "MASTER WORLD BUSINESS",
    "67": "VISA VIRTUAL",
    "68": "MASTER EU VIRTUAL",
    "69": "MASTERCARD EU CLIP",
    "70": "TRANSPONDERS",
    "71": "MASTER EU ELECTRONIC",
    "72": "VISA INFINITE",
    "73": "TRAVELCLUB",
    "74": "MASTERCARD EU DEBIT",
    "75": "VISA VPAY",
    "76": "MASTERCARD EU WORLD",
    "77": "AMEX SERVIRED",
    "78": "CUP (CAIXA ATM)",
    "79": "MASTER EU CONSUMER PREPAID",
    "80": "MASTER EU COMMERCIAL PREPAID",
    "81": "MAESTRO CONSUMER PREPAID",
    "82": "MAESTRO COMMERCIAL PREPAID",
    "83": "MAESTRO SMALL BUSINESS",
    "84": "MASTERCARD WORLD",
    "85": "VIA-T COMPANY",
    "86": "AMAZON PAY",
    "88": "CUP COMPANY",
    "89": "CUP CONSUMER",
    "90": "JCB COMPANY",
    "91": "MASTER MONTH",
    "92": "MASTER EU PLATINUM DEBIT",
    "93": "DINERS CONSUMER",
    "94": "DINERS COMMERCIAL",
    "97": "MISCELLANEOUS",
    "98": "AGROTARJETA BRAZIL",
}

card_description_types = {
    "01A": "VISA PREMIER ANDORRA",
    "01B": "VISA PREMIER EXTRANJERA",
    "01C": "VISA ELECTRON REDSYS",
    "01D": "VISA ELECTRON ANDORRA",
    "01E": "VISA ELECTRON EXTRANJERA",
    "01F": "VISA CASH ELECTRON SERVIRED",
    "01G": "VISA PURCHASING REDES",
    "01H": "VISA CASH CLASSIC SERVIRED",
    "01I": "VPAY REDSYS",
    "01J": "VISA CASH PREMIER SERVIRED",
    "01K": "VISA BUSINESS REDES",
    "01L": "VISA CASH SERVIRED",
    "01M": "VISA PLATINUM EXTRANJERA",
    "01N": "VISA BUSINESS SERVIRED",
    "01O": "VISA INFINITE SERVIRED",
    "01P": "VISA T&E CORPORATE SERVIRED",
    "01Q": "VISA CORPORATE T&E REDES",
    "01R": "VISA CASH ANONIMA SERVIRED",
    "01S": "VISA PLATINUM SERVIRED",
    "01T": "VISA BUSINESS EXTRANJERA",
    "01U": "VISA PURCHASING EXTRANJERA",
    "01V": "VISA CORPORATE T&E EXTRANJERA",
    "01W": "VISA TRAVEL MONEY EXTRANJERA",
    "01X": "VISA PURCHASING SERVIRED",
    "01Y": "VISA ELECTRON REDES",
    "01Z": "VISA INFINITE EXTRANJERA",
    "010": "VISA VPAY EXTRANJERA",
    "011": "VISA ELECTRON SERVIRED",
    "012": "VISA CLASSIC SERVIRED",
    "013": "VISA CLASSIC REDSYS",
    "014": "VISA CLASSIC REDES",
    "015": "VISA CLASSIC ANDORRA",
    "016": "VISA CLASSIC EXTRANJERA",
    "017": "VISA PREMIER SERVIRED",
    "018": "VISA PREMIER REDSYS",
    "019": "VISA PREMIER REDES",
    "02A": "MASTERCARD EU WORLD SIGNIA EXT",
    "02B": "MASTER EU COMMERC. PREP EXTR.",
    "02C": "MASTERCARD EU ORO SERVIRED",
    "02D": "DEBIT MASTERCARD EU EXTRANJERA",
    "02E": "MASTERCARD EU ELECTRONICS EXT",
    "02F": "CLIP EXTRANJERA",
    "02G": "MASTERCARD EU ORO EXTRANJERA",
    "02H": "MASTER EU PLATINUM EXTRANJERA",
    "02K": "MASTER EU BUSINESS REDES",
    "02M": "MASTER EU PLATINUM SERVIRED",
    "02N": "MASTER EU BUSINESS SERVIRED",
    "02P": "MASTER EU CORPORATE SERVIRED",
    "02Q": "MASTER EU CORPORATE REDES",
    "02R": "MASTER EXTRANJERA EU B2B",
    "02S": "MC EU PLATINUM SERVIRED DB",
    "02T": "MASTERCARD EU BUSINESS EXTRANJ",
    "02U": "MASTERCARD EU PURCHASING EXT",
    "02V": "MASTERCARD EU CORPORATE EXT",
    "02W": "MASTERCARD EU WORLD EXTRANJERA",
    "02X": "MASTER EXTRANJERA MES",
    "021": "MASTERCARD EU DEBITO SERVIRED",
    "022": "MASTERCARD EU SERVIRED",
    "023": "MASTERCARD EU REDSYS",
    "024": "MASTERCARD EU REDES",
    "025": "MASTERCARD EU ANDORRA",
    "026": "MASTERCARD EU EXTRANJERA",
    "027": "MASTER EU CONSUMER PREP. SERV",
    "028": "MASTER EU CONSUMER PREP EXTR.",
    "029": "MASTER EU COMMERC. PREP SERV",
    "031": "MONEDERO 4B ANONIMO",
    "032": "MONEDERO 4B DEBITO SIN BANDA",
    "033": "MONEDERO 4B DEBITO CON BANDA",
    "034": "4B DEBITO",
    "035": "TARJETA EMV 4B",
    "036": "CUP COMPRAS EXTRANJERA",
    "042": "EUROCHEQUE SERVIRED (BAJA)",
    "043": "EUROCHEQUE SERMEPA_(BAJA)",
    "044": "EUROCHEQUE REDES (BAJA)",
    "045": "EUROCHEQUE ANDORRA (BAJA)",
    "046": "EUROCHEQUE EXTRANJERA (BAJA)",
    "050": "CAIXA OBERTA",
    "051": "MONEDERO TELEFONICO CAIXA",
    "06A": "MASTERCARD WORLD BUSINESS",
    "06D": "AGROTARJETA BRASIL",
    "06M": "MASTERCARD WORLD EXTRANJERA",
    "06T": "MASTERCARD BUSINESS CORPORATE",
    "06U": "MASTERCARD PURCHASING EXT",
    "06W": "MASTER PLATINUM/WORLD EXTRANJ",
    "062": "MASTERCARD SERVIRED",
    "063": "MASTERCARD REDSYS",
    "064": "MASTERCARD REDES",
    "065": "MASTERCARD ANDORRA",
    "066": "MASTERCARD EXTRANJERA",
    "067": "MASTERCARD DEBITO CASH S4B",
    "068": "MASTERCARD ATM EXTRANJERA",
    "070": "CAJA MADRID - RED 6000",
    "080": "WECHAT",
    "081": "AMAZON PAY",
    "090": "TARJETAS PRIVADAS",
    "091": "MISCELANEO",
    "092": "ALIPAY PRIVADA",
    "093": "QR ALIPAY",
    "10A": "MAESTRO ATM SERVIRED",
    "10B": "MAESTRO COMMERC. PREPAGO EXTR",
    "10C": "MAESTRO CONSUMER PREPAGO EXTR",
    "10D": "MAESTRO ATM ANDORRA",
    "10E": "MAESTRO SMALL BUSINESS EXTRANJ",
    "10F": "MAESTRO SMALL BUSINESS SERV.",
    "100": "R.U.F.",
    "101": "MAESTRO CONSUMER PREPAGO SERV",
    "102": "MAESTRO SERVIRED",
    "103": "MAESTRO REDSYS",
    "104": "MAESTRO REDES",
    "105": "MAESTRO ANDORRA",
    "106": "MAESTRO EXTRANJERA",
    "107": "MAESTRO ATM REDES",
    "108": "MAESTRO ATM EXTRANJERA",
    "109": "MAESTRO COMMERC. PREPAGO SERV",
    "110": "TARJETA EURO6000",
    "116": "CHINA UNION PAY (CUP)",
    "120": "AMEX NACIONAL",
    "121": "AMEX SERVIRED",
    "126": "AMEX EXTRANJERA",
    "136": "CIRRUS (ATM) EXTRANJERA",
    "140": "DINERS NACIONAL",
    "146": "DINERS EXTRANJERA",
    "147": "DINERS CONSUMER",
    "148": "DINERS COMMERCIAL",
    "156": "PLUS (ATM) EXTRANJERA",
    "160": "JCB EXTRANJERA",
    "163": "JCB EMPRESA",
    "166": "JCB CONSUMO",
    "170": "CITICORP",
    "185": "CLAU",
    "190": "VISA B2B",
    "194": "VISA INFINITE REDES",
    "20F": "MULTIBANCO (SIBS)",
    "20H": "SERMECHIP",
    "200": "GASOLEO",
    "201": "TRANSPONDEDORES",
    "202": "TRASPONDEDOR EMPRESA",
    "223": "CUP EMPRESA",
    "226": "CHINA UNION PAY CONSUMO",
}

groups = {
    1: "VISA SPAIN (REDSYS INTERNAL)",
    2: "SYSTEM 4B",
    3: "SEMP (REDSYS INTERNAL)",
    5: "REDSYS (Private SVR and Cross-border of National Entity)",
    6: "AMEX",
    8: "DINERS",
    11: "ANDORRAN ENTITY",
    12: "FOREIGN ENTITY",
    13: "CECA NETWORK",
    17: "IMMEDIATE PAYMENTS",
    23: "E5K MIGRATED TO REDSYS (ENTITIES OF THE 6000 NETWORK THAT PROCESS IN REDSYS)",
    9000: "SERVIRED",
}

regions_by_brand = {
    0: {  # Unassigned
        "1": "UNITED STATES OF AMERICA",
        "2": "CANADA",
        "3": "CENTRAL EUROPE, MIDDLE EAST, AND AFRICA",
        "4": "ASIA AND PACIFIC",
        "5": "CARIBBEAN, MEXICO, CENTRAL AND SOUTH AMERICA",
        "6": "EUROPEAN UNION",
        "7": "EUROPAY INTERNATIONAL",
        "8": "EUROPEAN ECONOMIC AREA (NON-EU)",
    },
    1: {  # Visa
        "A": "ASIA AND PACIFIC",
        "B": "EASTERN EUROPE, MIDDLE EAST, AND AFRICA",
        "C": "CANADA",
        "E": "EUROPE",
        "F": "LATIN AMERICA AND CARIBBEAN",
        "1": "UNITED STATES",
        "2": "CANADA",
        "3": "EUROPE",
        "4": "ASIA-PACIFIC (OCEMA)",
        "5": "LATIN AMERICA/CARIBBEAN",
        "6": "CEMEA",
    },
    2: {  # Mastercard
        "A": "CANADA",
        "B": "LATIN AMERICA AND CARIBBEAN",
        "C": "ASIA AND PACIFIC",
        "D": "EUROPE",
        "E": "MIDDLE EAST AND AFRICA",
        "F": "SOUTHEAST ASIA/NEAR EAST/AFRICA",
        "M": "REST OF THE WORLD (MASTERCARD)",
        "1": "UNITED STATES",
        "6": "EASTERN EUROPE",
    },
    9: {  # JCB
        "1": "NORTH AND SOUTH AMERICA",
        "2": "JAPAN",
        "3": "ASIA AND OCEANIA (EXCLUDING JAPAN)",
        "4": "EUROPE, MIDDLE EAST, AND AFRICA (EXCLUDING SEPA)",
        "5": "SEPA",
    },
}

usages = {"1": "ATM & PURCHASES", "2": "ATM", "3": "PURCHASES"}

funding_sources = {
    "C": "CREDIT",
    "D": "DEBIT",
    "E": "CREDIT",
    "F": "DEBIT",
    "G": "CREDIT",
    "H": "DEBIT",
    "I": "CREDIT",
    "J": "MIXED",
    "X": "MIXED",
}

check_digits = {"0": False, "1": True}

usage_scopes = {"W": "WORLD", "R": "REGION", "E": "EUROPE", "N": "COUNTRY"}

issuer_types = {
    "00": "NATIONAL",
    "10": "NON-FINANCIAL",
    "20": "ANDORRAN",
    ">=50": "FOREIGN",
}

processing_entity_types = {
    "00": "NATIONAL",
    "10": "NON-FINANCIAL",
    "20": "ANDORRAN",
    ">=50": "FOREIGN",
}

card_types = {
    "C": "CONSUMER",
    "E": "CORPORATE",
    "CR": "RESTRICTED CONSUMER",
    "ER": "RESTRICTED CORPORATE",
}

contactless = {"0": "NO", "1": "YES", "2": "MOBILE"}

token = {"0": False, "1": True}

prepaid = {"0": False, "1": True}

chip_technology = {"0": False, "1": True}


#def create_conditional_translation(translation_dict, key):
def create_conditional_translation(
    translation_dict: Dict[str, str], key: str
) -> Callable[[Dict[str, Any]], str]:
    """
    Creates a lambda function to handle conditional translations based on the provided dictionary.

    Args:
        translation_dict (dict): A dictionary where the keys are the exact matches or conditions
                                 (e.g., ">=50") and the values are the corresponding translations.

    Returns:
        function: A lambda function that performs the conditional translation.
    """

    def translator(record: dict):
        value = record.get(key, "")

        # Exact match first
        if value in translation_dict:
            return translation_dict[value]

        # Check for any conditional rules
        for condition, translation in translation_dict.items():
            if condition.startswith(">="):
                threshold = int(condition[2:])
                if int(value) >= threshold:
                    return translation
            elif condition.startswith("<="):
                threshold = int(condition[2:])
                if int(value) <= threshold:
                    return translation
            elif condition.startswith(">"):
                threshold = int(condition[1:])
                if int(value) > threshold:
                    return translation
            elif condition.startswith("<"):
                threshold = int(condition[1:])
                if int(value) < threshold:
                    return translation

        # If no match, return a default or unknown value
        return "Unknown"

    return lambda parsed_data: translator(parsed_data)


# Generate the translation lambdas using the generalized factory
processing_entity_translation = create_conditional_translation(
    processing_entity_types, "ProcessingEntityType"
)
issuer_type_translation = create_conditional_translation(issuer_types, "IssuerType")

# Define the translation rules in order
translation_rules = [
    (
        "Region",
        lambda parsed_data: regions_by_brand.get(int(parsed_data["Brand"]), {}).get(
            parsed_data["Region"], "Unknown"
        ),
    ),
    ("Brand", brands),
    ("CardName", card_names),
    ("CardDescription", card_description_types),
    ("Group", lambda parsed_data: groups.get(int(parsed_data["Group"]), "Unknown")),
    ("Usage", usages),
    ("FundingSource", funding_sources),
    ("CheckDigit", check_digits),
    ("UsageScope", usage_scopes),
    ("IssuerType", issuer_type_translation),  # uses the generated lambda
    (
        "ProcessingEntityType",
        processing_entity_translation,
    ),  # uses the generated lambda
    ("CardType", card_types),
    ("Contactless", contactless),
    ("Token", token),
    ("Prepaid", prepaid),
    ("ChipTechnology", chip_technology),
    ("LowAccountRange", lambda parsed_data: int(parsed_data["LowAccountRange"])),
    ("HighAccountRange", lambda parsed_data: int(parsed_data["HighAccountRange"])),
]

# Define fields to exclude
excluded_fields = [
    "StructureCode",
    "MinimumLength",
    "MaximumLength",
    "GroupType",
    "Organism",
    "ProcessorCode",
    "ProcessingEntityType",
    "ICAProcessor",
    "BINProcessorPrefix",
]
