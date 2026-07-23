# Glossario del progetto

Glossario dei termini di controllo di gestione e dei termini tecnici usati nei documenti e nella pipeline di questo repository. Le voci sono in ordine alfabetico. Per il contesto d'uso vedere il [questionario di contesto aziendale](questionario-contesto-aziendale.md) e i documenti in [../02-dati/](../02-dati/) e [../03-reportistica/](../03-reportistica/).

---

**Actual (consuntivo)**
I dati economici effettivamente registrati in contabilità per un periodo chiuso. È il termine di confronto di budget e forecast nell'analisi degli scostamenti.

**Allocazione**
Attribuzione di un costo a uno o più centri di costo secondo una regola definita. Include sia l'imputazione diretta all'origine sia il ribaltamento successivo tramite driver.

**Budget**
Il piano economico annuale approvato, articolato per centro di costo e natura di costo e mensilizzato. Una volta approvato non si modifica: le revisioni in corso d'anno prendono la forma di forecast.

**Budget flessibile**
Budget ricalcolato ai volumi effettivi del periodo, usato per i centri produttivi: consente di scomporre lo scostamento totale in effetti di volume, prezzo, efficienza e mix.

**Centro di costo (CdC)**
Unità organizzativa minima a cui vengono attribuiti i costi, di norma coincidente con un reparto, una linea o un ufficio, con un unico responsabile. È l'oggetto elementare del modello di controllo di questo progetto (circa 320 centri di esempio in [../../pipeline/config/centri_di_costo.csv](../../pipeline/config/centri_di_costo.csv)).

**CdC ausiliario (o di servizio)**
Centro che eroga servizi ad altri centri senza generare direttamente output vendibile: manutenzione, utilities, magazzini interni, qualità. I suoi costi vengono ribaltati sui centri utilizzatori tramite driver.

**CdC produttivo**
Centro che genera direttamente l'output aziendale: linee, reparti, impianti. È il destinatario finale dei ribaltamenti e il livello a cui si misurano costi unitari ed efficienza.

**CdC di struttura**
Centro funzionale non ribaltabile ai fini della responsabilità (direzione, AFC, HR, IT, legale). I suoi costi possono essere allocati ai centri finali solo per analisi full cost, mantenendoli sempre distinti dai costi controllabili.

**CdC virtuale (o tecnico)**
Centro senza corrispondenza organizzativa, usato come contenitore temporaneo: raccolta di costi comuni da riallocare, progetti, commesse interne. Va monitorato perché non diventi un "calderone" permanente.

**Co.Ge. (contabilità generale)**
La contabilità civilistico-fiscale, tenuta secondo il piano dei conti orientato agli schemi CEE (artt. 2424-2425 c.c.). È la fonte primaria dei costi e il riferimento con cui la contabilità analitica deve quadrare.

**Co.An. (contabilità analitica)**
La contabilità gestionale che riclassifica i costi della Co.Ge. per destinazione (centri di costo) e per natura gestionale. In un sistema integrato quadra con la Co.Ge. per costruzione, ma la quadratura mensile resta un controllo formale obbligatorio.

**Competenza economica**
Principio per cui costi e ricavi si attribuiscono al periodo in cui maturano, non a quello di pagamento o registrazione. Per una chiusura mensile attendibile va "mensilizzata": ratei, risconti, ammortamenti mensili e fatture da ricevere.

**Costi controllabili vs costi allocati**
Distinzione fondamentale nel report di ogni CdC: i costi controllabili sono quelli su cui il responsabile può agire direttamente; i costi allocati arrivano dai ribaltamenti e servono alla visione full cost. Vanno sempre esposti separatamente.

**Cut-off**
Delimitazione rigorosa delle operazioni di fine periodo (bolle, movimenti di magazzino, fatture) tra un mese e il successivo, per evitare che i costi "scivolino" nel periodo sbagliato.

**Driver (di allocazione)**
Grandezza misurabile usata per ripartire i costi di un centro su altri centri: headcount/FTE, metri quadri, ore macchina, ore MOD, numero ticket, righe d'ordine, consumi rilevati. Deve essere causale, disponibile mensilmente, accettato dai responsabili e stabile in corso d'anno.

**Fast closing**
Insieme di tecniche organizzative (pre-close, scritture automatiche, checklist con owner e deadline, soglie di materialità) per chiudere la gestione mensile in 4-5 giorni lavorativi. Vedi [../01-processi/calendario-chiusura.md](../01-processi/calendario-chiusura.md).

**Fatture da ricevere (FDR)**
Scritture di competenza per costi maturati la cui fattura non è ancora pervenuta. La best practice è generarle automaticamente dal ciclo passivo (ordini/entrata merci, logica GR/IR) invece di raccoglierle a mano.

**Forecast**
Stima aggiornata del risultato atteso, elaborata in corso d'anno sulla base dei consuntivi e delle informazioni più recenti. Deve essere una "best estimate" onesta, non un target rinegoziato.

**Forecast accuracy**
Misura a posteriori dello scarto tra forecast e actual. Va tracciata nel tempo per capire se le stime migliorano e dove il processo di previsione è debole.

**FTE (Full Time Equivalent)**
Numero di risorse equivalenti a tempo pieno. È il driver più comune per i costi del personale e per il ribaltamento dei servizi generali, oltre che un KPI trasversale di ogni CdC.

**Gerarchia dei centri di costo**
Struttura ad albero su 4-5 livelli (legal entity → direzione → funzione/area → reparto → CdC elementare) allineata all'organigramma. Le aggregazioni del reporting seguono la gerarchia, non il codice del centro.

**KPI (Key Performance Indicator)**
Indicatore sintetico di prestazione associato a un centro o a un processo (es. costo orario di trasformazione, costo per riga d'ordine, costo per FTE). Il catalogo di progetto è in [../03-reportistica/catalogo-kpi.md](../03-reportistica/catalogo-kpi.md).

**Mapping conto → natura**
Tabella che associa ogni conto Co.Ge. a una natura di costo gestionale. È un'anagrafica critica sotto governance del controllo di gestione: nel progetto risiede in [../../pipeline/config/piano_dei_conti.csv](../../pipeline/config/piano_dei_conti.csv).

**Mart (data mart)**
Tabella dati finale, pulita e aggregata, pronta per il consumo da parte dei report (es. costi per CdC, natura e mese, actual vs budget). È l'output intermedio della pipeline a monte del reporting pack.

**Natura di costo**
Classificazione gestionale del "che cosa" si è speso: personale, materiali, servizi, godimento beni di terzi, ammortamenti, ecc. Incrociata con il centro di costo (il "dove"), forma la matrice base della Co.An.

**Pipeline**
La catena automatizzata di elaborazione dati del progetto: ingestione degli export, validazione, ribaltamenti, produzione dei report. Vedi [../../pipeline/README.md](../../pipeline/README.md).

**Piano dei conti**
L'elenco strutturato dei conti della Co.Ge. (mastri, conti, sottoconti). In Italia è orientato agli schemi di bilancio CEE ed è la base da cui parte il mapping verso le nature gestionali.

**Quadratura**
Verifica formale che due insiemi di dati coincidano entro soglie definite: tipicamente Co.An. vs Co.Ge. per natura di costo, e totale post-ribaltamenti vs totale pre-ribaltamenti. I delta vanno spiegati e documentati, mai ignorati.

**Rateo e risconto**
Scritture di competenza: il rateo anticipa un costo maturato non ancora rilevato (es. quota mensile di 13ª/14ª, ferie, premi); il risconto rinvia ai mesi futuri un costo già registrato (es. canone o assicurazione annuale pagata anticipatamente).

**Reporting pack**
Il fascicolo mensile standard distribuito ai responsabili: conto economico del CdC con actual vs budget vs forecast su mese e YTD, stima full-year, FTE e trend 12 mesi, con layout unico per tutti i centri.

**Ribaltamento**
Riallocazione periodica dei costi dei centri ausiliari (ed eventualmente di struttura) sui centri finali tramite driver. Il metodo standard del progetto è la cascata (step-down); le regole sono in [../../pipeline/config/regole_ribaltamento.csv](../../pipeline/config/regole_ribaltamento.csv).

**Rolling forecast**
Forecast a orizzonte mobile di 12-18 mesi, aggiornato trimestralmente (o mensilmente sulle voci chiave) e costruito driver-based (volumi, organici, tariffe), che supera la logica del solo "a finire anno".

**Scostamento (variance)**
Differenza tra actual e valore di riferimento (budget o forecast), su mese e YTD. Con 300+ centri si gestisce per eccezioni: soglie combinate — i valori proposti sono in [requisiti-report.md, § 4](../03-reportistica/requisiti-report.md) (giallo: |scostamento| > 5% e > 2.500 €; rosso: > 10% e > 5.000 €) — e commento del responsabile solo sopra soglia.

**Single source of truth**
Principio per cui esiste un'unica base dati ufficiale da cui derivano tutti i report, riconciliata con il bilancio civilistico. È l'antidoto allo "shadow reporting" in Excel dei responsabili.

**Soft close / hard close**
Chiusura mensile semplificata con soglie di materialità (soft close) contrapposta alla chiusura completa e rigorosa di fine trimestre o esercizio (hard close). Il compromesso consente il fast closing senza sacrificare l'attendibilità annuale.

**Step-down (metodo a cascata)**
Metodo di ribaltamento in cui i centri ausiliari si chiudono in sequenza ordinata e documentata, ciascuno ribaltando sui centri a valle. È il compromesso standard tra il metodo diretto (semplice ma impreciso) e quello reciproco (accurato ma complesso).

**Tariffa standard**
Prezzo interno predeterminato per i servizi erogati da un centro ausiliario (es. €/ora manutenzione). I centri utilizzatori sono addebitati a tariffa; la varianza di assorbimento resta sul centro erogante e ne misura l'efficienza.

**WD (Working Day)**
Giorno lavorativo del mese successivo alla chiusura, usato come unità del calendario di closing: WD1 = primo giorno lavorativo del mese. Es.: "ribaltamenti e quadratura entro WD3, pubblicazione del reporting pack entro WD5".

**YTD (Year To Date)**
Valore progressivo dall'inizio dell'esercizio al mese di riferimento. Ogni confronto del reporting pack va letto sia sul mese sia YTD, con proiezione full-year (stima a finire).
