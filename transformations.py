import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

    def term_string_to_int_months(df):
        df.term = df.term.astype("str")
        df["term"] = df["term"].str.extract("(\d+)")
        df["term"] = pd.to_numeric(df["term"])

    def explore_nulls(df):
        nulls = pd.DataFrame(df.isnull().sum()).reset_index()
        nulls.columns = ["column", "null_count"]
        return nulls


class Plotter:
    def nulls_by_feature(nulls):
        nulls = nulls[nulls["null_count"] > 0]
        sns.barplot(x="null_count", y="column", data=nulls)
        plt.title("Top 10 Columns by Null Count")
        plt.xlabel("Count of Null Values")
        plt.ylabel("Columns")
        plt.show()


def percentage_nulls_by_feature(nulls):
    sns.set_palette("viridis")

    # Filter out columns with no nulls and sort by null_count
    nulls = nulls[nulls["null_count"] > 0].sort_values("null_count", ascending=False)

    # Calculate the percentage of nulls
    nulls["percentage"] = (nulls["null_count"] / 54231) * 100

    # Plotting using the calculated percentages
    ax = sns.barplot(x="percentage", y="column", data=nulls)

    plt.title("Top Columns by Null Count as Percentage")
    plt.xlabel("Percentage of Null Values")
    plt.ylabel("Columns")

    # Adding annotations
    for p in ax.patches:
        width = p.get_width()  # get bar length
        plt.text(
            width + 0.3,  # set the text at 0.3 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + half of the bar height
            "{:1.2f}%".format(width),  # format the value as a percentage
            ha="left",  # horizontal alignment
            va="center",
        )

    plt.show()
