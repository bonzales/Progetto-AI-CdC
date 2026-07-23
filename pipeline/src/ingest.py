# -*- coding: utf-8 -*-
"""Caricamento e normalizzazione di configurazioni, movimenti e budget.

Gli importi vengono convertiti subito in CENTESIMI INTERI (int64):
tutti i totali e le quadrature della pipeline sono calcolati su interi,
mai su float. La ricerca dei file dati privilegia pipeline/dati_reali/
(drop folder per gli export ERP) e ripiega su pipeline/dati_esempio/.
"""
import re
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = PIPELINE_DIR / "config"
DATI_ESEMPIO_DIR = PIPELINE_DIR / "dati_esempio"
DATI_REALI_DIR = PIPELINE_DIR / "dati_reali"
OUTPUT_DIR = PIPELINE_DIR / "output"

RE_PERIODO = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def _in_cent(serie):
    """Converte una serie di importi in euro in centesimi interi."""
    return (serie.astype(float).round(2) * 100).round().astype("int64")


def _percorso_dati(nome_file):
    """Preferisce i dati reali (drop folder), altrimenti i dati di esempio."""
    reale = DATI_REALI_DIR / nome_file
    return reale if reale.exists() else DATI_ESEMPIO_DIR / nome_file


def periodi_fino_a(mese):
    """Elenco dei periodi da gennaio dell'anno fino al mese richiesto."""
    anno, m = mese.split("-")
    return [f"{anno}-{i:02d}" for i in range(1, int(m) + 1)]


def carica_config():
    """Carica anagrafica CdC, piano dei conti e regole di ribaltamento."""
    cdc = pd.read_csv(CONFIG_DIR / "centri_di_costo.csv", dtype=str)
    cdc = cdc.fillna("")
    cdc["livello"] = cdc["livello"].astype(int)
    conti = pd.read_csv(CONFIG_DIR / "piano_dei_conti.csv", dtype=str)
    regole = pd.read_csv(CONFIG_DIR / "regole_ribaltamento.csv",
                         dtype={"cdc_origine": str, "cdc_destinazione": str,
                                "driver": str})
    regole["quota"] = regole["quota"].astype(float)
    return {"cdc": cdc, "conti": conti, "regole": regole}


def carica_movimenti(mese):
    """Carica i movimenti da gennaio al mese richiesto (per actual e YTD).

    Il file del mese richiesto e' obbligatorio; i mesi precedenti mancanti
    vengono semplicemente saltati (YTD parziale).
    """
    if not RE_PERIODO.match(mese):
        raise ValueError(f"Periodo non valido: {mese!r} (atteso YYYY-MM)")
    blocchi = []
    for periodo in periodi_fino_a(mese):
        percorso = _percorso_dati(f"movimenti_{periodo}.csv")
        if not percorso.exists():
            if periodo == mese:
                raise FileNotFoundError(
                    f"File movimenti mancante per il mese richiesto: {percorso}\n"
                    f"Suggerimento: rilanciare con --genera-dati per creare i "
                    f"dati sintetici di esempio.")
            continue
        df = pd.read_csv(percorso, dtype={"data": str, "periodo": str,
                                          "conto": str, "cdc": str,
                                          "descrizione": str})
        blocchi.append(df)
    movimenti = pd.concat(blocchi, ignore_index=True)
    # normalizzazione: periodo derivato dalla data se assente o vuoto
    if "periodo" not in movimenti.columns:
        movimenti["periodo"] = movimenti["data"].str[:7]
    movimenti["periodo"] = movimenti["periodo"].fillna(
        movimenti["data"].str[:7]).str.strip()
    for col in ("conto", "cdc"):
        movimenti[col] = movimenti[col].str.strip()
    movimenti["importo_cent"] = _in_cent(movimenti["importo"])
    return movimenti


def carica_budget(anno, fino_a_mese):
    """Carica il budget dell'anno, limitato ai periodi fino al mese richiesto."""
    percorso = _percorso_dati(f"budget_{anno}.csv")
    if not percorso.exists():
        raise FileNotFoundError(f"File budget mancante: {percorso}")
    budget = pd.read_csv(percorso, dtype={"periodo": str, "cdc": str,
                                          "natura_costo": str})
    budget["importo_cent"] = _in_cent(budget["importo_budget"])
    return budget[budget["periodo"] <= fino_a_mese].copy()


def carica_totali_controllo():
    """Carica i totali di controllo per mese (dal bilancio di verifica ERP)."""
    percorso = _percorso_dati("totali_controllo.csv")
    if not percorso.exists():
        raise FileNotFoundError(f"File totali di controllo mancante: {percorso}")
    totali = pd.read_csv(percorso, dtype={"periodo": str})
    totali["numero_movimenti"] = totali["numero_movimenti"].astype(int)
    totali["totale_cent"] = _in_cent(totali["totale_importo"])
    return totali
