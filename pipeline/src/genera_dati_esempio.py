# -*- coding: utf-8 -*-
"""Generatore di dati contabili sintetici DICHIARATAMENTE FITTIZI.

Produce in pipeline/dati_esempio/ (cartella non versionata):
  - movimenti_AAAA-MM.csv  : movimenti contabili mensili per CdC/conto
  - budget_AAAA.csv        : budget mensile per CdC/natura di costo
  - totali_controllo.csv   : totali di controllo per mese (simula il
                             bilancio di verifica dell'ERP)

Seed fisso (42) per riproducibilita': ogni rigenerazione produce gli
stessi identici dati.
"""
import calendar
import csv
import random
from pathlib import Path

import pandas as pd

PIPELINE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = PIPELINE_DIR / "config"
DATI_DIR = PIPELINE_DIR / "dati_esempio"

SEED = 42
ANNO = 2026

# Peso di ogni natura di costo sul costo mensile di un CdC, per classe.
# I pesi di ogni classe sommano a 1.0.
PROFILI_NATURA = {
    "produttivo": [("Materie prime", 0.38), ("Materiali ausiliari", 0.05),
                   ("Utenze", 0.08), ("Manutenzioni", 0.06),
                   ("Lavorazioni esterne", 0.06), ("Trasporti", 0.03),
                   ("Personale", 0.24), ("Ammortamenti", 0.10)],
    "ausiliario": [("Materiali ausiliari", 0.10), ("Utenze", 0.10),
                   ("Manutenzioni", 0.15), ("Personale", 0.45),
                   ("Servizi generali", 0.10), ("Ammortamenti", 0.10)],
    "struttura": [("Personale", 0.45), ("Consulenze", 0.10),
                  ("Servizi IT", 0.10), ("Servizi generali", 0.08),
                  ("Godimento beni terzi", 0.08), ("Assicurazioni", 0.04),
                  ("Spese generali", 0.05), ("Oneri diversi", 0.04),
                  ("Ammortamenti", 0.06)],
    "commerciale": [("Personale", 0.35), ("Spese commerciali", 0.35),
                    ("Trasporti", 0.10), ("Godimento beni terzi", 0.08),
                    ("Servizi IT", 0.05), ("Formazione", 0.02),
                    ("Oneri diversi", 0.05)],
}

# Costo mensile base (EUR) per CdC, estratto a caso in questi intervalli.
BASE_MENSILE = {"produttivo": (60_000, 220_000), "ausiliario": (25_000, 70_000),
                "struttura": (18_000, 60_000), "commerciale": (15_000, 55_000)}

# Stagionalita' della produzione (agosto quasi fermo, dicembre ridotto).
STAGIONALITA_PRODUZIONE = {1: 1.00, 2: 0.98, 3: 1.05, 4: 1.01, 5: 1.04,
                           6: 1.06, 7: 0.96, 8: 0.55, 9: 1.06, 10: 1.08,
                           11: 1.04, 12: 0.90}
# Personale: ferie in agosto, tredicesima a dicembre.
STAGIONALITA_PERSONALE = {m: 1.00 for m in range(1, 13)}
STAGIONALITA_PERSONALE[8] = 0.75
STAGIONALITA_PERSONALE[12] = 1.80

# CdC attivi lasciati volutamente SENZA movimenti: dimostrano il warning
# di completezza della validazione (hanno comunque un budget).
CDC_SENZA_MOVIMENTI = {"COM-MKT-009", "S3-STR-006"}

FORNITORI = ["Metallux S.p.A.", "Elettroforniture Nord S.r.l.",
             "Logistica Adriatica S.r.l.", "Energia Piu' S.p.A.",
             "TecnoService S.r.l.", "Ricambi Industriali S.r.l.",
             "Studio Bianchi & Associati", "CleanFacility S.r.l.",
             "InfoSistemi S.p.A.", "Trasporti Padana S.r.l."]

MESI_IT = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
           "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def _fattore_stagionale(classe, natura, mese_n):
    """Fattore stagionale per classe CdC e natura di costo."""
    if natura == "Personale":
        return STAGIONALITA_PERSONALE[mese_n]
    if classe in ("produttivo", "ausiliario"):
        return STAGIONALITA_PRODUZIONE[mese_n]
    return 1.0  # struttura e commerciale: costi sostanzialmente piatti


def _descrizione(rnd, natura, mese_n, progressivo):
    if natura == "Personale":
        return f"Costo del personale {MESI_IT[mese_n]}"
    if natura == "Ammortamenti":
        return "Quota ammortamento mensile"
    return f"Fattura {rnd.choice(FORNITORI)} n. {ANNO}/{progressivo:05d}"


def _spezza_importo(rnd, totale, n_pezzi):
    """Divide un importo in n movimenti che sommano esattamente al totale."""
    pesi = [rnd.uniform(0.5, 1.5) for _ in range(n_pezzi)]
    somma_pesi = sum(pesi)
    pezzi = [round(totale * p / somma_pesi, 2) for p in pesi[:-1]]
    pezzi.append(round(totale - sum(pezzi), 2))
    return pezzi


def genera(anno=ANNO, seed=SEED):
    """Genera 12 mesi di movimenti, budget e totali di controllo."""
    rnd = random.Random(seed)
    DATI_DIR.mkdir(parents=True, exist_ok=True)

    cdc = pd.read_csv(CONFIG_DIR / "centri_di_costo.csv", dtype=str)
    conti = pd.read_csv(CONFIG_DIR / "piano_dei_conti.csv", dtype=str)
    conti_per_natura = conti.groupby("natura_costo")["conto"].apply(list).to_dict()

    foglie = cdc[(cdc["livello"] == "3") & (cdc["attivo"] == "SI")]
    for classe, profilo in PROFILI_NATURA.items():
        for natura, _ in profilo:
            assert natura in conti_per_natura, f"natura non a piano: {natura}"

    # dimensione economica base di ogni CdC (stabile su tutto l'anno)
    basi = {}
    for r in foglie.itertuples(index=False):
        lo, hi = BASE_MENSILE[r.classe]
        basi[r.codice] = rnd.uniform(lo, hi)

    righe_budget = []
    totali_controllo = []
    progressivo = 0
    tot_movimenti = 0

    for mese_n in range(1, 13):
        periodo = f"{anno}-{mese_n:02d}"
        ultimo_giorno = calendar.monthrange(anno, mese_n)[1]
        righe_mov = []
        totale_mese = 0.0

        for r in foglie.itertuples(index=False):
            base = basi[r.codice]
            for natura, peso in PROFILI_NATURA[r.classe]:
                fattore = _fattore_stagionale(r.classe, natura, mese_n)
                importo_budget = round(base * peso * fattore, 2)
                righe_budget.append((periodo, r.codice, natura,
                                     f"{importo_budget:.2f}"))
                if r.codice in CDC_SENZA_MOVIMENTI:
                    continue  # actual volutamente assente (warning demo)
                # actual = budget con scostamento casuale +/- realistico
                actual = importo_budget * (1 + rnd.uniform(-0.10, 0.14))
                n_pezzi = 1 if natura in ("Personale", "Ammortamenti") \
                    else rnd.randint(1, 3)
                for pezzo in _spezza_importo(rnd, round(actual, 2), n_pezzi):
                    progressivo += 1
                    giorno = rnd.randint(1, ultimo_giorno)
                    righe_mov.append((f"{periodo}-{giorno:02d}", periodo,
                                      rnd.choice(conti_per_natura[natura]),
                                      r.codice,
                                      _descrizione(rnd, natura, mese_n,
                                                   progressivo),
                                      f"{pezzo:.2f}"))
                    totale_mese = round(totale_mese + pezzo, 2)

        righe_mov.sort(key=lambda x: (x[0], x[3]))
        with open(DATI_DIR / f"movimenti_{periodo}.csv", "w", newline="",
                  encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["data", "periodo", "conto", "cdc", "descrizione",
                        "importo"])
            w.writerows(righe_mov)
        totali_controllo.append((periodo, len(righe_mov),
                                 f"{totale_mese:.2f}"))
        tot_movimenti += len(righe_mov)

    with open(DATI_DIR / f"budget_{anno}.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["periodo", "cdc", "natura_costo", "importo_budget"])
        w.writerows(righe_budget)

    with open(DATI_DIR / "totali_controllo.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["periodo", "numero_movimenti", "totale_importo"])
        w.writerows(totali_controllo)

    return {"anno": anno, "n_movimenti": tot_movimenti,
            "n_righe_budget": len(righe_budget),
            "n_cdc": len(foglie), "cartella": str(DATI_DIR)}


if __name__ == "__main__":
    esito = genera()
    print(f"Dati sintetici generati in {esito['cartella']}: "
          f"{esito['n_movimenti']} movimenti, "
          f"{esito['n_righe_budget']} righe di budget, "
          f"{esito['n_cdc']} CdC.")
