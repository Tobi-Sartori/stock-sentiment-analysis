import os

from airflow.decorators import dag
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import datetime, timedelta

from include.python_operators.news.news_api_to_s3 import (
    TestPostgresConnectionOperator, get_data_news_api)


@dag(
    description="This dag gets data Polygon API",
    default_args={
        "id": "process_news",
        "owner": "Tobias Sartori",
        "start_date": datetime(2025, 1, 9),
        "retries": 0,
        "execution_timeout": timedelta(hours=1),
        "depends_on_past": False,
        "max_active_runs": 1,
    },
    start_date=datetime(2025, 2, 10),
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=True,
    tags=["news"],
)
def _get_data_news_api():

    get_data_from_news_api = PythonOperator(
        task_id="populate_news_api",
        python_callable=get_data_news_api,
    )

    get_data_from_news_api


_get_data_news_api()
