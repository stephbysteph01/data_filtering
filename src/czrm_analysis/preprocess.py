"""Preprocessing helpers for CzRM data."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _normalize_text(value: Any) -> Any:
    if pd.isna(value):
        return None
    text = str(value).strip()
    text = ' '.join(text.split())
    return text.upper()


def _normalize_category(value: Any) -> Any:
    text = _normalize_text(value)
    if text is None:
        return None
    return text.upper()


def normalize_dates(df: pd.DataFrame, date_columns: list[str] | None = None) -> pd.DataFrame:
    """Convert recognizable date columns to pandas timestamps.

    Heuristic: if values contain '/' (e.g. 'DD/MM/YYYY'), parse with dayfirst=True.
    Otherwise rely on pandas automatic parsing which handles ISO-like formats.
    """
    normalized = df.copy()
    date_columns = date_columns or [
        'CreatedDate__c',
        'ClosedDate__c',
        'CreatedDate',
        'ClosedDate',
    ]
    for col in date_columns:
        if col in normalized.columns:
            series = normalized[col].astype(str).replace({'nan': None})
            sample = series.dropna().astype(str).head(100)
            dayfirst = False
            if not sample.empty:
                # If many values contain '/', likely DD/MM/YYYY
                slash_ratio = sum(1 for v in sample if '/' in v) / len(sample)
                if slash_ratio > 0.1:
                    dayfirst = True
            normalized[col] = pd.to_datetime(series, errors='coerce', dayfirst=dayfirst)
    return normalized


def clean_data(df: pd.DataFrame, dataset_type: str = 'open') -> pd.DataFrame:
    """Clean and harmonize CzRM data for analysis."""
    cleaned = df.copy()
    for col in cleaned.columns:
        if cleaned[col].dtype == object:
            cleaned[col] = cleaned[col].map(_normalize_text)

    if 'Municipality_Category__c' in cleaned.columns:
        cleaned['Municipality_Category__c'] = cleaned['Municipality_Category__c'].fillna('NON SPECIFICATO')
        cleaned['Municipality_Category__c'] = cleaned['Municipality_Category__c'].map(_normalize_category)

    text_columns = [
        'FirstStructure__c',
        'Type',
        'Case_Theme_Area__c',
        'Case_Topic_Service__c',
        'Origin',
        'Closed_Reason__c',
        'Rejected_URP__c',
        'SendExternal__c',
        'SendExternalName__c',
        'ImmediateClosure__c',
        'Case_Alert_Police_Warning__c',
    ]
    for col in text_columns:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].map(_normalize_text)
            cleaned[col] = cleaned[col].fillna('NON DISPONIBILE')

    if dataset_type.lower() in {'open', 'aperto', 'aperti'}:
        date_col = 'CreatedDate__c' if 'CreatedDate__c' in cleaned.columns else 'CreatedDate'
    else:
        date_col = 'ClosedDate__c' if 'ClosedDate__c' in cleaned.columns else 'ClosedDate'

    if date_col in cleaned.columns:
        cleaned = normalize_dates(cleaned, [date_col])
        cleaned = cleaned[cleaned[date_col].notna()].copy()
        cleaned['month'] = cleaned[date_col].dt.to_period('M').astype(str)

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned


def clean_coordinates(df: pd.DataFrame, lat_col: str = 'Latitude', lon_col: str = 'Longitude') -> pd.DataFrame:
    """Validate/normalize coordinate columns if present."""
    cleaned = df.copy()
    for col in (lat_col, lon_col):
        if col in cleaned.columns:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
    return cleaned