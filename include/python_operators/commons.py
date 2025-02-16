import yaml


def extract_keywords(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    keywords = set()

    if "us_stocks" in data["stocks"] and "stocks" in data["stocks"]["us_stocks"]:
        for stock in data["stocks"]["us_stocks"]["stocks"]:
            if "keywords" in stock:
                keywords.update(stock["keywords"])

    if (
        "crypto_stocks" in data["stocks"]
        and "stocks" in data["stocks"]["crypto_stocks"]
    ):
        for stock in data["stocks"]["crypto_stocks"]["stocks"]:
            if "keywords" in stock:
                keywords.update(stock["keywords"])

    return keywords
