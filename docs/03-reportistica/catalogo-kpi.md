# Catalogo KPI del controllo di gestione

> **Come usare questo documento.** Catalogo di partenza dei KPI per il controllo di gestione per centri di costo, organizzato per area. Va **validato con i responsabili di area**: ogni KPI adottato deve avere formula condivisa, fonte dati disponibile mensilmente e soglia di attenzione accettata da chi ne risponde — l'accettazione del modello da parte dei responsabili è condizione di funzionamento, non un optional. Le soglie indicate in *corsivo* sono proposte di esempio da sostituire con i valori concordati. I KPI selezionati alimentano i report definiti in [requisiti-report.md](requisiti-report.md); le fonti dati citate devono trovare riscontro nell'[inventario fonti dati](../02-dati/inventario-fonti-dati.md).

**Stato del documento**

- [ ] Bozza in compilazione
- [ ] KPI di produzione validati con i responsabili — data: `__ / __ / ____`
- [ ] KPI commerciali validati — data: `__ / __ / ____`
- [ ] KPI di logistica validati — data: `__ / __ / ____`
- [ ] KPI di staff/struttura validati — data: `__ / __ / ____`
- [ ] Soglie approvate dalla direzione AFC — data: `__ / __ / ____`

## Criteri di ammissione di un KPI al catalogo

Un KPI entra nel set mensile solo se rispetta tutti i criteri:

- [ ] **Causale**: misura qualcosa su cui il responsabile del CdC può agire.
- [ ] **Calcolabile in automatico**: numeratore e denominatore disponibili da una fonte dell'inventario, con frequenza almeno pari a quella del KPI.
- [ ] **Definito senza ambiguità**: formula scritta, perimetro chiaro (quali CdC, quali nature di costo).
- [ ] **Accettato**: il responsabile di area ha validato formula e soglia.
- [ ] **Confrontabile nel tempo**: la definizione non cambia in corso d'anno (le modifiche decorrono dal 1° gennaio successivo, salvo errori di formula).

---

## 1. KPI di produzione

| # | KPI | Formula | Fonte dati | Frequenza | Soglia di attenzione (proposta) |
|---|---|---|---|---|---|
| P1 | Costo orario di trasformazione | Costi diretti CdC produttivo / ore macchina (o ore MOD) del periodo | Co.An. (pipeline) + MES/rilevazione ore | Mensile | *> +5% vs standard di budget* |
| P2 | Efficienza produttiva (OEE semplificato) | Ore produttive effettive / ore disponibili | MES / rilevazioni di reparto | Mensile | *< 75%* |
| P3 | Varianza su costi standard | (Costo effettivo − costo standard) × volumi, scomposta in volume/prezzo/efficienza | Co.An. + distinte/standard ERP | Mensile | *\|varianza\| > 3% del costo standard del CdC* |
| P4 | Incidenza scarti e rilavorazioni | Costo scarti + rilavorazioni / costo di produzione del CdC | MES + Co.An. | Mensile | *> 2%* |
| P5 | Incidenza straordinari | Ore straordinario / ore ordinarie lavorate | Payroll (rilevazione presenze) | Mensile | *> 8% per 2 mesi consecutivi* |
| P6 | Costo manutenzione per macchina/linea | Costi di manutenzione attribuiti / n. macchine (o ore macchina) | Co.An. + CMMS/ordini di manutenzione | Mensile | *> +10% vs media mobile 12 mesi* |
| P7 | Consumo energia per unità prodotta | kWh (o Smc) del CdC / unità prodotte | Contatori di reparto / bollette ripartite + MES | Mensile | *> +8% vs stesso mese anno precedente* |

## 2. KPI commerciali

| # | KPI | Formula | Fonte dati | Frequenza | Soglia di attenzione (proposta) |
|---|---|---|---|---|---|
| KC1 | Incidenza costi commerciali | Costi CdC commerciali / ricavi del periodo | Co.An. + Co.Ge. ricavi | Mensile | *> valore di budget +0,5 punti* |
| KC2 | Costo per ordine acquisito | Costi CdC commerciali / n. ordini cliente acquisiti | Co.An. + ERP vendite | Mensile | *> +10% vs budget* |
| KC3 | Incidenza provvigioni | Provvigioni maturate / ricavi da agenti | Co.Ge./payroll agenti + ERP vendite | Mensile | *fuori dal range contrattuale atteso ±0,3 punti* |
| KC4 | Costo trasferte per persona commerciale | Costi di trasferta CdC commerciali / FTE commerciali | Co.An. (natura trasferte) + HR | Mensile | *> +15% vs budget YTD* |
| KC5 | Costo di acquisizione cliente (CAC) | Costi commerciali + marketing del periodo / n. nuovi clienti attivi | Co.An. + CRM | Trimestrale | *> +20% vs media 4 trimestri* |

## 3. KPI di logistica

| # | KPI | Formula | Fonte dati | Frequenza | Soglia di attenzione (proposta) |
|---|---|---|---|---|---|
| KL1 | Costo per riga d'ordine spedita | Costi CdC logistici / n. righe d'ordine spedite | Co.An. + WMS/ERP | Mensile | *> +5% vs budget* |
| KL2 | Costo trasporto per unità di peso | Costi di trasporto / kg (o kg×km) spediti | Co.An. (natura trasporti) + TMS/bolle | Mensile | *> +7% vs budget, al netto carburante se indicizzato* |
| KL3 | Costo per pallet movimentato | Costi di magazzino / n. pallet movimentati | Co.An. + WMS | Mensile | *> +10% vs media mobile 6 mesi* |
| KL4 | Saturazione magazzino | Posti pallet occupati / posti pallet disponibili | WMS | Mensile | *> 90% (rischio extra-costi di deposito esterno)* |
| KL5 | Puntualità consegne (OTIF) | Consegne complete e puntuali / consegne totali | ERP vendite / TMS | Mensile | *< 95%* |

## 4. KPI di staff e struttura

| # | KPI | Formula | Fonte dati | Frequenza | Soglia di attenzione (proposta) |
|---|---|---|---|---|---|
| S1 | Costo per FTE della funzione | Costi totali CdC di struttura / FTE della funzione | Co.An. + HR | Mensile | *> +5% vs budget YTD* |
| S2 | Incidenza costi di struttura | Costi CdC di struttura / ricavi | Co.An. + Co.Ge. ricavi | Mensile | *> valore di budget +0,5 punti* |
| S3 | Costo HR per cedolino elaborato | Costi CdC HR (payroll admin) / n. cedolini del mese | Co.An. + payroll | Mensile | *> +10% vs budget* |
| S4 | Costo AFC per fattura registrata | Costi CdC amministrazione / n. fatture attive+passive registrate | Co.An. + ERP contabilità | Mensile | *> +10% vs budget* |
| S5 | Costo IT per ticket risolto | Costi CdC IT (esercizio) / n. ticket chiusi | Co.An. + sistema ticketing | Mensile | *> +15% vs media mobile 6 mesi* |

## 5. KPI trasversali (su ogni CdC)

| # | KPI | Formula | Fonte dati | Frequenza | Soglia di attenzione (proposta) |
|---|---|---|---|---|---|
| T1 | Scostamento costi diretti controllabili | Actual − budget (assoluto e %) su mese e YTD | Pipeline (marts scostamenti) | Mensile | *soglie combinate di [requisiti-report.md §4](requisiti-report.md#4-soglie-di-evidenziazione)* |
| T2 | FTE e costo del personale del CdC | FTE medi e costo natura personale vs budget | Payroll + Co.An. | Mensile | *FTE > budget +0,5 oppure costo > +5%* |
| T3 | Rapporto costi controllabili / allocati | Costi diretti controllabili / costi totali full cost | Pipeline (post-ribaltamento) | Mensile | *informativo: se < 50%, rivedere il disegno delle allocazioni* |
| T4 | Assorbimento budget YTD | Actual YTD / budget annuo | Pipeline | Mensile | *> quota teorica di avanzamento +3 punti (es. > 53% a giugno)* |
| T5 | Stima full-year | Actual YTD + forecast mesi residui (o proiezione pro-quota fino a Fase 5) | Pipeline + forecast | Mensile | *> budget annuo +2%* |
| T6 | Scostamento ricorrente | N. mesi consecutivi sopra soglia gialla | Pipeline (storico scostamenti) | Mensile | *≥ 3 mesi → escalation al direttore di area* |

---

## 6. KPI di processo del progetto

Misurano la qualità del processo di chiusura e del sistema di reporting stesso ("misurare il processo, non solo i numeri"). Sono calcolati dalla pipeline e riportati nel report L3 e nel post-mortem mensile previsto dal [calendario di chiusura](../01-processi/calendario-chiusura.md).

| # | KPI | Formula | Fonte dati | Frequenza | Obiettivo (proposta) |
|---|---|---|---|---|---|
| X1 | Giorni di chiusura gestionale | Data pubblicazione report − ultimo giorno del mese (in giorni lavorativi) | Log pipeline + calendario | Mensile | *≤ 5 WD; trend in riduzione* |
| X2 | % CdC sopra soglia con scostamento commentato e approvato | CdC sopra soglia con commento approvato entro WD5 / CdC sopra soglia totali | Coda di revisione commenti | Mensile | *100%* |
| X3 | N. errori di quadratura intercettati | Violazioni bloccanti rilevate da [`valida.py`](../../pipeline/src/valida.py) (quadratura Co.Ge./Co.An., CdC orfani, conti non mappati, duplicati) | Report anomalie della pipeline | Mensile | *intercettati: tutti; sfuggiti in report pubblicati: 0* |
| X4 | N. rettifiche post-pubblicazione | Report ri-emessi in versione `_rev` dopo la distribuzione | Archivio report | Mensile | *≤ 1/mese; cause analizzate nel post-mortem* |
| X5 | % commenti AI approvati senza modifiche | Commenti pubblicati identici alla bozza AI / commenti totali | Log revisione commenti | Mensile | *≥ 70% a regime (indicatore di qualità del prompt); il cancello di uscita della Fase 4 della [roadmap](../04-roadmap/roadmap.md) è ≥ 60%* |
| X6 | Forecast accuracy (da Fase 5) | 1 − \|forecast a 3 mesi − actual\| / actual, per natura principale | Storico forecast vs actual | Trimestrale | *≥ 92% sul totale costi* |
| X7 | Task di chiusura in ritardo | N. task del calendario chiusi oltre la deadline / task totali | Checklist di chiusura | Mensile | *≤ 10%* |

---

## 7. Governance del catalogo

- **Owner del catalogo**: `________` — *es. responsabile controllo di gestione*
- Le modifiche a formule e soglie seguono lo stesso processo autorizzativo delle anagrafiche (proposta → validazione owner → decorrenza dichiarata) e sono versionate in Git insieme al resto del repository.
- Ogni KPI adottato deve comparire con definizione nel [glossario](../00-contesto/glossario.md).
- Revisione completa del catalogo: annuale, in sede di budget; verifica intermedia a metà anno.

**Selezione iniziale per il pilota (Fase 2 della [roadmap](../04-roadmap/roadmap.md))** — spuntare i KPI attivati sul perimetro pilota:

- [ ] T1, T2, T4 (minimo indispensabile su ogni CdC pilota)
- [ ] X1, X3 (processo)
- [ ] Altri: `________________`
