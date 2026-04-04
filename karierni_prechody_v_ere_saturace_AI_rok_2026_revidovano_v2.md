# Kariérní přechody v éře saturace AI (2026)

## Případová studie a přenositelný návod

**Jak uspět na prvním IT pohovoru bez IT školy, bez praxe a s vědomím, že AI umí kód za vás.**

---

## Abstrakt

Reálný případ člověka, který během přibližně 45 aktivních dní přešel z manuální profese (CNC operátor) k nabídce placeného testu od e-commerce firmy — na prvním IT pohovoru v životě.

**Klíčové zjištění:** V roce 2026 už není paměťová znalost programovacích jazyků bariérou vstupu do IT. Tou bariérou je schopnost systémového myšlení, rychlé abstrakce a řízení AI nástrojů.

Tento text slouží jako:
*   **Kazuistika** — co se stalo a proč to fungovalo.
*   **Template** — jak postupovat, pokud máte podobné kognitivní nastavení.
*   **Upozornění** — tato cesta není vhodná pro každého; předpoklady jsou popsány explicitně v sekci 5.

> ### Epistemický status tohoto textu
> Než čtenář pokračuje, je nutné pojmenovat, čím tento dokument je a čím není.
> 
> Je to *informovaná hypotéza podpořená případovou studií* — ne prokázaný mechanismus. Kazuistika dokumentuje jeden výsledek v jednom kontextu. Nevidíme lidi, kteří strávili 45 dní intenzivní práce s LLM a nabídku nedostali. Nevidíme ani ty, kteří nabídku dostali, ale placený test neprošli. Predikční hodnota proto závisí na míře podobnosti čtenářova profilu s profilem autora — a ta podobnost není samozřejmá.
> 
> Makroekonomický kontext (sekce 1, sekce 2) je podpořen dostupnou literaturou a je robustnější než závěry z individuální kazuistiky. Přenositelné principy (sekce 4) jsou platné i nezávisle na psychometrickém rámci — jsou to v jádru principy dobrého inženýrství.

---

### Poznámka k časové ose
Autor ukončil zaměstnání na konci ledna 2026. Únor byl věnován dekompresi — žádný cílený vývoj, žádný strukturovaný sprint. Aktivní adopce začala ve druhé polovině února 2026. Pohovor proběhl 2. dubna 2026.

**Reálný časový rámec adopce:** přibližně 45 aktivních dní.

Číslo "45 dní" není zaokrouhlení ani marketingový claim. Je to autorův vlastní odhad aktivně odpracovaného období, nikoli kalendářní vzdálenost od libovolného bodu.

---

## 1. Nová realita: AI jako vyrovnávač (ale ne pro všechny)

Do roku 2026 se nástroje jako GPT, Claude, DeepSeek nebo Gemini staly běžnou součástí vývoje. Generování kódu na úrovni junior–medior je otázkou sekund.

**Důsledek:** Firmy přestávají platit za syntaxi. Platí za řešení problémů, za architekturu, za schopnost vidět strukturu v chaosu.

To otevírá dveře lidem z netradičních prostředí — ale jen těm, kteří mají určité kognitivní předpoklady. Jaké přesně, je předmětem sekce 2.

### Zároveň: co AI jako equalizer nezarovná

Je důležité pojmenovat, co se zároveň *zvýšilo* jako bariéra vstupu.

Syntaktická bariéra (znalost API, frameworků, jazyků) dramaticky poklesla. Ale zároveň vzrostla jiná bariéra: schopnost smysluplně specifikovat problém, validovat výstup LLM a rozpoznat halucinaci od správné odpovědi. AI, která generuje plausibilně znějící kód s chybou uprostřed, je nebezpečná přesně v míře, v jaké uživatel nedokáže výstup kriticky posoudit.

Nadměrné spoléhání na LLM bez rozvíjení vlastního kritického myšlení vede k tomu, co výzkumníci kognitivních věd označují jako **kognitivní automatizační past (CAP)** — systematické oslabování analytických schopností, které jsou nyní nejvíce ceněné. Hrozba je reálná a přímo ohrožuje ty, kteří si myslí, že AI je zkratka k odbornosti, ale je jí zkratka jen k její iluzi.

AI je equalizer selektivní: snižuje jednu bariéru, zatímco jiné transformuje.

---

## 2. Klíčový determinant: schopnost přenášet principy přes domény

Zde je nutné pojmenovat věc přímo.

Existuje psychologický konstrukt zvaný **fluidní inteligence (Gf)** — schopnost řešit nové problémy bez spoléhání se na naučené znalosti. Je to opak **krystalizované inteligence (Gc)**, která zahrnuje paměť, syntaxi a naučená fakta.

Cattell-Horn-Carrollova (CHC) teorie — v současné kognitivní psychologii nejkomplexnější hierarchický model struktury inteligence
- předpovídá, že v prostředí, kde AI přebírá krystalickou složku inteligence, roste relativní hodnota její fluidní části . Tato kazuistika je konzistentní s touto předpovědí. Empiricky: Fluidní inteligence vykazuje statisticky signifikantní pozitivní korelaci s výší příjmů (β = 0.09; korigované p = 0.013), zatímco krystalická i. tuto korelaci v podmínkách AI-saturovaného trhu ztrácí jako prediktivní proměnná pro mzdovou prémii.

**Je ale nutné říct, co o tom víme a co nevíme.**

*   **Co víme:** Autor během 45 dní zvládl přejít z nulové IT znalosti k funkčním produkčním systémům na GCP, IoT telemetrii, predikci stavů baterie a sémantickému indexování dokumentů. To je pozorovatelný fakt, doložitelný artefakty na GitHubu.
*   **Co nevíme:** Zda je příčinou "vysoká Gf" v psychometrickém smyslu. Gf autora nebyla standardizovaně měřena. "Vysoká Gf" je hypotéza — interpretační rámec, který dává pozorovanému chování smysl, ale není v tomto textu verifikována. Stejné výsledky lze vysvětlit i jinými proměnnými: délkou soustředěného úsilí, existující strukturou technického myšlení z CNC prostředí, nebo kontextovou shodou — firma v tomto konkrétním momentu hledala právě tento typ profilu.

Pozorovatelné chování, které hypotézu podporuje:
*   Přenos diagnostického vzorce z CNC (symptom → mechanismus → minimální oprava) přímo do LLM debuggingu bez explicitního "učení" tohoto přístupu.
*   Přenos tolerančního myšlení do datové validace (±0.75 °C = flag).
*   Rýchlá orientace v nových doménách bez memorování základů.

Tato chování jsou popsatelná a čtenář může posoudit, zda je rozpoznává u sebe. Psychometrický konstrukt Gf k tomu není nutný.

> **Praktický závěr bez přehnaných claims:**
> Pokud jste v minulosti opakovaně a rychle přecházeli do nových domén a nacházeli v nich strukturální analogie k tomu, co již umíte — tato cesta stojí za zvážení. Pokud vaše silná stránka spočívá v systematickém, postupném učení nazpaměť, tradiční cesta (kurz → praxe → junior role) je pravděpodobně spolehlivější.

---

## 3. Případová studie: Z CNC operátora na prvním IT pohovoru za 45 dní

### Výchozí stav (leden 2026)
*   Několik let v manuálních profesích: zahradník, práce s koňmi, montáže, CNC operátor.
*   Žádná IT historie, žádný IT titul.
*   Odchod z CNC kvůli systémovému stropu — prostředí neumožňovalo optimalizaci ani smysluplnou zpětnou vazbu.

### Spouštěč
Únor 2026: dekomprese po ukončení zaměstnání. Žádný cílený vývoj. Druhá polovina února: první experimenty s LLM-asistovaným vývojem.

**Klíčové rozhodnutí:** Nedelegovat syntaxi a učit se ji zpaměti, ale naučit se klást otázky tak, aby LLM produkoval spolehlivý, verifikovatelný výstup.

### Co vzniklo za 45 dní

*   **[Produkční GCP stack](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/GCP/gcp_stack_ingest_v3.md):** Cloud Run, Cloud Scheduler, GCS, Firestore, Telegram delivery. Čtyři aktivní služby, šest scheduler jobů, vše serverless, provozní náklady blízko nule.
*   **[Těžební ETL pipeline](https://github.com/outpost2026/Kazuistiky-LLM-sprint/tree/GCP):** Automatické těžební python scrapery umístěné na google cloud service, vyhledávají zájmové inzeráty (bazos, prace.cz, jobs.cz a další), filtrují dle boolean logiky a vytříděné výsledky - alfa leady - odesílají na mobilní telefon
*   **[Predikce stavu baterie (SOC)](https://github.com/outpost2026/Kazuistiky-LLM-sprint/tree/LFP_soc_predict_pipeline):** Vstup: BMS log LFP baterie + meteo data s horizon masking z LiDAR transformace. Výstup: predikce na 5 dní, odchylka ±5 % oproti pozorované kapacitě.
*   **[Sémantický RAG indexer](https://github.com/outpost2026/RAG-indexer):** Klasifikace lokálních dokumentů do 18 typů, kaskádové dekódování (UTF-8 / CP1250 / ISO-8859-2), produkce strukturovaného JSON manifestu.
*   **[CAD-to-LLM pipeline](https://github.com/outpost2026/cad2llm):** SketchUp → COLLADA → deterministický JSON pro prostorovou analýzu LLM. Testováno na 30 uzlech (Outpost Zone 2), 0 % nekonzistencí.

Vše zdokumentováno v **[pitevní knize (70+ záznamů)](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/pitevni_kniha_v8.md)**, dostupné na GitHubu.

### Pohovor (2. dubna 2026, první IT pohovor v životě)

**Vstupní test — část 1:**
Zadání: identifikujte chybu v 5řádkovém code snippetu.
*Chování autora:* Místo snahy o uhodnutí odpovědi okamžité přiznání limitu — *"Tohle si standardně vyhledám nebo nechám vygenerovat LLM. Pokud je toto podmínka přijetí, chci to vědět hned, abych neplýtval vaším časem."* Programátor odpověděl, že to nevadí, a přešel na druhou část.

**Vstupní test — část 2 (návrh automatizace):** 
Zadání (zkráceně): navrhněte systém, který z CSV/XML od dodavatelů automaticky určí celní kategorii (CN/HS) a tím i DPH; zamyslete se nad cenou a rychlostí.
*Odpověď autora* (psáno ručně, přes hranice vyhrazeného boxu na papíře, doslova out of the box):
*   Raw data → sémantická analýza + korelace s CN/HS nomenklaturou → klasifikační skript
*   Validace: ingest → parsování → ruční kontrola vzorku → verzování
*   Výstup: JSON/CSV dle potřeby
*   Korekce: logy, post-mortem běhy, diferenční analýzy → ladění → finální výstup
   >Data Engineering Pipeline - Zahrnutí logů, post-mortem analýz a verzování mohlo ukázat programátorovi, že není myšleno jen na to "aby to běželo", ale aby to bylo udržitelné v produkci.

*Chyběly:* confidence threshold, odhad nákladů, konkrétní technika klasifikace.

**Průběh pohovoru:**
Po vyhodnocení testu programátor přizval majitele firmy. Konverzace přešla na téma reálné automatizace firemních procesů. Autor popsal meteo pipeline v logice: `raw → parsing → korelace → predikce → validace výstupu → produkce`. Diskuze se posunula z testování paměti na architektonickou konzultaci.

*   *Zpětná vazba programátora:* "Velmi příjemný, rychle jste mě zaujal. Oblast transfer learningu byla zajímavá, o tom bych se rád dozvěděl více."
*   *Zpětná vazba majitele:* "Evidentně se rychle učíte, jste schopen adaptace. Z profilu je však zřejmá vaše potřeba autonomie a samostatnosti. Ve firmě potřebujeme lidi, kteří věci dotahují do konce a jsou schopni komunikace s týmem. To jsou věci, které o vás nevím a nelze je nyní posoudit."

**Výsledek:** Nabídka placeného testu — firma zadá reálný automatizační problém a zaplatí za jeho řešení v rámci výběrového řízení.

### Proč to fungovalo

1.  **Přenos vzorců přes domény.** Vlastní budovaný off-grid uzel (LFP, BMS, FV energetika, vše DIY), CNC diagnostika (symptom → mechanismus → minimální oprava), zkušenosti z vývojem vlastních skriptů pro autorovo použití, vše se přímo zobrazilo na architektuře ETL pipeline i na přístupu k debuggingu. Toto přenesení nebylo vědomou strategií — bylo to přirozené chování pro člověka, jehož defaultní mód je "povrch → mechanismus → struktura → implikace."
2.  **Artefakty jako důkaz.** GitHub repozitáře s `requirements.txt`, měřitelnými výstupy (predikce SOC ±5 %) a dokumentací rozhodnutí. Firma si repozitáře prohlédla před pohovorem. Autor na ně odkázal v závěru pohovoru; programátor potvrdil, že se díval.
3.  **Diagnostická kultura.** 70+ záznamů v pitevní knize znamená, že každá chyba byla data, ne selhání. Tento přístup je přímo přenositelný na týmovou práci: dokumentovaný failure mode je sdílitelné know-how, ne osobní ostuda. Inspirace pochází z NASA a Google SRE kultury *blameless post-mortem* — principu, kde chyby nejsou příčinou trestu, ale surovinou pro systémové zlepšení. V tomto přístupu lze vidět praktickou aplikaci *double-loop learningu* (Argyris, Schön): oprava konkrétní chyby je single-loop; přehodnocení celé metodiky na základě vzorce chyb je double-loop. Deník se 70+ záznamy je nástrojem druhé smyčky.
4.  **Sociální přesnost.** Proaktivní přiznání limitu u části 1 místo improvizace zachránilo čas a vybudovalo důvěru. Závěrečný dotaz "jaký dojem jsem udělal?" byl neobvyklý, ale výsledkem byla přímá, hodnotná zpětná vazba — informace, kterou většina kandidátů nikdy nedostane.

### Kontext pohovoru jako proměnná
Je nutné pojmenovat jednu podmínku, která nemusí být obecně přenositelná: firma hledala lidi na automatizaci a autor přišel s příklady přesně z oblasti automatizace. Tato shoda není náhoda — ale její opakovatelnost závisí na schopnosti čtenáře cílit firmy s podobnou strukturou problémů. V jiném sektoru, u jiného typu firmy, by tentýž profil mohl být vnímán jako nedostatečně "tradiční."

---

## 4. Přenositelné principy

Pokud rozpoznáváte u sebe chování popsaná v sekci 2 (rychlý přechod do nových domén, hledání strukturálních analogií), a chcete podobnou cestu, použijte tento postup.

### Krok 1: Přestaňte soutěžit v paměťových znalostech
Neučte se syntaxi nazpaměť. Naučte se klást otázky LLM způsobem, který produkuje verifikovatelný výstup. Klíčová otázka není *"co je třetí parametr funkce X"*, ale *"jak bych navrhl systém, který..."*. 
Zároveň: neodevzdejte kritické myšlení. Každý výstup LLM je hypotéza, ne pravda. Trénujte schopnost výstup posoudit, otestovat a odmítnout. Tato schopnost je nyní cennější než schopnost kód napsat.

### Krok 2: Postavte vlastní hřiště s měřitelným výstupem
Vytvořte projekt, který produkuje číslo, soubor nebo alert — ne jen kód, který "by mohl fungovat."
*   IoT senzor s predikcí a kvantifikovanou odchylkou
*   ETL pipeline z veřejných dat s dokumentovanou přesností
*   Automatizace vlastní rutiny s logovatelným výstupem

### Krok 3: Dokumentujte jako inženýr, ne jako student
Veďte deník chyb. Každá chyba je data. Vytvářejte metodiky (příklad: *"Nejdřív raw data, pak model — nikdy naopak"*). Komprimujete tím roky zkušeností do týdnů. Toto není jen technika pro rychlý vstup do IT — je to praxe, která odděluje průměrné od výjimečných v každém oboru.

### Krok 4: Zviditelněte artefakty
Commitujte na GitHub. Vytvořte logické `README.md`, komentáře, `requirements.txt`, vzorová data. Firmy nevěří tvrzením — věří kódu, který lze spustit.

### Krok 5: Na pohovoru pojmenujte svůj limit dříve, než ho pojmenují oni
Pokud nedokážete vyřešit testovou úlohu — řekněte to hned a vysvětlete, jak byste ji řešili v reálné práci. To je silnější než špatná improvizace.

### Krok 6: Adresujte jejich obavu z vaší autonomie proaktivně
Pokud máte nelineární kariérní historii, majitel firmy ji uvidí. Proaktivní věta — *"Chápu, že moje samostatnost může být riziko. Tady je, jak zajistím viditelnost a komunikaci průběhu"* — je silnější než čekání na otázku.

### Krok 7: Dotáhněte to do konce
Toto je nejtěžší část. Rychlá abstrakce vymyslí řešení za hodinu. Dopsat dokumentaci, ošetřit chybové stavy, zabalit výsledek do podoby, kterou spustí kdokoli — to trvá déle a není to intelektuálně vzrušivé. Trénujte exekutivní funkce. Bez nich zůstanete v 80 %. Tento krok je také místem, kde lidé s vysokou Gf a nízkou exekutivní disciplínou systematicky selhávají. Rychlá abstrakce je výhoda v první fázi; dotažení je výhoda v té rozhodující.

---

## 5. Varování a limity

Tento přístup předpokládá:
1.  **Schopnost přenášet principy přes domény** — viz sekce 2; pokud ji nemáte, tradiční cesta (kurz → praxe → junior pozice) je spolehlivější.
2.  **Toleranci pro nejistotu** — žádná pevná cesta, žádná záruka výsledku.
3.  **Energii a čas pro sprint** — prvních 45 dní vyžaduje vysokou intenzitu, ne pomalé lineární učení.
4.  **Ochotu selhávat strukturovaně** — 70+ chyb v deníku není selhání, je to palivo. Ale musíte je dokumentovat, ne ignorovat.
5.  **Schopnost dotáhnout věci do konce** — tato kazuistika končí nabídkou placeného testu, ne přijatou nabídkou. Výsledek testu závisí na krocích 4 a 7 výše.

### Dodatečné slepé skvrny — co tento text neřeší

*   **Survivorship bias je strukturální.** Tento text dokumentuje jeden úspěšný případ. Neurčíme, kolik lidí s podobným profilem zkusilo stejnou cestu a neuspělo. Bez tohoto čísla není možné odhadnout skutečnou pravděpodobnost úspěchu.
*   **Juniorský trh se mění asymetricky.** Tlak AI na juniorské pozice není rovnoměrný. Firmy, které dříve přijímaly juniory jako "levnou pracovní sílu na rutinní úkoly", tyto pozice ruší nebo mění jejich charakter. Zároveň ale roste poptávka po lidech, kteří dokážou AI orchestrovat v konkrétním firemním kontextu — a ti zatím chybí. Tato kazuistika spadá do druhé kategorie, ale přechod není automatický.
*   **Gf bez exekutivy je neúplný balíček.** Vysoká schopnost abstrakce bez disciplíny dotahování generuje "80% lidi" — hodnotné v konzultační roli, problematické v roli, která vyžaduje produkci. Pokud rozpoznáváte u sebe vzorec rychlého nadšení a nedokončených projektů, je to signál k adresování ještě před startem, ne až po prvním neúspěchu.
*   **Kontext firmy je skrytá proměnná.** Pohovor proběhl u firmy, která aktivně hledala AI-orientované řešení konkrétních problémů. V jiném kontextu by stejný profil byl vnímán jako atraktivní, ale nezralý. Správná firma pro tento přístup existuje — ale vyžaduje cílený výběr, ne masové rozesílání CV.
*   **CAP riziko roste s úspěchem.** Čím více kandidát spoléhá na LLM k produkci funkčního kódu, tím méně rozvíjí vlastní diagnostické schopnosti na nízké úrovni. V krátkodobém horizontu to není problém. Ve střednědobém — při práci na legacy systémech, při debuggingu bez LLM přístupu, nebo při nutnosti vysvětlit rozhodnutí seniornímu kolegovi — se tato mezera ukáže.

---

## 6. Závěr: Co to znamená pro rok 2026

AI nesnížila důležitost inteligence — změnila, jaká inteligence se cení. Paměťová znalost (Gc) ztrácí hodnotu. Schopnost abstrakce, přenosu principů a systémového myšlení získává na ceně.

Lidé, kteří tato chování mají a pocházejí z netradičních prostředí, mají nyní přímější cestu do IT — pokud se naučí AI orchestrovat, nikoli s ní soutěžit, a pokud si zachovají kritické myšlení jako protiváhu k AI-generovaným výstupům.

Tato kazuistika je jeden datový bod. Není to důkaz. Je to případ, který stojí za pozornost, protože výsledek byl neobvyklý — a protože každý krok v něm je zdokumentovaný a ověřitelný.

---

## Příloha A: Empirický fundament — co říká literatura

*Tato sekce shrnuje relevantní empirická pozorování a případy ze širšího kontextu. Slouží jako věcné ukotvení kazuistiky, nikoli jako její důkaz. Jednotlivá pozorování jsou konzistentní s tezemi dokumentu, ale nenahrazují systematický výzkum.*

### A.1 Neurobiologie Gf a Gc: co víme
Výzkumy z let 2024–2025 identifikovaly odlišné neurobiologické koreláty obou konstruktů. Krystalizovaná inteligence vykazuje asociaci s procesy axonálního vedení a dlouhodobou strukturální organizací mozku — roste s věkem a vědomou akumulací zkušeností. Fluidní inteligence je úzce spojena s aktivitou GABAergních synapsí a flexibilitou neurotransmise — dosahuje vrcholu v rané dospělosti, s věkem klesá.
Klíčové ekonomické pozorování: Gf vykazuje statisticky signifikantní pozitivní korelaci s příjmy (β = 0.09; korigované p = 0.013) a je silnějším prediktorem mzdové prémie než formální vzdělání v prostředích vyžadujících adaptaci na nové problémy.

### A.2 Externalizace Gc do LLM: strukturální důsledek
Generativní AI systémy fungují jako distribuovaný repozitář krystalizované inteligence v planetárním měřítku. Z pohledu trhu práce to znamená: jakmile AI generuje syntakticky správný kód na úrovni medior vývojáře v řádu sekund, memorizace pravidel programovacích jazyků ztrácí ekonomickou hodnotu jako samostatná dovednost. Tato změna není budoucností — v prostředích využívajících AI-asistovaný vývoj je to pozorovaná realita roku 2026.
Důsledek není konec potřeby lidského vývojáře. Je to reinkarnace jeho role: od produkce syntaxe k definici problémů, architektuře řešení a kritické validaci výstupů.

### A.3 Blue-collar to tech: zdokumentované přechody
Fenomén přechodu z manuálních a průmyslových profesí do IT rolí prostřednictvím AI-asistovaného vývoje je v roce 2026 doložitelný napříč více zdroji.
Vzorec opakující se v těchto narativech je konzistentní s kazuistikou tohoto dokumentu: jedinci se zázemím v disciplínách s nulovou tolerancí k chybám (strojírenství, elektrotechnika, výrobní logistika) vykazují schopnost rychle adoptovat diagnostický přístup k softwaru. Znalost fyzické kauzality — kde chyba má měřitelný a okamžitý důsledek — se přenáší do práce se systémy, kde chyba rovněž má měřitelný důsledek, jen méně viditelný.
Technologičtí analytici pozorující tento trend poukazují na specifickou výhodu průmyslového zázemí: disciplína přesnosti (tolerance, specifikace, výmět) přirozeně rezonuje s požadavky na testování, validaci a dokumentaci v IT.

### A.4 Kognitivní automatizační past (CAP): reálné riziko
Výzkumníci z oblasti kognitivních věd opakovaně dokumentují negativní efekt nadměrného spoléhání na AI na udržení analytických schopností. Mechanismus: pokud systém rutinně přebírá kognitivní práci, mozek tuto práci postupně přestává trénovat. V prostředích, kde je AI dostupná nepřetržitě, je tato dynamika aktivní.
Praktický důsledek pro kariérní přechody: kandidát, který používá LLM jako myšlenkovou protézu namísto jako nástroj, buduje zdánlivou kompetenci. Zdánlivá kompetence obstojí při pohovoru orientovaném na architektonické myšlení. Neobstojí při šesti měsících reálné práce, kde se skrytá mezera ukáže.
Preventivní praxe: pravidelné řešení problémů bez LLM, vedení deníku vlastního myšlení (ne jen AI výstupů), a explicitní schopnost vysvětlit každé rozhodnutí v systému.

### A.5 Blameless post-mortem jako kompresní mechanismus
NASA, Google SRE a další organizace s vysokou spolehlivostí dlouhodobě praktikují kulturu, kde selhání systému není příčinou trestu jednotlivce, ale surovinou pro systémové zlepšení. Tento přístup — *blameless post-mortem* — umožňuje otevřenou dokumentaci chyb, ze které se učí celá organizace.
Aplikace na individuální kariérní přechod: deník chyb funguje jako osobní SRE praxe. Každý zaznamenaný failure mode je: (a) zdroj vlastního učení při opakování situace, (b) demonstrace diagnostické kultury pro potenciálního zaměstnavatele, (c) nástroj double-loop learningu — přehodnocení metodiky na základě vzorce chyb, ne jen oprava konkrétní instance.
Kompresní efekt 70+ záznamů v pitevní knize za 45 dní není anekdota. Je to kvantifikovaná praxe, která odpovídá měsícům zkušeností v prostředí bez explicitní zpětné vazby od mentora nebo týmu.

### A.6 Kontextová závislost výsledku: co se nereplikuje automaticky
Pro úplnost je nutné pojmenovat strukturální podmínky, které výsledek kazuistiky umožnily a jejichž přítomnost nelze zaručit v jiném kontextu:
*   Firma aktivně hledala automatizační kompetenci, nikoliv konvenční IT profil.
*   Pohovor probíhal ve formátu, který umožnil přechod od testování paměti k architektonické diskuzi — ne všechny procesy tuto flexibilitu mají.
*   Výsledkem byl placený test, ne přijatá pozice — kazuistika je otevřená.

Čtenář by měl tento dokument číst jako mapu terénu, ne jako navigaci s garantovanou trasou. Terén je reálný. Trasa závisí na profilu chodce.

---

## Příloha B: Literatura a zdroje

Tato literatura slouží jako inspirační a věcné zázemí. Část byla přímo relevantní pro interpretační rámce použité v textu, část rozšiřuje kontext pro čtenáře, kteří chtějí hlouběji porozumět konceptům, na které text narážel.

**Psychologie inteligence a kognitivní vědy:**
*   **Cattell, R. B.** — Teorie fluidní a krystalizované inteligence (Gf/Gc); základ pro interpretační rámec použitý v sekci 2.
*   **Carroll, J. B.** — Three Stratum Theory; rozšíření Cattellova modelu do hierarchické CHC struktury.
*   **Horn, J. L.** — empirická práce na oddělení Gf a Gc jako měřitelných konstruktů.

**Systémové myšlení a organizační učení:**
*   **Argyris, C. & Schön, D.** — Double-loop learning; rámec pro pochopení rozdílu mezi opravou chyby a přehodnocením systému, který chyby produkuje.
*   **Csikszentmihalyi, M.** — Flow; optimální poměr výzvy a kapacity, relevantní pro sprint v podmínkách nejistoty.

**Spolehlivost systémů a kultura post-mortem:**
*   **Google SRE Book (Beyer et al.)** — Site Reliability Engineering; praxe blameless post-mortem jako zdroj systémového učení.
*   **Prigogine, I.** — Teorie disipativních struktur; rámec pro pochopení jak systémy rostou v podmínkách chaosu, nikoli navzdory němu.

**Trh práce a AI:**
*   **Hoffman, R.** — Superagency; argument pro AI jako nástroj posílení lidské produktivity, nikoliv jejího nahrazení.
*   **Dokumentace k této kazuistice** — GitHub repozitář s pitevní knihou, metodikami a kódem; primární zdroj verifikovatelných artefaktů.

---
*Vydáno pod licencí CC BY-NC 4.0. Sdílení a úpravy pro nekomerční účely jsou povoleny s uvedením autora.*
*Soubor `LICENSE` v kořenovém adresáři repozitáře obsahuje plné znění licence.*
*Vytvořeno na základě reálné zkušenosti. Rozšířeno o analytický fundament, duben 2026.*
