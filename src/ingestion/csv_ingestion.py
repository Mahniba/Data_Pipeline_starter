"""
csv_ingestion.py

Purpose:
    Load the raw procurement CSV file into a Pandas DataFrame.

This module is responsible ONLY for ingestion.

It does NOT:
    - clean the data
    - remove duplicates
    - fix missing values
    - validate business rules
    - transform the data
"""



# 1. IMPORT LIBRARIES

# Path helps us work with file and folder locations safely.
# It is better than manually building Windows paths such as:
# C:\\Users\\Marieta\\Documents\\...
# Path works across different operating systems.
from pathlib import Path

# Pandas is the library we will use to read the CSV file.
# When Pandas reads the CSV, it converts the table into a
# DataFrame.
import pandas as pd

# 2. FIND THE PROJECT ROOT

# __file__ refers to this file:
# src/ingestion/csv_ingestion.py
# We then move upward three levels:
# 1. ingestion/
# 2. src/
# 3. data-pipeline-starter/
# This gives us the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# 3. DEFINE THE RAW CSV LOCATION
# Our Phase 2 dataset is located at:
# data/sample/procurement_raw_sample.csv
# We construct this path starting from the project root.
DEFAULT_CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "procurement_raw_sample.csv"
)

# 4. CREATE THE INGESTION FUNCTION
def load_csv(file_path: Path = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """
    Load a CSV file into a Pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        Location of the CSV file.

    Returns
    -------
    pd.DataFrame
        The raw procurement data.
    """
    # Check whether the CSV exists.
    # Before asking Pandas to read the file, we check that
    # the file actually exists.
    # This allows us to give a clear error message if the
    # source file cannot be found.
    if not file_path.exists():

        raise FileNotFoundError(
            f"Input file was not found: {file_path}"
        )

    # Read the CSV.
    # Pandas reads the CSV and creates a DataFrame.
    # IMPORTANT:
    # We are NOT cleaning anything here.
    # If the raw data contains:
    #     North West
    # we keep it as:
    #     North West
    # If organization is missing, we keep it missing.
    # If there are duplicates, we keep them.
    # Cleaning happens later.
    dataframe = pd.read_csv(file_path)


    # Return the DataFrame.
    return dataframe

# 5. TEST THE INGESTION WHEN RUN DIRECTLY

# This condition is true when we execute this file directly:
# python src/ingestion/csv_ingestion.py
# It prevents this test section from automatically running when
# another Python file imports load_csv().
if __name__ == "__main__":

    # Call our ingestion function.
    df = load_csv()
    # Display a summary.
    print("=" * 60)

    print("DATA INGESTION SUCCESSFUL")

    print("=" * 60)

    # Show the source file.
    print(f"Source file: {DEFAULT_CSV_PATH}")
    # Show number of rows.
    print(f"Rows: {df.shape[0]}")
    # Show number of columns.
    print(f"Columns: {df.shape[1]}")
    # Display column names.
    print("\nColumns:")

    for column in df.columns:

        print(f"  - {column}")


    print("=" * 60)