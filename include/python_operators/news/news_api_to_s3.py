import json
import logging

import requests
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from psycopg2 import OperationalError
from bs4 import BeautifulSoup
import requests

from include.python_operators.commons import extract_keywords

from settings.settings import s3ClientHelper

s3_client_helper = s3ClientHelper()

NEWS_API_KEY = Variable.get("NEWS_API_KEY")

def get_news_data_to_s3(keyword, yesterday, **kwargs):
    logging.info(f"Starting URL scraping for keyword: {keyword}, Execution Date (yesterday): {yesterday}"),
    
    news_data = request_news_api(keyword, yesterday)
    path = f"news/{yesterday}/{keyword}.json"

    s3_client_helper.save_file_to_s3(
        file=json.dumps(news_data),
        file_path=path
        )

    logging.info("Data saved to the S3 bucket for path: %s", path)



def request_news_api(keyword, yesterday):
    logging.info("Requesting news API for keyword: %s", keyword)

    logging.info(f"NEWS_API_KEY: {NEWS_API_KEY}")

    url = f"https://newsapi.org/v2/everything?q={keyword}&from={yesterday}&to={yesterday}&sortBy=popularity&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_text_content_from_url(url):
    logging.info("Scraping content from URL: %s", url)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    text_content = "\n ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])

    return text_content


def scrap_url_content_save_s3(keyword, yesterday, **kwargs):
    logging.info(f"Starting URL scraping for keyword: {keyword}, Execution Date (yesterday): {yesterday}")
    path = f"news/{yesterday}/{keyword}.json"
    response = s3_client_helper.get_file_from_s3(path)

    if response:
        logging.info("File found in S3 bucket for path: %s", path)
        data = json.loads(response['Body'].read().decode('utf-8'))
    else:
        logging.info("File not found in S3 bucket for path: %s", path)
        return None
        
    for article in data[:3]:
            logging.info("Scraping text content from URL: %s", article['url'])
            logging.info("Article: %s", article["title"])
            url = article['url']
            url_text_content = get_text_content_from_url(url)
            article["extracted_text_content"] = url_text_content
            s3_client_helper.save_file_to_s3(
                file=json.dumps(article),
                file_path=path
            )

        