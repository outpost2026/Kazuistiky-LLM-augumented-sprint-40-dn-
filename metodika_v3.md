# Metodika řešení málo známé problematiky s LLM

## Případová studie: IoT perimetr pro off-grid autonomní uzel "Outpost 2026"

---

**Autor:** Ondřej Soušek  
**Repozitář:** [github.com/outpost2026](https://github.com/outpost2026)  
**Datum:** 2026-03-26  
**Verze:** 1.0  
**Licence:** CC BY-SA 4.0

---

## Proč tenhle dokument?

Tohle není tutorial, jak naprogramovat ESP32. Není to návod, jak postavit solární systém. Není to sbírka hotových kódů.

**Tohle je nahlédnutí pod pokličku – ukázka myšlenkového procesu při řešení komplexní, málo známé problematiky s asistencí LLM (Large Language Model).**

Během 24 hodin jsem prošel od fyzických součástek na stole k ucelenému plánu, identifikaci skrytých blokátorů a objednávce chybějících komponent. Celý proces byl zaznamenán jako série promptů a odpovědí – z toho vznikl tento dokument.

**Cílové skupiny:**
- **Já (operátor)** – jako znalostní báze pro příští podobné projekty
- **Zvídaví čtenáři** – kteří chtějí vidět, jak někdo reálně pracuje s LLM na technickém projektu
- **Začátečníci v IoT** – kteří hledají strukturu, ne jen kód
- **Uživatelé LLM** – kteří chtějí posunout svou práci z "zeptám se a zkopíruji" na metodickou

---

## Obsah

1. [Proč metodika?](#proč-metodika)
2. [Kontext projektu: Outpost 2026](#kontext-projektu-outpost-2026)
3. [Přehled fází procesu](#přehled-fází-procesu)
4. [Detailní rozpis fází s ukázkami](#detailní-rozpis-fází-s-ukázkami)
5. [Klíčové principy](#klíčové-principy)
6. [Porovnání s běžnými přístupy](#porovnání-s-běžnými-přístupy)
7. [Role LLM v procesu](#role-llm-v-procesu)
8. [Aplikace na jiné domény](#aplikace-na-jiné-domény)
9. [Co dál? – Iterace metodiky](#co-dál--iterace-metodiky)

---

## Proč metodika?

Při práci s LLM je snadné sklouznout do režimu "zeptám se, zkopíruju, modlím se, aby to fungovalo". To je **vibe coding** – a v hardwarovém světě to vede ke spáleným čipům, zbytečným objednávkám a frustraci.

Tenhle dokument popisuje **alternativní přístup**:
- **Kotvení ve fyzické realitě** – než začnu řešit problém, explicitně popíšu, co mám a co nevím
- **Binární MVP** – definuji "hotovo" jako binární stav, ne kvalitativní
- **RAW_FIRST** – před kódem ověřím surový vstup
- **Explicitní bottleneck** – pojmenuji, co mi brání, oddělím fyzické od znalostních
- **Strojově čitelná dokumentace** – dokumentuji strukturovaně, ne jen textem

---

## Kontext projektu: Outpost 2026

### Fyzický základ

Off-grid systém (vývojový uzel "Outpost"):

| Komponent | Parametry |
|-----------|----------|
| FV výkon | 1900 Wp (4×475 Wp) + 400 Wp (2×200 Wp) |
| Baterie | LiFePO4 630 Ah / 16 kWh |
| Střídač | POW-HVM3.2H-24V (3200 W) |
| BMS | JK-PB2A16S20P V19 |
| Lokace | Praha 8 |

### Cíl projektu

Implementovat IoT vrstvu pro:
1. **Telemetrii** – data z BMS, střídače, teplot, perimetru
2. **Bezpečnost** – detekce pohybu, otevření dveří, alarmy
3. **Ochranu baterie** – teplotní alarm, zákaz nabíjení pod 0 °C
4. **Vzdálený monitoring** – GCP cloud, Telegram notifikace

### Výchozí stav (25. 3. 2026)

- **Laskakit BOM** – fyzicky na stole (ESP32, ESP8266, senzory, MAX3232)
- **BMS** – JK s GPS konektorem, ale bez kabelu
- **Střídač** – RJ45 konektor, ale bez kabelu
- **Já** – ESP32/ESP8266 vidím poprvé v životě

---

## Přehled fází procesu

| Fáze | Název | Výstup |
|------|-------|--------|
| **0** | Kotvení v realitě | Explicitní popis výchozího stavu |
| **1** | Celek – rámcování | Binární MVP kritérium, priority |
| **2** | Abstrakce – struktura | Handoff JSON, BOM tabulka |
| **3** | Dílčí zpřesnění | Detailní návod pro jeden segment |
| **4** | Identifikace bottleneck | Explicitní pojmenování blokátoru |
| **5** | Sumarizace – syntéza | Rozhodovací podklad |
| **6** | Fyzická akce | Objednávka, dokumentace |
| **7** | Verifikace a iterace | Testovací protokol, zpětná vazba |

---

## Detailní rozpis fází s ukázkami

### Fáze 0: Kotvení v realitě

**Princip:** Než začneš řešit problém, explicitně popiš, co máš, co nevíš, co ti chybí.

**Můj prompt:**
```
K: přišla mi celá objednávka z laskakit.cz, mám na stole fyzicky veškeré 
objednané součástky pro telemetrii, IoT PoC, kabely, kalafunu. Mám čas 
na prototypování, jako první chci vyzkoušet logování do PC z hlavního 
střídače pro základní přehled toků E zde na outpostu
```

**Co je zde klíčové:**
- Explicitní popis výchozího stavu ("mám na stole")
- Definice prvního cíle ("logování do PC")
- Kontextová vazba na předchozí dokumenty

**Typický chybný vzorec:** "Jak připojím střídač k ESP32?" – bez kontextu, bez popisu, co už mám.

---

### Fáze 1: Celek – rámcování

**Princip:** Definuj cíl, priority a co je "hotovo" (binární MVP kritérium).

**Výstup (přijatý od LLM, operátorem odsouhlasený):**
```
Binární MVP kritérium:
"Data dorazí do GCS alespoň jednou z fyzického ESP32"

Pro fázi 0 – logování do PC:
"Surový výstup z POW střídače je viditelný v sériovém terminálu 
na PC po dobu 5 sekund nepřetržitě."
```

**Co je zde klíčové:**
- MVP není "funkční telemetrie", ale binární stav
- Každá fáze má vlastní binární kritérium
- Kritérium je měřitelné a ověřitelné

---

### Fáze 2: Abstrakce – struktura

**Princip:** Rozlož problém na komponenty, identifikuj závislosti, vytvoř architekturu.

**Můj výstup (handoff JSON – zkrácená verze):**
```json
{
  "meta": {
    "dokument": "outpost_iot_handoff_2026-03-26",
    "verze": "3.0"
  },
  "fyzicky_stav_2026_03_26": {
    "laskakit_bom": { "stav": "fyzicky_k_dispozici" },
    "gme_bom": { "stav": "pripraveno_k_objednani" }
  },
  "road_block_status": [
    {"blokator": "JST PH konektor pro BMS", "status": "objednán"},
    {"blokator": "RJ45 kabel pro střídač", "status": "objednán"}
  ],
  "prioritni_poradi_po_doruceni_gme": ["..."]
}
```

**Co je zde klíčové:**
- Strojově čitelný formát (JSON) – ne jen text
- Verzování (v3.0)
- Explicitní blokátory a závislosti
- Prioritizace

---

### Fáze 3: Dílčí zpřesnění

**Princip:** Vyber jeden segment, jdi do hloubky, ale udržuj vazbu na celek.

**Můj prompt:**
```
Rozpracuj podrobně variantu B
Kontext - vše dnes dělám, vidím poprvé v životě
```

**LLM odpověď – struktura (zkráceno):**
```
# Varianta B: JK BMS TTL telemetrie – kompletní návod

## Krok 1: Identifikace konektoru na BMS
## Krok 2: Co potřebuješ z BOM
## Krok 3: Zapojení – bezpečnostní pravidla
## Krok 4: První RAW_FIRST test – bez kódu
## Krok 5: Identifikace binárního rámce
## Krok 6: Instalace ESPHome
## Krok 7: Odeslání do PC / GCP
```

**Co je zde klíčové:**
- Explicitní předpoklad "vidím poprvé v životě"
- Kroky jsou sekvenční, každý s kontrolním bodem
- Bezpečnostní pravidla před samotným zapojením
- RAW_FIRST test před jakýmkoli kódem

---

### Fáze 4: Identifikace bottleneck

**Princip:** Explicitně pojmenuj, co ti brání v postupu. Odděl fyzické od znalostních.

**Můj prompt:**
```
dupont kabel nelze zastrčit, celé tělo konektoru TTL má 7 mm 
(vnější délka > plastový obal + piny 1,2,3,4)
```

**LLM odpověď:**
```
GPS konektor na BMS je JST PH s roztečí 2.0 mm – Dupont kabel (2.54 mm) 
fyzicky nezapadne. To je běžný problém.

Máš dvě cesty:
A) Koupit správný JST PH 4pin konektor s předkrimpovanými vodiči
B) Provizorní připojení bez konektoru (riziko poškození)
```

**Co je zde klíčové:**
- Fyzický blokátor je pojmenován přesně (JST PH vs Dupont)
- Jsou nabídnuty varianty s hodnocením rizika
- Následuje doporučení (cesta A)

---

### Fáze 5: Sumarizace – syntéza

**Princip:** Shromáždi poznatky z předchozích fází do rozhodovacího podkladu.

**Můj prompt:**
```
Navrhni BOM pro nákup na GME.cz, udělám objednávku nyní.
Restrains: Pouze položky z seznamu url, vynechat nevhodné, 
zachovat sirénu = zvukové odstrašení (vysvětlit odběr = 200mA je trvalý odběr?)
```

**LLM odpověď – struktura:**
- Objednávkový košík (tabulka s kódy, cenami)
- Siréna – vysvětlení odběru
- Položky vyřazené z nákupu
- Doporučená struktura objednávky
- Implementační poznámky

**Co je zde klíčové:**
- Rozhodovací podklad je strukturovaný
- Každá položka má zdůvodnění
- Explicitní vysvětlení nejistoty (odběr sirény)

---

### Fáze 6: Fyzická akce

**Princip:** Rozhodnutí musí vést k fyzické akci. Dokumentuj, co bylo provedeno.

**Můj prompt:**
```
Ještě jsem nalezl doma tento měnič: [parametry]
```

**LLM odpověď (relevantní část):**
```
[analýza parametrů]
[aktualizace BOM – vyřazení ESP01 modulu, úspora 134 Kč]
[revidovaný nákupní košík]
```

**Co je zde klíčové:**
- Každá akce je zdokumentována
- Nález měniče vede k revizi BOM a úspoře
- Rozhodnutí je explicitní ("vyřazuji ESP01 modul")

---

### Fáze 7: Verifikace a iterace

**Princip:** Ověř, že akce vedla k očekávanému výsledku. Pokud ne, vrať se do fáze 0.

**V této fázi projektu:** Čeká se na doručení GME objednávky. První verifikační body budou:

1. **Loopback test MAX3232** – před připojením ke střídači
2. **RAW_FIRST BMS** – vidět binární data (0x4E 0x57) v terminálu
3. **RAW_FIRST střídač** – vidět data v terminálu (2400 baud)

**Co je zde klíčové:**
- Verifikace je naplánována předem
- Každá verifikace má explicitní kritérium
- Verifikace je oddělena od vlastní implementace

---

## Klíčové principy

| Princip | Formulace | Příklad z praxe |
|---------|-----------|-----------------|
| **Kotvení v realitě** | Popiš výchozí stav, než začneš řešit problém | "Mám na stole X, chybí Y" |
| **Binární MVP** | Definuj "hotovo" jako binární stav | "Data v terminálu" vs "funkční telemetrie" |
| **RAW_FIRST** | Než napíšeš kód, ověř surový vstup | Loopback test, sériový terminál |
| **Explicitní bottleneck** | Pojmenuj, co ti brání | "JST PH vs Dupont – odlišná rozteč" |
| **Strojově čitelná dokumentace** | Dokumentuj strukturovaně | JSON s metadaty, verzemi |
| **Syntéza před rozhodnutím** | Shromáždi poznatky do jednoho podkladu | Handoff JSON, BOM tabulka |
| **Akce s dokumentací** | Každá akce má záznam | "Objednáno GME-01 až GME-05" |
| **Verifikace před iterací** | Než půjdeš dál, ověř, že předchozí krok funguje | Loopback test před zapojením ke střídači |

---

## Porovnání s běžnými přístupy

| Fáze | Běžný uživatel | Metodický přístup (tento dokument) |
|------|----------------|-----------------------------------|
| **Kotvení** | "Jak zapojím BMS?" | "Mám BMS JK, GPS konektor JST PH 2.0 mm, Dupont nejde, nemám kabel" |
| **Rámec** | "Chci číst data" | "Cíl: RAW_FIRST data v terminálu, pak ESPHome, pak GCP" |
| **Struktura** | Řeší jeden senzor | Handoff JSON s prioritami, závislostmi, blokátory |
| **Zpřesnění** | Kopíruje kód z fóra | "Rozpracuj variantu B – krok za krokem, předpokládej, že to dělám poprvé" |
| **Bottleneck** | "Nejde to" | "JST PH konektor – Dupont nelze zastrčit, odlišná rozteč" |
| **Syntéza** | Otevřených 10 záložek | Jeden handoff JSON, jedna BOM tabulka |
| **Akce** | Koupí "něco" | Objednávka s explicitními kódy, zdůvodněním, cenou |
| **Verifikace** | "Snad to pojede" | Loopback test, RAW_FIRST před kódem, explicitní milestone |

---

## Role LLM v procesu

V této metodice má LLM specifickou roli. **Není to generátor kódů ani náhrada myšlení.**

| Role | Popis | Příklad z projektu |
|------|-------|-------------------|
| **Sémantický kurátor** | Překlad "unknown unknowns" do odborného slovníku | "To, co vidíš, je binární rámec JK BMS, začíná 0x4E 0x57" |
| **Syntetizér** | Konsolidace fragmentárních informací do struktury | Handoff JSON z 13 promptů |
| **Externí paměť** | Udržování kontextu napříč fázemi | Vracení se k BOM, pinoutům, prioritám |
| **Analytik variant** | Porovnání možností s explicitními kritérii | BOM analýza (vhodné/částečně/nevhodné) |
| **Validátor** | Kontrola konzistence, identifikace mezer | "Chybí DC-DC měnič – doporučuji dokoupit" |

**Uživatel zůstává v roli architekta a rozhodovatele.** LLM je nástroj, nikoli náhrada.

---

## Aplikace na jiné domény

Tento proces je doménově nezávislý. Lze ho použít pro:

### Řemeslné projekty
- Instalace FVE, elektroinstalace, opravy
- Kotvení: "Mám panel X, střídač Y, chybí kabel Z"

### Softwarový vývoj
- Nová knihovna, API integrace, debugging
- RAW_FIRST: "Než napíšu kód, ověřím API response v curl"

### Nákup a výběr techniky
- Výběr komponent, ověření kompatibility
- Syntéza: "Tabulka variant s cenami, parametry, zdůvodněním"

---

## Co dál? – Iterace metodiky

Tento dokument je **verze 1.0**. Bude iterován na základě:

1. **Zpětné vazby** – od čtenářů, kteří metodiku aplikují
2. **Vlastní zkušenosti** – při pokračování projektu Outpost 2026
3. **Selhání** – co nefungovalo, půjde do "pitevní knihy"

**Plánované rozšíření:**
- Šablona pro handoff JSON
- Checklist pro RAW_FIRST testy
- Vzorové BOM tabulky pro různé typy projektů
- Skripty pro automatickou extrakci handoff z promptů

---

## Příloha: Struktura handoff JSON (šablona)

```json
{
  "meta": {
    "dokument": "název_dokumentu",
    "verze": "x.y",
    "datum_vytvoreni": "YYYY-MM-DD",
    "operator": "jméno",
    "stav": "aktivni | čeká_se | dokončeno"
  },
  "fyzicky_stav": {
    "komponenty_k_dispozici": [],
    "komponenty_objednany": [],
    "chybi": []
  },
  "road_block_status": [
    {"blokator": "popis", "status": "vyřešeno | čeká_se | blokuje", "řešení": "popis"}
  ],
  "prioritni_poradi": [
    {"poradi": 1, "nazev": "úkol", "zavislost": [], "milestone": "binární kritérium"}
  ],
  "otevrene_otazky": [
    {"id": "Q001", "téma": "téma", "otázka": "otázka", "zpusob_ověření": "postup"}
  ],
  "bezpecnostni_poznamky": [],
  "dokumentace_fotek": []
}
```

---

## Závěr

Tento dokument vznikl jako **vedlejší produkt** reálného technického projektu. Není to teoretická úvaha, ale **extrakt z praxe** – z 24 hodin práce, 13 promptů a desítek rozhodnutí.

Pokud si z něj odnášíte jednu věc, ať je to:

**Než se zeptáš LLM "jak na to", nejdřív explicitně popiš, co máš, co nevíš a co je tvým cílem. A před tím, než napíšeš první řádek kódu, ověř, že surový vstup vypadá tak, jak očekáváš.**

---

## Odkazy

- [Repozitář Outpost 2026](https://github.com/outpost2026)
- [Laskakit BOM](https://www.laskakit.cz)
- [JK BMS ESPHome komponenta](https://github.com/syssi/esphome-jk-bms)
- [POWMR střídač ESPHome komponenta](https://github.com/odya/esphome-powmr-hybrid-inverter)
---

**Licence:** Tento dokument je vydán pod licencí CC BY-SA 4.0. Můžete ho sdílet, upravovat a používat za podmínky uvedení autora a zachování stejné licence.
