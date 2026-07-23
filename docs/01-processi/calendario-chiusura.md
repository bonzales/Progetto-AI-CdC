# Calendario di chiusura mensile — Fast closing

> **Tipo documento:** template compilabile · **Owner del calendario:** Controllo di Gestione (process owner) · **Stato:** ☐ bozza ☐ condiviso ☐ in vigore
>
> **Obiettivo dichiarato: reporting pack per CdC pubblicato entro WD5, con limite massimo WD8.**
> "WDn" (*working day n*, come da [glossario](../00-contesto/glossario.md)) = n-esimo **giorno lavorativo** del mese successivo a quello di chiusura. Il calendario va pubblicato e condiviso con tutti gli attori: ogni task ha un owner e una scadenza (giorno e, dove serve, orario), e lo stato viene aggiornato a ogni chiusura.

Riferimenti: il flusso delle attività è descritto in [processo-to-be.md](processo-to-be.md); il confronto con i tempi attuali è nella baseline di [processo-as-is.md](processo-as-is.md).

---

## 1. Istruzioni per l'uso del template

- [ ] Adattare attività e responsabili alla propria organizzazione: le righe precompilate riflettono un fast closing tipico e vanno corrette, non prese alla lettera.
- [ ] Sostituire i ruoli in corsivo con **nomi e cognomi**: un task senza owner nominale è un task in ritardo.
- [ ] Dove indicato un orario (es. "entro le 13:00"), è la deadline oltre la quale i task a valle slittano di un giorno.
- [ ] Duplicare questo file (o la sola tabella) per ogni chiusura mensile, aggiornando la colonna **Stato**: ☐ da fare / [IC] in corso / [OK] fatto / [RIT] in ritardo.
- [ ] A fine chiusura compilare il post-mortem (sezione 5) e riportare i KPI di closing.
- [ ] Regola di materialità: la chiusura mensile è un **soft close** — sopra la soglia di materialità concordata (es. 5.000 € per singola posta) si registra, sotto si stima o si rinvia; l'hard close con criteri completi resta trimestrale/annuale. Soglia adottata: _____ €.

---

## 2. Pre-close — ultimi 3 giorni lavorativi del mese (GG−3 → GG−0)

Il fast closing si vince **prima** della fine del mese: tutto ciò che è anticipabile va anticipato.

| Quando | Attività | Responsabile | Sistema | Stato |
|---|---|---|---|---|
| GG−3 | Congelamento anagrafiche del periodo: nessuna apertura/chiusura CdC, nessuna modifica a mapping conti e driver con effetto sul mese in chiusura | *Controller (owner anagrafiche)* | Git / anagrafiche versionate | ☐ |
| GG−3 | Pulizia ordini di acquisto aperti: sollecito chiusura/annullamento ordini evasi non fatturati | *Ufficio acquisti* | ERP | ☐ |
| GG−2 | Verifica registrazioni intercompany e circolarizzazione saldi (se applicabile) | *Contabilità generale* | ERP / email | ☐ |
| GG−2 | Aggiornamento valori driver del mese (headcount/FTE, mq, ore macchina, ticket, righe d'ordine) | *HR / Operations / IT* | Export gestionali → `inbox/` | ☐ |
| GG−1 | Cut-off logistico: bolle di entrata/uscita del mese tutte registrate, istruzioni di cut-off a magazzino | *Logistica* | ERP / WMS | ☐ |
| GG−1 | Pre-fatturazione attiva: emissione fatture su consegne del mese | *Contabilità clienti* | ERP | ☐ |
| GG−0 | Comunicazione "ultimo giorno utile registrazioni fornitori" ai reparti; da qui in poi si va di accrual da ordini | *Contabilità fornitori* | Email / ERP | ☐ |

---

## 3. Calendario giorno per giorno (WD1 → WD8)

> Target: **pubblicazione a WD5**. I giorni WD6→WD8 sono il buffer massimo tollerato (es. mesi con festività, chiusure trimestrali, anomalie dati). Se si sfora WD8 sistematicamente, il problema è strutturale: vedi sezione 4.

| Giorno | Entro | Attività | Responsabile | Sistema | Stato |
|---|---|---|---|---|---|
| **WD1** | 11:00 | Chiusura subledger cespiti: ammortamenti mensili calcolati e registrati | *Contabilità cespiti* | ERP | ☐ |
| **WD1** | 13:00 | Chiusura magazzino: valorizzazione giacenze e WIP con cut-off verificato | *Logistica / Contabilità* | ERP / WMS | ☐ |
| **WD1** | 17:00 | Costo del personale del mese: dati payroll definitivi **oppure** costo standard con conguaglio al mese successivo | *Payroll / HR* | Gestionale paghe → `inbox/` | ☐ |
| **WD2** | 11:00 | Fatture da ricevere generate sistematicamente da ordini/entrata merci (logica GR/IR); integrazioni manuali solo sopra soglia di materialità | *Contabilità fornitori* | ERP | ☐ |
| **WD2** | 13:00 | Ratei e risconti mensilizzati: 13ª/14ª, ferie/permessi, bonus e premi, canoni e assicurazioni annuali, manutenzioni | *Contabilità generale* | ERP (scritture ricorrenti automatizzate) | ☐ |
| **WD2** | 17:00 | Riconciliazione intercompany chiusa; ultime registrazioni Co.Ge. del periodo; **blocco del periodo contabile** | *Contabilità generale* | ERP | ☐ |
| **WD3** | 09:00 | Export automatici ERP nel drop folder (`movimenti_AAAA-MM.csv`, movimenti analitici, paghe, driver) e run della pipeline: ingest, validazione, controlli bloccanti C1-C7 | *Pipeline (automatico); presidio: Controller* | Pipeline ([`pipeline/README.md`](../../pipeline/README.md)) | ☐ |
| **WD3** | 11:00 | Gestione anomalie eventuali: correzioni a monte e rilancio del run (idempotente) | *Controller + Contabilità* | ERP / Pipeline | ☐ |
| **WD3** | 15:00 | Ribaltamenti a cascata su actual, budget e forecast; quadratura Co.Ge./Co.An. e controlli C8-C10 superati; **primo conto economico per CdC disponibile** | *Pipeline (automatico); presidio: Controller* | Pipeline | ☐ |
| **WD4** | 10:00 | Calcolo scostamenti (mese, YTD, full-year) e flag eccezioni sopra soglia; generazione bozze report per CdC e sintesi direzionale; commenti AI in bozza sui CdC sopra soglia | *Pipeline (automatico)* | Pipeline + API Claude | ☐ |
| **WD4** | 17:00 | Analisi delle eccezioni e revisione dei commenti AI da parte dei controller; approfondimenti con i responsabili operativi dove serve | *Controller* | Report bozza | ☐ |
| **WD5** | 11:00 | Review finale del pacchetto con CFO/direzione AFC; eventuali rettifiche → rilancio run | *CFO + Controller* | Report bozza | ☐ |
| **WD5** | 13:00 | **Approvazione formale** del pacchetto (tracciata: chi, quando, versione del run) | *CFO / Resp. CdG* | Pipeline / log approvazioni | ☐ |
| **WD5** | 15:00 | **Pubblicazione e distribuzione**: `report/YYYY-MM/` su cartella condivisa/SharePoint + email automatiche a ogni responsabile di CdC; sintesi alla direzione | *Pipeline (automatico, post-approvazione)* | SharePoint / email | ☐ |
| **WD6** | — | *Buffer:* slittamenti da festività o anomalie; raccolta commenti dei responsabili sugli scostamenti sopra soglia | *Responsabili CdC* | Modulo commenti / email | ☐ |
| **WD7** | — | *Buffer:* consolidamento commenti dei responsabili; risposte a richieste di chiarimento | *Controller* | — | ☐ |
| **WD8** | 17:00 | **Limite massimo**: pacchetto pubblicato in ogni caso; post-mortem della chiusura e aggiornamento KPI di closing (sezione 5) | *Team AFC* | — | ☐ |

> Nota trimestrale: nei mesi di chiusura trimestrale (hard close) aggiungere le attività specifiche (inventari fisici, valutazioni complete, riconciliazioni estese) e considerare il target a WD8 anziché WD5.

---

## 4. Prerequisiti per accorciare i tempi e colli di bottiglia tipici

### 4.1 Prerequisiti (senza questi il fast closing non parte)

- [ ] **CdC obbligatorio all'origine** su ogni registrazione di costo (fattura passiva, prima nota, paghe, ammortamenti): elimina le imputazioni analitiche a posteriori.
- [ ] **Scritture ricorrenti automatizzate** in ERP per ratei, risconti e ammortamenti mensili: nessuna raccolta manuale a fine mese.
- [ ] **Fatture da ricevere da ciclo passivo** (ordini/entrata merci) e non da email ai reparti.
- [ ] **Contratto dati scritto con l'ERP/partner**: nomi file, tracciati, encoding, orari degli export schedulati (vedi [inventario-fonti-dati.md](../02-dati/inventario-fonti-dati.md)).
- [ ] **Anagrafiche sotto governance**: anagrafica CdC, mapping conto→natura e tabella driver versionati, con congelamento nel periodo di chiusura.
- [ ] **Calendario pubblicato** con owner nominali e orari, visibile a tutti gli attori; escalation definita per i ritardi.
- [ ] **Soglia di materialità formalizzata** per il soft close mensile.
- [ ] **Pipeline collaudata** (livello A1 del [processo TO-BE](processo-to-be.md#5-livelli-di-automazione-progressivi-autonomy-slider) completato): quadrature automatiche affidabili.

### 4.2 Colli di bottiglia tipici e rimedi

| Collo di bottiglia | Sintomo | Rimedio |
|---|---|---|
| Fatture passive in ritardo | "Aspettiamo l'ultima fattura" e la chiusura slitta di giorni | Accrual sistematici da ordini/entrata merci (GR/IR); sotto soglia di materialità non si aspetta nessuno |
| Payroll tardivo | Il costo del personale arriva a WD5 o oltre | Costo standard per CdC a WD1 con conguaglio sul mese successivo |
| Intercompany non riconciliato | Delta IC scoperti a ridosso della pubblicazione | Riconciliazione continua in corso di mese; cut-off IC anticipato a GG−2 |
| Inventari e cut-off logistico | Rettifiche di magazzino tardive che riaprono il conto economico | Cut-off rigoroso su bolle a GG−1; conte cicliche in corso d'anno invece dell'inventario "monstre" |
| Excel manuali nel percorso critico | Un file, una persona, nessun versioning: basta un'assenza per fermare tutto | Sostituzione con la pipeline versionata; gli Excel residui censiti in [processo-as-is.md](processo-as-is.md#4-inventario-dei-file-excel-attuali) e progressivamente dismessi |
| Imputazioni analitiche a posteriori | Centinaia di righe senza CdC da riattribuire a mano | CdC obbligatorio all'origine + regole di derivazione automatica; classificazione assistita AI solo come proposta con revisione umana |
| Anomalie dati scoperte tardi | Quadrature fatte a report già impaginato | Controlli bloccanti C1-C10 a WD3, prima di ogni report (vedi [matrice controlli](processo-to-be.md#3-matrice-dei-controlli-automatici)) |
| Rettifiche post-pubblicazione | Versioni multiple del "numero ufficiale" in circolazione | Run idempotente per periodo + approvazione tracciata: una sola versione ufficiale; le rettifiche tardive confluiscono nel mese successivo o in un ri-run dichiarato |
| Attori senza deadline | Ognuno consegna "quando può" | Calendario con owner e orario per ogni task; stato aggiornato ogni giorno; escalation al CFO sui ritardi ripetuti |

---

## 5. Post-mortem e KPI di closing

Da compilare a ogni chiusura (15 minuti, team AFC): il calendario migliora solo se viene misurato.

| KPI | Target | Mese ____ | Note |
|---|---|---|---|
| Giorno lavorativo di pubblicazione | ≤ WD5 (max WD8) | *es. WD6* | |
| Task completati in ritardo rispetto alla deadline | 0 | | *quali e perché* |
| Numero di run della pipeline necessari | ≤ 2 | | *anomalie incontrate* |
| Rettifiche post-pubblicazione | 0 | | *causa radice* |
| Controlli bloccanti falliti al primo run | ≤ 2 | | *quali (C1-C12)* |
| % commenti AI pubblicati senza modifiche sostanziali | crescente | | |

**Azioni di miglioramento decise questo mese:**

- [ ] *es. anticipare l'export driver HR a GG−3 perché arrivato tardi due mesi su tre*
- [ ] …

---

*Documenti collegati: [processo-as-is.md](processo-as-is.md) (baseline dei tempi attuali), [processo-to-be.md](processo-to-be.md) (flusso e controlli), [roadmap.md](../04-roadmap/roadmap.md) (quando entrano in vigore i target).*
