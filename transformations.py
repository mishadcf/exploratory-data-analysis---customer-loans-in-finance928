# The `Transforms` class provides methods for cleaning and transforming data in a loan payments
# DataFrame, while the `Plotter` class offers visualization capabilities for exploring data
# distributions and null values.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Transforms:
    """Utility class for cleaning and transforming data in loan payments DataFrame for exploratory data analysis."""

    @staticmethod
    def cols_to_numeric(cols, df):
        """Convert specified columns to numeric data type."""
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                raise ValueError(f"Column {col} does not exist in DataFrame")

    @staticmethod
    def cols_to_datetime(cols, df):
        """Convert specified columns to datetime data type."""
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', format='mixed')
            else:
                raise ValueError(f"Column {col} does not exist in DataFrame")

    @staticmethod
    def cols_to_category(cols, df):
        """Convert specified columns to category data type."""
        for col in cols:
            if col in df.columns:
                df[col] = df[col].astype("category")
            else:
                raise ValueError(f"Column {col} does not exist in DataFrame")

  

    @staticmethod
    def explore_nulls(df):
        """Return a DataFrame with counts of null values in each column."""
        nulls = pd.DataFrame(df.isnull().sum()).reset_index()
        nulls.columns = ["column", "null_count"]
        nulls["percentage"] = (nulls.null_count / 54321) * 100.0
        return nulls
    
    @staticmethod
    def drop_cols_with_morethanhalf_nulls(df):
        half_count = len(df) / 2
        return df.dropna(thresh=half_count, axis=1)
    
    @staticmethod
    def numeric_null_fill_with_median(df):
    # Fill numeric columns with the median
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(df[col].median())
    
    @staticmethod
    def categoric_null_fill_with_mode(df):
        
    # Fill categorical columns with the mode
        for col in df.select_dtypes(include=['object', 'category']).columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    @staticmethod
    def term_string_to_digit(cols, df):
        """Extract numeric term from string and convert to integer."""
        for col in cols:
            if col not in df.columns:
                raise ValueError(f"Column {col} does not exist in DataFrame")
            df[col] = pd.to_numeric(df[col].str.extract("(\d+)", expand=False))
    
    @staticmethod
    def clean_outliers_by_IQR(col,df):
       upper_bound =  df[col].median() + 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))
       return df[df[col] <= upper_bound]
    
    
   
class Plotter:
    
    def __init__(self, dataframe):
        """
        Initializes the Plotter with a dataframe.
        :param dataframe: A pandas DataFrame containing the data to plot.
        """
        self.dataframe = dataframe

    @staticmethod    
        
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
        
      
    def plot_skewness(self, columns =None):
        """
        Plots histograms of the specified columns to visualize skewness.
        :param columns: A list of column names from the dataframe whose distributions are to be plotted.
        """
        # Check if columns list is empty
        if columns is None:
            columns = self.dataframe.columns.tolist() # Default to all columns if none specified
            
           # Check if columns list is empty
        if not columns:
            print("No columns provided for plotting.")
            return
    
        
        # Number of rows and columns for subplots
        n_rows = len(columns) // 2 + len(columns) % 2
        n_cols = 2

        # Setting up the plot dimensions
        plt.figure(figsize=(n_cols * 5, n_rows * 4))

        for index, column in enumerate(columns, 1):
            plt.subplot(n_rows, n_cols, index)
            # Check if column exists in the dataframe
            if column in self.dataframe.columns:
                # Plotting the histogram
                self.dataframe[column].hist(bins=30)
                plt.title(f'Histogram of {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')
            else:
                print(f"Column '{column}' not found in the dataframe.")

        plt.tight_layout()
        plt.show()
        
    def plot_outliers(self):
        # Selecting numeric columns only
        numeric_cols = self.dataframe.select_dtypes(include=['number']).columns.tolist()
        
        # Number of rows and columns for subplots
        n_cols = 3
        n_rows = len(numeric_cols) // n_cols + (len(numeric_cols) % n_cols > 0)
        
        # Set up the matplotlib figure
        plt.figure(figsize=(n_cols * 6, n_rows * 4))
        
        for index, column in enumerate(numeric_cols, 1):
            plt.subplot(n_rows, n_cols, index)
            sns.boxplot(y=self.dataframe[column])
            plt.title(f'Box Plot of {column}')
            plt.xlabel(column)
        
        plt.tight_layout()
        plt.show()
            
            


