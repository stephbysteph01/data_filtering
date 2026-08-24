"""CzRM analysis package for Roma Capitale reports."""

from .analysis import aggregate_by_field, compare_open_closed, export_report, plot_results, summarize
from .io import export_report as export_xlsx, load_data
from .preprocess import clean_data, clean_coordinates, normalize_dates

__version__ = '0.1.0'

__all__ = [
    'load_data',
    'clean_data',
    'clean_coordinates',
    'normalize_dates',
    'aggregate_by_field',
    'compare_open_closed',
    'summarize',
    'plot_results',
    'export_xlsx',
    'export_report',
]