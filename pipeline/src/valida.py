# -*- coding: utf-8 -*-
"""Controlli di qualita' dati e quadrature sul mese da elaborare.

Il rapporto di validazione distingue:
  - ERRORI  : bloccanti, la pipeline si ferma e NON pubblica report;
  - WARNING : segnalati nei report ma non bloccanti.
"""

TOLLERANZA_QUADRATURA_CENT = 1            # 0,01 EUR
TOLLERANZA_QUOTE = 1e-6
SOGLIA_IMPORTO_ANOMALO_CENT = 500_000 * 100  # 500.000 EUR a movimento

CLASSI_FINALI = ("produttivo", "commerciale")
CLASSI_RIBALTABILI = ("ausiliario", "struttura")


def _elenco(codici, massimo=8):
    """Compatta un elenco di codici per i messaggi del rapporto."""
    codici = sorted(codici)
    testo = ", ".join(codici[:massimo])
    if len(codici) > massimo:
        testo += f" (e altri {len(codici) - massimo})"
    return testo


def valida(mese, config, movimenti, totali_controllo):
    """Esegue tutti i controlli e ritorna il rapporto strutturato."""
    errori, warning = [], []
    cdc = config["cdc"]
    conti = config["conti"]
    regole = config["regole"]
    mov_mese = movimenti[movimenti["periodo"] == mese]

    def errore(controllo, esito):
        errori.append({"controllo": controllo, "esito": esito})

    def avviso(controllo, esito):
        warning.append({"controllo": controllo, "esito": esito})

    # ------------------------------------------------ presenza movimenti
    if mov_mese.empty:
        errore("presenza movimenti",
               f"nessun movimento contabile trovato per il periodo {mese}")

    # ------------------------------------- quadratura vs totale di controllo
    riga_ctrl = totali_controllo[totali_controllo["periodo"] == mese]
    if riga_ctrl.empty:
        errore("quadratura totale di controllo",
               f"totale di controllo assente per il periodo {mese}")
    else:
        atteso = int(riga_ctrl["totale_cent"].iloc[0])
        caricato = int(mov_mese["importo_cent"].sum())
        delta = caricato - atteso
        if abs(delta) > TOLLERANZA_QUADRATURA_CENT:
            errore("quadratura totale di controllo",
                   f"totale movimenti {caricato / 100:,.2f} EUR diverso dal "
                   f"totale di controllo {atteso / 100:,.2f} EUR "
                   f"(delta {delta / 100:,.2f} EUR)")
        n_atteso = int(riga_ctrl["numero_movimenti"].iloc[0])
        if n_atteso != len(mov_mese):
            avviso("numero movimenti",
                   f"attesi {n_atteso} movimenti, caricati {len(mov_mese)}")

    # ------------------------------------------------ CdC e conti sconosciuti
    codici_cdc = set(cdc["codice"])
    sconosciuti = set(mov_mese["cdc"]) - codici_cdc
    if sconosciuti:
        errore("CdC sconosciuti",
               f"{len(sconosciuti)} CdC movimentati non presenti in "
               f"anagrafica: {_elenco(sconosciuti)}")

    conti_noti = set(conti["conto"])
    conti_ignoti = set(mov_mese["conto"]) - conti_noti
    if conti_ignoti:
        errore("conti sconosciuti",
               f"{len(conti_ignoti)} conti movimentati non presenti nel "
               f"piano dei conti: {_elenco(conti_ignoti)}")

    # --------------------------------------- movimenti su CdC non imputabili
    foglie = cdc[cdc["livello"] == 3]
    non_foglia = set(mov_mese["cdc"]) & (codici_cdc - set(foglie["codice"]))
    if non_foglia:
        errore("imputazione su CdC aggregati",
               f"movimenti su CdC di livello 1-2 (non imputabili): "
               f"{_elenco(non_foglia)}")
    inattivi = set(foglie[foglie["attivo"] != "SI"]["codice"])
    mov_inattivi = set(mov_mese["cdc"]) & inattivi
    if mov_inattivi:
        errore("imputazione su CdC disattivati",
               f"movimenti su CdC non attivi: {_elenco(mov_inattivi)}")

    # ------------------------------------------------ importi nulli/anomali
    nulli = mov_mese[mov_mese["importo_cent"].isna() |
                     (mov_mese["importo_cent"] == 0)]
    if not nulli.empty:
        errore("importi nulli",
               f"{len(nulli)} movimenti con importo nullo o mancante")
    anomali = mov_mese[mov_mese["importo_cent"].abs() >
                       SOGLIA_IMPORTO_ANOMALO_CENT]
    if not anomali.empty:
        avviso("importi anomali",
               f"{len(anomali)} movimenti oltre "
               f"{SOGLIA_IMPORTO_ANOMALO_CENT / 100:,.0f} EUR: verificare")
    negativi = mov_mese[mov_mese["importo_cent"] < 0]
    if not negativi.empty:
        avviso("importi negativi",
               f"{len(negativi)} movimenti negativi (storni?): verificare")

    # ------------------------------------------- completezza CdC attivi
    foglie_attive = set(foglie[foglie["attivo"] == "SI"]["codice"])
    senza_movimenti = foglie_attive - set(mov_mese["cdc"])
    if senza_movimenti:
        avviso("CdC senza movimenti",
               f"{len(senza_movimenti)} CdC attivi senza movimenti nel mese: "
               f"{_elenco(senza_movimenti)}")

    # ------------------------------------------------ regole di ribaltamento
    somme = regole.groupby("cdc_origine")["quota"].sum()
    sbagliate = somme[(somme - 1.0).abs() > TOLLERANZA_QUOTE]
    if not sbagliate.empty:
        errore("quote di ribaltamento",
               f"quote che non sommano a 1,0 per {len(sbagliate)} CdC "
               f"origine: {_elenco(sbagliate.index)}")

    classe_cdc = dict(zip(cdc["codice"], cdc["classe"]))
    attivo_cdc = dict(zip(cdc["codice"], cdc["attivo"]))
    origini_ignote = set(regole["cdc_origine"]) - codici_cdc
    if origini_ignote:
        errore("regole di ribaltamento",
               f"CdC origine non in anagrafica: {_elenco(origini_ignote)}")
    origini_non_ribaltabili = {
        c for c in set(regole["cdc_origine"]) & codici_cdc
        if classe_cdc[c] not in CLASSI_RIBALTABILI}
    if origini_non_ribaltabili:
        errore("regole di ribaltamento",
               f"CdC origine con classe non ribaltabile: "
               f"{_elenco(origini_non_ribaltabili)}")
    dest_invalide = {
        c for c in set(regole["cdc_destinazione"])
        if c not in codici_cdc or classe_cdc[c] not in CLASSI_FINALI
        or attivo_cdc[c] != "SI"}
    if dest_invalide:
        errore("regole di ribaltamento",
               f"destinazioni non valide (ignote, non finali o non attive): "
               f"{_elenco(dest_invalide)}")

    # CdC ausiliari/struttura movimentati ma privi di regole: i loro costi
    # resterebbero non allocati, quindi il controllo e' bloccante.
    ribaltabili_mossi = {c for c in set(mov_mese["cdc"]) & codici_cdc
                         if classe_cdc[c] in CLASSI_RIBALTABILI}
    senza_regole = ribaltabili_mossi - set(regole["cdc_origine"])
    if senza_regole:
        errore("copertura regole di ribaltamento",
               f"CdC ausiliari/struttura con costi ma senza regole: "
               f"{_elenco(senza_regole)}")

    return {"mese": mese,
            "errori": errori,
            "warning": warning,
            "bloccato": bool(errori),
            "n_movimenti_mese": len(mov_mese),
            "totale_mese_cent": int(mov_mese["importo_cent"].sum())}


def main():
    """Entrypoint CLI: esegue i soli controlli di validazione/quadratura."""
    import argparse
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ingest

    parser = argparse.ArgumentParser(
        description="Esegue i soli controlli di validazione e quadratura "
                    "sul mese indicato, senza generare report.")
    parser.add_argument("--mese", required=True, metavar="YYYY-MM",
                        help="periodo da validare, es. 2026-06")
    args = parser.parse_args()

    config = ingest.carica_config()
    movimenti = ingest.carica_movimenti(args.mese)
    totali_controllo = ingest.carica_totali_controllo()
    rapporto = valida(args.mese, config, movimenti, totali_controllo)

    print(f"Validazione {args.mese}: {len(rapporto['errori'])} errori "
          f"bloccanti, {len(rapporto['warning'])} warning.")
    for errore in rapporto["errori"]:
        print(f"  ERRORE   {errore['controllo']}: {errore['esito']}")
    for avviso in rapporto["warning"]:
        print(f"  WARNING  {avviso['controllo']}: {avviso['esito']}")
    return 1 if rapporto["bloccato"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
