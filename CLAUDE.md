# CLAUDE.md — Guida operativa per Claude Code

## Scopo del progetto

Automazione del controllo di gestione di un'azienda italiana con più di 300 centri di costo: pipeline Python deterministica che ingerisce i dati contabili, li valida, esegue i ribaltamenti e produce la reportistica mensile, con l'AI usata solo per orchestrare gli strumenti e commentare numeri già calcolati. L'utente finale è l'imprenditore e il team AFC, **non** uno sviluppatore: ogni output e ogni spiegazione devono essere comprensibili a chi fa controllo di gestione.

## Mappa del repository

```
Progetto-AI-CdC/
├── README.md                          Visione, quick start, mappa del repository
├── CLAUDE.md                          Questo file
├── .claude/agents/                    Sub-agenti specializzati (vedi sotto)
├── docs/
│   ├── 00-contesto/                   Questionario aziendale, glossario, stakeholder
│   ├── 01-processi/                   Processo as-is, to-be, calendario di chiusura
│   ├── 02-dati/                       Inventario fonti, modello dati, piano CdC
│   ├── 03-reportistica/               Requisiti report, catalogo KPI
│   ├── 04-roadmap/                    Roadmap del progetto
│   └── 05-metodologia/                Metodologia AI (principi, Superpowers, sicurezza)
└── pipeline/
    ├── README.md                      Istruzioni d'uso della pipeline
    ├── requirements.txt
    ├── config/                        centri_di_costo.csv (~320 CdC), piano_dei_conti.csv,
    │                                  regole_ribaltamento.csv
    ├── src/                           genera_dati_esempio.py, ingest.py, valida.py,
    │                                  ribalta.py, report.py, main.py
    ├── dati_esempio/                  Dati sintetici generati (--genera-dati), NON versionati
    ├── dati_reali/                    Drop folder per gli export ERP reali, NON versionata
    │                                  (se un file esiste qui, ingest.py lo preferisce ai dati di esempio)
    └── output/                        Generato dalla pipeline, NON versionato
```

## Convenzioni vincolanti

1. **Tutto in italiano.** Documenti, commenti nel codice, messaggi di log, output dei report: italiano professionale. I termini tecnici inglesi consolidati (forecast, driver, actual, budget) vanno bene.
2. **Formato periodi: `YYYY-MM`** (es. `2026-06`), ovunque: nomi di cartelle di output, parametri CLI, colonne dei dati, testi dei report.
3. **I numeri nei report vengono SOLO dalla pipeline.** Mai calcolare, inventare o stimare valori contabili: né somme, né percentuali, né scostamenti. Se un numero serve e non esiste negli output, si estende la pipeline (o si riesegue), non si calcola "a mente". Ogni cifra citata deve essere tracciabile a un file in `pipeline/output/`.
4. **Ogni modifica alla pipeline va verificata** rieseguendo:

   ```bash
   python3 pipeline/src/main.py --mese 2026-06
   ```

   e controllando le quadrature (totale Co.Ge. = totale Co.An., totale pre-ribaltamento = totale post-ribaltamento, tutti i CdC presenti). Confrontare i totali prima/dopo la modifica: se cambiano, la differenza deve essere attesa e spiegata.
5. **Niente commit di dati reali.** In `pipeline/output/` e nei dati di esempio circolano solo dati sintetici; i dati contabili veri non si versionano mai.
6. **Incrementi piccoli e verificabili:** una modifica per volta, mai rifacimenti massicci di codice di calcolo senza test di quadratura prima/dopo.

## Comandi utili

| Comando | Cosa fa |
|---|---|
| `pip install -r pipeline/requirements.txt` | Installa le dipendenze |
| `python3 pipeline/src/genera_dati_esempio.py` | Genera i dati contabili sintetici di esempio |
| `python3 pipeline/src/main.py --mese 2026-06` | Esegue l'intera pipeline per il mese indicato (ingest → validazione → ribaltamento → report) |
| `python3 pipeline/src/valida.py --mese 2026-06` | Esegue i soli controlli di validazione/quadratura del mese |
| `python3 pipeline/src/report.py --mese 2026-06` | Rigenera i soli report del mese (riesegue in memoria ingest, validazione e ribaltamento) |

Per opzioni e dettagli aggiornati fare fede a [pipeline/README.md](pipeline/README.md) e agli `argparse` degli script: in caso di dubbio leggere lo script prima di invocarlo.

## Regole operative per Claude Code

- **Prima di lavorare su qualunque tema di merito**, leggere [docs/00-contesto/questionario-contesto-aziendale.md](docs/00-contesto/questionario-contesto-aziendale.md) se compilato: contiene il contesto aziendale reale (assetto, sistemi, vincoli). Se non è compilato, segnalarlo e non dare per scontato nulla sull'azienda.
- **Usare i sub-agenti** di [.claude/agents/](.claude/agents/) per i compiti specialistici:
  - `controller-cdg` — interpretare scostamenti e scrivere commenti ai report (legge i numeri, non li calcola);
  - `data-engineer` — modifiche a pipeline, tracciati e performance (test di quadratura prima/dopo);
  - `report-builder` — template Excel/HTML e formattazione dei report;
  - `qa-quadratura` — verifica adversariale di quadrature e coerenza prima di ogni consegna.
- **Metodologia:** i principi d'uso dell'AI (autonomy slider, ciclo generazione-verifica, sicurezza dei dati, anti-pattern) sono in [docs/05-metodologia/metodologia-ai.md](docs/05-metodologia/metodologia-ai.md) e vanno rispettati.
- **Terminologia:** usare le definizioni del [glossario](docs/00-contesto/glossario.md) (CdC ausiliario/produttivo/di struttura, ribaltamento, driver, ecc.).
- **Prima di dichiarare concluso un task** che tocca dati o report: pipeline rieseguita, quadrature controllate, output ispezionato. "Fatto" senza verifica non esiste.
