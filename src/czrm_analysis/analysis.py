"""Analysis functions for CzRM reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from .core import ensure_columns

matplotlib.use('Agg')


def aggregate_by_field(df: pd.DataFrame, field: str, date_col: str | None = None, month_col: str = 'month') -> pd.DataFrame:
    """Aggregate rows by a categorical field, optionally by month."""
    ensure_columns(df, [field])
    grouped = df[[field]].copy()

    if date_col and date_col in df.columns:
        grouped['month'] = pd.to_datetime(df[date_col], errors='coerce').dt.to_period('M').astype(str)
    elif month_col in df.columns:
        grouped['month'] = df[month_col]
    else:
        grouped['month'] = 'TOTAL'

    summary = grouped.groupby([field, 'month'], dropna=False).size().reset_index(name='count')
    return summary.sort_values(['month', 'count'], ascending=[True, False]).reset_index(drop=True)


def compare_open_closed(open_df: pd.DataFrame, closed_df: pd.DataFrame, field: str, open_date_col: str, closed_date_col: str) -> pd.DataFrame:
    """Compare aggregated open vs closed counts for the same category and month."""
    open_df = open_df.copy()
    closed_df = closed_df.copy()

    if field not in open_df.columns:
        open_df[field] = 'N/D'
    if field not in closed_df.columns:
        fallback = 'Closed_Reason__c' if 'Closed_Reason__c' in closed_df.columns else 'N/D'
        closed_df[field] = closed_df[fallback]

    open_summary = aggregate_by_field(open_df, field, open_date_col)
    closed_summary = aggregate_by_field(closed_df, field, closed_date_col)
    open_summary = open_summary.rename(columns={'count': 'open_count'})
    closed_summary = closed_summary.rename(columns={'count': 'closed_count'})

    merged = open_summary.merge(closed_summary, on=[field, 'month'], how='outer')
    merged['open_count'] = merged['open_count'].fillna(0).astype(int)
    merged['closed_count'] = merged['closed_count'].fillna(0).astype(int)
    merged['delta'] = merged['open_count'] - merged['closed_count']
    return merged.sort_values(['month', 'open_count'], ascending=[True, False]).reset_index(drop=True)


def summarize(df: pd.DataFrame) -> dict[str, Any]:
    """Return a compact summary dict for quick inspection."""
    summary = {
        'rows': int(len(df)),
        'columns': list(df.columns),
        'months': sorted(df['month'].dropna().unique().tolist()) if 'month' in df.columns else [],
    }
    return summary


def plot_results(comparison_df: pd.DataFrame, output_dir: str | Path, field_name: str | None = None) -> list[Path]:
    """Create two relevant charts: monthly trends and top categories distribution."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison_df = comparison_df[comparison_df['month'].notna()].copy()

    if field_name is None:
        field_name = next(
            col for col in comparison_df.columns if col not in {'month', 'open_count', 'closed_count', 'delta'}
        )

    monthly = comparison_df.groupby('month', dropna=False)[['open_count', 'closed_count']].sum().reset_index()
    first_chart = output_dir / 'monthly_open_closed_trend.png'
    plt.figure(figsize=(10, 5))
    plt.plot(monthly['month'], monthly['open_count'], marker='o', label='Aperti')
    plt.plot(monthly['month'], monthly['closed_count'], marker='o', label='Chiusi')
    plt.title('Andamento mensile delle segnalazioni')
    plt.xlabel('Mese')
    plt.ylabel('Conteggio')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(first_chart, dpi=200)
    plt.close()

    # Create two separate top-categories charts: one using open_count totals, one using closed_count totals
    open_totals = comparison_df.groupby(field_name, dropna=False)['open_count'].sum().sort_values(ascending=False).head(10)
    closed_totals = comparison_df.groupby(field_name, dropna=False)['closed_count'].sum().sort_values(ascending=False).head(10)

    open_chart = output_dir / 'top_categories_open.png'
    plt.figure(figsize=(10, 5))
    plt.bar(open_totals.index.astype(str), open_totals.values, color='tab:green')
    plt.title(f'Top 10 categorie aperte per {field_name}')
    plt.xlabel(field_name)
    plt.ylabel('Conteggio aperti')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(open_chart, dpi=200)
    plt.close()

    closed_chart = output_dir / 'top_categories_closed.png'
    plt.figure(figsize=(10, 5))
    # Normalize closed totals to percentages of the closed total to improve readability
    closed_sum = closed_totals.sum() if closed_totals.sum() > 0 else 1
    closed_pct = (closed_totals / closed_sum) * 100
    bars = plt.bar(closed_pct.index.astype(str), closed_pct.values, color='tab:orange')
    plt.title(f'Top {len(closed_totals)} categorie chiuse per {field_name} (percentuale del totale chiusi)')
    plt.xlabel(field_name)
    plt.ylabel('Percentuale (%)')
    plt.xticks(rotation=45, ha='right')
    # Annotate bars with percentage labels
    for bar, pct in zip(bars, closed_pct.values):
        height = bar.get_height()
        plt.annotate(f"{pct:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    plt.savefig(closed_chart, dpi=200, bbox_inches='tight')
    plt.close()

    return [first_chart, open_chart, closed_chart]


def export_report(report_tables: dict[str, pd.DataFrame], output_path: str | Path) -> Path:
    """Write a multi-sheet Excel report for analysis results."""
    from .io import export_report as export_excel

    output_path = Path(output_path)
    export_excel(report_tables, output_path)
    return output_path


__all__ = ['aggregate_by_field', 'compare_open_closed', 'summarize', 'plot_results', 'export_report']