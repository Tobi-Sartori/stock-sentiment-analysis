from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

# Define the DAG
with DAG(
    "master_dag",
    schedule_interval=None,
    start_date="0 5 * * *",
    catchup=True,
    depends_on_past=True,
    max_active_runs=1,
) as parent_dag:

    child_dag_ids = ["get_data_news_api", "get_data_stocks"]

    trigger_tasks_get_data = [
        TriggerDagRunOperator(
            task_id=f"trigger_{dag_id}",
            trigger_dag_id=dag_id,
            conf={"message": f"Triggered by parent {dag_id}"},
            wait_for_completion=True,
        )
        for dag_id in child_dag_ids
    ]

    child_dag_ids_process_data = ["process_data_news_api", "process_data_stocks"]
    process_data_task = [
        TriggerDagRunOperator(
            task_id=f"trigger_{dag_id}",
            trigger_dag_id=dag_id,
            conf={"message": f"Triggered by parent {dag_id}"},
            wait_for_completion=True,
        )
        for dag_id in child_dag_ids
    ]

    dummy_task = DummyOperator(
        task_id="dummy_task",
    )

    dummy_task
