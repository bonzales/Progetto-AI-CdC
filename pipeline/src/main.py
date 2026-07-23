# -*- coding: utf-8 -*-
"""Entrypoint CLI della pipeline dimostrativa di controllo di gestione.

Uso (dalla radice del repository):
    python3 pipeline/src/main.py --genera-dati --mese 2026-06
    python3 pipeline/src/main.py --mese 2026-06

Passi: ingest -> validazione (si ferma sugli errori bloccanti) ->
ribaltamento -> report. Rilanciare lo stesso mese sovrascrive l'output
del mese: la pipeline e' idempotente per periodo.
"""
import argparse
import re
import sys
from pathlib import Path

# rende importabili i moduli della pipeline anche lanciando lo script
# dalla radice del repository (python3 pipeline/src/main.py ...)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import genera_dati_esempio
import ingest
import ribalta
import report
import valida


def _argomenti():
    parser = argparse.ArgumentParser(
        description="Pipeline dimostrativa di controllo di gestione: "
                    "ingest, validazione, ribaltamento e report mensili.")
    parser.add_argument("--mese", required=True, metavar="YYYY-MM",
                        help="periodo da elaborare, es. 2026-06")
    parser.add_argument("--genera-dati", action="store_true",
                        help="rigenera i dati sintetici di esempio prima "
                             "dell'elaborazione (seed fisso, riproducibile)")
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", args.mese):
        parser.error("--mese deve essere nel formato YYYY-MM, es. 2026-06")
    return args


def main():
    args = _argomenti()
    mese = args.mese
    anno = mese[:4]
    print(f"=== Pipeline controllo di gestione — periodo {mese} ===")

    if args.genera_dati:
        esito_gen = genera_dati_esempio.genera(anno=int(anno))
        print(f"[0/4] Dati sintetici rigenerati in {esito_gen['cartella']}: "
              f"{esito_gen['n_movimenti']} movimenti, "
              f"{esito_gen['n_cdc']} CdC attivi.")

    # ------------------------------------------------------------- ingest
    try:
        config = ingest.carica_config()
        movimenti = ingest.carica_movimenti(mese)
        budget = ingest.carica_budget(anno, mese)
        totali_controllo = ingest.carica_totali_controllo()
    except FileNotFoundError as errore:
        print(f"ERRORE INGEST: {errore}")
        return 1
    n_mese = int((movimenti["periodo"] == mese).sum())
    print(f"[1/4] Ingest: {len(movimenti)} movimenti caricati "
          f"({n_mese} nel mese {mese}), "
          f"{len(config['cdc'])} CdC in anagrafica, "
          f"{len(config['conti'])} conti, "
          f"{len(config['regole'])} regole di ribaltamento.")

    # -------------------------------------------------------- validazione
    rapporto = valida.valida(mese, config, movimenti, totali_controllo)
    print(f"[2/4] Validazione: {len(rapporto['errori'])} errori bloccanti, "
          f"{len(rapporto['warning'])} warning.")
    for avviso in rapporto["warning"]:
        print(f"      WARNING  {avviso['controllo']}: {avviso['esito']}")
    if rapporto["bloccato"]:
        for errore in rapporto["errori"]:
            print(f"      ERRORE   {errore['controllo']}: {errore['esito']}")
        print("Pipeline INTERROTTA: correggere gli errori bloccanti. "
              "Nessun report pubblicato.")
        return 1

    # ------------------------------------------------------- ribaltamento
    esito_ribalta = ribalta.ribalta(movimenti, config)
    print(f"[3/4] Ribaltamento: totale pre "
          f"{report.eur(esito_ribalta['tot_pre_cent'])} EUR = "
          f"totale post {report.eur(esito_ribalta['tot_post_cent'])} EUR "
          f"(quadratura verificata al centesimo).")

    # -------------------------------------------------------------- report
    percorsi = report.genera_report(mese, config, movimenti, esito_ribalta,
                                    budget, totali_controllo, rapporto)
    print(f"[4/4] Report generati in {percorsi[0].parent}:")
    for percorso in percorsi:
        print(f"      - {percorso.name}")

    print("")
    print(f"Riepilogo {mese}: actual mese "
          f"{report.eur(rapporto['totale_mese_cent'])} EUR su "
          f"{rapporto['n_movimenti_mese']} movimenti; "
          f"cumulato YTD {report.eur(esito_ribalta['tot_pre_cent'])} EUR. "
          f"Esito: OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
