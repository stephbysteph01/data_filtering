"""Command line entry point for the CzRM analysis workflow."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .analysis import compare_open_closed, plot_results, summarize
from .io import export_report, load_data
from .preprocess import clean_data


def main(data_dir: str = 'data', output_dir: str = 'data/processed') -> dict:
    """Run the default analysis flow on raw CSV files in the data directory."""
    open_df = clean_data(load_data(data_dir, 'open'), dataset_type='open')
    closed_df = clean_data(load_data(data_dir, 'closed'), dataset_type='closed')

    comparison = compare_open_closed(
        open_df,
        closed_df,
        field='Case_Theme_Area__c',
        open_date_col='CreatedDate__c',
        closed_date_col='ClosedDate__c',
    )

    comparison_path = Path(output_dir)
    comparison_path.mkdir(parents=True, exist_ok=True)
    chart_paths = plot_results(comparison, comparison_path / 'charts', field_name='Case_Theme_Area__c')
    export_report(
        {
            'summary_open': pd.DataFrame([summarize(open_df)]),
            'summary_closed': pd.DataFrame([summarize(closed_df)]),
            'comparison': comparison,
        },
        comparison_path / 'czrm_report.xlsx',
    )

    report = {
        'summary_open': summarize(open_df),
        'summary_closed': summarize(closed_df),
        'comparison': comparison,
        'charts': [str(p) for p in chart_paths],
        'excel_report': str(comparison_path / 'czrm_report.xlsx'),
    }
    print(report)
    return report


if __name__ == '__main__':
    main()