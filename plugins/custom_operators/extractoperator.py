from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

class ExtractOperator(BaseOperator):
    def __init__(self, conn_id, sql, output_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.sql = sql
        self.output_path = output_path

    def execute(self, context):
        pg_hook = PostgresHook(postgres_conn_id=self.conn_id)
        df = pg_hook.get_pandas_df(sql=self.sql)
        df.to_parquet(self.output_path, index=False)
