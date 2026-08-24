# CzRM analysis for Roma Capitale

Questo progetto analizza le segnalazioni/reclami del CzRM di Roma Capitale a partire dai dataset Open Data del Comune di Roma.

## Obiettivo

- caricare i file CSV relativi alle segnalazioni aperte e chiuse;
- pulire e normalizzare i dati;
- aggregare per municipio, tema, origine e mese;
- confrontare il volume di segnalazioni aperte e chiuse;
- generare grafici significativi e un report Excel.

## Fonte dati

I dati provengono dal portale Open Data di Roma Capitale, dataset "CzRM di Roma Capitale - Dati delle segnalazioni anno 2026".

Licenza: CC BY 4.0 (https://w3id.org/italia/controlled-vocabulary/licences/A21_CCBY40)

## Struttura del progetto

- `data/` (o `data/raw/` per compatibilità): directory in cui inserire i file CSV originali
- `data/processed/`: output generati dal progetto (report Excel e grafici)
- `src/czrm_analysis/`: codice Python dell'analisi
- `tests/`: test automatici

## Requisiti principali

- pandas
- numpy
- matplotlib
- openpyxl

Oppure usa il file `requirements.txt`.

## Uso rapido

1. crea un virtual environment
2. installa le dipendenze
3. inserisci i CSV in `data/`
4. esegui:

```bash
python -m czrm_analysis
```

Il comando carica i file CSV, pulisce i dati, genera grafici e salva un report in `data/processed/`.

## Nota sui dati

I file aperti e chiusi non condividono un ID caso univoco tra i due insiemi. Per questo motivo il progetto non unisce righe per ID, ma aggrega e confronta i conteggi separatamente.
