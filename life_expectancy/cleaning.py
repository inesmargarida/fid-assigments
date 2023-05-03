"""Cleans data relative to the life expectancy in Europe grouped by 
Country (or other, like group of countries), Age, Sex, and Time."""

import argparse
import typing

import pandas as pd

from . import RAW_DATA_PATH, SAVE_PATH


# mafaldavs
def load_data(file_path: str) -> pd.DataFrame:
    """Loads raw data from a given CSV file."""
    return pd.read_csv(file_path, sep="[,\t]", engine="python")


def clean_data(df_unclean: pd.DataFrame, region_filter: str = "PT"):
    """Cleans data relative to the life expectancy in Europe."""

    # Change name of column 'geo\time' to 'region
    df_unclean.rename(columns={r"geo\time": "region"}, inplace=True)
    # Unpivots the date to long format, so that we have the following columns: unit, sex, age, region, year, value.
    df_unclean = _unpivot_dates(df_unclean)

    # Ensures year is an int
    df_cleaned_year = _clean_column(df_unclean, "year", int)
    # Ensures value is a float
    df_cleaned = _clean_column(df_cleaned_year, "value", float)

    # Filters only the data where region equal to 'region_filter'.
    return df_cleaned[df_cleaned["region"] == region_filter]


def save_data(df_data: pd.DataFrame, save_path: str):
    """Save the given pd.DataFrame to the specified CSV file."""

    # Ensure that no numerical index is saved.
    try:
        df_data.to_csv(save_path, index=False)
        return True
    except:
        return False


def _unpivot_dates(df_data: pd.DataFrame) -> pd.DataFrame:
    """Unpivots the dates to long format.
    Returns a pd.DataFrame with the following columns: unit, sex, age, region, year, value."""

    return pd.melt(
        df_data,
        id_vars=["unit", "sex", "age", "region"],
        var_name="year",
        value_name="value",
    )


def _clean_column(df_data: pd.DataFrame, name: str, dtype: typing.Type) -> pd.DataFrame:
    """Clean a column in a pd.DataFrame by converting it to a specified data type.

    Args:
        df_data (pd.DataFrame): The DataFrame containing the column to clean.
        name (str): The name of the column to clean.
        dtype (dtype): The data type to convert the column to.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with the specified column cleaned
        and converted to the specified data type."""

    # Try to convert to the specified dtype
    try:
        df_data = df_data.astype({name: dtype})

    # If not possible, do the appropriate data cleaning and remove the NaNs
    except ValueError:
        df_data[name] = df_data[name].str.extract(r"(\d*\.?\d*)", expand=False)
        df_data[name] = df_data[name].apply(pd.to_numeric, errors="coerce")
        df_data = df_data.dropna()
        df_data = df_data.astype({name: dtype})

    return df_data


def main(region_filter: str = "PT"):
    """Main function that orchestrates data cleaning and saving."""

    # Load data
    df_unclean = load_data(RAW_DATA_PATH)

    # Clean data
    df_clean = clean_data(df_unclean, region_filter)

    # Save data
    saved = save_data(df_clean, SAVE_PATH)

    if saved:
        print("Data has been cleaned and saved!")


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="Insert region to filter data.")
    args = parser.parse_args()

    main(args.region)
