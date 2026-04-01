# Od nuly k produkci: LLM augmentovaný vývojový sprint

**Případová studie v AI augmentovaném učení**

---

Tento repozitář, respektive sada kazuistik ukazuje, jak při učení softwaru využít postupy z technické praxe a urychlit tak práci s AI. Obsahuje rozbory spolehlivosti modelů, metodiku pro stavbu IoT systémů a příklady automatizace, která řeší konkrétní úkoly v reálném světě.
Cílem tohoto dokumentu není popsat vývojáře (k němu se autor ani nehlásí).

Je popsat metody – konkrétně které přístupy fungovaly, které selhaly a co o tom říkají data.


---


## Co tato případová studie zkoumá

1. Jak byly LLM nástroje používány, které konkrétní postupy produkovaly spolehlivý výstup vs. které způsobovaly regrese - **[kazuistika Gemini překlad](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Kazuistika_Gemini_preklad.md)**
3. Jakou roli hrály předchozí ne-softwarové zkušenosti v urychlení adopce - **[Kód, který už dávno znáte](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_05_transfer_learning_cz.md)**
4. Příběh o tom, jak automatizace přestává být jen nástrojem a stává se generátorem reálných zdrojů - **[Můj kód je lepší nákupčí než já: Jak mi Python sehnal Dell za 2 000 Kč](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/block_04_case_self_bootstrapping_cz.md)**
5. Součástí repozitáře je rovněž **[metodologie práce s LLM](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/metodika_prace_s_LLM.md)** jako user case z fyzického světa - rozhodovací procesy pro realizaci komplexního úkolu vývoje IoT telemetrie začátečníkem
6. Jak si vedlo pět nejlepších AI modelů v mé krátké praxi - **[Empirická evaluace LLM modelů v deterministickém workflow](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Empiricka_evaluace_v2.md)** - Gemini stále naráží na stejné problémy


## Co bylo dosaženo

- ETL scraping pipeline nasazené na GCP Cloud Run s Cloud Scheduler
- Ingest meteorologických dat z ČHMÚ
- Off-grid solární telemetrická pipeline: BMS data, LAZ LiDAR geodata, pvlib solární modelování
- Telegram notifikace pro všechny výstupy pipeline


Všechny systémy běží 24/7 s téměř nulovými náklady na serverless infrastruktuře.


## Pro koho to je

Vývojáři začínající s LLM asistovanými workflow. Lidé, kteří narazili na situaci, kdy "AI mi pořád dává nefunkční kód". Kdokoliv, kdo zvažuje, zda samostatné LLM augmentované učení může produkovat produkční výsledky bez formálního školení nebo týmu.

---

*Toto je živý dokument. Bloky jsou přidávány iterativně.*
*Aktuální verze pokrývá: metodologii vývoje, způsoby selhání, klíčové principy.*
