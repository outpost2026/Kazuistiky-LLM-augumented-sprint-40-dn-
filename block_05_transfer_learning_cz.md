# Case Study: Kód, který už dávno znáte

**Příběh o tom, jak zkušenosti z jiných oborů zrychlují učení softwaru a proč „začínat od nuly“ je ve skutečnosti mýtus.**

***

Často se předpokládá, že technické samostudium začíná v bodě nula. Cesta k odbornosti je pak vnímána jako závod v tom, jak rychle dokážete nasát nové informace.

Tento sprint ale ukázal něco jiného. Autor neměl žádnou předchozí zkušenost s Pythonem, cloudovou infrastrukturou ani formální softwarové vzdělání. Podle tabulek měla cesta k produkčnímu nasazení trvat měsíce. Trvala týdny. Ne proto, že by učení bylo rychlejší, ale proto, že velká část znalostí už existovala — jen v jiné formě a v jiném oboru.

## Mechanismus: Rozpoznávání vzorců napříč obory

Učení přenosem (transfer learning) u lidí není metafora. Když mozek narazí na známý vzorec v novém oboru, nestaví ho od nuly. Mapuje novou situaci na existující strukturu a jen ladí detaily.

Zde jsou čtyři konkrétní případy, kdy znalosti z fyzického světa posloužily jako přímá mapa pro řešení softwarových problémů.

***

## Přenos 1: Nedokumentované systémy → Protokol RAW FIRST

**Původní obor:** Reverzní inženýrství fyzických součástek. V kutilské elektronice často narazíte na motor nebo senzor bez manuálu. Pravidlo zní: měř, než začneš předpokládat. Věř multimetru, ne dokumentaci.

**Nový obor:** Integrace API a parsování protokolů. Při práci na vývoji těžebního skriptu dat z meteorologických stanic “Praha-Kbely” nešlo uplatnit standardní metody analýzy architektury moderních webových stránek instituce, bylo potřeba “hacknout” jejich vnitřní API pro extrakci dat. Vznikl proto protokol **RAW FIRST** — softwarový ekvivalent multimetru:

### Než napíšeš parser, podívej se na surová data

```bash
curl -s -X POST "https://api.example.com/endpoint" | python3 -m json.tool | head -40
```

Čtyři chyby v meteo-pipeline byly způsobeny tím, že LLM předpokládala strukturu API, která neodpovídala realitě. Všechny nastaly tam, kde nebyl aplikován RAW FIRST. Tam, kde proběhla kontrola surových dat jako první, se neobjevila ani jedna chyba.

* **Co se přeneslo**: Instinkt nedůvěřovat dokumentaci (**nebo předpokladům AI**) a ověřit skutečný signál dříve, než nad ním postavím abstrakci.

***

## Přenos 2: Myšlení v tolerancích → Validace dat

**Původní obor:** Obsluha CNC strojů. V CNC obrábění má každý rozměr svou toleranci (např. 24,00 mm ± 0,05 mm). Co je mimo, je zmetek. Tolerance není doporučení, je to binární brána.

**Nový obor:** Křížová validace dat ze senzorů. Při korelaci dat z baterie (JK BMS) a meteostanic (Open-Meteo, ČHMÚ) se zrodil tento přístup:

```python
# Křížová validace teploty: BMS vs. stanice ČHMÚ
delta_t = abs(bms_temp - chmu_temp)
TOLERANCE = 0.75  # stupně Celsia

if delta_t > TOLERANCE:
    flag_for_review(timestamp, delta_t, "temp_crossval_fail")
```

Hodnota ±0,75 °C nebyla výsledkem statistické analýzy. Byla nastavena stejným instinktem jako u CNC: jaká odchylka je pro aplikaci přijatelná a co už značí problém k řešení?

* **Co se přeneslo:** Zvyk vnímat každé měření jako dvojici „hodnota + nejistota“ a instinkt definovat kritéria přijetí dříve, než začne zpracování.

***

## Přenos 3: Analýza poruch → Ladění s LLM

**Původní obor:** Diagnostika fyzických systémů. Když CNC stroj vyrábí zmetky nebo solární panel dává málo energie, diagnostika má jasný řád: popsat symptom, určit hranice systému, najít mechanismus příčiny, aplikovat minimální opravu a ověřit výsledek.

Při práci s LLM určuje **kvalita vaší diagnózy kvalitu odpovědi modelu**. Prompt „nefunguje to“ vede k hádání. Prompt „symptom je X, hranice systému Y, vyloučil jsem Z“ vede k cílené analýze.

* **Co se přeneslo:** Diagnostická struktura. Izolace symptomu a přesný popis, který eliminuje fázi „pokus-omyl“ u vývojáře i u AI.

***

## Přenos 4: Postupná stavba → Inkrementální nasazení

**Původní obor:** Off-grid instalace a integrace systémů. Stavba solárního systému se nedělá naráz. Postupuje se v krocích, kde každý krok končí ověřením (např. změřit napětí panelů před připojením k baterii). Přeskakování kroků nešetří čas, ale vyrábí drahé chyby.

**Nový obor:** Nasazení cloudové infrastruktury (GCP). Postup v Cloudu kopíroval logiku stavby elektrárny:

1. Napsat funkci lokálně, otestovat s mock daty.
2. Nasadit na Cloud Run, otestovat „naživo“ přes curl.
3. Nastavit Cloud Scheduler, ručně ověřit spuštění.
4. Zapnout automatiku a sledovat první tři běhy.

* **Co se přeneslo:** Disciplína ověřitelných mezistavů. Pochopení, že odložené ověření je jen odložená (a dražší) chyba.

***

## Závěr: Máte větší náskok, než si myslíte

Tyto vzorce chování se vyvinuly v oborech, kde chyby měly okamžité fyzické následky (zmetek, zkrat, zničená baterie). Silná zpětná vazba ve fyzickém světě urychluje osvojení těchto principů.

Pokud přicházíte k softwaru z jiného oboru, neptejte se jen: „Co všechno ještě nevím?“

Ptejte se: **„Které problémy v softwaru mají stejnou strukturu jako ty, které jsem už vyřešil jinde?“**

Tolerance strojaře a práh validátoru dat vypadají na povrchu jinak, ale v jádru jsou stejným rozhodnutím. Najděte tyto ekvivalence včas. Jsou to vaše „předinstalované“ znalosti, které vám dávají neférovou výhodu.

***

*Tato kazuistika dokumentuje, že technické dovednosti jsou často jen jiným zápisem starých dobrých principů z fyzického světa.*
