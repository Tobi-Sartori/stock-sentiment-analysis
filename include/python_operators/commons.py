import yaml
import logging

def extract_keywords(yaml_file):

    logging.info("Extracting keywords from %s", yaml_file)
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    keywords = set()

    if "us_stocks" in data.get("stocks", {}) and "stocks" in data["stocks"]["us_stocks"]:
        for stock in data["stocks"]["us_stocks"].get("stocks", []):
            keywords.update(stock.get("keywords", []))
            logging.info("Keywords extracted: %s", keywords)

    if "crypto_stocks" in data.get("stocks", {}) and "stocks" in data["stocks"]["crypto_stocks"]:
        for stock in data["stocks"]["crypto_stocks"].get("stocks", []):
            keywords.update(stock.get("keywords", []))
            logging.info("Keywords extracted: %s", keywords)


    return sorted(keywords) 
