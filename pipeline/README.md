# Pipeline dimostrativa di controllo di gestione

Pipeline Python end-to-end che dimostra il ciclo mensile di controllo di gestione su **~320 centri di costo**: caricamento movimenti, validazione con quadrature bloccanti, ribaltamento dei CdC ausiliari e di struttura, reportistica per area e per CdC.

> **Attenzione**: la pipeline lavora su **dati sintetici dichiaratamente fittizi**, generati con seed fisso per riproducibilità. Serve a dimostrare il processo e a fare da base per l'aggancio ai dati reali dell'ERP.

## Cosa fa

| Passo | Modulo | Descrizione |
|---|---|---|
| 0 (opzionale) | [`src/genera_dati_esempio.py`](src/genera_dati_esempio.py) | Genera 12 mesi di movimenti sintetici plausibili + budget mensile per CdC/natura + totali di controllo (seed 42, sempre identici) |
| 1 | [`src/ingest.py`](src/ingest.py) | Carica configurazioni e movimenti fino al mese richiesto; normalizza tipi e periodi; converte gli importi in **centesimi interi** (mai float nei totali) |
| 2 | [`src/valida.py`](src/valida.py) | Controlli bloccanti (quadratura vs totale di controllo, CdC/conti sconosciuti, importi nulli, quote di ribaltamento ≠ 1) e warning (CdC senza movimenti, importi anomali) |
| 3 | [`src/ribalta.py`](src/ribalta.py) | Ribaltamento a cascata (prima ausiliari, poi struttura, verso produttivi/commerciali) con tracciabilità (`origine_ribaltamento`) e **asserzione**: totale pre = totale post al centesimo |
| 4 | [`src/report.py`](src/report.py) | Un Excel per area (sintesi + un foglio per CdC), `scostamenti.csv` per CdC (fonte citabile dai commenti), sintesi HTML per la direzione, riepilogo quadrature |

La pipeline è **idempotente per periodo**: rilanciare lo stesso mese sovrascrive integralmente l'output di quel mese (le rettifiche contabili tardive si gestiscono rilanciando il run).

## Prerequisiti

- Python 3.11+
- Dipendenze: `pip install -r pipeline/requirements.txt` (pandas 3.x, openpyxl, Jinja2 — nessun database necessario)

## Comandi

Dalla **radice del repository**:

```bash
# prima esecuzione: genera i dati sintetici ed elabora giugno 2026
python3 pipeline/src/main.py --genera-dati --mese 2026-06

# esecuzioni successive (i dati esistono già)
python3 pipeline/src/main.py --mese 2026-06

# soli controlli di validazione/quadratura, senza generare report
python3 pipeline/src/valida.py --mese 2026-06

# rigenera i soli report (riesegue in memoria ingest, validazione e ribaltamento)
python3 pipeline/src/report.py --mese 2026-06
```

Codici di uscita: `0` = OK, `1` = errori bloccanti di validazione o file mancanti (nessun report pubblicato), `2` = parametri errati.

## Struttura dell'output

```
pipeline/output/2026-06/
├── report_Stabilimento_Verona_2026-06.xlsx    ← sintesi area + 1 foglio per CdC
├── report_Stabilimento_Bergamo_2026-06.xlsx
├── report_Stabilimento_Bari_2026-06.xlsx
├── report_Rete_Commerciale_2026-06.xlsx
├── report_Sede_Centrale_2026-06.xlsx
├── scostamenti.csv                            ← scostamenti per CdC (machine-readable, ordinati dal più sfavorevole)
├── sintesi_2026-06.html                       ← totali per area, top 10 scostamenti sfavorevoli
└── riepilogo_quadrature.txt                   ← totali di controllo pre/post ribaltamento
```

Convenzioni nei report: i valori sono **costi**, quindi scostamento positivo (actual > budget) = **sfavorevole** (in rosso). Gli scostamenti sono calcolati sui costi diretti; i ribaltamenti sono esposti a parte come "costo pieno".

## File di configurazione (versionati, manutenuti dal controller)

| File | Contenuto |
|---|---|
| [`config/centri_di_costo.csv`](config/centri_di_costo.csv) | Anagrafica gerarchica di 316 CdC (3 stabilimenti, rete commerciale, sede centrale) con classe, area, responsabile, driver di ribaltamento, flag attivo |
| [`config/piano_dei_conti.csv`](config/piano_dei_conti.csv) | 61 conti economici (schema CEE B6–B14) con natura di costo |
| [`config/regole_ribaltamento.csv`](config/regole_ribaltamento.csv) | 361 regole di allocazione: per ogni CdC ausiliario/di struttura, destinazioni, driver e quote (che devono sommare a 1,0 — controllo bloccante) |

Il disegno dell'anagrafica è documentato in [`../docs/02-dati/piano-centri-di-costo.md`](../docs/02-dati/piano-centri-di-costo.md); il modello dati complessivo in [`../docs/02-dati/modello-dati.md`](../docs/02-dati/modello-dati.md).

## Come passare ai dati reali dell'ERP

La pipeline cerca i file **prima** in `pipeline/dati_reali/` (drop folder, non versionata) e solo in mancanza ripiega su `pipeline/dati_esempio/`. Per usare i dati veri basta depositare in `pipeline/dati_reali/` file con lo **stesso tracciato** (CSV UTF-8, separatore virgola, decimali con punto):

**`movimenti_AAAA-MM.csv`** — un file per mese contabile:

| Colonna | Formato | Esempio |
|---|---|---|
| `data` | `AAAA-MM-GG` | `2026-06-15` |
| `periodo` | `AAAA-MM` | `2026-06` |
| `conto` | codice del piano dei conti | `6101` |
| `cdc` | codice CdC di livello 3 (foglia) | `S1-PRD-001` |
| `descrizione` | testo libero | `Fattura Metallux n. 2026/00123` |
| `importo` | numero con 2 decimali | `1234.56` |

**`budget_AAAA.csv`**: `periodo, cdc, natura_costo, importo_budget` (la natura deve coincidere con quelle del piano dei conti).

**`totali_controllo.csv`**: `periodo, numero_movimenti, totale_importo` — il totale di riscontro preso dal bilancio di verifica dell'ERP; la quadratura con i movimenti caricati è un **controllo bloccante**.

Note pratiche per gli export TeamSystem/Zucchetti: gli export nativi usano spesso encoding CP1252 e formato numerico italiano (virgola decimale, punto migliaia); l'adeguamento del parsing va fatto in [`src/ingest.py`](src/ingest.py) una volta noto il tracciato reale (vedi [`../docs/02-dati/inventario-fonti-dati.md`](../docs/02-dati/inventario-fonti-dati.md)).

## Limiti attuali

- **Dati sintetici**: importi e scostamenti sono plausibili ma fittizi; 2 CdC sono lasciati volutamente senza movimenti per dimostrare i warning di completezza.
- **Ribaltamento a cascata semplice**: un solo passaggio ausiliari → struttura → finali, senza prestazioni reciproche tra CdC ausiliari (niente metodo algebrico/iterativo); le quote sono statiche a config, non ricalcolate ogni mese dai valori effettivi dei driver.
- **YTD nell'anno solare**: il cumulato riparte da gennaio; niente confronti anno su anno.
- **Persistenza minima**: niente layer raw/staging/marts in Parquet né motore DuckDB (previsti dalla roadmap); a questa scala i tempi di run restano comunque di pochi secondi.
- **Nessuna distribuzione automatica**: i report vanno condivisi a mano (niente invio email/SharePoint).
- **Formati di input rigidi**: encoding UTF-8 e decimali con punto; il parsing dei formati ERP italiani è da adeguare al tracciato reale.

## Prossimi passi

1. Contratto dati con il fornitore ERP e drop folder validata (`inbox/` → controllo schema → `raw/` → `processed/`/`rejected/`).
2. Architettura medallion su filesystem (raw/staging/marts in Parquet) con DuckDB come motore SQL delle aggregazioni e riconciliazioni.
3. Quote di ribaltamento calcolate dai driver effettivi del mese (ore, headcount, kWh) invece che fisse.
4. Commenti gestionali automatici sugli scostamenti tramite AI **a valle dei numeri già calcolati** (mai in sostituzione): vedi [`../docs/05-metodologia/metodologia-ai.md`](../docs/05-metodologia/metodologia-ai.md).
5. Distribuzione automatica (email ai responsabili di CdC, cartella condivisa/SharePoint) secondo la [roadmap](../docs/04-roadmap/roadmap.md).
