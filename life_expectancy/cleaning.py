"""cleaning"""
import argparse
import pathlib
import pandas as pd


PROJECT_DIR = pathlib.Path(__file__).parent
RAW_DATA_PATH = PROJECT_DIR.joinpath("data/eu_life_expectancy_raw.tsv")
SAVE_PATH = PROJECT_DIR.joinpath("data/pt_life_expectancy.csv")


def clean_data(region_filter="PT"):
    """clean data"""
    # Loads the eu_life_expectancy_raw.tsv data from the data folder.
    df_raw_data = pd.read_csv(RAW_DATA_PATH, sep="[,\t]", engine="python")

    # Unpivots the date to long format, so that we have the following columns: unit, sex, age, region, year, value.
    df_un_pivot_dates = pd.melt(
        df_raw_data,
        id_vars=["unit", "sex", "age", "geo\\time"],
        var_name="year",
        value_name="value",
    )

    df_un_pivot_dates.rename(columns={"geo\\time": "region"}, inplace=True)

    # Ensures year is an int (with the appropriate data cleaning if required)
    df_un_pivot_dates = df_un_pivot_dates.astype({"year": "int"})

    # Ensures value is a float (with the appropriate data cleaning if required, and do remove the NaNs).
    df_un_pivot_dates["value"] = df_un_pivot_dates["value"].str.extract(
        r"(\d*\.?\d*)", expand=False
    )
    df_un_pivot_dates["value"] = df_un_pivot_dates["value"].apply(
        pd.to_numeric, errors="coerce"
    )
    df_un_pivot_dates = df_un_pivot_dates.astype({"value": "float"})
    df_cleaned = df_un_pivot_dates.dropna()

    # Filters only the data where region equal to PT (Portugal).
    df_filtered_region = df_cleaned[df_cleaned["region"] == region_filter]

    # Save the resulting data frame to the data folder as pt_life_expectancy.csv.
    # Ensure that no numerical index is saved.
    df_filtered_region.to_csv(SAVE_PATH, index=False)

    return df_filtered_region


if __name__ == "__main__":  # pragma: no cover

    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="Insert region to filter data.")
    args = parser.parse_args()
    clean_data(args.region)
