"""I/O helpers for CzRM dataset: CSV load and Excel export placeholders."""
from typing import Any
import pandas as pd


def load_csv(path: str, **kwargs) -> pd.DataFrame:
    """Load a CSV file into a DataFrame. Real parsing (encoding, columns) to be implemented."""
    return pd.read_csv(path, **kwargs)


def save_to_excel(df: pd.DataFrame, path: str, **kwargs) -> None:
    """Save DataFrame to Excel using openpyxl engine by default."""
    df.to_excel(path, engine=kwargs.pop('engine','openpyxl'), index=False, **kwargs)
