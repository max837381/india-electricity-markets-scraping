import pandas as pd
import sys
import pandas as pd
import bs4 as bs
from urllib import request
import re
import os
import urllib
from tabula.io import read_pdf
import tabula.io as tabula
import statistics as stat
from math import isnan
from itertools import filterfalse
import numpy as np
import dateparser

# Specify the input and output file paths
input_file_path = '/Users/max/Documents/UCSC/M.S. Applied Economics and Finance/Spring 2023/Income Dynamics Lab - India Electricity/PDFFeeder2018.pdf'
output_file_path = '/Users/max/Documents/UCSC/M.S. Applied Economics and Finance/Spring 2023/Income Dynamics Lab - India Electricity/test.csv'



# Read the PDF file and extract the tables
tables = tabula.read_pdf(input_file_path, pages='all', multiple_tables=True)

# Define a function to calculate summary statistics for each column, excluding the first column
def calculate_summary_statistics(df):
    # Filter out non-numeric rows and exclude the first column
    numeric_df = df.iloc[:,1:].apply(pd.to_numeric, errors='coerce').dropna(how='all')

    # Calculate the summary statistics for each numeric column
    summary_statistics = pd.concat([numeric_df.max(), numeric_df.min(), round(numeric_df.mean(), 4)], axis=1)
    summary_statistics.columns = ['pandas max', 'pandas min', 'pandas average']
    # Transpose the summary statistics to display horizontally
    summary_statistics = summary_statistics.T

    return summary_statistics


# Define a function to export a table and its summary statistics to a CSV file
def export_table(df, file):
    # Export the table to the CSV file
    df.to_csv(file, index=False)
    # Calculate summary statistics for each column, excluding the first column
    summary_statistics = calculate_summary_statistics(df)
    # Export the summary statistics to the CSV file
    summary_statistics.to_csv(file, mode='a', index=True, header=True)
    # Add a blank row between tables
    file.write('\n\n')

# Initialize variables
total_rows = 0
total_columns = 0
max_rows = 0
max_columns = 0
min_rows = 0
min_columns = 0
num_empty_tables = 0

# Export each table and its summary statistics to the CSV file
with open(output_file_path, 'w') as f:
    for table in tables:
        # Calculate the dimensions of the table
        num_rows, num_columns = table.shape
        # Update variables for dimensions
        total_rows += num_rows
        total_columns += num_columns
        if num_rows > max_rows:
            max_rows = num_rows
        if num_columns > max_columns:
            max_columns = num_columns
        if min_rows == 0 or num_rows < min_rows:
            min_rows = num_rows
        if min_columns == 0 or num_columns < min_columns:
            min_columns = num_columns
        # Check if table is empty
        if num_rows == 0 or num_columns == 0:
            num_empty_tables += 1
            continue
        # Export the table and its summary statistics to the CSV file
        export_table(table, f)
        # Extract the dates from the column names
        #dates = extract_dates(table)
        # Print the dates to the user
        #print(f"Dates extracted from table {tables.index(table)}: {dates}")

    # Calculate the average dimensions of tables
    num_tables = len(tables) - num_empty_tables
    avg_rows = total_rows / num_tables
    avg_columns = total_columns / num_tables

    # Print summary statistics to the user
    print(f"Average number of rows: {avg_rows:.2f}")
    print(f"Average number of columns: {avg_columns:.2f}")
    print(f"Max rows: {max_rows}")
    print(f"Max columns: {max_columns}")
    print(f"Min rows: {min_rows}")
    print(f"Min columns: {min_columns}")
    print(f"Number of tables with 0 rows: {num_empty_tables}")
    print(f"Number of tables with 0 columns: {num_empty_tables}")




def extract_dates(df):
    date_cols = []
    for col in df.columns:
        date_str = col.split()[0]  # Extract the first word as the potential date string
        date = dateparser.parse(date_str)
        if date:
            date_cols.append(col)
            print(f"Found date {date} in column {col}")
    return date_cols


from datetime import datetime


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%b-%y")
    except ValueError:
        return None


def parse_and_combine_tables(tables):
    parsed_tables = []

    for table in tables:
        # Parse the date strings in the column names
        parsed_table = table.copy()
        parsed_table.columns = [parse_date(col.split()[0]) if parse_date(col.split()[0]) else col for col in
                                table.columns]

        # Append the parsed table to the list of parsed tables
        parsed_tables.append(parsed_table)

    # Combine the parsed tables based on the date
    combined_table = pd.concat(parsed_tables, axis=1)

    return combined_table


combined_table = parse_and_combine_tables(tables)
with open(output_file_path, 'w') as f:
    for table in tables:
        # ...
        # Export the table and its summary statistics to the CSV file
        export_table(table, f)

combined_table.to_csv("datemerge.csv", index=False)


#export_table(combined_table, "datemerge.csv")
print(combined_table)







