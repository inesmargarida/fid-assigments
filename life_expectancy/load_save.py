"""Module provides functions for laoding and saving data referent to Life Expectancy"""

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """Loads raw data from a given CSV file."""
    return pd.read_csv(file_path, sep="[,\t]", engine="python")


def save_data(df_data: pd.DataFrame, save_path: str):
    """Save the given pd.DataFrame to the specified CSV file."""

    # Ensure that no numerical index is saved.
    try:
        df_data.to_csv(save_path, index=False)
        return True
    except:
        return False
