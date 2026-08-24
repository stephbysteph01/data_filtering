"""Shared utilities for czrm_analysis."""


def ensure_column(df, col, default=None):
    """Ensure DataFrame-like object has a column; placeholder."""
    try:
        if col not in df.columns:
            df[col] = default
    except Exception:
        pass
    return df
