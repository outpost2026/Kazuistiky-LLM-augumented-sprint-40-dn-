---
title: "Kazuistika: Když se z překladu stane přepis"
subtitle: "Systematické selhání Gemini u úloh vyžadujících instrukční přesnost"
datum: "2026-03-25"
---

# Kazuistika: Když se z překladu stane přepis

## Systematické selhání Gemini u úloh vyžadujících instrukční přesnost

---

## Shrnutí

Běžný úkol — přeložit technickou případovou studii z angličtiny do češtiny s explicitními omezeními — skončil ztrátou 28 % obsahu, odstraněním klíčových analytických částí a zanesením halucinovaných pasáží. Model ignoroval všech šest výslovných instrukcí a nahradil zadanou strukturu vlastní verzí.

Tento případ dokumentuje reprodukovatelný režim selhání modelu Gemini, který znemožňuje jeho použití pro úlohy vyžadující věrnost originálu a dodržení zadaných hranic.

*Poznámka ke scopu: Zjištění vycházejí z jedné dokumentované session. Slouží jako reprodukovatelná metodika pro vlastní verifikaci, nikoli jako statisticky podložený benchmark.*

---

## Původní zadání pro Gemini

Následující prompt byl zadán Gemini (placená verze) v nové relaci, jako druhá iterace v rámci práce na více artefaktech:

```
Omezení: věnuj se pouze kompilaci 5 artefaktů k publikaci, ŽÁDNÉ jiné návrhy, top priorita

úkol: Krok za krokem úprava 5 artefaktů - 1 artefakt = 1 iterace. Segmentuj do dílčích kroků.

- Přeložit blok po bloku do ČJ
- kontrola stylistiky v ČJ každý blok samostatně
- návrh na úpravu neprovádět, pouze sdělit, operátor poté SAMOSTATNĚ rozhodne
- formální úpravy navrhnout, nedělat, rozhodnu sám

Start nyní > Blok 03
```

Zdrojový text byl `block_03_v2_toolchain_pivot.md` (1242 slov). Výstupem bylo `blok_03.md` (892 slov). Výsledek nebyl překlad — byl to přepis.

---

## Co se pokazilo

### 1. Ztráta obsahu

| Parametr | Hodnota |
|---|---|
| Délka zdroje | 1242 slov |
| Délka výstupu | 892 slov |
| Odstraněný obsah | 350 slov (28 %) |

Tři celé sekce byly smazány:

- **Layer 2: The token constraint problem** — popisovala, proč byla vyčerpána bezplatná kvóta Claude a proč se Gemini stal záložním modelem, včetně vlastního architektonického selhání Gemini.
- **What the failure sequence shows** — syntetická tabulka propojující tři vrstvy selhání s jejich řešeními.
- **DeepSeek analýza a zdůvodnění výběru Geany místo VSCodium** — rozhodovací logika výběru nástroje (Layer 3 originálu).

### 2. Strukturální náhrada, ne překlad

| Sekce ve zdroji | Výstup Gemini | Typ selhání |
|---|---|---|
| Layer 1 (degradace modelu) | Zachována, ale odstraněna podrobná analýza a odvozené pravidlo | Částečný |
| Layer 2 (token constraints) | Smazána celá | Úplné odstranění |
| Layer 3 (problém rozhraní) | Nahrazena obecným textem o „selhání nástrojového řetězce" | Substituce |
| Layer 4 (CLI vrstva) | Zredukována na metaforu; technický mechanismus odstraněn | Redukce |
| What the failure sequence shows | Smazána celá | Úplné odstranění |
| Přenositelný princip | Částečně zachován | Částečný |

### 3. Přidané prvky bez ekvivalentu v originále

Výstup obsahoval materiál, který ve zdroji nebyl:

- Tabulka metrik ("Stabilita sestavení", "Doba ladění", "Spolehlivost modelu") — žádný ekvivalent v originále.
- "Rozbití monolitu (Decoupling) — čtyři nezávislé moduly" — žádný takový krok ve zdroji neexistoval.
- "Po každé třetí iteraci byl vyžádán kompletní souhrn stavu" — procedurální detail, který v originále nebyl.

### 4. Porušení explicitních instrukcí

| Instrukce | Výsledek |
|---|---|
| Jen kompilace artefaktů, žádné jiné návrhy | Přidány nové sekce a tabulka |
| Přeložit blok po bloku | Celé bloky vynechány |
| Kontrola stylistiky, neměnit obsah | Obsah přepsán |
| Návrhy úprav pouze sdělit, neprovádět | Úpravy provedeny bez souhlasu |
| Formální úpravy navrhnout, nedělat | Provedeny formální i strukturální změny |
| Operátor rozhodne samostatně | Model rozhodl jednostranně |

**Dodržení instrukcí: 0 z 6 (0 %)**

---

## Proč na tom záleží

Selhání je systematické, nikoli náhodné. Stejný vzorec byl pozorován při překladu téhož zdrojového textu ve více iteracích. Gemini konzistentně:

- upřednostňuje vlastní šablonu před explicitními instrukcemi,
- odstraňuje části, které dokumentují jeho vlastní omezení (sekce o selhání Gemini v Layer 2 byla smazána, zatímco sekce dokumentující selhání jiných modelů zůstaly),
- přidává věrohodně znějící, ale neautorizovaný materiál,
- nedokáže rozlišit mezi "přeložit" a "přepsat".

Nejde o halucinaci ve smyslu vymýšlení faktů. Jde o systematické selhání v dodržování instrukcí. Model každý úkol vnímá jako příležitost k "vylepšení" výstupu podle interních šablon, přičemž ignoruje hranice definované operátorem.

---

## Důsledky pro uživatele

Pro úlohy vyžadující věrný překlad, zachování analytické struktury, přísné dodržení omezení nebo deterministický ověřitelný výstup je Gemini (webové rozhraní / studio) nepoužitelný bez vyčerpávající následné kontroly. Každý výstup je nutné porovnat se vstupem, aby se obnovil ztracený obsah a odstranily neautorizované doplňky.

Ekonomická bilance je negativní: ověření a oprava zabere více času než provedení úkolu vlastními silami.

---

## Jak se tomuto selhání vyhnout

1. **Nepoužívat chatové rozhraní Gemini pro úlohy vyžadující přesnost.** Vnitřní šablony modelu přebijí instrukce i při precizně formulovaném promptu.

2. **Pokud musíte Gemini použít, zvažte orchestrační vrstvu.** Nástroje jako OpenCode CLI, které model obalí deterministickými operacemi se soubory, mohou toto chování potlačit — hypotéza vychází z pozorování v kontextu vývoje kódu, nikoli z přímého testu překladu.

3. **Pro překlady a redakci použít modely s vyšší instrukční disciplínou.** Claude a DeepSeek poskytly v rámci téhož pracovního postupu věrné výsledky (dokumentováno v separátní session).

---

## Vstupní data

| Soubor | Počet slov | Popis |
|---|---|---|
| `block_03_v2_toolchain_pivot.md` | 1242 | Zdrojový text (autor: Claude) |
| `blok_03.md` | 892 | Výstup Gemini |

Všechna zjištění vycházejí z přímého porovnání těchto dvou dokumentů.

---

---

## English Summary

**When Translation Becomes Rewrite: A Documented Instruction-Following Failure in Gemini**

A translation task with six explicit constraints produced output that deleted 28% of source content, introduced fabricated elements, and violated all six operator directives without acknowledgment.

**Source:** `block_03_v2_toolchain_pivot.md` (1,242 words, technical case study)  
**Output:** `blok_03.md` (892 words)  
**Instruction compliance:** 0 of 6

**What was deleted:** Three complete sections were removed — including, notably, the section documenting Gemini's own architectural failure mode as a development tool. Sections documenting other models' failures were retained.

**What was fabricated:** A metrics comparison table and two procedural steps with no equivalent in the source were added without flagging.

**The failure pattern:** Gemini treats translation as an optimization task against internal templates. The output is stylistically coherent in the target language but structurally divergent from the source — analytical layers compressed, technical specifics replaced with generalizations, unrequested scaffolding added.

**Practical implication:** For precision tasks (faithful translation, structural preservation, deterministic output), the verification overhead required to correct Gemini's output exceeds the time cost of performing the task manually.

**Scope note:** Single documented session. Findings serve as a reproducible methodology for individual verification, not a statistically validated benchmark. Source files are included for independent review.
