# -*- coding: utf-8 -*-
"""Ribaltamento a cascata dei CdC ausiliari e di struttura sui CdC finali.

Metodo a cascata semplice: prima i CdC ausiliari, poi quelli di struttura,
verso i CdC produttivi e commerciali. Le regole (config/regole_ribaltamento.csv)
destinano solo a CdC finali, quindi nessun CdC intermedio riceve costi da
ribaltare a sua volta. La tracciabilita' e' garantita dalla colonna
origine_ribaltamento ("DIRETTO" per i costi propri, altrimenti il codice
del CdC di provenienza).

INVARIANTE (asserito nel codice): il totale dei costi pre-ribaltamento
e' identico al totale post-ribaltamento, al centesimo. L'allocazione
lavora in centesimi interi e assegna il resto di arrotondamento
all'ultima destinazione di ogni regola.
"""
import pandas as pd

ORDINE_CASCATA = ("ausiliario", "struttura")
CLASSI_FINALI = ("produttivo", "commerciale")


def _alloca(riga, regole_origine):
    """Ripartisce un importo (centesimi) sulle destinazioni di una regola."""
    out = []
    residuo = int(riga.importo_cent)
    ultima = len(regole_origine) - 1
    for i, reg in enumerate(regole_origine.itertuples(index=False)):
        if i < ultima:
            quota_cent = int(round(riga.importo_cent * reg.quota))
        else:
            quota_cent = residuo  # il resto va all'ultima destinazione
        residuo -= quota_cent
        out.append((riga.periodo, reg.cdc_destinazione, riga.natura_costo,
                    quota_cent, riga.cdc))
    return out


def ribalta(movimenti, config):
    """Applica la cascata di ribaltamento e verifica la quadratura.

    Ritorna un dizionario con:
      diretti       : costi diretti per periodo/CdC/natura (pre-ribaltamento)
      post          : costi finali per periodo/CdC/natura/origine_ribaltamento
      tot_pre_cent  : totale complessivo pre-ribaltamento (centesimi)
      tot_post_cent : totale complessivo post-ribaltamento (centesimi)
    """
    cdc = config["cdc"]
    conti = config["conti"]
    regole = config["regole"]
    classe_cdc = dict(zip(cdc["codice"], cdc["classe"]))

    # costi diretti aggregati per periodo / CdC / natura di costo
    mov = movimenti.merge(conti[["conto", "natura_costo"]], on="conto",
                          how="left")
    diretti = (mov.groupby(["periodo", "cdc", "natura_costo"],
                           as_index=False)["importo_cent"].sum())
    tot_pre = int(diretti["importo_cent"].sum())

    righe_finali = []
    # i costi diretti dei CdC finali restano dove sono
    for r in diretti.itertuples(index=False):
        if classe_cdc.get(r.cdc) in CLASSI_FINALI:
            righe_finali.append((r.periodo, r.cdc, r.natura_costo,
                                 int(r.importo_cent), "DIRETTO"))

    regole_per_origine = {origine: gruppo.sort_values("cdc_destinazione")
                          for origine, gruppo in regole.groupby("cdc_origine")}

    # cascata: prima gli ausiliari, poi la struttura
    for classe in ORDINE_CASCATA:
        blocco = diretti[diretti["cdc"].map(classe_cdc) == classe]
        for r in blocco.itertuples(index=False):
            reg = regole_per_origine.get(r.cdc)
            if reg is None:
                raise ValueError(
                    f"CdC {r.cdc} ({classe}) con costi ma senza regole di "
                    f"ribaltamento: eseguire prima la validazione")
            righe_finali.extend(_alloca(r, reg))

    post = pd.DataFrame(righe_finali,
                        columns=["periodo", "cdc", "natura_costo",
                                 "importo_cent", "origine_ribaltamento"])
    tot_post = int(post["importo_cent"].sum())

    # quadratura fondamentale: il ribaltamento non crea ne' distrugge costi
    assert tot_pre == tot_post, (
        f"quadratura ribaltamento violata: pre={tot_pre} cent, "
        f"post={tot_post} cent, delta={tot_post - tot_pre} cent")

    return {"diretti": diretti, "post": post,
            "tot_pre_cent": tot_pre, "tot_post_cent": tot_post}
