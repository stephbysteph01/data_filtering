"""Shared utilities for czrm_analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def resolve_data_dir(data_dir: str | Path) -> Path:
    """Return a validated data directory path."""
    path = Path(data_dir)
    if not path.exists():
        raise FileNotFoundError(f"Data directory does not exist: {path}")
    return path


def ensure_columns(df, required_columns: Iterable[str]) -> None:
    """Check that required columns are present; raise a clear error if missing."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")


def ensure_column(df, col, default=None):
    """Ensure a DataFrame-like object has a column."""
    try:
        if col not in df.columns:
            df[col] = default
    except Exception:
        pass
    return df