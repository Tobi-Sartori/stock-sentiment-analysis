from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
import logging


from include.python_operators.commons import (extract_keywords)
from include.python_operators.news.proccess_news import (
    s3_to_landing_postgress
)


default_args = {
    "id": "process_news",
    "owner": "Tobias Sartori",
    "start_date": days_ago(1),
    "depends_on_past": True,
    "retries": 1,
    "max_active_runs": 1,
}

with DAG(
    "process_news",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    start_task = DummyOperator(task_id="start_task")

    get_all_today_news = PythonOperator(
        task_id="get_all_today_news",
        python_callable=s3_to_landing_postgress,
    )


    create_landing_table = SQLExecuteQueryOperator(
        task_id="create_landing_table",
        conn_id="capstone_db",
        sql="""
            DROP TABLE IF EXISTS landing_news_{{ ds_nodash }};
            
            CREATE TABLE landing_news_{{ ds_nodash }} (
                title VARCHAR(255),
                author VARCHAR(255),
                press_vehicle VARCHAR(255),
                keyword VARCHAR(255),
                content TEXT,
                s3_url VARCHAR(255),
                dt_published_at TIMESTAMP
            );
        """,
    )


    end_task = DummyOperator(task_id="end_task")


    start_task >> create_landing_table >> end_task
