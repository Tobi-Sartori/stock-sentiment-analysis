import json
import logging

import boto3
import requests
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from psycopg2 import OperationalError
from bs4 import BeautifulSoup
import requests

from include.python_operators.commons import extract_keywords


def get_news_data_to_s3(keyword, ds):
    logging.info("Getting data from the news API for keyword: %s", keyword)

    news_data = request_news_api(keyword, ds)

    path = f"news/{ds}/{keyword}.json"
    logging.info("Data saved to the S3 bucket for path: %s", path)


def load_s3_data_to_postgres(keyword, ds):
    logging.info(
        "Loading data from the S3 bucket to the Postgres database for keyword: %s",
        keyword,
    )

    # Load the data from the S3 bucket
    # Save the data to the Postgres database


def request_news_api(keyword):
    logging.info("Requesting news API for keyword: %s", keyword)

    url = f"https://newsapi.org/v2/everything?q={keyword}&from={ds}&to={ds}&sortBy=popularity&apiKey={settings.NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()

def scrap_url_content(url):
    logging.info("Scraping content from URL: %s", url)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    text_content = "\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])

    return text_content


def news_api_dq_check(keyword):
    logging.info("Checking data quality for keyword: %s", keyword)

    return news_data

