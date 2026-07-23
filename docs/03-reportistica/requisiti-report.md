# Requisiti della reportistica mensile

> **Come usare questo documento.** È un template compilabile: il team AFC lo completa insieme ai destinatari dei report (responsabili di CdC, direttori di area, vertice aziendale). Ogni report previsto ha una "scheda requisito" da compilare. Le parti in *corsivo* sono esempi di risposta, da sostituire con i valori reali. I requisiti qui definiti guidano lo sviluppo del modulo [`pipeline/src/report.py`](../../pipeline/src/report.py) e vanno tenuti allineati al [catalogo KPI](catalogo-kpi.md) e al [calendario di chiusura](../01-processi/calendario-chiusura.md).

**Stato del documento**

- [ ] Bozza in compilazione
- [ ] Rivisto con i responsabili di CdC pilota
- [ ] Validato dalla direzione AFC
- Ultima revisione: `__ / __ / ____` — a cura di: `________`

---

## 1. Principi generali della reportistica

1. **Reporting per responsabilità**: ogni destinatario riceve solo i numeri di cui risponde, al livello di dettaglio adeguato al suo ruolo. Con 300+ CdC non si distribuiscono 300 report indistinti: si distribuiscono schede individuali ai responsabili e sintesi per eccezione ai livelli superiori.
2. **Un layout unico per tutti i CdC**: la scheda di centro di costo ha struttura identica per tutti i 300+ centri; cambia solo il contenuto. Nessuna personalizzazione ad hoc per singolo responsabile.
3. **Costi diretti controllabili sempre separati dai costi allocati**: il responsabile risponde dei primi; i secondi servono alla visione full cost e non generano soglie di allerta a suo carico.
4. **Gestione per eccezioni**: le soglie di evidenziazione (vedi §4) decidono che cosa merita attenzione e commento; il resto si legge solo se serve.
5. **Nessun report senza quadratura**: i report vengono pubblicati solo se i controlli di [`pipeline/src/valida.py`](../../pipeline/src/valida.py) sono passati. Un report non quadrato non esce, mai.
6. **Numeri calcolati dalla pipeline, commenti generati dall'AI, approvazione umana**: la separazione dei ruoli è descritta al §6 e nella [metodologia AI](../05-metodologia/metodologia-ai.md).

---

## 2. Destinatari e livelli di report

| Livello | Report | Destinatario | Contenuto in sintesi | Volume |
|---|---|---|---|---|
| L1 — Operativo | Scheda singolo CdC | Responsabile del centro di costo | Actual vs budget del proprio centro, mese e YTD, con commento | 1 scheda per CdC (~320/mese) |
| L2 — Direzionale di area | Sintesi per area/direzione | Direttore di funzione/area (es. Direttore di stabilimento, Direttore commerciale) | Aggregato dei CdC dell'area, ranking scostamenti interni, KPI di area | 1 per area (*es. 8-12/mese*) |
| L3 — Vertice | Top scostamenti aziendali | Imprenditore / CFO / Comitato di direzione | I 10-15 scostamenti più rilevanti a livello azienda, quadro sintetico, forecast full-year | 1/mese |

**Domande da compilare**

- Quante aree/direzioni esistono nella gerarchia dei CdC (livello 2 della gerarchia definita in [piano-centri-di-costo.md](../02-dati/piano-centri-di-costo.md))? `____` — *es. 9: Produzione VR, Produzione BS, Logistica, Commerciale Italia, Commerciale Export, Acquisti, AFC, HR, IT*
- Chi riceve il report L3 oltre all'imprenditore? `________________` — *es. CFO, Direttore Generale*
- Esistono destinatari "in copia" (es. controller di stabilimento riceve tutte le schede L1 del suo stabilimento)? `________________`
- Serve una versione consolidata per il Collegio Sindacale / soci? `[ ] Sì [ ] No` — se sì, con quale frequenza? `________`

---

## 3. Schede requisito per report

> Compilare una scheda per ogni report. Le tre schede seguenti sono pre-impostate sui tre livelli standard; duplicare la scheda vuota in fondo per eventuali report aggiuntivi.

### 3.1 Scheda requisito — Report L1: Scheda singolo CdC

| Campo | Valore da compilare |
|---|---|
| Nome report | Scheda mensile centro di costo |
| Codice identificativo | `RPT-L1-CDC` |
| Destinatario | Responsabile del CdC (campo `responsabile` dell'anagrafica [`centri_di_costo.csv`](../../pipeline/config/centri_di_costo.csv)) |
| Contenuto | Costi per natura del singolo CdC, sezione costi diretti controllabili + sezione costi allocati, FTE, commento automatico approvato |
| Formato | `[x] Excel  [ ] HTML  [ ] PDF` — *un file Excel per responsabile; se un responsabile ha più CdC, un file con un foglio per CdC* |
| Frequenza | `[x] Mensile  [ ] Trimestrale` |
| Giorno di consegna target | `WD __` — *es. WD5 del calendario di chiusura* |
| Canale di distribuzione | `________` — *es. cartella condivisa `report/AAAA-MM/` + email con link* |
| Ordinamento righe | *Per natura di costo, ordine del piano dei conti gestionale* |
| Note | `________` |

**Colonne richieste** (spuntare quelle da includere):

- [x] Actual mese
- [x] Budget mese
- [x] Scostamento assoluto mese (Actual − Budget)
- [x] Scostamento % mese
- [x] Actual YTD
- [x] Budget YTD
- [x] Scostamento assoluto YTD
- [x] Scostamento % YTD
- [x] Actual anno precedente (stesso periodo YTD)
- [x] Forecast full-year (quando disponibile, da Fase 5 della [roadmap](../04-roadmap/roadmap.md))
- [ ] Ultimo forecast mese (actual vs forecast, oltre che vs budget)
- [ ] Trend ultimi 12 mesi (mini-tabella o grafico)
- Altre colonne richieste: `________________`

### 3.2 Scheda requisito — Report L2: Sintesi per area/direzione

| Campo | Valore da compilare |
|---|---|
| Nome report | Sintesi mensile di area |
| Codice identificativo | `RPT-L2-AREA` |
| Destinatario | Direttore di area/funzione |
| Contenuto | Totale area per natura di costo; elenco dei CdC dell'area con actual/budget/scostamento; ranking dei CdC per scostamento; KPI di area dal [catalogo KPI](catalogo-kpi.md); elenco CdC sopra soglia con stato del commento |
| Formato | `[ ] Excel  [x] HTML  [ ] PDF` — *pagina HTML statica navigabile + Excel di dettaglio in allegato* |
| Frequenza | `[x] Mensile` |
| Giorno di consegna target | `WD __` — *es. WD5* |
| Canale di distribuzione | `________` |
| Colonne | Le stesse del report L1, aggregate per CdC (una riga per CdC, non per natura) |
| Note | `________` |

### 3.3 Scheda requisito — Report L3: Top scostamenti per il vertice

| Campo | Valore da compilare |
|---|---|
| Nome report | Top scostamenti e quadro mensile |
| Codice identificativo | `RPT-L3-TOP` |
| Destinatario | Imprenditore / CFO / Comitato di direzione |
| Contenuto | Quadro azienda (totale costi actual vs budget, mese e YTD); top `__` scostamenti per valore assoluto (*es. 15*) con CdC, natura, importo, %, commento sintetico; scostamenti ricorrenti (sopra soglia da ≥ `__` mesi consecutivi, *es. 3*); stima full-year; stato del processo di chiusura (giorni impiegati, anomalie intercettate) |
| Formato | `[ ] Excel  [ ] HTML  [x] PDF` — *1-2 pagine, leggibile da mobile* |
| Frequenza | `[x] Mensile` |
| Giorno di consegna target | `WD __` — *es. WD5, dopo la review dei commenti* |
| Canale di distribuzione | `________` — *es. email diretta* |
| Criterio di selezione dei top scostamenti | *\|scostamento assoluto\| decrescente, solo righe sopra soglia rossa; pareggi risolti per scostamento %* |
| Note | `________` |

### 3.4 Scheda requisito vuota (da duplicare per report aggiuntivi)

| Campo | Valore da compilare |
|---|---|
| Nome report | `________` |
| Codice identificativo | `RPT-__-____` |
| Destinatario | `________` |
| Contenuto | `________` |
| Colonne | `________` |
| Soglie di evidenziazione | `________` |
| Formato | `[ ] Excel  [ ] HTML  [ ] PDF` |
| Frequenza | `________` |
| Giorno di consegna target | `WD __` |
| Canale di distribuzione | `________` |
| Note | `________` |

---

## 4. Soglie di evidenziazione

Le soglie sono **combinate** (percentuale **e** valore assoluto insieme), per evitare falsi allarmi su importi piccoli e per non perdere scostamenti grandi in percentuale modesta. Si applicano ai **soli costi diretti controllabili**; i costi allocati sono esposti ma non generano allerta sul CdC ricevente.

| Livello | Condizione (proposta da validare) | Effetto nel report | Obbligo di commento |
|---|---|---|---|
| Verde | sotto soglia gialla | nessuna evidenza | no |
| Giallo (attenzione) | \|Δ%\| > `5` % **e** \|Δ\| > `2.500` € | cella evidenziata | commento AI, revisione facoltativa del responsabile |
| Rosso (allerta) | \|Δ%\| > `10` % **e** \|Δ\| > `5.000` € | riga evidenziata + inclusa nei report L2/L3 | commento AI + presa visione obbligatoria del responsabile |
| Ricorrente | sopra soglia gialla per ≥ `3` mesi consecutivi | flag "ricorrente" in L2/L3 | escalation al direttore di area |

**Da compilare / validare con i responsabili:**

- Le soglie valgono sia sul mese sia sull'YTD? `[ ] Solo mese  [ ] Solo YTD  [x] Entrambi (proposta)`
- Soglie differenziate per dimensione del CdC (es. % più stretta per centri con budget > 1 M€)? `[ ] Sì [ ] No` — se sì, regola: `________`
- Gli scostamenti **favorevoli** (actual < budget) sopra soglia vanno evidenziati? `[x] Sì (proposta: stessa soglia, colore distinto)  [ ] No` — *un risparmio anomalo spesso segnala costi non registrati o fasature, non efficienza*
- Approvazione delle soglie: nome `________` data `__ / __ / ____`

---

## 5. Mock della scheda CdC tipo (report L1)

> **ATTENZIONE: tutti i numeri, i nomi e i codici di questo mock sono FITTIZI**, inventati a solo scopo illustrativo del layout. Non rappresentano alcuna azienda reale. I codici seguono lo schema di codifica **target** definito in [piano-centri-di-costo.md, sez. 3](../02-dati/piano-centri-di-costo.md) (es. `P142`); l'anagrafica demo della pipeline usa invece codici parlanti (es. `S1-PRD-001`).

**Scheda centro di costo — periodo 2026-06**

| Campo | Valore |
|---|---|
| CdC | `P142 — Reparto Confezionamento` |
| Stabilimento | Verona |
| Responsabile | M. Rossi |
| Tipo centro | Produttivo |
| FTE medi del mese | 14,5 (budget: 14,0) |

**Sezione A — Costi diretti controllabili** (importi in €)

| Natura di costo | Actual mese | Budget mese | Δ mese | Δ% mese | Actual YTD | Budget YTD | Δ YTD | Δ% YTD | Actual YTD a.p. | Forecast FY |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Personale | 52.300 | 50.000 | +2.300 | +4,6% | 305.100 | 300.000 | +5.100 | +1,7% | 289.400 | 612.000 |
| Materiali di consumo | 18.700 | 12.500 | **+6.200** | **+49,6%** | 81.200 | 75.000 | +6.200 | +8,3% | 72.800 | 158.000 |
| Servizi (manutenzioni) | 6.100 | 9.000 | −2.900 | −32,2% | 49.800 | 54.000 | −4.200 | −7,8% | 51.200 | 105.000 |
| Godimento beni di terzi | 3.000 | 3.000 | 0 | 0,0% | 18.000 | 18.000 | 0 | 0,0% | 17.400 | 36.000 |
| Ammortamenti | 7.400 | 7.400 | 0 | 0,0% | 44.400 | 44.400 | 0 | 0,0% | 41.900 | 88.800 |
| Altri costi operativi | 1.150 | 1.300 | −150 | −11,5% | 7.600 | 7.800 | −200 | −2,6% | 7.100 | 15.400 |
| **Totale costi diretti** | **88.650** | **83.200** | **+5.450** | **+6,6%** | **506.100** | **499.200** | **+6.900** | **+1,4%** | **479.800** | **1.015.200** |

**Sezione B — Costi allocati da ribaltamento** (informativi, non controllabili dal responsabile)

| Centro erogante | Driver | Actual mese | Budget mese | Δ mese | Actual YTD | Budget YTD |
|---|---|---:|---:|---:|---:|---:|
| A021 Manutenzione centrale | ore_intervento | 4.200 | 3.800 | +400 | 24.100 | 22.800 |
| A034 Utilities stabilimento VR | consumo_kwh | 9.850 | 9.200 | +650 | 61.400 | 55.200 |
| S007 Servizi generali VR | mq_occupati | 2.100 | 2.100 | 0 | 12.600 | 12.600 |
| **Totale costi allocati** | | **16.150** | **15.100** | **+1.050** | **98.100** | **90.600** |

**Totale full cost del CdC**: mese 104.800 € (budget 98.300 €, Δ +6.500 €); YTD 604.200 € (budget 589.800 €, Δ +14.400 €).

**Commento (generato dall'AI, approvato da: G. Bianchi, controller — 06/07/2026):**

> Nel mese di giugno il centro P142 registra costi diretti per 88.650 €, superiori al budget di 5.450 € (+6,6%). Lo scostamento principale riguarda i materiali di consumo (+6.200 €, +49,6% sul mese), che da soli spiegano l'intero superamento; il dato YTD (+8,3%) indica che il fenomeno si è concentrato nel mese. In direzione opposta, i servizi di manutenzione risultano inferiori al budget di 2.900 € nel mese (−32,2%), coerentemente con un YTD sotto budget del 7,8%: possibile slittamento di interventi pianificati, da verificare con il centro A021. Il costo del personale eccede il budget mensile di 2.300 € (+4,6%), in presenza di 0,5 FTE medi sopra il previsto. Si segnala che i materiali di consumo superano la soglia di allerta: commento del responsabile richiesto.

---

## 6. Regole per il commento automatico AI

Regole vincolanti per il modulo di generazione dei commenti (dettaglio tecnico in [metodologia-ai.md](../05-metodologia/metodologia-ai.md)):

1. **L'AI commenta esclusivamente numeri calcolati dalla pipeline.** Il prompt contiene la tabella scostamenti già calcolata (CdC, natura, actual, budget, delta, delta %, YTD, anno precedente, FTE, flag soglia) in formato strutturato. L'AI non esegue calcoli, non stima, non arrotonda per conto proprio, non introduce cifre nuove.
2. **Validazione automatica a valle**: ogni cifra citata nel commento deve esistere nella tabella di input; in caso contrario il commento viene scartato e rigenerato, e dopo `2` tentativi falliti il CdC viene marcato "commento manuale richiesto".
3. **Formato del commento**: da 3 a 5 frasi, in italiano professionale. Struttura attesa: (a) quadro d'insieme del mese (totale actual vs budget); (b) evidenza dei **3 scostamenti principali** per valore assoluto, con importo e percentuale; (c) causa **solo se desumibile dai dati disponibili** (es. FTE sopra budget, fasatura evidente dal confronto mese/YTD, driver di ribaltamento variato), altrimenti formula esplicita "da approfondire con il responsabile" — mai cause inventate.
4. **Tono neutro e fattuale**: nessuna colpevolizzazione, nessun giudizio sulle persone, nessun superlativo, nessuna raccomandazione operativa non richiesta. Il commento descrive, non prescrive.
5. **Perimetro**: il commento riguarda i costi diretti controllabili; i costi allocati si citano solo se lo scostamento allocato supera la soglia gialla, indicando il centro erogante.
6. **Revisione umana obbligatoria**: nessun commento viene distribuito senza approvazione esplicita di un controller. Il flusso è: pipeline → bozza AI → coda di revisione → approvazione/modifica/riscrittura → pubblicazione. Il report riporta nome dell'approvatore e data (come nel mock al §5).
7. **Tracciabilità**: per ogni commento si conservano bozza AI originale, versione approvata, autore della revisione, modello e versione del prompt utilizzati.
8. **Lingua e terminologia**: italiano; termini del [glossario](../00-contesto/glossario.md); i termini tecnici consolidati (budget, forecast, actual, YTD) restano in inglese.

**Da compilare:**

- Chi approva i commenti L1? `________` — *es. controller di stabilimento per i CdC produttivi, controller centrale per gli altri*
- Chi approva il commento di sintesi L3? `________` — *es. CFO*
- Tempo massimo dedicato alla revisione per ciclo mensile: `____ ore` — *es. 4 ore totali; se superato, rivedere soglie o prompt*

---

## 7. Requisiti non funzionali

- [ ] Tempo di generazione dell'intero pacchetto report < `15` minuti dal completamento della quadratura
- [ ] Nomi file convenzionali: `RPT-L1_<codice CdC>_<AAAA-MM>.xlsx`, `RPT-L2_<area>_<AAAA-MM>.html`, `RPT-L3_<AAAA-MM>.pdf`
- [ ] Archiviazione storica di tutti i report pubblicati in `report/AAAA-MM/` (non sovrascrivere mai un report già distribuito: le rettifiche generano versione `_rev2`)
- [ ] Ogni report riporta: periodo, data/ora di generazione, versione dei dati di origine, esito dei controlli di quadratura
- [ ] Accessibilità: gli Excel devono essere leggibili senza macro; l'HTML senza dipendenze da server applicativi
