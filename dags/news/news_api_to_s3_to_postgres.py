from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup


from include.python_operators.commons import (extract_keywords,
                                              get_news_data_to_s3,
                                              load_s3_data_to_postgres,
                                              scrap_url_content)

default_args = {
    "id": "news_api_to_s3_to_postgres",
    "owner": "Tobias Sartori",
    "start_date": days_ago(1),
    "depends_on_past": True,
    "retries": 1,
    "max_active_runs": 1,
}

with DAG(
    "news_api_to_s3_to_postgres",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    start_task = DummyOperator(task_id="start_task")

    extract_keywords_task = PythonOperator(
        task_id="extract_keywords",
        python_callable=extract_keywords,
        op_args=["config_yamls/stocks.yaml"],
    )

    keywords = extract_keywords("config_yamls/stocks.yaml")

    with TaskGroup("news_keyword_extract_load") as news_keyword_extract_load:
        for keyword in keywords:
            keyword_naming = keyword.replace(" ", "_")

            get_news_task = PythonOperator(
                task_id=f"get_news_{keyword_naming}",
                python_callable=get_news_data_to_s3,
                op_args=[keyword],
            )

            scrap_url_content_task = PythonOperator(
                task_id=f"scrap_url_content_{keyword_naming}",
                python_callable=scrap_url_content,
                op_args=[keyword],
            )

            load_s3_task = PythonOperator(
                task_id=f"load_s3_{keyword_naming}",
                python_callable=load_s3_data_to_postgres,
                op_args=[keyword],
            )

            get_news_task >> load_s3_task

    end_task = DummyOperator(task_id="end_task")

    start_task >> extract_keywords_task >> news_keyword_extract_load >> end_task
