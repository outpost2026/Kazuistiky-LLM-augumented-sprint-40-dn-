# GCP – infrastrukturní kontext a datové dumpy

Tato branch dokumentuje **správu, provoz a evoluci GCP portfolia** projektu PrahaScrapersV1. Obsahuje jednak aktuální přehled celého stacku (ingest), jednak historické dumpy z bucketů, které ilustrují vývoj pipeline a typ ukládaných dat.

## 🗂️ Obsah

- **gcp_stack_ingest_v3.md** – živý snapshot GCP projektu (stav 2026-03-14)

  Popisuje kompletní serverless-first architekturu: Cloud Run, Functions, Scheduler, Firestore, BigQuery, meteo pipeline, VM (legacy), buckety a service accounts.  
  → Slouží jako **zdroj pravdy** pro GCP nastavení a rozhodnutí.

- Ostatní **.py` soubory** – dumpové vzorky z produkčních bucketů
  
## 🧭 Kontext

- **Projekt:** `PrahaScrapersV1` (`project-4ac30110-41b1-4783-a5d`)
- **Primární region:** `europe-west1`
- **Architektura:** serverless-first (Cloud Run/Functions), VM pouze pro legacy ETL
- **Hlavní komponenty:** miner-orchestrator, chmu-meteo-miner, iot-ingest-beta, Firestore, Scheduler (6 jobů vč. meteo)

## 🔍 Pro koho je tato branch

- Pro **audit GCP nastavení** – přehled služeb, SA, bucketů, schedulerů
- Pro **analýzu výstupů pipeline** – ukázky dat, která putují do GCS / RAG
- Pro **zpětnou rekonstrukci vývoje** – dump commitů + historie změn v kazuistikách

## 📌 Poznámka

Všechny citlivé údaje (API klíče, credentials) nejsou součástí repozitáře. Ingest popisuje **pouze konfiguraci a topologii**, nikoli tajemství.

> Stav k 2026-03-14 – aktualizace ingestu se řídí direktivou *serverless-first*.
