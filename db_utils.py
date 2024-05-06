# The `RDSDatabaseConnector` class handles data retrieval 
import yaml
import pandas as pd
import sqlalchemy
import seaborn as sns
from sqlalchemy import text




class RDSDatabaseConnector:
    
    def get_creds(self):
        """
        The function `get_creds` reads and returns the contents of a YAML file named "credentials.yaml".
        :return: A dictionary containing the credentials loaded from the "credentials.yaml" file.
        """
        with open("credentials.yaml", "r") as file:
            result = dict(yaml.safe_load(file))
            return result

    
        """
        The function initializes a SQLAlchemy engine using credentials fetched from a method.
        """
    def __init__(self):
        creds = self.get_creds()
        creds_string = f"postgresql://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}"
        self.engine = sqlalchemy.create_engine(creds_string)

    def execute_query(self, query):
        """
        The function `execute_query` executes a SQL query using the provided engine and returns the
        fetched results.
        
        :param query: The `execute_query` method takes a SQL query as input and executes it using the
        `engine` attribute of the class instance. The method connects to the database using the engine,
        executes the query, and returns the fetched results as a list of rows
        :return: The `execute_query` method returns the result of the query execution in the form of a
        list of rows fetched from the database.
        """
        with self.engine.connect() as conn:
            statement = text(query)
            result = conn.execute(statement)
            return result.fetchall()

    def extract_data(self):
        """
        The `extract_data` function retrieves all data from the "loan_payments" table and returns it as
        a pandas DataFrame.
        :return: A DataFrame containing all the data from the "loan_payments" table is being returned.
        """
        result = pd.DataFrame(self.execute_query("SELECT * FROM loan_payments"))
        return result

    """
    The function `save_extracted_data` extracts data and saves it to a CSV file named "loan_data.csv".
    """
    def save_extracted_data(self):
        data = self.extract_data()
        data.to_csv("loan_data.csv")




