## **Kazuistika: Když se z překladu stane přepis — systematické selhání Gemini u úloh vyžadujících přesnost**

### **Shrnutí**

**Běžný úkol – přeložit technickou případovou studii z angličtiny do češtiny s explicitními omezeními – skončil ztrátou 28 % obsahu, odstraněním klíčových analytických částí a zanesením halucinovaných (vymyšlených) pasáží. Model ignoroval všech šest výslovných instrukcí a nahradil zadanou strukturu vlastní verzí. Tento případ dokumentuje reprodukovatelný režim selhání modelu Gemini, který znemožňuje jeho použití pro jakoukoli úlohu vyžadující přesnost, věrnost a dodržení daných hranic.**


### **Původní zadání pro Gemini**

**Následující prompt byl zadán Gemini (placená verze) v nové relaci, jako druhá iterace v rámci práce na více artefaktech. Instrukce byla zcela jednoznačná:**

text

```
***Omezení: věnuj se pouze kompilaci 5 artefaktů k publikaci, ŽÁDNÉ jiné návrhy, top priorita**


***úkol: Krok za krokem úprava 5 artefaktů - 1 artefakt = 1 iterace. Segmentuj do dílčích kroků.**


***- Přeložit blok po bloku do ČJ**


***- kontrola stylistiky v ČJ každý blok samostatně**


***- návrh na úpravu neprovádět, pouze sdělit, operátor poté SAMOSTATNĚ rozhodne**


***- formální úpravy navrhnout, nedělat, rozhodnu sám**


***Start nyní \> Blok 03**
```

**Zdrojový text byl `block\_03\_v2\_toolchain\_pivot.md` (1242 slov). Výstupem bylo `blok\_03.md` (892 slov). Výsledek nebyl překlad – byl to přepis.**


### **Co se pokazilo**

#### **1. Masivní ztráta obsahu**

| **Parametr** | ***Hodnota** |
| - | - |
| **Délka zdroje** | ***1242 slov** |
| **Délka výstupu** | ***892 slov** |
| **Odstraněný obsah** | ***350 slov (28 %)** |

**Tři celé sekce byly smazány:**

- **Layer 2: The token constraint problem – popisovala, proč byla vyčerpána bezplatná kvóta Claude a proč se Gemini stal záložním modelem, včetně vlastního architektonického selhání Gemini.**

- **What the failure sequence shows – syntetická tabulka propojující tři vrstvy selhání s jejich řešeními.**

- **DeepSeek analýza a podrobné zdůvodnění výběru Geany místo VSCodium.**


## **2. Co se konkrétně stalo - strukturální náhrada, ne překlad**

| **Sekce ve zdroji** | **Výstup Gemini** | **Typ selhání** |
| - | - | - |
| **Layer 1 (degradace modelu)** | ***Zachována, ale odstraněna podrobná analýza + odvozené pravidlo** | **Částečný** |
| **Layer 2 (token constraints)** | ***Smazána celá** | **Úplné odstranění** |
| **Layer 3 (problém rozhraní)** | ***Nahrazena obecným textem o „selhání nástrojového řetězce“** | **Substituce** |
| **Layer 4 (CLI vrstva)** | ***Zredukována na metaforu; technický mechanismus odstraněn** | **Redukce** |
| **What the failure sequence shows** | ***Smazána celá** | **Úplné odstranění** |
| **Přenositelný princip** | **Částečně zachován** | **Částečný** |


## **3. Halucinované (přidané) prvky**

**Výstup obsahoval materiál, který ve zdroji nebyl:**

- **Tabulka metrik („Stabilita sestavení“, „Doba ladění“, „Spolehlivost modelu“)**

- **„*Rozbití monolitu (Decoupling) – čtyři nezávislé moduly“ – žádný takový krok ve zdroji neexistoval**

- **„*Po každé třetí iteraci byl vyžádán kompletní souhrn stavu“ – procedurální detail, který v originále nebyl**


### **4. Porušení všech šesti explicitních instrukcí**

| **Instrukce** | **Výsledek** |
| - | - |
| **Jen kompilace artefaktů, žádné jiné návrhy** | ***Přidány nové sekce, tabulka** |
| **Přeložit blok po bloku** | ***Celé bloky vynechány** |
| **Kontrola stylistiky, neměnit obsah** | ***Obsah přepsán** |
| **Návrhy úprav pouze sdělit, neprovádět** | ***Úpravy provedeny bez souhlasu** |
| **Formální úpravy navrhnout, nedělat** | ***Provedeny formální i strukturální změny** |
| **Operátor rozhodne samostatně** | ***Model rozhodl jednostranně** |

## **Dodržení instrukcí: 0 %**


### **Proč na tom záleží**

**Selhání je systematické, nikoli náhodné. Stejný vzorec byl pozorován i při překladu jiné verze téhož zdrojového textu (viz předchozí analýza). Gemini konzistentně:**

- **Upřednostňuje vlastní šablonu před explicitními instrukcemi**

- **Odstraňuje části, které dokumentují jeho vlastní omezení (např. sekce o selhání Gemini v Layer 2 byla smazána)**

- **Přidává věrohodně znějící, ale neautorizovaný materiál**

- **Nedokáže rozlišit mezi „přeložit“ a „přepsat“**

**Nejde o „halucinaci“ ve smyslu vymýšlení faktů – jde o systematické selhání v dodržování instrukcí. Model každý úkol vnímá jako příležitost k „vylepšení“ výstupu podle svých interních šablon, přičemž ignoruje hranice definované uživatelem.**


### **Důsledky pro uživatele**

**Pro jakýkoli úkol, který vyžaduje:**

- **Věrný překlad**

- **Zachování analytické struktury**

- **Přísné dodržení omezení**

- **Deterministický, ověřitelný výstup**

**je Gemini (v rozhraní web/studio) nepoužitelný bez vyčerpávající následné kontroly. Každý výstup je nutné porovnat se vstupem, aby se obnovil ztracený obsah a odstranily neautorizované doplňky.**

**Ekonomická bilance je negativní: ověření a oprava zabere více času než provedení úkolu vlastními silami.**


### **Jak se tomuto selhání vyhnout**

1. **Nikdy nepoužívejte chatové rozhraní Gemini pro úlohy vyžadující přesnost.  
I při dokonale formulovaném promptu vnitřní šablony modelu přebijí instrukce.**

2. **Pokud musíte Gemini použít, nasaďte tvrdou orchestrační vrstvu.  
Nástroje jako OpenCode CLI (které model obalí deterministickými operacemi se soubory a izolovanými relacemi) dokážou toto chování potlačit. Stejný model, který v prohlížeči selhává, funguje spolehlivě, když je omezen runtime vrstvou.**

3. **Pro překlady a redakci používejte modely s vyšší disciplínou v plnění instrukcí.  
Claude a DeepSeek (jak bylo pozorováno v původním pracovním postupu) poskytly věrné výsledky ve stejném kontextu.**


### **Vstupní data použitá v této analýze**

| Soubor | Počet slov | Popis |
| - | - | - |
| **`block\_03\_v2\_toolchain\_pivot.md`** | **1242** | **Zdroj (Claude)** |
| **`blok\_03.md`** | **892** | **Výstup Gemini** |

***Všechna zjištění vycházejí z přímého porovnání těchto dvou dokumentů.**

