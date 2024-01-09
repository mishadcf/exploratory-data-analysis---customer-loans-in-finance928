import yaml
import pandas as pd
import sqlalchemy
import seaborn as sns


class RDSDatabaseConnector:
    def get_creds(self):
        with open("credentials.yaml", "r") as file:
            result = dict(yaml.safe_load(file))
            return result

    def __init__(self):
        creds = self.get_creds()
        creds_string = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        self.engine = sqlalchemy.create_engine(creds_string)

    def execute_query(self, query):
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return result.fetchall()

    def extract_data(self):
        result = pd.DataFrame(self.execute_query("SELECT * FROM loan_payments"))
        return result

    def save_extracted_data(self):
        data = self.extract_data()
        data.to_csv("loan_data.csv")


class Plotter:
    def __init__(self, dataframe):
        self.df = dataframe

    def plots(self):
        return sns.histplot(self.dataframe)


class DataInfo:
    def __init__(self, dataframe, info=None):
        self.df = dataframe
        self.info = info

    def null_checker(self, column):
        return f"Percentage of nulls in column {column} is {self.dataframe[column].isnull().sum()/ 54123 * 100.0}"
