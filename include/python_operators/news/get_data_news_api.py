from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
from airflow.models import Variable
import psycopg2
from psycopg2 import OperationalError

class TestPostgresConnectionOperator(BaseOperator):
    """
    Airflow operator to test connection to a PostgreSQL database using secrets from Airflow Variables.
    """
    
    @apply_defaults
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = Variable.get("POSTGRES_HOST")
        self.database = Variable.get("POSTGRES_DB")
        self.user = Variable.get("POSTGRES_USER")
        self.password = Variable.get("POSTGRES_PASSWORD")
        self.port = Variable.get("POSTGRES_PORT", default_var=5432)

    def execute(self, context):
        try:
            conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            conn.close()
            self.log.info("Connection to PostgreSQL successful!")
        except OperationalError as e:
            self.log.error(f"Failed to connect to PostgreSQL: {e}")
            raise AirflowException(f"PostgreSQL connection failed: {e}")



def get_data_news_api():
    print("Populating the news API")
    print("this is a test")
    a = "Hello World"



