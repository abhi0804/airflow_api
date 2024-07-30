from airflow.models import BaseOperator
import pandas as pd

class TransformOperator(BaseOperator):
    def __init__(self, input_path, output_path, transformations, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_path = input_path
        self.output_path = output_path
        self.transformations = transformations

    def execute(self, context):
        df = pd.read_parquet(self.input_path)
        for col, transform in self.transformations.items():
            if transform == 'str_to_int':
                df[col] = df[col].astype(int)
            elif transform == 'float_to_str':
                df[col] = df[col].astype(str)
        df.to_parquet(self.output_path, index=False)
