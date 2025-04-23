from airflow.models import BaseOperator

class MarkCSVOperator(BaseOperator):
    def __init__(self, input_file:str, output_file:str, separator:str, column:int, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.output_file = output_file
        self.separator = separator
        self.column = column

    def execute(self, context):
        import csv
        with open(self.input_file, 'r') as f:
            for data in f.readlines():
                fields = data.strip('/n').split(self.separator)
                fields[self.column] = '***'
                data = self.separator.join(fields)
                with open(self.output_file, 'a') as f:
                    f.write(data)