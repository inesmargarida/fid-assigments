"""Module for processing data relative to the life expectancy in Europe"""
from pathlib import Path


PROJECT_DIR = Path(__file__).parent
RAW_DATA_PATH = PROJECT_DIR.joinpath("data/eu_life_expectancy_raw.tsv")
SAVE_PATH = PROJECT_DIR.joinpath("data/pt_life_expectancy.csv")
