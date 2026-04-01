# Od nuly k produkci: LLM augmentovaný vývojový sprint

**Případová studie v AI augmentovaném učení**

---

Tento repozitář dokumentuje 40denní sprint, ve kterém vývojář, osoba jako vy, bez předchozích zkušeností s Pythonem, cloudovou infrastrukturou nebo LLM nástroji postavil a nasadil produkční systémy na Google Cloud Platform – s využitím jazykových modelů jako primárního vývojového nástroje.

Cílem tohoto dokumentu není popsat vývojáře. Je popsat *metody* – konkrétně které přístupy fungovaly, které selhaly a co o tom říkají data.

## Co bylo postaveno

- ETL scraping pipeline nasazené na GCP Cloud Run s Cloud Scheduler
- Ingest meteorologických dat z ČHMÚ
- Off-grid solární telemetrická pipeline: BMS data, LAZ LiDAR geodata, pvlib solární modelování
- RAG-ready indexer dokumentů se sémantickou klasifikací (tento repozitář)
- Telegram notifikace pro všechny výstupy pipeline

Všechny systémy běží 24/7 s téměř nulovými náklady na serverless infrastruktuře.

## Co tato případová studie zkoumá

1. Jak byly LLM nástroje používány – a zneužívány – během sprintu
2. Které konkrétní postupy produkovaly spolehlivý výstup vs. které způsobovaly regrese - **[kazuistika Gemini překlad](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/Kazuistika_Gemini_preklad.md)**
3. Jakou roli hrály předchozí ne-softwarové zkušenosti v urychlení adopce
4. Naměřený čas do kompetence v 6 technologických doménách

## Pro koho to je

Vývojáři začínající s LLM asistovanými workflow. Lidé, kteří narazili na situaci, kdy "AI mi pořád dává nefunkční kód". Kdokoliv, kdo zvažuje, zda samostatné LLM augmentované učení může produkovat produkční výsledky bez formálního školení nebo týmu.
- Součástí repozitáře je rovněž *[metodologie práce s LLM](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/main/metodika_prace_s_LLM.md)* jako **user case z fyzického světa** - rozhodovací procesy pro realizaci komplexního úkolu

---

*Toto je živý dokument. Bloky jsou přidávány iterativně.*
*Aktuální verze pokrývá: metodologii vývoje, způsoby selhání, klíčové principy.*
