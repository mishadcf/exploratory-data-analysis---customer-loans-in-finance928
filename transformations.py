import pandas as pd


class Transforms:
    """General utility functions for cleaning loan payments DataFrame to enable exploratory data analysis"""

    def cols_to_numeric(cols, df):
        for col in cols:
            df[col] = pd.to_numeric(df[col])

    def cols_to_datetime(cols, df):
        for col in cols:
            df[col] = pd.to_datetime(df[col])

    def cols_to_category(cols, df):
        for col in cols:
            df[col] = df[col].astype("category")
