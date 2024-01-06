if __name__ == "__main__":
    import yaml
    import pandas as pd
    import sqlalchemy

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

    # # Usage
    # db_connector = RDSDatabaseConnector()
    # rows = db_connector.execute_query("SELECT * FROM loan_payments")
    # for row in rows:
    #     print(row)
