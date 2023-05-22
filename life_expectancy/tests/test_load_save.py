"""Tests for the load_save module"""
import pandas as pd
from life_expectancy import load_save

def test_load_data_csv(monkeypatch) -> None:
    """Patch read_csv method, testing load_data function."""

    def _mockreturn_load_csv() -> str:
        """Result to receive when mock."""
        return "DataFrame loaded from csv file."

    monkeypatch.setattr(pd, "read_csv", _mockreturn_load_csv)

    assert load_save.load_data("fake_load_path") == "DataFrame loaded from csv file."


def test_save_data(monkeypatch) -> None:
    """Test the save_data function, Patch to_csv method"""

    def _mockreturn_save_csv() -> str:
        """Result to receive when mock."""
        return "DataFrame saved to csv file."

    monkeypatch.setattr(pd.DataFrame, "to_csv", _mockreturn_save_csv)

    assert load_save.save_data(pd.DataFrame(), "fake_save_path") is True
