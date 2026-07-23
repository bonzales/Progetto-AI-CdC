# Mappa degli stakeholder

> **Template da compilare.** Sostituire i segnaposto `[Nome]` con le persone reali, adattare i ruoli alla propria organizzazione (aggiungere o togliere righe) e validare la colonna RACI in sede di kickoff. La mappa va tenuta aggiornata: è il riferimento per capire chi coinvolgere su ogni decisione del progetto.

Le persone indicate qui devono essere coerenti con le risposte della sezione B del [questionario di contesto aziendale](questionario-contesto-aziendale.md).

## Legenda RACI

| Sigla | Significato | In pratica |
|---|---|---|
| **R** | Responsible | Esegue il lavoro |
| **A** | Accountable | Risponde del risultato e decide (uno solo per attività) |
| **C** | Consulted | Consultato prima delle decisioni |
| **I** | Informed | Informato dopo le decisioni |

## Tabella degli stakeholder

| Ruolo | Nome | Funzione aziendale | Interesse nel progetto | RACI complessivo | Canale preferito |
|---|---|---|---|---|---|
| Imprenditore / CFO (sponsor) | [Nome] | Direzione / AFC | Visione tempestiva e affidabile dei costi per decidere; ritorno dell'investimento del progetto | **A** | *es.: riunione quindicinale + sintesi email* |
| Controller (project owner operativo) | [Nome] | Controllo di gestione | Ridurre il lavoro manuale, governare modello dati, ribaltamenti e reportistica | **R** | *es.: canale Teams/Slack dedicato, quotidiano* |
| Responsabile amministrativo | [Nome] | Amministrazione / Co.Ge. | Chiusure mensili sostenibili; quadratura Co.Ge.-Co.An.; qualità delle registrazioni all'origine | **R/C** | *es.: email + incontro in fase di chiusura (WD1-WD3)* |
| Referente IT / sistemi | [Nome] | IT interno o fornitore ERP | Fattibilità delle estrazioni, accessi, sicurezza, policy cloud/AI | **C** (R sulle estrazioni) | *es.: ticket + call su necessità* |
| Responsabili di CdC — capofila produzione | [Nome] | Produzione / stabilimento | Report utili e leggibili; driver e soglie percepiti come equi; costi controllabili distinti da quelli allocati | **C** | *es.: incontro mensile di review scostamenti* |
| Responsabili di CdC — capofila area staff | [Nome] | Es.: HR, Logistica, Commerciale | Come sopra, per i centri di spesa | **C** | *es.: incontro mensile di review scostamenti* |
| Consulente / commercialista | [Nome] | Studio esterno | Coerenza con bilancio civilistico e adempimenti; tempi di consegna dei dati contabili (se la contabilità è esterna) | **C/I** | *es.: email + call trimestrale* |
| Payroll / consulente del lavoro | [Nome] | Interno o studio esterno | Fornitura mensile del costo del personale con dettaglio per CdC, nei tempi del calendario di chiusura | **C/I** | *es.: email con scadenza fissa mensile* |
| DPO / referente privacy *(se presente)* | [Nome] | Compliance | Rispetto dei vincoli su dati personali e uso di servizi AI (sezione I del questionario) | **C** | *es.: email, coinvolgimento su richiesta* |

> **Nota sui responsabili di CdC:** con 300+ centri non vanno mappati tutti qui, ma per ogni direzione/area va indicato un **capofila** che partecipa alla definizione di driver, soglie e layout dei report e fa da portavoce dei colleghi. L'elenco completo responsabile-per-centro vive nell'anagrafica CdC ([../02-dati/piano-centri-di-costo.md](../02-dati/piano-centri-di-costo.md)).

## Matrice RACI per macro-attività

Compilare con le sigle R/A/C/I (una sola **A** per riga).

| Attività | Sponsor (CFO) | Controller | Resp. amm.vo | IT | Capofila CdC | Consulente |
|---|---|---|---|---|---|---|
| Compilazione questionario di contesto | A | R | R | C | C | C |
| Disegno gerarchia e anagrafica CdC | A | R | C | I | C | I |
| Definizione driver e regole di ribaltamento | A | R | C | I | C | I |
| Estrazioni dati e automazione pipeline | I | A | C | R | I | I |
| Calendario di chiusura (fast closing) | A | R | R | C | I | C |
| Layout report e soglie di eccezione | A | R | I | I | C | I |
| Validazione quadratura con bilancio | A | R | R | I | I | C |
| Change management e formazione responsabili | A | R | I | I | C | I |

## Cerimonie di progetto

| Cerimonia | Scopo | Partecipanti | Frequenza | Durata | Quando |
|---|---|---|---|---|---|
| **Kickoff** | Condividere obiettivi, perimetro, ruoli (questa mappa) e piano; consegnare il questionario | Tutti gli stakeholder della tabella | Una tantum | 2 ore | [data] |
| **Stato avanzamento (SAL)** | Verificare avanzamento, rimuovere blocchi, decidere le priorità della fase successiva | Sponsor, controller, IT (+ altri su necessità) | Quindicinale in fase di costruzione | 45 min | [giorno/ora fissi] |
| **Review di chiusura mensile** | Analizzare il reporting pack, gli scostamenti sopra soglia e i commenti dei responsabili | Sponsor, controller, capofila CdC | Mensile (entro WD5-WD7) | 1-1,5 ore | [es.: primo lunedì utile dopo WD5] |
| **Post-mortem del closing** | Esaminare i KPI del processo (giorni di chiusura, task in ritardo, rettifiche post-pubblicazione) e migliorare il calendario | Controller, resp. amministrativo, IT | Mensile, subito dopo la pubblicazione | 30 min | [data/ora] |
| **Comitato anagrafiche e regole** | Approvare aperture/chiusure CdC, modifiche a mapping conti, driver e soglie (data governance) | Controller (A), resp. amministrativo, capofila CdC interessati | Trimestrale (o su richiesta) | 1 ora | [date] |
| **Retrospettiva di fase / go-live** | A fine di ogni fase della [roadmap](../04-roadmap/roadmap.md): cosa ha funzionato, cosa cambiare | Tutti gli stakeholder principali | A fine fase | 1 ora | [date] |

## Regole di comunicazione ed escalation

- [ ] Definire il canale unico ufficiale del progetto (cartella condivisa / Teams / altro): ______
- [ ] Ogni decisione su anagrafiche, driver e soglie viene verbalizzata (anche 3 righe) e archiviata nel repository
- [ ] Percorso di escalation: blocco operativo → controller; conflitto su regole/driver → sponsor (CFO); tempi di risposta attesi: ______
- [ ] Aggiornare questa mappa a ogni cambio di persone o di ruoli
