# Roadmap del progetto

> Roadmap per fasi con criteri di uscita verificabili, nello stile "piccoli incrementi verificabili": ogni fase produce qualcosa di funzionante e misurabile prima di passare alla successiva. Le durate sono indicative per un team di 1-3 persone (AFC + eventuale supporto esterno) che lavora al progetto in parallelo all'operatività ordinaria.

## Tabella riassuntiva

| Fase | Nome | Obiettivo in una riga | Deliverable chiave | Criterio di uscita | Durata indicativa |
|---|---|---|---|---|---|
| 0 | Discovery | Capire e documentare contesto, processi e dati | Documenti di `docs/` compilati | Documenti compilati e validati dagli owner | 2-3 settimane |
| 1 | Fondamenta dati | Anagrafiche pulite e primo flusso dati funzionante | Anagrafica CdC, mapping conti, drop folder attivo | 1 mese storico caricato e quadrato con la Co.Ge. | 3-4 settimane |
| 2 | Pipeline MVP | Pipeline completa su un perimetro pilota | Report Excel per 20-30 CdC pilota | Report pilota = report manuale del controller, scostamento zero | 4-6 settimane |
| 3 | Estensione | Tutti i 300+ CdC + sintesi HTML | Pacchetto report completo L1+L2 | Ciclo mensile completo entro WD5 su tutti i CdC | 4-6 settimane |
| 4 | Commento AI | Commenti automatici con approvazione umana | Bozze AI + coda di revisione + distribuzione | 100% CdC sopra soglia commentati, 0 cifre non tracciabili | 3-4 settimane |
| 5 | Industrializzazione | Processo che gira da solo, forecast | Scheduling, storicizzazione, rolling forecast | 3 chiusure consecutive senza intervento manuale non pianificato | 4-6 settimane + continuativo |

---

## Fase 0 — Discovery

**Obiettivo.** Fotografare l'azienda, il processo di chiusura attuale e il patrimonio dati prima di scrivere una riga di codice: prima si semplifica e si capisce, poi si automatizza. Automatizzare il caos produce solo caos più veloce.

**Attività**

- Compilare il [questionario di contesto aziendale](../00-contesto/questionario-contesto-aziendale.md) con l'imprenditore e il team AFC.
- Mappare il processo di chiusura attuale in [processo-as-is.md](../01-processi/processo-as-is.md): chi fa cosa, con quali file, in quanti giorni, dove si perde tempo.
- Compilare l'[inventario delle fonti dati](../02-dati/inventario-fonti-dati.md): ERP, payroll, fogli Excel "ombra", con formati, encoding e disponibilità temporale.
- Compilare la [mappa degli stakeholder](../00-contesto/mappa-stakeholder.md) e il [glossario](../00-contesto/glossario.md).
- Prima ricognizione dell'anagrafica CdC esistente: quanti centri attivi, dismessi, duplicati, senza responsabile.

**Deliverable**

- Documenti di `docs/00-contesto/`, `docs/01-processi/processo-as-is.md`, `docs/02-dati/inventario-fonti-dati.md` compilati.

**Criterio di uscita (misurabile)**

- [ ] Tutti i documenti di discovery compilati in ogni campo obbligatorio e **validati per iscritto** dagli owner indicati (imprenditore per il contesto, responsabile AFC per processi e dati).
- [ ] Elenco delle fonti dati con, per ciascuna, un file di esempio reale ottenuto e archiviato.
- [ ] Nessuna domanda del questionario lasciata "da chiarire" su punti bloccanti (perimetro CdC, sistemi sorgente, calendario).

**Durata indicativa.** 2-3 settimane.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Interviste rimandate per urgenze operative | Slot fissi in calendario, questionari precompilati in bozza da far solo correggere |
| As-is idealizzato ("come dovrebbe essere" invece di "come è") | Farsi mostrare i file reali dell'ultima chiusura, non descrizioni a memoria |
| Fonti dati "ombra" non dichiarate | Chiedere esplicitamente quali Excel personali usano i responsabili |

---

## Fase 1 — Fondamenta dati

**Obiettivo.** Anagrafiche pulite e governate, mapping conti→nature definito, primo flusso di dati reale dall'ERP al repository. Senza fondamenta dati affidabili ogni automazione a valle degrada.

**Attività**

- Pulire e ristrutturare l'anagrafica CdC secondo [piano-centri-di-costo.md](../02-dati/piano-centri-di-costo.md): un responsabile per centro, tipologia esplicita (produttivo/ausiliario/struttura/virtuale), date di validità, gerarchia a 4-5 livelli, niente codici riciclati; risultato in [`centri_di_costo.csv`](../../pipeline/config/centri_di_costo.csv).
- Costruire la tabella di mapping conto Co.Ge. → natura di costo gestionale ([`piano_dei_conti.csv`](../../pipeline/config/piano_dei_conti.csv)), con owner e processo di aggiornamento.
- Definire il contratto dati con chi produce gli export ERP (nome file `movimenti_AAAA-MM.csv` — l'export grezzo dell'ERP viene rinominato al deposito nel drop folder —, separatore, encoding, colonne obbligatorie, formato importi italiano) e documentarlo nell'[inventario fonti](../02-dati/inventario-fonti-dati.md).
- Attivare il drop folder (`inbox/` → validazione → `raw/` → `processed/`/`rejected/`) e ottenere il primo export ERP reale di un mese storico.
- Definire il [modello dati](../02-dati/modello-dati.md) (dimensioni, fatti, partizionamento per periodo).

**Deliverable**

- Anagrafica CdC pulita e versionata; mapping conti completo; contratto dati scritto; primo export ERP archiviato in `raw/`; [`ingest.py`](../../pipeline/src/ingest.py) funzionante sul mese di prova.

**Criterio di uscita (misurabile)**

- [ ] **Un mese storico caricato e quadrato con la Co.Ge.**: totale costi caricati per natura = totale conti economici di costo del bilancio di verifica dello stesso mese, con delta ≤ 0,01 € oppure delta documentati riga per riga (poste solo civilistiche vs solo gestionali).
- [ ] 100% dei movimenti di costo del mese di prova attribuiti a un CdC presente in anagrafica (zero CdC orfani) e a un conto mappato (zero conti non mappati).
- [ ] Anagrafica CdC: 100% dei centri attivi con responsabile valorizzato e tipologia assegnata.

**Durata indicativa.** 3-4 settimane.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Export ERP diverso dalle attese (encoding CP1252, tracciato variabile) | Contratto dati scritto e validazione automatica del file in ingresso fin dal primo giorno |
| Anagrafica CdC storicamente sporca (doppioni, centri morti) | Bonifica una tantum con l'AFC prima di scrivere codice che ci si appoggia |
| Delta Co.Ge./Co.An. non spiegabili | Non procedere: ogni delta va classificato; è il fondamento della credibilità del sistema |

---

## Fase 2 — Pipeline MVP

**Obiettivo.** Pipeline completa end-to-end (ingestione → validazione → ribaltamenti → report Excel) su un **perimetro pilota di 20-30 CdC** scelti per rappresentatività (almeno un produttivo, un ausiliario ribaltato, un centro di struttura).

**Attività**

- Implementare i controlli bloccanti di [`valida.py`](../../pipeline/src/valida.py): quadratura Co.Ge./Co.An., completezza CdC, conti non mappati, duplicati, formati.
- Implementare i ribaltamenti a cascata in [`ribalta.py`](../../pipeline/src/ribalta.py) secondo [`regole_ribaltamento.csv`](../../pipeline/config/regole_ribaltamento.csv), con sequenza documentata; ribaltare con le stesse regole anche il budget.
- Caricare il budget per il perimetro pilota.
- Generare le schede CdC Excel (report L1) secondo [requisiti-report.md](../03-reportistica/requisiti-report.md), con costi diretti separati dagli allocati e soglie di evidenziazione.
- Run idempotente per periodo: `python3 pipeline/src/main.py --mese AAAA-MM` ricalcola integralmente il mese.
- **Doppio binario**: per il mese di test il controller produce anche il report manuale come ha sempre fatto.

**Deliverable**

- Pipeline eseguibile end-to-end sul pilota; report Excel per 20-30 CdC; report anomalie della validazione; documentazione in [`pipeline/README.md`](../../pipeline/README.md).

**Criterio di uscita (misurabile)**

- [ ] **Report pilota validato dal controller contro il report manuale: scostamento zero** su ogni cella (actual mese, YTD, ribaltamenti inclusi) per tutti i CdC pilota; ogni differenza spiegata e risolta — se ha ragione il manuale si corregge la pipeline, se ha ragione la pipeline si documenta l'errore storico del manuale.
- [ ] Rilanciando due volte la pipeline sullo stesso periodo, output identici byte per byte (idempotenza verificata).
- [ ] Almeno un errore artificiale per tipo (CdC orfano, conto non mappato, sbilancio) iniettato nei dati di test e correttamente bloccato dalla validazione.
- [ ] Firma di validazione del controller: nome `________` data `__ / __ / ____`.

**Durata indicativa.** 4-6 settimane.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Differenze pipeline vs manuale difficili da diagnosticare | Confronto per livelli: prima i totali per natura, poi per CdC, poi le singole righe |
| Regole di ribaltamento storiche non documentate (vivono nella testa del controller) | Sessioni dedicate di reverse engineering dei fogli Excel esistenti, regole scritte in `regole_ribaltamento.csv` |
| Perimetro pilota troppo facile (solo centri semplici) | Includere obbligatoriamente almeno un caso di ribaltamento a cascata multi-livello |

---

## Fase 3 — Estensione a tutti i 300+ CdC

**Obiettivo.** Portare la pipeline validata sull'intero perimetro (tutti i 300+ CdC) e aggiungere i report di sintesi: HTML per aree/direzioni (L2) e top scostamenti per il vertice (L3, ancora senza commento AI).

**Attività**

- Completare anagrafica, budget e regole di ribaltamento per tutti i centri.
- Estendere i controlli di completezza: tutti i CdC attesi presenti ogni mese, gestione aperture/chiusure centri con date di validità.
- Generare il report HTML di sintesi per area (L2) e il report top scostamenti (L3) secondo [requisiti-report.md](../03-reportistica/requisiti-report.md).
- Primo ciclo di distribuzione manuale (il controller invia i file) per raccogliere feedback dai responsabili.
- Misurare i tempi del ciclo completo e aggiornare il [calendario di chiusura](../01-processi/calendario-chiusura.md) e il [processo to-be](../01-processi/processo-to-be.md).

**Deliverable**

- Pacchetto mensile completo: ~320 schede L1, sintesi L2 per ogni area, report L3; KPI di processo X1, X3 e X4 del [catalogo KPI](../03-reportistica/catalogo-kpi.md) calcolati (X2 si attiva in Fase 4, quando esistono i commenti AI).

**Criterio di uscita (misurabile)**

- [ ] Un ciclo mensile reale completato su tutti i 300+ CdC **entro WD5**, con quadratura Co.Ge./Co.An. superata e zero CdC mancanti.
- [ ] Campione di verifica: per almeno 15 CdC fuori dal perimetro pilota (scelti dal controller, non da chi ha sviluppato), confronto puntuale con la contabilità: scostamento zero.
- [ ] Feedback strutturato raccolto da almeno 10 responsabili di CdC; anomalie segnalate risolte o pianificate.
- [ ] Tempo di run dell'intera pipeline < 15 minuti.

**Durata indicativa.** 4-6 settimane.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Code lunghe di casi particolari (centri anomali, budget mancanti) | Registro dei casi particolari con owner e scadenza; niente eccezioni gestite "a mano" fuori pipeline |
| Responsabili che continuano a usare il proprio Excel ombra | Rendere il report ufficiale più tempestivo e affidabile dell'alternativa; coinvolgerli su soglie e layout |
| Budget non ribaltato con le stesse regole dell'actual | Controllo automatico: stessa sequenza e stessi driver su actual e budget |

---

## Fase 4 — Commento AI e distribuzione automatica

**Obiettivo.** Aggiungere il commento automatico AI alle schede sopra soglia e automatizzare la distribuzione, mantenendo l'approvazione umana come cancello obbligatorio.

**Attività**

- Implementare il modulo di commento secondo le regole di [requisiti-report.md §6](../03-reportistica/requisiti-report.md#6-regole-per-il-commento-automatico-ai) e la [metodologia AI](../05-metodologia/metodologia-ai.md): l'AI riceve la tabella scostamenti già calcolata e produce bozze in formato strutturato; validazione automatica che ogni cifra citata esista nei dati di input.
- Costruire la coda di revisione: bozza → approvazione/modifica del controller → pubblicazione; tracciare bozza originale, versione approvata, approvatore.
- Automatizzare la distribuzione: cartella condivisa `report/AAAA-MM/` + email ai responsabili, **attivata solo dopo l'approvazione dei commenti**.
- Un mese in parallelo: commenti AI e commenti scritti dal controller a confronto, per tarare il prompt.

**Deliverable**

- Schede L1 e report L3 con commento approvato; log di revisione; distribuzione automatica funzionante; KPI X2 e X5 attivi.

**Criterio di uscita (misurabile)**

- [ ] Un ciclo mensile in cui il **100% dei CdC sopra soglia** ha un commento approvato da un umano prima dell'invio (KPI X2 = 100%).
- [ ] Zero cifre nei commenti pubblicati non tracciabili ai dati della pipeline (verifica automatica attiva e superata).
- [ ] Quota di bozze AI approvate senza modifiche ≥ 60% (KPI X5: 60% è il cancello di uscita della fase; il target a regime nel [catalogo KPI](../03-reportistica/catalogo-kpi.md) è ≥ 70%) e tempo totale di revisione entro il budget-ore definito nei requisiti.
- [ ] Nessun report distribuito automaticamente prima dell'approvazione (verificato dai log di distribuzione).

**Durata indicativa.** 3-4 settimane.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Commenti generici o cause inventate dall'AI | Prompt con regola "causa solo se desumibile dai dati, altrimenti 'da approfondire'"; validazione cifre; revisione umana |
| Revisione che diventa collo di bottiglia | Commento obbligatorio solo sopra soglia; misurare X5 e migliorare il prompt finché la revisione non converge |
| Perdita di fiducia per un commento errato distribuito | Il cancello umano è bloccante per design; ogni incidente analizzato nel post-mortem |

---

## Fase 5 — Industrializzazione

**Obiettivo.** Il processo gira in modo affidabile senza eroismi: scheduling automatico, storicizzazione completa, primo rolling forecast. Da qui in poi il progetto diventa esercizio + miglioramento continuo.

**Attività**

- Scheduling del run (cron / Task Scheduler) con lock anti-concorrenza, retry, log strutturati e notifica di esito; run manuale sempre possibile per le rettifiche (`--mese` su mese già chiuso, con versione `_rev`).
- Storicizzazione: partizioni per periodo conservate e mai riscritte silenziosamente; versioning di regole di ribaltamento, mapping e forecast per poter ricostruire ogni numero pubblicato.
- Primo rolling forecast driver-based (volumi, organici, tariffe) su orizzonte 12 mesi, aggiornamento trimestrale; colonna forecast attivata nei report; misura della forecast accuracy (KPI X6).
- Post-mortem mensile del closing (KPI X1, X4, X7) e backlog di miglioramento continuo.
- Valutare i trigger per evoluzioni successive (BI self-service, publish su database) solo a fronte di richieste reali degli utenti.

**Deliverable**

- Pipeline schedulata e monitorata; archivio storico ricostruibile; primo forecast pubblicato nei report; procedura di esercizio documentata (chi fa cosa se il run fallisce).

**Criterio di uscita (misurabile)**

- [ ] **3 chiusure mensili consecutive** completate entro WD5 senza interventi manuali non pianificati sul codice o sui dati (le rettifiche contabili rilanciate via pipeline non contano come intervento manuale).
- [ ] Test di ricostruzione superato: un mese di 6+ mesi prima rigenerato dalla storia (dati raw + regole versionate) con risultati identici a quelli pubblicati.
- [ ] Forecast pubblicato per almeno un trimestre e forecast accuracy misurata (baseline stabilita, target KPI X6 concordato).
- [ ] Procedura di esercizio testata da una persona diversa da chi ha sviluppato la pipeline.

**Durata indicativa.** 4-6 settimane per l'impianto, poi continuativa.

**Rischi principali**

| Rischio | Mitigazione |
|---|---|
| Dipendenza da una singola persona (bus factor) | Procedura di esercizio scritta e provata da un secondo operatore; tutto versionato in Git |
| Forecast trattato come target negoziato invece che best estimate | Regola esplicita: il forecast si giudica sulla accuracy, non sull'aderenza al budget |
| Manutenzione evolutiva sottostimata | Budget-ore mensile dedicato; backlog visibile; post-mortem come rito fisso |

---

## Principi di esecuzione

1. **Mai passare di fase senza criterio di uscita soddisfatto.** I criteri sono checkbox verificabili, non opinioni: finché una casella è vuota, la fase non è chiusa. Se un criterio si rivela sbagliato, si cambia il criterio esplicitamente (con approvazione dell'owner di progetto), non lo si ignora.
2. **Il confronto col report manuale è il test di regressione del progetto.** La validazione "scostamento zero" della Fase 2 non si fa una volta sola: a ogni modifica rilevante di pipeline, mapping o regole di ribaltamento, il mese di riferimento viene rigenerato e confrontato con l'output validato. Qualsiasi differenza inattesa blocca il rilascio.
3. **Piccoli incrementi verificabili.** Ogni settimana deve produrre qualcosa di dimostrabile su dati reali (un controllo in più, un report in più, un mese in più caricato), mai "grandi rilasci" a sorpresa dopo mesi di lavoro sommerso.
4. **Prima semplificare, poi automatizzare.** Non si replica in pipeline un ribaltamento stratificato o un foglio storico che nessuno sa più spiegare: prima lo si ridisegna e documenta, poi lo si automatizza.
5. **Mai pubblicare report non quadrati.** I controlli bloccanti non si scavalcano "per fare prima", nemmeno una volta: la credibilità del sistema è il suo unico vero asset.
6. **L'AI propone, l'umano dispone.** Ogni contenuto generato dall'AI passa da un'approvazione umana prima di raggiungere un destinatario; l'AI non calcola mai i numeri, li commenta soltanto.
7. **Tutto versionato, tutto ricostruibile.** Codice, mapping, regole di ribaltamento, soglie, prompt e forecast vivono in Git; ogni numero pubblicato deve poter essere rigenerato a distanza di mesi.
8. **Coinvolgere i responsabili, misurare il processo.** Driver, soglie e layout si definiscono con chi li userà; i KPI di processo del [catalogo](../03-reportistica/catalogo-kpi.md#6-kpi-di-processo-del-progetto) e il post-mortem mensile dicono se il sistema sta migliorando davvero.
