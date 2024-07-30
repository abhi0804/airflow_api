from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

class LoadOperator(BaseOperator):
    def __init__(self, input_path, s3_bucket, s3_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_path = input_path
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

    def execute(self, context):
        s3_hook = S3Hook()
        s3_hook.load_file(filename=self.input_path, key=self.s3_key, bucket_name=self.s3_bucket, replace=True)
