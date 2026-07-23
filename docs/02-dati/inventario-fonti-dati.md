# Inventario delle fonti dati

> **Documento di discovery — template compilabile.**
> Va completato dal team AFC insieme al referente IT / partner ERP prima di costruire la pipeline.
> I valori in *corsivo* sono esempi di risposta: sostituiteli con i dati reali della vostra azienda.
> Ogni fonte censita qui diventa un "contratto dati" che la pipeline (vedi [pipeline/README.md](../../pipeline/README.md)) userà per validare i file in ingresso.

## 1. Scopo e istruzioni di compilazione

Questo documento censisce **tutte le fonti dati** necessarie alla reportistica mensile per centri di costo. Per ciascuna fonte dobbiamo sapere: dove nasce il dato, come si estrae, con quale frequenza, chi lo estrae e quanto è affidabile oggi.

Come compilare:

1. Completate la tabella della sezione 2 (una riga per fonte; aggiungete righe se servono).
2. Per ogni fonte **primaria** (qualità critica per la chiusura: bilancino, Co.An., paghe, budget) compilate una scheda di dettaglio della sezione 3.
3. Rispondete alle domande della sezione 4 sulle modalità di estrazione.
4. Validate la proposta di drop folder della sezione 5 con l'IT.
5. La checklist della sezione 6 è la regola di accettazione dei file: verrà implementata come controllo automatico bloccante in `pipeline/src/valida.py`.

Scala di **qualità percepita** usata in tabella:

| Voto | Significato |
|------|-------------|
| 5 | Dato affidabile, tracciato stabile, mai richiesto rilavoro manuale |
| 4 | Affidabile con piccole sistemazioni occasionali |
| 3 | Utilizzabile ma richiede pulizia manuale ogni mese |
| 2 | Spesso incompleto o incoerente, quadrature frequenti da rifare |
| 1 | Inaffidabile: oggi si ricostruisce a mano |

## 2. Censimento delle fonti

| # | Fonte | Sistema di origine | Contenuto | Formato export | Frequenza disponibile | Chi la estrae | Qualità percepita (1–5) | Note |
|---|-------|--------------------|-----------|----------------|------------------------|----------------|--------------------------|------|
| 1 | Bilancino di verifica Co.Ge. | *es. TeamSystem Alyante — da compilare* | Saldi dare/avere per conto, progressivi mese e anno | *CSV / XLSX — da compilare* | *Mensile, disponibile WD1 — da compilare* | *da compilare* | *da compilare* | Fonte di **quadratura primaria**: ogni altro flusso deve riconciliarsi con questo |
| 2 | Movimenti Co.An. / imputazioni per CdC | *modulo analitica dell'ERP — da compilare* | Movimenti economici con conto, CdC, importo, data, causale | *CSV — da compilare* | *Mensile — da compilare* | *da compilare* | *da compilare* | Verificare se il CdC è **obbligatorio all'origine** della registrazione (vedi sez. 4) |
| 3 | Anagrafica centri di costo | *ERP / foglio Excel del controller — da compilare* | Codice, descrizione, gerarchia, responsabile, stato | *CSV / XLSX* | *A ogni variazione* | *da compilare* | *da compilare* | Diventerà l'anagrafica unica versionata in [pipeline/config/centri_di_costo.csv](../../pipeline/config/centri_di_costo.csv); regole in [piano-centri-di-costo.md](piano-centri-di-costo.md) |
| 4 | Piano dei conti Co.Ge. | *ERP — da compilare* | Codice conto, descrizione, tipo (patrimoniale/economico), mapping a natura di costo | *CSV / XLSX* | *A ogni variazione* | *da compilare* | *da compilare* | Il mapping conto → natura è sotto governance del controllo di gestione ([pipeline/config/piano_dei_conti.csv](../../pipeline/config/piano_dei_conti.csv)) |
| 5 | Budget per CdC e natura | *Excel di budgeting / EPM — da compilare* | Importi budget per periodo, conto/natura, CdC, versione | *XLSX — da compilare* | *Annuale + revisioni forecast — da compilare* | *da compilare* | *da compilare* | Il budget va ribaltato **con le stesse regole dell'actual**, altrimenti il confronto è disomogeneo |
| 6 | Cespiti / ammortamenti | *modulo cespiti ERP — da compilare* | Quote di ammortamento mensili per cespite, conto, CdC | *CSV / XLSX* | *Mensile — da compilare* | *da compilare* | *da compilare* | Verificare che l'ammortamento sia calcolato **mensilmente**, non solo a fine anno |
| 7 | Costo del personale da paghe | *es. Zucchetti Paghe / consulente del lavoro — da compilare* | Costo aziendale per dipendente o per CdC: retribuzioni, oneri, ratei 13ª/14ª, ferie, TFR | *XLSX / CSV — da compilare* | *Mensile, disponibile WD? — da compilare* | *da compilare* | *da compilare* | Collo di bottiglia tipico: se arriva tardi, valutare costo standard con conguaglio. Verificare presenza dei **ratei mensilizzati** |
| 8 | Magazzino / produzione (se rilevante) | *MES / modulo magazzino ERP — da compilare* | Consumi materiali, versamenti, ore macchina/MOD, WIP, scarti | *CSV — da compilare* | *Mensile con cut-off — da compilare* | *da compilare* | *da compilare* | Rilevante per i CdC produttivi e per i driver (ore macchina); richiede **cut-off rigoroso** su bolle e movimenti |
| 9 | Driver di ribaltamento (FTE, mq, ticket, ore intervento…) | *HR, facility, IT service desk — da compilare* | Valori mensili dei driver usati dalle regole di allocazione | *XLSX / CSV* | *Mensile — da compilare* | *da compilare* | *da compilare* | Ogni driver in [pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv) deve avere una fonte censita qui |
| 10 | Ordini aperti / fatture da ricevere (consigliata) | *ciclo passivo ERP — da compilare* | Ordini con entrata merci non fatturata (logica GR/IR) | *CSV* | *Mensile, pre-close* | *da compilare* | *da compilare* | Serve per generare accruals sistematici invece di raccogliere le FDR a mano |
| 11 | *altra fonte — da compilare* | | | | | | | |
| 12 | *altra fonte — da compilare* | | | | | | | |

## 3. Scheda di dettaglio per fonte (contratto dati)

Compilare **una scheda per ogni fonte primaria** (almeno: righe 1, 2, 3, 4, 5, 7 della tabella). Copiare il blocco seguente per ogni fonte. Queste informazioni diventano il contratto dati che la pipeline verifica a ogni caricamento.

### Scheda fonte: ____________________

- **Nome file convenzionale**: *es. `coan_YYYYMM.csv` → `coan_202606.csv`* — da compilare: ____________
- **Formato**: [ ] CSV [ ] XLSX [ ] TXT a larghezza fissa [ ] altro: ____________
- **Separatore** (se CSV): *es. `;` (tipico degli export italiani)* — da compilare: ____
- **Encoding**: [ ] CP1252 (tipico ERP italiani) [ ] UTF-8 [ ] altro: ____________
- **Formato importi**: [ ] italiano (`1.234,56`) [ ] anglosassone (`1234.56`) — da compilare
- **Formato date**: *es. `GG/MM/AAAA`* — da compilare: ____________
- **Colonne obbligatorie** (nome esatto e ordine): *es. `CONTO; DESCR_CONTO; CDC; DATA_REG; IMPORTO; SEGNO; CAUSALE`* — da compilare: ____________
- **Righe da scartare**: [ ] intestazioni ripetute [ ] righe di totale/subtotale [ ] piè di pagina — specificare: ____________
- **Il periodo è dichiarato**: [ ] nel nome file [ ] in una colonna [ ] in nessun modo (da correggere!)
- **Quando è disponibile nel mese**: *es. WD1 entro le 12:00* — da compilare: ____________
- **Owner dell'estrazione** (nome e sostituto): ____________
- **Canale di consegna**: [ ] drop folder (sez. 5) [ ] email (da migrare a drop folder) [ ] export schedulato diretto
- **Note e anomalie note**: *es. il campo CDC è vuoto sulle scritture di prima nota manuali* — ____________

## 4. Modalità di estrazione

Per ogni fonte va scelta una modalità. In ordine di preferenza:

| Modalità | Come funziona | Quando usarla | Rischi |
|----------|---------------|---------------|--------|
| **Export schedulato** | L'ERP pianifica la stampa/export e deposita il file nella drop folder (o l'operatore lo fa a calendario con procedura scritta) | Preferita per tutte le fonti mensili: quasi tutti i gestionali italiani (TeamSystem, Zucchetti) hanno stampe pianificabili | Il tracciato può cambiare con gli aggiornamenti ERP: il contratto dati (sez. 3) intercetta la rottura |
| **Manuale con procedura** | Un operatore esegue l'export seguendo una procedura documentata passo-passo e deposita il file in drop folder | Accettabile in fase iniziale o per fonti a bassa frequenza (anagrafiche, budget) | Dipendenza dalla persona; prevedere sempre un sostituto formato |
| **API / ODBC** | La pipeline interroga direttamente il sistema (es. API REST/OData di Business Central con OAuth2; ODBC in sola lettura su viste concordate col partner ERP) | Solo se l'ERP la supporta ufficialmente; ODBC diretto sulle tabelle proprietarie **solo** con benestare del partner e su viste dedicate | Schemi proprietari non documentati; rottura agli aggiornamenti; costi di licenza |

Domande da porre al referente IT / partner ERP (compilare):

- [ ] L'ERP consente di **pianificare** l'export del bilancino e dei movimenti analitici? Chi lo configura? — *risposta:* ____________
- [ ] Il CdC è **obbligatorio** in registrazione su fatture passive, prima nota, paghe, ammortamenti? Se no, su quali causali manca? — *risposta:* ____________
- [ ] Esistono API o viste ODBC ufficialmente supportate per Co.Ge./Co.An.? A quale costo? — *risposta:* ____________
- [ ] Gli export sono stabili tra un aggiornamento ERP e l'altro? Chi ci avvisa se cambia un tracciato? — *risposta:* ____________
- [ ] Chi possiede le credenziali tecniche e come vengono custodite? — *risposta:* ____________

## 5. Drop folder: percorso proposto

Pattern proposto: una cartella condivisa (file server aziendale o SharePoint sincronizzato) con questa struttura. La pipeline valida ogni file in `inbox/`, lo archivia immutato in `raw/` e lo sposta in `processed/` oppure `rejected/` con notifica.

```text
\\server\controllo_gestione\dati\        <- percorso da confermare con IT: ____________
|-- inbox\                    file appena depositati, in attesa di validazione
|-- raw\                      archivio immutabile per fonte e periodo
|   |-- coge\2026-06\
|   |-- coan\2026-06\
|   |-- paghe\2026-06\
|-- processed\                file accettati (copia di cortesia, gia' archiviati in raw)
|-- rejected\                 file rifiutati dalla validazione, con report anomalie
```

Regole operative:

- I file in `raw/` **non si modificano mai**: sono l'evidenza di audit di ciò che l'ERP ha prodotto.
- Un file rifiutato si corregge **alla fonte** (nell'ERP o nella procedura di export) e si rideposita in `inbox/`: mai correggere a mano il file.
- Naming: `<fonte>_<AAAA-MM>.<ext>`, con il periodo sempre nel formato `AAAA-MM` — *es. `movimenti_2026-06.csv` (tracciato letto dalla pipeline, vedi [pipeline/README.md](../../pipeline/README.md)), `paghe_2026-06.xlsx`*. L'export grezzo dell'ERP (es. *coge_202606.csv*) viene rinominato secondo questa convenzione al deposito nella drop folder. Il periodo nel nome deve coincidere con il contenuto.
- Ogni rifiuto genera una notifica (email o Teams) all'owner della fonte con il dettaglio delle righe anomale.

Decisioni da prendere:

- [ ] Percorso definitivo della drop folder: ____________
- [ ] Chi ha accesso in scrittura a `inbox/`: ____________
- [ ] Canale di notifica dei rifiuti: [ ] email [ ] Teams [ ] altro: ____________

## 6. Checklist di qualità minima per accettare un file

Un file entra in pipeline **solo se** supera tutti questi controlli (implementati in automatico; le violazioni bloccano il caricamento):

- [ ] **Tracciato stabile**: colonne, nomi e ordine conformi al contratto dati della fonte (sez. 3).
- [ ] **Periodo dichiarato**: il periodo nel nome file esiste, è nel formato atteso ed è coerente con le date contenute nel file.
- [ ] **Quadratura col bilancino**: il totale dei movimenti per conto coincide con i saldi del bilancino di verifica dello stesso periodo (tolleranza 0,01 €).
- [ ] **Formati leggibili**: encoding riconosciuto, importi convertibili in numero (formato italiano gestito), date valide.
- [ ] **Nessuna riga spuria**: niente righe di totale, subtotale o intestazioni ripetute in mezzo ai dati.
- [ ] **Completezza plausibile**: numero di righe e totale importi confrontabili col mese precedente (scostamenti anomali segnalati).
- [ ] **Riferimenti validi**: ogni CdC citato esiste nell'anagrafica, ogni conto esiste nel piano dei conti ed è mappato a una natura di costo.
- [ ] **Nessun duplicato** sulla chiave della fonte (es. stessa registrazione caricata due volte).
- [ ] **Estrazione a subledger chiuso**: il file è stato estratto dopo la chiusura del modulo di origine secondo il [calendario di chiusura](../01-processi/calendario-chiusura.md).

## 7. Collegamenti

- [Modello dati target](modello-dati.md) — dove finiscono i dati censiti qui (livelli raw/staging/marts).
- [Piano dei centri di costo](piano-centri-di-costo.md) — anagrafica CdC e regole di ribaltamento.
- [Calendario di chiusura](../01-processi/calendario-chiusura.md) — quando ogni fonte deve essere disponibile.
- [Glossario](../00-contesto/glossario.md) — definizioni dei termini usati in questo documento.
- [pipeline/README.md](../../pipeline/README.md) — come la pipeline consuma questi file.
