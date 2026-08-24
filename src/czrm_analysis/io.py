"""I/O helpers for CzRM dataset: CSV load and Excel export."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .core import resolve_data_dir


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load a CSV file into a DataFrame using a robust default encoding."""
    encodings = kwargs.pop('encodings', ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1'])
    sep = kwargs.pop('sep', ';')
    last_error = None
    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding, sep=sep, low_memory=False, **kwargs)
        except UnicodeDecodeError as exc:
            last_error = exc
        except Exception:
            # Fallback to other encodings for files with non-standard metadata.
            continue
    if last_error is not None:
        raise last_error
    return pd.read_csv(path, sep=sep, low_memory=False, **kwargs)


def load_data(data_dir: str | Path, dataset_type: str = 'open') -> pd.DataFrame:
    """Load all CSV files related to the requested CzRM dataset subset."""
    base_dir = resolve_data_dir(data_dir)
    dataset_type = dataset_type.lower()

    if dataset_type in {'open', 'aperto', 'aperti'}:
        keywords = ('open', 'aperto', 'aperti')
    elif dataset_type in {'closed', 'chiuso', 'chiusi'}:
        keywords = ('closed', 'chiuso', 'chiusi')
    else:
        raise ValueError("dataset_type must be 'open' or 'closed'")

    csv_files = sorted(base_dir.glob('*.csv'))
    matches = []
    for file in csv_files:
        name = file.name.lower()
        if any(keyword in name for keyword in keywords):
            matches.append(file)

    if not matches:
        matches = csv_files
    if not matches:
        raise FileNotFoundError(f'No CSV files found in {base_dir}')

    frames = [load_csv(path) for path in matches]
    combined = pd.concat(frames, ignore_index=True)
    return combined


def save_to_excel(df: pd.DataFrame, path: str | Path, **kwargs) -> None:
    """Save a DataFrame to Excel using the openpyxl engine by default."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out_path, engine=kwargs.pop('engine', 'openpyxl'), index=False, **kwargs)


def export_report(report_tables: dict[str, pd.DataFrame], output_path: str | Path) -> None:
    """Export multiple report tables to an Excel workbook."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name, df in report_tables.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)


__all__ = ['load_csv', 'load_data', 'save_to_excel', 'export_report']