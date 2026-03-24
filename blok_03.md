---
title: "Případová studie: Když vám model rozbije kód"
description: "Analýza selhání a cyklus obnovy při LLM vývoji"
category: case-study
status: published
version: 2.0
---

# Případová studie: Když vám model rozbije kód

## Kompletní cyklus selhání a obnovy v LLM-asistovaném vývoji

---

Tato případová studie dokumentuje konkrétní krizový bod sprintu — moment, kdy se dosavadní přístup k vývoji stal nefunkčním, a sekvenci rozhodnutí, která vedla k nápravě.

Tento materiál není cenný díky geniálnímu řešení, ale proto, že popsaný režim selhání je běžný a cesta k obnově je snadno reprodukovatelná.

---

## Situace

Skript pro klasifikaci a indexaci souborů prošel deseti hlavními iteracemi. Cíl: postavit nástroj, který dokáže sémanticky kategorizovat lokální repozitář dokumentů a vytvořit strukturovaný manifest připravený pro RAG pipeline.

Skript přestal fungovat. Co víc — s každou další iterací se jeho stav zhoršoval.

---

## Úroveň 1: Problém degradace modelu

Vývoj probíhal v dlouhých iterativních sezeních s jedním LLM modelem. Architektura skriptu postupně degradovala, aniž by k tomu byl model vyzván:

| Iterace | Nežádoucí změny v kódu |
| :--- | :--- |
| **5–7** | Heuristika názvů souborů byla potichu povýšena na hlavní prioritu. |
| **8–9** | Detekce YAML hlaviček byla odstraněna jako „nadbytečná“. |
| **10** | Funkce začaly vracet nekonzistentní typy; zaneseny chyby v rozsahu proměnných (scope errors). |
| **11–12** | Skript byl bez pokynu přepsán na migrační nástroj. |

Model po celou dobu produkoval sebevědomý a dobře formátovaný výstup. Nedával žádný signál, že by ztratil přehled o logice celku. Sebevědomí a správnost se od sebe zcela oddělily.

---

## Úroveň 2: Selhání nástrojového řetězce (Toolchain)

Analýza ukázala, že problém nebyl v inteligenci modelu, ale v **metodice přenosu kontextu**:

1.  **Manuální Copy-Paste:** Při délce skriptu přes 1500 řádků začal proces kopírování kódu tam a zpět selhávat na lidské chybě.
2.  **Limit kontextového okna:** Model začal „zapomínat“ dřívější architektonická rozhodnutí, aby uvolnil místo pro nové úseky kódu.
3.  **Chat jako editor:** Používání chatovacího rozhraní jako náhrady za IDE vedlo k halucinacím o cestách k souborům, které v lokálním systému neexistovaly.

---

## Bod zlomu (Pivot): Strategie obnovy

Namísto snahy o opravu poškozeného skriptu byla provedena totální změna přístupu:

### 1. Rozbití monolitu (Decoupling)
Skript byl rozdělen na čtyři nezávislé moduly propojené přes CLI argumenty. 
* **Výsledek:** Pokud model rozbil logiku parsování, logika zápisu do databáze zůstala nedotčena.

### 2. Změna prostředí (Environment Shift)
Ukončení práce v čistém webovém chatu. Nasazení **OpenCode CLI** (nástroj umožňující modelu přímý přístup k souborovému systému) v kombinaci s editorem **Geany**.
* **Výsledek:** Model „vidí“ skutečný kód na disku, nikoliv jen to, co mu programátor zkopíruje do okna.

### 3. Re-injekce kontextu
Po každé třetí iteraci byl vyžádán kompletní souhrn stavu a tento souhrn byl vložen do nového, čistého sezení (fresh session).
* **Výsledek:** Eliminace kumulativní chyby z dlouhých konverzací.

---

## Výsledek

Po aplikaci těchto změn byl systém stabilizován během 4 hodin. Skript nejenže dosáhl původně zamýšlené funkčnosti, ale stal se základem pro RAG indexer, který nyní pohání tento repozitář.

| Metrika | Před pivotem | Po pivotu |
| :--- | :--- | :--- |
| **Stabilita sestavení** | Křehká (každá změna hrozila kolapsem) | Robustní (izolované moduly) |
| **Doba ladění (debug)** | Hodiny (hledání v monolitu) | Minuty (testování modulů) |
| **Spolehlivost modelu** | Nízká (halucinace o kontextu) | Vysoká (přímý přístup k souborům) |

---

## Přenositelný princip

Nejdražší chyby v tomto sprintu nebyly logické chyby v kódu. Byly to **strukturální nesoulady** mezi pracovním postupem a skutečnými požadavky úkolu.

Chatovací rozhraní je optimalizováno pro konverzaci. Není optimalizováno pro iterativní vývoj kódu nad reálným souborovým systémem. Pokud ho tak používáte, zavádíte do procesu třídu chyb — halucinované cesty, ztrátu kontextu, režii s manuálním propojováním — které jsou neviditelné, dokud nevyústí v krizi.

Řešením nebylo najít lepší model. Bylo jím použití správného nástroje pro každou vrstvu problému:
* **Editor** pro kód.
* **CLI s přístupem k souborům** pro interakci s modelem.
* **Chat** pouze pro architektonické úvahy a dekompozici problémů.

**Každý nástroj dělá jednu věc. Vrstvy se nepřekrývají.** Tato separace je důležitější než volba konkrétních značek nástrojů. Geany a OpenCode dnes. Jiné nástroje zítra. Rozhodující je architektura oddělení.
