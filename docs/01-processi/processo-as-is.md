# Processo AS-IS — Chiusura e reporting mensile attuale

> **Tipo documento:** template compilabile · **Owner:** Controllo di Gestione / AFC · **Stato:** ☐ bozza ☐ in compilazione ☐ validato
>
> Questo documento mappa il processo **attuale** (AS-IS) di chiusura mensile e produzione della reportistica per centri di costo. È il punto di partenza obbligato del progetto: non si automatizza ciò che non si conosce, e soprattutto **non si automatizza il caos** — prima si fotografa il processo, poi lo si semplifica ([processo TO-BE](processo-to-be.md)), infine lo si automatizza.

---

## 1. Istruzioni per la compilazione

- [ ] Compilare la tabella della sezione 3 **fase per fase**, partendo dalle righe precompilate: correggerle, eliminarle o aggiungerne di nuove finché la sequenza non rispecchia fedelmente ciò che accade ogni mese.
- [ ] Per ogni fase indicare **una sola persona come attore principale** (chi materialmente esegue), anche se altri collaborano.
- [ ] Le durate vanno stimate in **ore-persona effettive**, non in giorni di calendario (una fase può durare 2 ore di lavoro distribuite su 3 giorni di attesa: annotare entrambe le cose).
- [ ] Il "giorno del mese" è il giorno in cui la fase **tipicamente** avviene (es. *WD3*, *tra il 5 e il 10 del mese successivo*): se varia molto, indicare l'intervallo e segnalarlo come criticità.
- [ ] Nella colonna criticità essere concreti: *"il file si rompe se cambia l'ordine delle colonne dell'export"* è utile, *"processo migliorabile"* non lo è.
- [ ] Censire **tutti** i file Excel nella sezione 4, compresi quelli "personali" dei singoli controller e gli Excel "ombra" dei responsabili di CdC: sono spesso il vero processo.
- [ ] Far validare il documento a chi esegue materialmente le attività, non solo al responsabile AFC.
- [ ] Aggiornare il [glossario](../00-contesto/glossario.md) con i termini interni emersi durante la mappatura.

**Chi compila:** il controller/referente AFC che segue la chiusura, con intervista alle persone coinvolte. **Tempo stimato di compilazione:** 2-4 ore più le interviste.

---

## 2. Dati di inquadramento

| Domanda | Risposta |
|---|---|
| Quante chiusure mensili complete vengono prodotte all'anno? (12? solo trimestrali? saltate ad agosto?) | *es. 11 — agosto accorpato a settembre* |
| Oggi il report mensile è disponibile in quale giorno del mese successivo? | *es. tra il 18 e il 25* |
| Quante persone partecipano alla chiusura (anche solo per una fase)? | *es. 6: 2 contabilità, 1 payroll, 2 controller, 1 IT* |
| Quante versioni del report vengono prodotte prima di quella "definitiva"? | *es. 2-3, con rettifiche dopo il primo invio* |
| Esiste un calendario di chiusura scritto e condiviso? | ☐ sì ☐ no ☐ esiste ma non è rispettato |
| I ribaltamenti sui CdC finali vengono fatti anche sul budget o solo sull'actual? | ☐ entrambi ☐ solo actual ☐ non si fanno |
| Quanti destinatari riceve il report (responsabili di CdC, direzione)? | *es. 25 responsabili + CdA* |

---

## 3. Mappatura fase per fase

> Le righe seguenti descrivono un processo manuale **tipico**: vanno corrette, integrate o eliminate. Aggiungere righe per fasi mancanti (es. intercompany, magazzino, cespiti, commenti dei responsabili). Numerare le fasi nell'ordine reale di esecuzione.

| # | Attività | Attore / ruolo | Sistema / strumento | Input | Output | Durata tipica | Giorno del mese | Criticità / pain point |
|---|---|---|---|---|---|---|---|---|
| 1 | Estrazione bilancino di verifica dalla Co.Ge. | *es. Contabilità generale* | *es. ERP TeamSystem/Zucchetti, stampa a video → export Excel* | Registrazioni contabili del mese | File Excel/CSV bilancino | *es. 0,5 h* | *es. WD4* | *es. l'export cambia layout a ogni aggiornamento ERP; encoding e formati importi da sistemare a mano* |
| 2 | Verifica completezza registrazioni (fatture passive, note spese, paghe) | *es. Contabilità fornitori* | *es. ERP + solleciti via email* | Scadenzario, email fornitori | Elenco fatture mancanti | *es. 4 h* | *es. WD2 → WD6* | *es. fatture passive in ritardo: la chiusura resta aperta "in attesa dell'ultima fattura"* |
| 3 | Imputazioni analitiche mancanti (attribuzione CdC alle registrazioni senza centro) | *es. Controller* | *es. Excel di appoggio + rettifiche in ERP* | Bilancino, lista movimenti senza CdC | Movimenti completi di CdC | *es. 6 h* | *es. WD5 → WD8* | *es. il CdC non è obbligatorio all'origine: ogni mese centinaia di righe da riattribuire a memoria* |
| 4 | Rettifiche di competenza: ratei (13ª/14ª, ferie, premi), risconti su canoni annuali, fatture da ricevere, ammortamenti | *es. Contabilità generale + Controller* | *es. Excel "Ratei_Risconti.xlsx" + prima nota manuale* | Contratti, ordini aperti, tabelle cespiti | Scritture di assestamento mensili | *es. 8 h* | *es. WD6 → WD9* | *es. fatture da ricevere raccolte a mano via email ai reparti; nessuna sistematicità da ordini/entrata merci* |
| 5 | Raccolta dati extra-contabili (costo del personale per CdC, ore, headcount, driver) | *es. Payroll / HR* | *es. Export gestionale paghe + Excel* | Cedolini elaborati, organico | File costo del personale per CdC | *es. 3 h* | *es. WD8 (dipende dal ciclo paghe)* | *es. il payroll arriva tardi e in un formato diverso ogni mese; conguagli imprevedibili* |
| 6 | Ribaltamenti dei CdC ausiliari e di struttura sui CdC finali | *es. Controller senior* | *es. Excel "Ribaltamenti_v12_DEF.xlsx" con macro* | Bilancino analitico, tabella driver | Conto economico per CdC full cost | *es. 8 h* | *es. WD9 → WD11* | *es. cascata di riferimenti tra 6 fogli; la sa usare una sola persona; nessun versioning: impossibile ricostruire i numeri di 3 mesi fa* |
| 7 | Quadratura Co.Ge./Co.An. e verifica totali | *es. Controller* | *es. Excel, confronto manuale* | Bilancino Co.Ge., ribaltato Co.An. | Delta spiegati (o non spiegati) | *es. 3 h* | *es. WD11* | *es. quadratura fatta "a occhio" sui totali; i delta sotto una certa soglia vengono ignorati senza documentarli* |
| 8 | Produzione dei report per CdC e della sintesi direzionale | *es. Controller* | *es. Excel: copia-incolla da file ribaltamenti a template report* | CE per CdC, budget, forecast | 300+ tab/report per CdC + slide direzione | *es. 10 h* | *es. WD12 → WD14* | *es. copia-incolla manuale soggetto a errori; i grafici si rompono; nessuna analisi per eccezioni: tutti i CdC trattati allo stesso modo* |
| 9 | Analisi scostamenti e commento | *es. Controller + CFO* | *es. Excel + Word/PowerPoint* | Report actual vs budget | Commenti agli scostamenti principali | *es. 6 h* | *es. WD14 → WD16* | *es. il tempo si esaurisce nella produzione dei numeri: l'analisi è compressa o saltata* |
| 10 | Invio ai responsabili di CdC e alla direzione | *es. Controller* | *es. Email manuale con allegati* | Report finali | Email inviate | *es. 2 h* | *es. WD16 → WD20* | *es. invio manuale a 25+ destinatari: errori di destinatario, versioni diverse in circolazione, nessuna conferma di lettura* |
| 11 | Gestione richieste di chiarimento e rettifiche post-invio | *es. Controller* | *es. Email + Excel* | Domande dei responsabili | Report corretti "v2", "v3" | *es. 4 h* | *es. fino a fine mese* | *es. le rettifiche generano versioni multiple del "numero ufficiale"; i responsabili si costruiscono Excel ombra* |
| … | *aggiungere fasi mancanti* | | | | | | | |

### 3.1 Passaggi di mano e attese

> Elencare i punti in cui il processo **si ferma in attesa** di qualcuno o qualcosa: sono i primi candidati all'automazione o alla rimozione.

| Da fase | A fase | Cosa si aspetta | Attesa tipica | Note |
|---|---|---|---|---|
| *es. 2* | *es. 3* | *es. ultime fatture passive* | *es. 2-4 giorni* | *es. risolvibile con accruals da ordini* |
| | | | | |

---

## 4. Inventario dei file Excel attuali

> Censire **ogni** file Excel/Access che partecipa alla chiusura, inclusi quelli personali e quelli dei responsabili di CdC. Questo inventario alimenta l'[inventario fonti dati](../02-dati/inventario-fonti-dati.md) e decide cosa la pipeline dovrà sostituire.

| Nome file (e percorso) | Proprietario | Cosa fa | Alimentato da | Alimenta | Fragilità note |
|---|---|---|---|---|---|
| *es. `Ribaltamenti_v12_DEF.xlsx` (rete: `\\srv\afc\chiusure\`)* | *es. M. Rossi (controller senior)* | *es. ribalta 45 CdC ausiliari sui finali con driver in un foglio nascosto* | *es. export bilancino + file paghe* | *es. template report CdC* | *es. macro VBA non documentata; riferimenti assoluti a percorsi locali; la conosce solo il proprietario; versioni "DEF", "DEF2", "DEFdef" ambigue* |
| *es. `Budget_2026_rev3.xlsx`* | *es. CFO* | *es. budget per CdC e natura* | *es. raccolta manuale dai responsabili* | *es. report scostamenti* | *es. il budget non è ribaltato: confronto actual full cost vs budget diretto disomogeneo* |
| | | | | | |
| | | | | | |

**Domande di controllo sull'inventario:**

- [ ] Esistono file che **solo una persona** sa usare o aggiornare? Quali? → *elencare: sono single point of failure*
- [ ] Esistono macro VBA? Sono documentate? ☐ sì ☐ no
- [ ] I file hanno un versioning riconoscibile o si va "a nome file"? *es. "_v3_DEF_ultimo.xlsx"*
- [ ] Quali responsabili di CdC tengono un **Excel ombra** perché non si fidano (o non aspettano) il report ufficiale? → *elencare: misurano la sfiducia nel dato ufficiale*

---

## 5. Stima dell'effort attuale

> Obiettivo: quantificare i **giorni-persona/mese** assorbiti oggi dalla chiusura e dal reporting. Sarà la baseline per misurare il beneficio dell'automazione (vedi [roadmap](../04-roadmap/roadmap.md)).

### 5.1 Effort per ruolo

| Ruolo / persona | Ore/mese su chiusura e reporting | di cui raccolta/pulizia dati | di cui calcoli e quadrature | di cui produzione report | di cui analisi vera | Note |
|---|---|---|---|---|---|---|
| *es. Controller senior* | *es. 60 h* | *es. 20 h* | *es. 20 h* | *es. 15 h* | *es. 5 h* | *es. l'analisi è la parte sacrificata* |
| *es. Controller junior* | | | | | | |
| *es. Contabilità generale* | | | | | | |
| *es. Contabilità fornitori* | | | | | | |
| *es. Payroll/HR* | | | | | | |
| *es. IT* | | | | | | |
| **Totale** | **… h/mese ≈ … giorni-persona/mese** | | | | | |

### 5.2 Indicatori di sintesi AS-IS (baseline)

| Indicatore | Valore attuale | Come misurato |
|---|---|---|
| Giorni di calendario dalla fine mese al report definitivo | *es. WD20* | *data invio ultima versione* |
| Giorni-persona/mese totali sul processo | *es. 12* | *somma tabella 5.1* |
| % del tempo dedicata ad analisi (vs produzione dati) | *es. 10%* | *tabella 5.1* |
| N. rettifiche/riedizioni del report dopo il primo invio | *es. 2-3/mese* | *conteggio versioni* |
| N. errori rilevati dai destinatari negli ultimi 6 mesi | *es. 4* | *email di segnalazione* |

---

## 6. Sintesi dei pain point (da votare)

> Al termine della mappatura, elencare i 5-10 pain point più gravi e farli **prioritizzare** dagli stakeholder (vedi [mappa stakeholder](../00-contesto/mappa-stakeholder.md)). Guideranno l'ordine di attacco della [roadmap](../04-roadmap/roadmap.md).

| # | Pain point | Fasi coinvolte | Impatto (A/M/B) | Frequenza | Priorità assegnata |
|---|---|---|---|---|---|
| 1 | *es. ribaltamenti in Excel non versionati e conosciuti da una sola persona* | *6* | *A* | *mensile* | |
| 2 | *es. CdC non obbligatorio all'origine: riattribuzioni manuali massive* | *3* | *A* | *mensile* | |
| 3 | *es. report disponibile troppo tardi: i responsabili usano Excel ombra* | *8-11* | *A* | *mensile* | |
| 4 | | | | | |
| 5 | | | | | |

---

*Documento collegato: il processo obiettivo è descritto in [processo-to-be.md](processo-to-be.md); il calendario target in [calendario-chiusura.md](calendario-chiusura.md).*
