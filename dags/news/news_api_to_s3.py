from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
import logging


from include.python_operators.commons import (extract_keywords)


from include.python_operators.news.news_api_to_s3 import (
    get_news_data_to_s3,
    scrap_url_content_save_s3,
)

default_args = {
    "id": "news_api_to_s3",
    "owner": "Tobias Sartori",
    "start_date": days_ago(1),
    "depends_on_past": True,
    "retries": 1,
    "max_active_runs": 1,
}

with DAG(
    "news_api_to_s3",
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

    ## TODO: This is executed when the DAG is parsed, not when the DAG actually runs, which can cause unexpected behavior.
    keywords = extract_keywords("config_yamls/stocks.yaml")

    with TaskGroup("news_keyword_extract_load") as news_keyword_extract_load:
        for keyword in keywords:
            keyword_naming = keyword.replace(" ", "_")
            get_news_task = PythonOperator( ## Get news data from news api, save json to s3
                task_id=f"get_news_{keyword_naming}",
                python_callable=get_news_data_to_s3,
                op_kwargs={'keyword': keyword, 'yesterday': '{{ macros.ds_add(ds, -1) }}'},
            )
            
            scrap_url_content_saveS3_task = PythonOperator( ## Read json from s3, Scrap url content from s3, save to s3
                task_id=f"scrap_url_content_save_s3_{keyword_naming}",
                python_callable=scrap_url_content_save_s3,
                op_kwargs={'keyword': keyword, 'yesterday': '{{ macros.ds_add(ds, -1) }}'}
            )

            get_news_task >> scrap_url_content_saveS3_task

    end_task = DummyOperator(task_id="end_task")

    start_task >> extract_keywords_task >> news_keyword_extract_load >> end_task



## TODO: This is the right way to do it

"""    with TaskGroup("test_ops") as test_ops:

        load_data_to_landing_table = PythonOperator.partial(
            task_id="get_news",
            python_callable=s3_to_landing_postgress,
        ).expand_kwargs(
            extract_keywords_task.output.map(lambda keyword: {
                "op_args": [keyword, '{{ macros.ds_add(ds, -1) }}'],
                "task_id": f"get_news_{keyword.replace(' ', '_')}",
            })
        )


        load_data_to_landing_table
"""