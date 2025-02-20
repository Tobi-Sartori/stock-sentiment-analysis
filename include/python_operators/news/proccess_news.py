from settings.settings import s3ClientHelper
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
import json

import boto3
import json
from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class S3JsonToPostgresOperator(BaseOperator):
    """
    Custom Airflow Operator to:
    1. List objects in an S3 path
    2. Stream JSON files directly from S3
    3. Parse JSON data
    4. Insert data into PostgreSQL
    """

    @apply_defaults
    def __init__(self, s3_prefix, table_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_bucket = "tobi-capstone-bucket"
        self.s3_path = s3_prefix
        self.postgres_conn_id = "capstone_db"
        self.table_name = table_name

    def list_s3_objects(self):
        """List all JSON objects in an S3 prefix"""
        s3_client = boto3.client("s3")
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []

        for page in paginator.paginate(Bucket=self.s3_bucket, Prefix=self.s3_prefix):
            if "Contents" in page:
                for obj in page["Contents"]:
                    if obj["Key"].endswith(".json"):  # Filter JSON files
                        objects.append(obj["Key"])

        if not objects:
            raise AirflowException(f"No JSON files found in s3://{self.s3_bucket}/{self.s3_prefix}")

        return objects

    def stream_json_from_s3(self, s3_key):
        """Stream JSON data directly from S3 without downloading"""
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=self.s3_bucket, Key=s3_key)
        json_data = json.loads(response["Body"].read().decode("utf-8"))  # Convert JSON to Python dict
        return json_data

    def insert_into_postgres(self, json_data):
        """Insert parsed JSON into PostgreSQL"""
        if isinstance(json_data, dict):  
            json_data = [json_data]  # Convert single object to list

        pg_hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        connection = pg_hook.get_conn()
        cursor = connection.cursor()

        for record in json_data:
            keys = record.keys()
            values = tuple(record.values())

            insert_query = f"""
            INSERT INTO {self.table_name}
            (
                title, 
                author, 
                press_vehicle, 
                keyword, 
                content, 
                s3_url, 
                dt_published_at
            )
            VALUES (
                record['title'],
                record['author'],
                record['press_vehicle'],
                record['keyword'],
                record['content'],
                record['s3_url'],
                record['dt_published_at']
            )
            """
            cursor.execute(insert_query, values)

        connection.commit()
        cursor.close()
        connection.close()

    def execute(self, context):
        """Main execution logic"""
        self.log.info(f"Listing JSON files from s3://{self.s3_bucket}/{self.s3_prefix}")
        files = self.list_s3_objects()

        for s3_key in files:
            self.log.info(f"Streaming JSON file: {s3_key}")
            json_data = self.stream_json_from_s3(s3_key)

            self.log.info(f"Inserting JSON data into {self.table_name}")
            self.insert_into_postgres(json_data)

        self.log.info("Data successfully inserted into PostgreSQL!")


