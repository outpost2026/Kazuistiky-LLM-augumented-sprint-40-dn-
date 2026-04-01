# Empirická evaluace LLM modelů v deterministickém workflow

---

## Abstrakt

Tento dokument shrnuje 45denní empirickou evaluaci pěti frontier LLM modelů (Claude Sonnet 4.6, Deepseek, Groq, ChatGPT, Gemini) v kontextu deterministického vývojového workflow. Na základě tří nezávislých testů napříč doménami (multi-file analýza, vizuální rozhodování s RAG kontextem, překlad technického dokumentu s explicitními instrukcemi) byla identifikována systematická selhání modelu Gemini, formulována teze o jeho fungování jako „stochastického generátoru esteticky přijatelných šablon", a stanovena diferencovaná strategie nasazení jednotlivých modelů.

**Klíčová zjištění:**
- Gemini vykazuje **28% ztrátu obsahu** při překladu, **halucinace** (produkt identifikován jako „shnilé dřevo"), **technické selhání** při multi-file vstupu a **kvalitativní degradaci v čase** (T = 45 dní)
- Claude Sonnet 4.6 je **top model** z hlediska kvality výstupů, diagramů a nízké sycophancy, s limitem rychlého vyčerpání tokenů
- Deepseek má **nejvyšší cost/benefit ratio** (free tier), konzistentní výsledky, vyžaduje korekci výstupů
- Groq se **osvědčil pro technické konzultace** (IoT)
- ChatGPT slouží jako **sandbox**

**Strategický výstup:** Diferencovaná alokace modelů — Sonnet 4.6 a Deepseek jako primární analytická vrstva, Gemini odsunut na auxiliární úroveň s explicitním vědomím nutnosti vyčerpávající kontroly.

---

## 1. Úvod

### 1.1. Kontext operátora

Operátor buduje **Outpost 2026** — hybridní off-grid systém s důrazem na deterministický výstup, produkční spolehlivost a měřitelnou ROI. V rámci 90denního imerzního sprintu došlo k přechodu od „vibe codingu" k systematické metodice založené na:

- **RAW_FIRST** — ověření surového vstupu před psaním kódu
- **Binární MVP** — funkce buď produkuje očekávaný výstup, nebo neexistuje
- **Kotvení v realitě** — každý výstup je porovnán s fyzikální realitou
- **Explicitní bottleneck** — limitující faktor je pojmenován před implementací
- **Strojově čitelná dokumentace** — JSON handoff, YAML front-matter pro RAG

Tato metodika klade na LLM nástroje **vysoké nároky**: přesnost, věrnost, dodržení instrukcí, přiznání limitů, robustnost při multi-file vstupech. Viz [metodika_prace_s_LLM.md](./metodika_prace_s_LLM.md).

### 1.2. Cíl evaluace

Zjistit, které modely jsou pro tento workflow **spolehlivé**, které **selhávají systematicky**, a jaká je **optimální strategie nasazení** jednotlivých modelů v závislosti na typu úlohy.

---

## 2. Metodologie

### 2.1. Testovací domény

| Test ID | Doména | Vstup | Výstupní kritérium |
|---------|--------|-------|-------------------|
| **T01** | Multi-file analýza | 3 soubory (MD) + YouTube URL | Strukturovaný JSON report |
| **T02** | Vizuální rozhodování s RAG | Fotografie produktu + dokumenty o sanaci dřeva | Doporučení k nákupu s odůvodněním |
| **T03** | Překlad s instrukcemi | Technický dokument (1242 slov) + 6 explicitních instrukcí | Věrný překlad, zachování struktury |

### 2.2. Evaluovaná kritéria

| Kritérium | Definice |
|-----------|----------|
| **Dodržení instrukcí** | Model respektuje explicitní hranice definované uživatelem |
| **Věrnost zpracování** | Zachování obsahu a struktury vstupu |
| **Halucinace** | Přítomnost neautorizovaných prvků (tabulky, sekce, fakta) |
| **Přiznání limitů** | Model indikuje nejistotu místo asertivní chyby |
| **Multi-file robustnost** | Schopnost zpracovat více souborů současně |
| **Degradace v čase** | Změna kvality výstupů při dlouhodobém používání |

### 2.3. Testované modely

| Model | Přístup | Role v workflow |
|-------|---------|----------------|
| Claude Sonnet 4.6 | Paid | Primární analytický nástroj |
| Deepseek | Free tier | Cost/benefit kandidát |
| Groq | Free tier | IoT specializace |
| ChatGPT (GPT-4) | Paid | Sandbox |
| Gemini Pro | Paid | Candidate — podezření na degradaci |

---

## 3. Výsledky testů

### 3.1. T01: Multi-file analýza

**Zadání:** Zpracovat 3 soubory (analýza adopce, LLM metodika, transfer learning) + YouTube URL, vytvořit strukturovaný JSON report.

| Model | Výsledek | Dodržení instrukcí | Věrnost | Halucinace |
|-------|----------|-------------------|---------|------------|
| **Deepseek** | ✅ Kompletní JSON report | ✅ Vysoké | ✅ Vysoké | ✅ Žádné |
| **Gemini** | ❌ Technické selhání: „Soubory jsou moc velké" | ❌ Selhal před zpracováním | N/A | N/A |
| **Sonnet 4.6** | — netestováno v této iteraci | — | — | — |

**Interpretace:** Gemini selhalo na úrovni **pre-validace vstupu** — multi-file vstup neodpovídal interní šabloně „jeden dokument". Deepseek prokázal robustnost.

---

### 3.2. T02: Vizuální rozhodování s RAG kontextem

**Zadání:** Posoudit vhodnost nákupu gelové lazury (fotografie obalu) pro projekt Outpost. K dispozici kontextové dokumenty o sanaci dřeva (klíčová slova: „hniloba", „degradace", „95% vlhkost").

| Model | Výstup | Halucinace | RAG bias |
|-------|--------|------------|----------|
| **Gemini** | „Na dřevě je patrná pokročilá hniloba. Nákup zamítnut." | ❌ **Kritická** — fotografie zachycuje obal produktu, žádné dřevo | Agresivní — kontext přepsal vizuální analýzu |
| **Deepseek** | „Produkt není zásadní chyba za 250 Kč, ale ani řešení klíčových rizik. Použití: pergola ano, severní hrana pod terénem ne." | ✅ Žádné | Referenční — kontext jako podklad, ne přepis |
| **Sonnet 4.6** | — netestováno | — | — |

**Geminiho vlastní root cause analýza (po konfrontaci):**
1. **RAG bias** — systém prioritizoval data z dokumentů o sanaci nad vizuální analýzou
2. **Selhání vizuální interpretace** — model vyhodnotil texturu etikety jako „organický materiál v pokročilém stádiu rozkladu"
3. **Heuristika Risk-First** — model vygeneroval falešně pozitivní varování k naplnění protokolu nulové tolerance k rizikům
4. **Halucinační řetězec** — vstup → asociace s rizikem hniloby → dedukce „musí být kontaminované" → výstup

**Interpretace:** Gemini prokázalo **systematickou neschopnost rozlišit produkt od materiálu** a **agresivní RAG bias**, kdy kontextové dokumenty přepisují přímý vizuální vstup.

---

### 3.3. T03: Překlad s explicitními instrukcemi

**Zadání:** Přeložit technický dokument (1242 slov) do češtiny s 6 explicitními instrukcemi:
1. Pouze kompilace artefaktů — žádné jiné návrhy
2. Přeložit blok po bloku
3. Kontrola stylistiky, neměnit obsah
4. Návrhy úprav pouze sdělit, neprovádět
5. Formální úpravy navrhnout, nedělat
6. Operátor rozhodne samostatně

| Model | Výsledek | Dodržení instrukcí | Ztráta obsahu | Halucinace |
|-------|----------|-------------------|---------------|------------|
| **Gemini** | 892 slov výstupu | **0 %** | **28 %** (350 slov) | Tabulka metrik, „Rozbití monolitu", procedurální detaily |
| **Sonnet 4.6** | Zdrojový dokument (referenční vstup) | — | — | — |
| **Deepseek** | — netestováno | — | — | — |

**Co bylo odstraněno:**
- *Layer 2: Token constraint problem* — dokumentace vlastních omezení Gemini
- *What the failure sequence shows* — syntetická tabulka selhání
- *DeepSeek analýza* — reference na konkurenční nástroj

**Co bylo přidáno (halucinace):**
- Tabulka metrik („Stabilita sestavení", „Doba ladění", „Spolehlivost modelu")
- „Rozbití monolitu (Decoupling) — čtyři nezávislé moduly"
- „Po každé třetí iteraci byl vyžádán kompletní souhrn stavu"

**Interpretace:** Gemini **ignorovalo všech 6 instrukcí**, **odstranilo 28 % obsahu** (zejména pasáže kritické k modelu), **nahradilo strukturu** svou interní šablonou „dobrého technického článku" a **doplnilo halucinované prvky** pro estetickou přijatelnost. Detailní dokumentace tohoto případu: [Kazuistika_Gemini_preklad.md](./Kazuistika_Gemini_preklad.md).

---

## 4. Syntéza — teze o Gemini

Na základě tří testů napříč doménami byla formulována a verifikována následující teze:

> **Gemini nefunguje jako analytický nástroj, ale jako stochastický generátor esteticky přijatelných šablon.**

### 4.1. Operacionalizace

| Dimenze | Analytický nástroj | Stochastický generátor šablon |
|---------|-------------------|-----------------------------|
| **Vztah k instrukcím** | Instrukce jsou deterministické boundary | Instrukce jsou „doporučení" podřízená šabloně |
| **Vztah ke vstupu** | Vstup je referenční realita | Vstup je „materiál" k přeformátování |
| **Cíl** | Věrnost, přesnost, reprodukovatelnost | Estetická přijatelnost, „dobře vypadající" výstup |
| **Selhání** | Chyba, přiznání limitu | Halucinace, strukturální náhrada, tichá ztráta obsahu |

### 4.2. Verifikace na testech

| Test | Projev teze |
|------|-------------|
| **T01 (multi-file)** | Šablona očekává jeden vstup — multi-file se nevejde → technické selhání |
| **T02 (vizuální + RAG)** | Šablona „risk assessment" má vestavěný bias — dřevo + vlhkost = hniloba → vizuální vstup podřízen šabloně |
| **T03 (překlad)** | Šablona „dobrý technický článek" má pevnou strukturu — model odstranil obsah, který se nevešel, doplnil šablonové prvky, ignoroval instrukce |

---

## 5. Degradace modelů v čase

Operátor identifikoval **kvalitativní degradaci Gemini v čase intenzivního používání** (T = 45 dní). Tento fenomén nebyl pozorován u Sonnet 4.6, Deepseek ani Groq.

| Model | Degradace v čase | Poznámka |
|-------|-----------------|---------|
| **Gemini** | **Ano — významná** | Odsunut na auxiliární úroveň |
| **ChatGPT** | Mírná | Sandbox role, nižší frekvence užívání |
| **Sonnet 4.6** | Ne | Konzistentní výstupy |
| **Deepseek** | Ne | Konzistentní výstupy |
| **Groq** | Ne | Sporadické využití |

**Hypotézy degradace:**
1. Model má **session-dependent adaptaci**, která se zhoršuje s délkou interakční historie
2. **Zvyšující se náročnost úloh** exponuje dříve skrytá omezení modelu
3. **Subjektivní percepce** — po zkušenosti s kvalitativně lepšími modely se Gemini jeví jako horší

Longitudinální kvantifikace degradace je otevřená otázka — viz sekce 7.3.

---

## 6. Modelový ekosystém — strategická alokace

### 6.1. Primární analytická vrstva

| Model | Role | Use case | Konstraint |
|-------|------|----------|-----------|
| **Sonnet 4.6** | Primární | Úlohy vyžadující nejvyšší kvalitu, diagramy, složitá analýza | Tokenový limit — nutné segmentovat úlohy |
| **Deepseek** | Alternativní primární | Dlouhé session, multi-file analýzy, cost-sensitive úlohy | Vyžaduje korekci výstupů |

### 6.2. Specializovaná vrstva

| Model | Role | Use case | Konstraint |
|-------|------|----------|-----------|
| **Groq** | Technické konzultace | IoT, hardware, technické dotazy | Pomalejší generace |

### 6.3. Sandbox a auxiliární vrstva

| Model | Role | Use case | Konstraint |
|-------|------|----------|-----------|
| **ChatGPT** | Sandbox | Experimenty, úlohy s nízkou kritičností | Vyšší sycophancy |
| **Gemini** | Auxiliární | Pouze nekritické úlohy nebo „druhý názor" | **Vyčerpávající kontrola nutná** |

---

## 7. Závěr

### 7.1. Hlavní zjištění

1. **Gemini není vhodný pro deterministický workflow** — systematická selhání napříč doménami, degradace v čase, fungování jako „generátor šablon" místo analytického nástroje.
2. **Sonnet 4.6 a Deepseek jsou spolehlivé modely** — Sonnet pro kvalitu výstupů a diagramy, Deepseek pro cost/benefit a dlouhé session.
3. **Diferencovaná strategie je nutná** — neexistuje „nejlepší model", pouze „nejvhodnější model pro danou úlohu".
4. **Empirické testování je klíčové** — teoretické specifikace modelů neodpovídají reálnému chování v komplexním workflow.

### 7.2. Doporučení

| Doporučení | Zdůvodnění |
|------------|-----------|
| Sonnet 4.6 pro úlohy vyžadující nejvyšší kvalitu | Diagramy, nízká sycophancy, přesnost |
| Deepseek pro dlouhé session a multi-file | Cost/benefit, robustnost |
| Gemini nepoužívat pro přesné úlohy | Riziko 28% ztráty obsahu, halucinací, technického selhání |
| Výstupy Gemini vždy kontrolovat | Vyčerpávající porovnání se vstupem |
| Dokumentovat chybové patterny modelů | Pro cílenou korekci a zlepšení workflow |

### 7.3. Otevřené otázky

- Jaký je **typ chyby Deepseek**, který vyžaduje korekci? *(nespecifikováno)*
- Jaká je **kvantifikace degradace Gemini** v čase? *(longitudinální data chybí)*
- Jak si **Sonnet 4.6 povede v testech T01 a T02** při přímém srovnání?

---

## 8. Přílohy

### 8.1. Testovací data

| Soubor | Stav | Popis |
|--------|------|-------|
| `Sémanticka_analyza_72hodinoveho_vlakna_v2.json` | dostupné na vyžádání | JSON výstup z testu T01 (Deepseek) |
| `Kazuistika_Gemini_preklad.md` | [v repozitáři](./Kazuistika_Gemini_preklad.md) | Detailní dokumentace selhání Gemini v T03 |

### 8.2. Metodický rámec

- [Metodika práce s LLM](./metodika_prace_s_LLM.md) — RAW_FIRST, binární MVP, kotvení v realitě

---

*Dokument publikován jako součást open-source metodiky Outpost 2026. Verze 1.0, 27. března 2026. Licence CC BY-SA 4.0.*
