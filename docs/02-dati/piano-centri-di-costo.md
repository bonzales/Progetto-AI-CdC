# Piano dei centri di costo

> Guida e template per progettare e mantenere la tassonomia dei 300+ centri di costo (CdC). L'anagrafica operativa vive nel file versionato [pipeline/config/centri_di_costo.csv](../../pipeline/config/centri_di_costo.csv); le regole di allocazione in [pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv). Questo documento ne definisce struttura, codifica e governance.

## 1. Scopo

Con più di 300 centri l'anagrafica CdC è l'infrastruttura su cui poggia tutto il controllo di gestione: se degrada (codici riciclati, gerarchie incoerenti, responsabili non aggiornati), degradano report, ribaltamenti e confrontabilità storica. Qui si fissano le regole **prima** di automatizzare: prima si semplifica il modello, poi lo si mette in pipeline.

## 2. Principi di progettazione della tassonomia

### 2.1 Gerarchia a 4 livelli

La struttura è ad albero, allineata all'organigramma:

| Livello | Nome | Esempio | Quanti (ordine di grandezza) |
|---------|------|---------|------------------------------|
| 1 | Azienda / legal entity | *Alfa Meccanica S.p.A.* | 1–3 |
| 2 | Area / direzione | *Operations, Commerciale, Supply Chain, Struttura* | 4–8 |
| 3 | Reparto / funzione | *Lavorazioni meccaniche – Brescia, Vendite Italia* | 20–40 |
| 4 | CdC elementare | *Tornitura CNC – Brescia* | 300+ |

I costi si **imputano solo sui CdC elementari** (livello 4); i livelli 1–3 sono nodi di aggregazione per la reportistica. Le aggregazioni vivono nella gerarchia (`codice_padre`), **mai dentro il codice**.

### 2.2 Classi di centro

Ogni CdC elementare appartiene a una classe, che ne determina il trattamento nei ribaltamenti:

| Classe | Descrizione | Esempi | Trattamento |
|--------|-------------|--------|-------------|
| `produttivo` | Genera direttamente output | Linee, reparti macchina, celle di montaggio | Riceve le allocazioni; destinazione finale dei costi |
| `ausiliario` | Eroga servizi ad altri centri | Manutenzione, utilities, qualità, magazzini interni | Si **ribalta** sui centri a valle con driver causali |
| `struttura` | Funzioni centrali | Direzione, AFC, HR, IT, legale | Ribaltato solo per la vista full cost; nel report resta sempre separato dai costi controllabili |
| `commerciale` | Attività di vendita e marketing | Vendite Italia, export, marketing | Analizzato in % sui ricavi; di norma non ribaltato sui produttivi |

Se servono centri virtuali/tecnici (raccolta costi da riallocare, progetti), vanno censiti come classe a parte e chiusi a zero ogni mese: da valutare in fase di impianto. *Decisione:* [ ] servono [ ] non servono — note: ____________

### 2.3 Regole d'oro

- **Un solo responsabile per CdC** (principio di responsabilità): mai comitati, mai caselle vuote.
- Coerenza con l'organigramma: se cambia l'organizzazione, cambia la gerarchia — non i codici.
- Le altre dimensioni di analisi (commessa, canale, prodotto, cliente) restano **dimensioni separate** del modello dati: non si creano CdC per rappresentarle, altrimenti i 300 centri diventano 3.000.
- Date di validità e stato in anagrafica: un centro cessato non sparisce, viene disattivato.

## 3. Principi di codifica

Con 300+ centri la codifica interamente "parlante" (che incorpora sede, funzione e reparto nel codice) è fragile: ogni riorganizzazione la rompe. Si adotta una codifica **semi-parlante**: un prefisso di classe + un progressivo, con tutti gli attributi descrittivi gestiti come campi dell'anagrafica.

| Regola | Dettaglio |
|--------|-----------|
| Formato CdC elementare | 1 lettera di classe + 3 cifre progressive: `P001`–`P999` produttivi, `A001`–`A999` ausiliari, `S001`–`S999` struttura, `C001`–`C999` commerciali |
| Formato nodi aggregati | Livello 1: `AZ` + progressivo (*`AZ01`*); livello 2: sigla d'area stabile di 3 lettere (*`OPS`, `COM`, `SCM`, `STR`*); livello 3: `R` + 2 cifre (*`R01`*) |
| Stabilità | Il codice **non cambia mai** per tutta la vita del centro, anche se il centro cambia reparto, sede o responsabile: si aggiornano gli attributi e `codice_padre` |
| Nessun riuso | Un codice cessato **non si riassegna mai**: comprometterebbe lo storico e i confronti pluriennali |
| Niente significato nel codice | Sede, funzione, macchina, responsabile stanno nei campi anagrafici, non nel codice |
| Formato tecnico | Maiuscolo, senza spazi né caratteri speciali; i codici sono testo (mai numeri: `P010` non deve diventare `10`) |

> **Nota sulla demo.** L'anagrafica dimostrativa ([pipeline/config/centri_di_costo.csv](../../pipeline/config/centri_di_costo.csv)) usa volutamente codici parlanti a 3 livelli (es. `S1-PRD-001` = stabilimento 1 → reparti produttivi → centro 001) per rendere auto-esplicativi report ed esempi sui dati sintetici. Per l'anagrafica **reale** la raccomandazione resta la codifica semi-parlante di questa sezione; la decisione definitiva si prende in Fase 0/1 sulla base del [questionario di contesto, sez. E](../00-contesto/questionario-contesto-aziendale.md).

## 4. Template dell'anagrafica CdC

Colonne **target** dell'anagrafica reale (il file demo attuale se ne discosta in alcuni punti: vedi nota di raccordo a fine sezione). Separatore virgola, encoding UTF-8, decimali col punto. Le prime righe sono esempi da sostituire con l'anagrafica reale:

| codice | descrizione | livello | codice_padre | classe | responsabile | driver_ribaltamento | stato |
|--------|-------------|---------|--------------|--------|--------------|---------------------|-------|
| AZ01 | *Alfa Meccanica S.p.A.* | 1 | | | *A. Bianchi (AD)* | | attivo |
| OPS | *Operations* | 2 | AZ01 | | *L. Ferrari* | | attivo |
| R01 | *Lavorazioni meccaniche – Brescia* | 3 | OPS | | *M. Rossi* | | attivo |
| P001 | *Tornitura CNC – Brescia* | 4 | R01 | produttivo | *M. Rossi* | | attivo |
| A001 | *Manutenzione meccanica – Brescia* | 4 | R10 | ausiliario | *G. Verdi* | ore_intervento | attivo |
| S020 | *Sistemi informativi* | 4 | R40 | struttura | *P. Neri* | n_utenti_it | attivo |
| *…* | *da compilare per tutti i 300+ centri* | | | | | | |

Note di compilazione:

- `livello` e `codice_padre` definiscono l'albero: ogni riga (tranne il livello 1) deve avere un padre esistente di livello immediatamente superiore.
- `classe` e `driver_ribaltamento` si compilano solo sui CdC elementari (livello 4); il driver solo per ausiliari e struttura.
- `stato` ammette solo `attivo` / `cessato`.
- Attributi facoltativi consigliati (colonne aggiuntive, non obbligatorie per la pipeline): `stabilimento`, `data_apertura`, `data_cessazione`, `note`.

> **Raccordo con il CSV demo.** Il file dimostrativo attuale differisce dal template target in quattro punti: (1) i costi si imputano sui CdC di **livello 3** (la gerarchia demo ha 3 livelli, non 4); (2) al posto di `stato` usa il flag `attivo` con valori `SI`/`NO` (ed è ciò che [`valida.py`](../../pipeline/src/valida.py) controlla oggi); (3) ha la colonna aggiuntiva `area` (denormalizzazione del livello 1, usata dai report per raggruppare); (4) usa codici parlanti (nota in sez. 3). L'allineamento al template target avverrà in Fase 1 della [roadmap](../04-roadmap/roadmap.md) insieme all'anagrafica reale, aggiornando di pari passo la pipeline.

Checklist di completezza dell'anagrafica (da verificare prima del primo run):

- [ ] Tutti i CdC usati oggi nell'ERP sono presenti (nessun codice "orfano" nei movimenti).
- [ ] Ogni CdC elementare ha esattamente un responsabile indicato.
- [ ] Ogni CdC ausiliario e di struttura ha un driver di ribaltamento assegnato.
- [ ] Nessun costo risulta imputato su nodi di livello 1–3.
- [ ] I centri non più operativi sono marcati `cessato`, non eliminati.

## 5. Esempio concreto: azienda multi-stabilimento

*Alfa Meccanica S.p.A.*, due stabilimenti (Brescia e Verona). Lo stabilimento **non entra nel codice**: compare nella descrizione e nell'attributo facoltativo `stabilimento`; l'aggregazione per sede si ottiene filtrando l'anagrafica, quella organizzativa dalla gerarchia.

```text
AZ01 Alfa Meccanica S.p.A.                       (livello 1)
|-- OPS  Operations                              (livello 2)
|   |-- R01 Lavorazioni meccaniche - Brescia     (livello 3)
|   |   |-- P001 Tornitura CNC - Brescia         (produttivo)
|   |   |-- P002 Fresatura - Brescia             (produttivo)
|   |-- R02 Montaggio - Brescia                  (livello 3)
|   |   |-- P015 Linea montaggio 1 - Brescia     (produttivo)
|   |-- R03 Lavorazioni meccaniche - Verona      (livello 3)
|   |   |-- P101 Tornitura CNC - Verona          (produttivo)
|   |-- R10 Servizi tecnici - Brescia            (livello 3)
|       |-- A001 Manutenzione meccanica - Brescia (ausiliario, driver: ore_intervento)
|       |-- A005 Utilities e centrale termica - BS (ausiliario, driver: mq_occupati)
|       |-- A010 Controllo qualita - Brescia      (ausiliario, driver: ore_controllo)
|-- COM  Commerciale                             (livello 2)
|   |-- R20 Vendite Italia                       (livello 3)
|       |-- C001 Vendite Italia Nord             (commerciale)
|-- STR  Struttura                               (livello 2)
    |-- R40 Funzioni centrali                    (livello 3)
        |-- S001 Direzione generale              (struttura)
        |-- S010 Amministrazione finanza e controllo (struttura, driver: headcount)
        |-- S020 Sistemi informativi             (struttura, driver: n_utenti_it)
```

Caso tipico: la fresatura di Brescia passa sotto un nuovo reparto "Meccanica pesante" (`R05`). Il codice `P002` **resta identico**: si aggiorna solo `codice_padre` da `R01` a `R05`. Lo storico del centro rimane confrontabile.

## 6. Governance dell'anagrafica

| Evento | Chi lo richiede | Chi lo autorizza | Come si esegue |
|--------|-----------------|------------------|----------------|
| **Apertura nuovo CdC** | Responsabile d'area, con motivazione, responsabile proposto e classe | Controllo di gestione (owner unico dell'anagrafica) | Nuovo codice = primo progressivo libero della classe; inserimento in ERP e in `centri_di_costo.csv` nella stessa giornata; mai a chiusura in corso |
| **Modifica attributi** (responsabile, descrizione, padre) | Responsabile d'area o CdG | Controllo di gestione | Aggiornamento del CSV versionato in Git: la storia delle modifiche è l'audit trail |
| **Cessazione** | Responsabile d'area | Controllo di gestione | `stato = cessato` (mai cancellare la riga); blocco delle imputazioni in ERP; verifica che il centro sia a saldo zero nel mese di chiusura |
| **Riuso di un codice** | — | **Vietato sempre** | Nessuna eccezione, nemmeno per centri "mai usati": si apre un codice nuovo |

Regole di calendario e qualità:

- **Congelamento in chiusura**: dal pre-close alla pubblicazione dei report (vedi [calendario di chiusura](../01-processi/calendario-chiusura.md)) l'anagrafica non si tocca; le richieste si accodano al mese successivo.
- **Review annuale** (in sede di budget): verifica centri senza movimenti da 12 mesi (candidati alla cessazione), responsabili non più in organico, coerenza con l'organigramma.
- **Versioning**: `centri_di_costo.csv` e `regole_ribaltamento.csv` si modificano **solo** via Git: ogni modifica ha autore, data e motivazione nel messaggio di commit; è sempre possibile ricostruire con quale anagrafica è stato prodotto un report passato.
- La pipeline **blocca** il caricamento se nei movimenti compare un CdC assente dall'anagrafica (vedi [controlli di qualità](modello-dati.md#6-controlli-di-qualità-per-livello)).

Ruoli da nominare (da compilare, in coerenza con la [mappa stakeholder](../00-contesto/mappa-stakeholder.md)):

- [ ] Owner dell'anagrafica CdC (controllo di gestione): ____________
- [ ] Sostituto: ____________
- [ ] Referente ERP per l'allineamento dei codici: ____________

## 7. Regole di ribaltamento

### 7.1 Metodo

Si adotta il metodo **a cascata (step-down)**: i centri ausiliari si chiudono in sequenza documentata e stabile, ciascuno ribaltando sui centri a valle; i servizi reciproci tra ausiliari già chiusi si ignorano. È il compromesso standard a questa scala; il metodo reciproco (equazioni simultanee) si giustifica solo se gli scambi incrociati sono rilevanti.

Nella pipeline demo ([`ribalta.py`](../../pipeline/src/ribalta.py)) la sequenza di chiusura è **per classe**: prima tutti i CdC ausiliari, poi quelli di struttura, sempre e solo verso CdC **finali** (produttivi o commerciali) attivi. La cascata multi-livello — ordinamento fine per singolo CdC (es. utilities prima della manutenzione) e allocazioni ausiliario → ausiliario — è un'**estensione futura** prevista per i dati reali (vedi "Limiti attuali" in [pipeline/README.md](../../pipeline/README.md)).

### 7.2 Driver ammessi

I driver devono essere **causali, misurabili, disponibili mensilmente e accettati dai responsabili**. Ogni driver deve avere una fonte censita nell'[inventario delle fonti dati](inventario-fonti-dati.md).

| Driver | Descrizione | Fonte tipica | Adatto per |
|--------|-------------|--------------|------------|
| `ore_intervento` | Ore di manutenzione rilevate per centro | Sistema manutenzione / rapportini | Manutenzione |
| `mq_occupati` | Metri quadri occupati | Planimetrie (facility) | Utilities, affitti, pulizie |
| `consumo_kwh` | Consumi energia rilevati | Contatori di reparto | Energia |
| `headcount` / `fte` | Persone / FTE per centro | HR / paghe | HR, servizi generali |
| `n_utenti_it` | Utenze IT attive per centro | IT / Active Directory | Sistemi informativi |
| `n_ticket` | Ticket lavorati per centro | Service desk | IT, servizi interni |
| `ore_controllo` | Ore di controllo qualità per centro | Sistema qualità | Controllo qualità |
| `righe_ordine` | Righe d'ordine movimentate | ERP / WMS | Magazzini, logistica |
| `ore_produzione` | Ore di produzione lavorate per centro | MES / rilevazioni di reparto | Servizi di produzione, programmazione |
| `n_movimentazioni` | Movimentazioni di magazzino per centro | WMS / ERP | Magazzini, logistica interna |
| `valore_acquistato` | Valore degli acquisti gestiti per centro | ERP (ciclo passivo) | Ufficio acquisti — *proxy, causalità parziale* |
| `costi_diretti` | Costi diretti del centro ricevente | Pipeline | **Solo fallback**, non causale: usato nella demo per alcune allocazioni di struttura; sui dati reali va sostituito con un driver causale |

I nomi in tabella sono quelli effettivamente usati in [pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv) e nell'anagrafica demo. Da evitare: driver "comodi" ma non causali (i ricavi come driver di tutto, `costi_diretti` come scorciatoia permanente), catene di allocazione così lunghe che il costo non è più tracciabile, cambi di driver in corso d'anno (rompono la confrontabilità: si cambiano solo a inizio esercizio, in sede di budget).

### 7.3 Tabella delle regole

Struttura del file [pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv) (separatore virgola, encoding UTF-8, decimali col punto; una riga per coppia origine → destinazione):

| cdc_origine | cdc_destinazione | driver | quota |
|-------------|------------------|--------|-------|
| A005 | P001 | mq_occupati | 0.35 |
| A005 | P002 | mq_occupati | 0.30 |
| A005 | P015 | mq_occupati | 0.20 |
| A005 | P101 | mq_occupati | 0.15 |
| A001 | P001 | ore_intervento | 0.45 |
| A001 | P002 | ore_intervento | 0.35 |
| A001 | P015 | ore_intervento | 0.20 |
| S020 | *…* | n_utenti_it | *…* |

Vincoli (verificati automaticamente dalla pipeline, run bloccato se violati):

- Le `quota` di ciascun `cdc_origine` devono sommare **esattamente a 1.0**.
- Origine e destinazioni devono esistere in anagrafica ed essere **attive**; nella pipeline demo le destinazioni ammesse sono solo CdC **finali** (produttivi o commerciali). L'allocazione verso un altro CdC ausiliario (cascata multi-livello, es. utilities → manutenzione) è un'estensione futura: oggi verrebbe bloccata dalla validazione.
- Le quote derivano dai valori mensili o normalizzati del driver dichiarato: la colonna `driver` documenta la base causale e permette l'aggiornamento periodico delle quote.
- Dopo il ribaltamento ogni CdC ausiliario e di struttura deve chiudere a **saldo zero** nel periodo.

### 7.4 Regole di metodo

- **Stesse regole per actual, budget e forecast**: mai ribaltare l'uno e non gli altri, il confronto diventerebbe disomogeneo.
- Nel report di ogni CdC i **costi diretti controllabili** e i **costi allocati** restano sempre su righe separate: il responsabile risponde dei primi; i secondi servono alla visione full cost.
- Le regole si rivedono **una volta l'anno** in sede di budget; le versioni passate restano ricostruibili via Git.
- Ogni modifica alle quote va motivata con i valori aggiornati del driver (es. nuova distribuzione dei mq dopo un trasloco).

## 8. Checklist di primo impianto

- [ ] Classi e gerarchia validate con la direzione e i responsabili d'area.
- [ ] Schema di codifica approvato (sez. 3) e mappatura dei codici ERP esistenti sui nuovi codici (o conferma dei codici attuali se già conformi).
- [ ] Anagrafica completa dei 300+ centri caricata in [pipeline/config/centri_di_costo.csv](../../pipeline/config/centri_di_costo.csv).
- [ ] Responsabili confermati uno per uno (nessun centro senza owner).
- [ ] Driver scelti **insieme ai responsabili** dei centri riceventi: l'accettazione del modello è condizione di funzionamento, non un optional.
- [ ] Regole di ribaltamento compilate in [pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv) con quote che sommano a 1.0.
- [ ] Sequenza di chiusura step-down documentata e condivisa.
- [ ] Processo di governance (sez. 6) comunicato ai responsabili d'area.

## 9. Collegamenti

- [Modello dati target](modello-dati.md) — come l'anagrafica diventa `dim_centri_di_costo` e come si controllano i ribaltamenti.
- [Inventario delle fonti dati](inventario-fonti-dati.md) — fonti dei driver e dei movimenti per CdC.
- [Calendario di chiusura](../01-processi/calendario-chiusura.md) — finestra di congelamento dell'anagrafica e collocazione dei ribaltamenti (WD3).
- [Glossario](../00-contesto/glossario.md) — definizioni di ribaltamento, driver, step-down, full cost.
- [pipeline/README.md](../../pipeline/README.md) — esecuzione di `ribalta.py` e dei controlli collegati.
