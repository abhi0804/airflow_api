from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging

logger = logging.getLogger(__name__)

class PostgresOperatorTemplate(BaseOperator):
    @apply_defaults
    def __init__(self, postgres_conn_id, sql, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.sql = sql

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(self.sql)