import os
import sys

import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from czrm_analysis import clean_data, compare_open_closed


def test_importable():
    import czrm_analysis
    assert hasattr(czrm_analysis, '__version__')


def test_clean_data_standardizes_and_parses_dates():
    df = pd.DataFrame(
        {
            'FirstStructure__c': ['  via roma  '],
            'CreatedDate__c': ['2026-01-05 08:10:00'],
            'Municipality_Category__c': [None],
            'Case_Theme_Area__c': ['  mobilita  '],
        }
    )

    cleaned = clean_data(df, dataset_type='open')
    assert cleaned.loc[0, 'FirstStructure__c'] == 'VIA ROMA'
    assert cleaned.loc[0, 'Municipality_Category__c'] == 'NON SPECIFICATO'
    assert str(cleaned.loc[0, 'month']) == '2026-01'


def test_compare_open_closed_counts_per_theme_and_month():
    open_df = pd.DataFrame({
        'Case_Theme_Area__c': ['Mobilità', 'Mobilità'],
        'CreatedDate__c': ['2026-01-03', '2026-02-04'],
    })
    closed_df = pd.DataFrame({
        'Case_Theme_Area__c': ['Mobilità'],
        'ClosedDate__c': ['2026-01-05'],
    })

    comparison = compare_open_closed(
        clean_data(open_df, dataset_type='open'),
        clean_data(closed_df, dataset_type='closed'),
        field='Case_Theme_Area__c',
        open_date_col='CreatedDate__c',
        closed_date_col='ClosedDate__c',
    )

    assert comparison['open_count'].sum() == 2
    assert comparison['closed_count'].sum() == 1
