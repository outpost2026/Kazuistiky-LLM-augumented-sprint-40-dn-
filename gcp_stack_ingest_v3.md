---
dokument: GCP_Stack_Ingest
verze: "3.0"
snapshot: "2026-03-14"
zdroj: "gcloud CLI + session context"
platnost_do: "2026-09-14"
projekt_id: "project-4ac30110-41b1-4783-a5d"
projekt_number: "537446704644"
projekt_nazev: "PrahaScrapersV1"
region_primary: "europe-west1"
owner: "ondra.sousek@gmail.com"
architektura_direktiva: "SERVERLESS_ONLY — absolutní preference Cloud Run/Functions před VM. VM pouze pro legacy ETL pipeline (Jobs_Praha_mining). Každý nový vývoj MUSÍ být serverless."
---

# GCP Stack Ingest v3.0 · Snapshot 2026-03-14

## CHANGELOG: Co se změnilo oproti v2 (2026-03-09)

| Sekce | Stav v2 (09.03.) | Stav v3 (14.03.) |
|---|---|---|
| Scheduler jobs | 5 jobů | **6 jobů: +pipeline-meteo-hourly (hourly cron, meteo pipeline)** |
| miner-orchestrator URL | `jdpi45qekq-ew.a.run.app` | **`537446704644.europe-west1.run.app` (nový Cloud Run URL formát)** |
| GCS managed buckety | 2× gcf-v2-sources | **+3 managed buckety (gcf-sources, gcf-v2-uploads, run-sources)** |
| Enabled services | Functions, Run, Scheduler, Storage, Compute, Firestore | **+BigQuery suite (7 APIs), +Pub/Sub, +Datastore API** |
| Firestore detail | Aktivní, free tier | **+earliestVersionTime 14.03., realtimeUpdates ENABLED, retention 3600s** |
| Architektura direktiva | Implicitní | **EXPLICITNÍ: serverless před VM za všech okolností** |
| Meteo pipeline | Neexistovala | **AKTIVNÍ: chmu-meteo-miner, pipeline-meteo-hourly scheduler** |

---

## 1. PROJEKT — IDENTIFIKACE

```yaml
project_id: "project-4ac30110-41b1-4783-a5d"
project_number: "537446704644"
nazev: "PrahaScrapersV1"
account_owner: "ondra.sousek@gmail.com"
region_primary: "europe-west1"
organizace: "656334866876"
environment_tag: "CHYBÍ — přidat environment=Production"
```

> **REGION PRAVIDLO:** Všechny Cloud Functions, Cloud Run, Scheduler joby, GCS buckety → `europe-west1`.
> LLM navrhující `europe-west3` (Frankfurt) je ŠPATNĚ pro tento projekt.

---

## 2. ARCHITEKTURA — DIREKTIVA (NOVÉ v3)

```yaml
architektura:
  preferred: "Cloud Run / Cloud Functions (serverless)"
  legacy_only: "Compute Engine VM (instance-20260302-155349)"
  pravidlo: >
    VM se NESMÍ používat pro nový vývoj.
    VM zůstává POUZE pro stávající Jobs_Praha_mining ETL pipeline
    dokud nebude migrována na serverless.
  duvod: "Cost efficiency, zero idle, lepší observability, snadnější deploy"
```

---

## 3. COMPUTE ENGINE — VM (LEGACY)

```yaml
vm:
  instance_name: "instance-20260302-155349"
  zone: "europe-west1-d"
  machine_type: "e2-small"
  vcpu: 2
  ram_gb: 2
  external_ip: "NONE (ephemeral)"
  status: "TERMINATED"
  poznamka: "TERMINATED = správná architektura, zero idle cost"
  trigger: "Jobs_Praha_mining Scheduler → Compute API start"
  pattern: "Scheduler → VM start → ETL pipeline → GCS backup → auto-shutdown"
  migrace_target: "Serverless Cloud Run (budoucí)"
```

---

## 4. CLOUD FUNCTIONS + CLOUD RUN

> Cloud Functions 2nd gen = Cloud Run service. Každá funkce existuje zároveň jako CF i jako Cloud Run service. Toto není chyba — jsou to dvě reprezentace téhož deploye.

```yaml
services:
  - name: "outpost-material-pipeline"
    status: "ACTIVE"
    last_deploy: "2026-03-07T05:02Z"
    url: "https://outpost-material-pipeline-jdpi45qekq-ew.a.run.app"
    ucel: "Původní scraping pipeline (material Bazoš)"
    scheduler: "material-tezba-cron (PAUSED)"

  - name: "iot-ingest-beta"
    status: "ACTIVE"
    last_deploy: "2026-03-07T10:51Z"
    url: "https://europe-west1-project-4ac30110-41b1-4783-a5d.cloudfunctions.net/iot-ingest-beta"
    ucel: "IoT větev — ESP32 → Firestore ingestion"
    trasa: "ESP32 → HTTPS POST → iot-ingest-beta → Firestore → Telegram"

  - name: "miner-orchestrator"
    status: "ACTIVE"
    last_deploy: "2026-03-09T13:53Z"
    url_v2: "https://miner-orchestrator-jdpi45qekq-ew.a.run.app"
    url_v3: "https://miner-orchestrator-537446704644.europe-west1.run.app"
    url_aktivni: "https://miner-orchestrator-537446704644.europe-west1.run.app"
    ucel: "Centrální orchestrátor — přijímá triggery od 3 Scheduler jobů (notebooky, deep, material)"

  - name: "chmu-meteo-miner"
    status: "ACTIVE"
    last_deploy: "2026-03-13"
    url: "https://miner-orchestrator-537446704644.europe-west1.run.app"
    ucel: "Meteo pipeline — ČHMÚ Kbely P1PKBE01, diferenciální zápis do GCS"
    scheduler: "pipeline-meteo-hourly"
    source_bucket: "gcp-miner-rag-data-01"
    output_blob: "master_kbely.md"
    endpointy:
      - "KLIMA_10M"
      - "TEPLOTA_10M"
    payload_verified: '{"filter":null,"sort":null,"columns":[],"paging":{"start":1,"size":300},"search":{"columns":[],"text":""}}'
    poznamka: "SRAZKY_10M a VITR_10M zakomentovány — redundantní data"
```

---

## 5. CLOUD SCHEDULER — AKTIVNÍ JOBY

```yaml
scheduler_jobs:
  - id: "cron-notebooky"
    schedule: "30 9,18,21 * * *"
    timezone: "Europe/Prague"
    state: "ENABLED"
    target_type: "HTTP"
    uri: "https://europe-west1-project-4ac30110-41b1-4783-a5d.cloudfunctions.net/miner-orchestrator"
    ucel: "Fast-scan notebooky Bazoš"
    offset_poznamka: "Spouští se 6 minut před deep (ZÁZNAM 054)"

  - id: "cron-notebooky-deep"
    schedule: "36 9,18,21 * * *"
    timezone: "Europe/Prague"
    state: "ENABLED"
    target_type: "HTTP"
    uri: "https://europe-west1-project-4ac30110-41b1-4783-a5d.cloudfunctions.net/miner-orchestrator"
    ucel: "Deep-dive notebooky Bazoš"
    offset_poznamka: "6 minut po fast-scan — záměrný offset"

  - id: "cron-material"
    schedule: "30 8,19 * * *"
    timezone: "Europe/Prague"
    state: "ENABLED"
    target_type: "HTTP"
    uri: "https://europe-west1-project-4ac30110-41b1-4783-a5d.cloudfunctions.net/miner-orchestrator"
    ucel: "Scraping materiálů Bazoš"

  - id: "pipeline-meteo-hourly"
    schedule: "0 * * * *"
    timezone: "Europe/Prague"
    state: "ENABLED"
    target_type: "HTTP"
    uri: "https://miner-orchestrator-537446704644.europe-west1.run.app/"
    ucel: "Hodinový trigger meteo pipeline (ČHMÚ Kbely)"
    poznamka: "NOVÉ v3 — nasazeno 2026-03-13"

  - id: "Jobs_Praha_mining"
    schedule: "0 9,13,18 * * *"
    timezone: "Europe/Prague"
    state: "ENABLED"
    target_type: "Compute API"
    uri: "https://compute.googleapis.com/compute/v1/projects/project-4ac30110-41b1-4783-a5d/zones/europe-west1-d/instances/instance-20260302-155349/start"
    ucel: "Startuje VM pro ETL pipeline (legacy pattern)"
    poznamka: "POZOR — nevolá HTTP endpoint, startuje VM přes Compute API. Po startu přebírá @reboot cron na VM."

  - id: "material-tezba-cron"
    schedule: "0 10,15,20 * * *"
    timezone: "Europe/Prague"
    state: "PAUSED"
    target_type: "HTTP"
    uri: "https://outpost-material-pipeline-jdpi45qekq-ew.a.run.app/"
    ucel: "Stará scraping pipeline (zastavena, ne smazána — lze reaktivovat)"
```

---

## 6. CLOUD STORAGE — BUCKETY

```yaml
buckets:
  user_created:
    - name: "gcp-miner-rag-data-01"
      location: "EUROPE-WEST1"
      ucel: "PRIMÁRNÍ — ETL výstupy, RAG .md/.yaml soubory, meteo master"
      obsah_klic: "master_kbely.md (meteo), notebooky RAG indexy"

    - name: "outpost-material-czwebs"
      location: "EUROPE-WEST1"
      ucel: "Scraping zdroje / staging pro material pipeline"

  gcp_managed:
    - name: "gcf-sources-537446704644-europe-west1"
      typ: "GCF managed (nový v3)"
    - name: "gcf-v2-sources-537446704644-europe-west1"
      typ: "GCF managed"
    - name: "gcf-v2-uploads-537446704644.europe-west1.cloudfunctions.appspot.com"
      typ: "GCF managed (nový v3)"
    - name: "run-sources-project-4ac30110-41b1-4783-a5d-europe-west1"
      typ: "Cloud Run managed (nový v3)"

poznamka: "Managed buckety jsou automatické — nevyžadují správu, nemazat."
```

---

## 7. FIRESTORE

```yaml
firestore:
  typ: "FIRESTORE_NATIVE"
  region: "europe-west1"
  vytvoreno: "2026-03-07T09:35:06Z"
  free_tier: true
  delete_protection: "DISABLED"
  realtime_updates: "REALTIME_UPDATES_MODE_ENABLED"
  earliest_version_time: "2026-03-14T18:02:35Z"
  point_in_time_recovery: "DISABLED"
  version_retention_period: "3600s"
  concurrency_mode: "PESSIMISTIC"
  database_edition: "STANDARD"
  name: "projects/project-4ac30110-41b1-4783-a5d/databases/(default)"
  uid: "dcf5b63b-d06a-410c-b5d5-312f6914a212"
  iot_trasa: "ESP32 → HTTPS POST → iot-ingest-beta → Firestore → Telegram"
  todo: "Zvážit aktivaci delete_protection pro produkci"
```

---

## 8. ENABLED SERVICES (NOVÉ v3)

```yaml
enabled_services:
  core:
    - "cloudfunctions.googleapis.com"
    - "run.googleapis.com"
    - "cloudscheduler.googleapis.com"
    - "storage.googleapis.com"
    - "storage-api.googleapis.com"
    - "storage-component.googleapis.com"
    - "compute.googleapis.com"
    - "firestore.googleapis.com"
    - "datastore.googleapis.com"

  messaging:
    - "pubsub.googleapis.com"

  bigquery_suite:
    - "bigquery.googleapis.com"
    - "bigqueryconnection.googleapis.com"
    - "bigquerydatapolicy.googleapis.com"
    - "bigquerydatatransfer.googleapis.com"
    - "bigquerymigration.googleapis.com"
    - "bigqueryreservation.googleapis.com"
    - "bigquerystorage.googleapis.com"

poznamky:
  datastore: "Aktivní souběžně s Firestore — Datastore API je backward-compat vrstva, nepoužívat pro nový vývoj"
  bigquery: "Aktivováno — pravděpodobně jako dependency nebo pro budoucí analytiku (Investiční Architekt?)"
  pubsub: "Aktivováno — IoT signalizace nebo budoucí event-driven architektura"
```

---

## 9. SERVICE ACCOUNTS

```yaml
service_accounts:
  - display_name: "Compute Engine default SA"
    email: "537446704644-compute@developer.gserviceaccount.com"
    ucel: "ETL VM přistupuje k GCS"
    deploy_prikaz: "gcloud run deploy ... --service-account 537446704644-compute@developer.gserviceaccount.com"

  - display_name: "App Engine default SA"
    email: "project-4ac30110-41b1-4783-a5d@appspot.gserviceaccount.com"
    ucel: "Legacy — nepoužívat pro IoT ani nový vývoj"

todo:
  - >
    Vytvořit dedikovaný IoT SA:
    gcloud iam service-accounts create iot-outpost-sa
    --display-name='IoT Outpost Service Account'
    --project project-4ac30110-41b1-4783-a5d
  - "Přiřadit role: roles/datastore.user nebo roles/firebase.admin"
```

---

## 10. CLI SYNTAX REFERENCE

```bash
# KRITICKÉ: gcloud functions vs run mají INVERZNÍ syntax pro region

# Cloud Functions → --regions (množné číslo)
gcloud functions list --gen2 --regions europe-west1

# Cloud Run → --region (jednotné číslo)
gcloud run services list --region europe-west1

# Cloud Scheduler → --location (ne --region)
gcloud scheduler jobs list --location europe-west1

# Kompletní snapshot příkaz (spustit pro refresh ingestu):
echo '=== PROJECT ===' && gcloud config list && \
echo '=== FUNCTIONS ===' && gcloud functions list --gen2 --regions europe-west1 && \
echo '=== RUN ===' && gcloud run services list --region europe-west1 && \
echo '=== SCHEDULER ===' && gcloud scheduler jobs list --location europe-west1 \
  --format="table(name,schedule,timeZone,state,httpTarget.uri)" && \
echo '=== BUCKETS ===' && gcloud storage buckets list && \
echo '=== SERVICES ===' && gcloud services list --enabled \
  --filter="name:(functions OR run OR scheduler OR storage OR compute OR pubsub OR firestore OR bigquery)" && \
echo '=== FIRESTORE ===' && gcloud firestore databases list && \
echo '=== SA ===' && gcloud iam service-accounts list
```

---

## 11. METEO PIPELINE — PROVOZNÍ REFERENCE (NOVÉ v3)

```yaml
meteo_pipeline:
  stanice: "P1PKBE01 (Praha Kbely)"
  stanice_url: "https://www.chmi.cz/namerena-data/merici-stanice/meteorologicke/p1pkbe01-praha-kbely"
  api_base: "https://data-provider.chmi.cz"
  service_name: "chmu-meteo-miner"
  deploy_prikaz: >
    gcloud run deploy chmu-meteo-miner
    --source .
    --region europe-west1
    --allow-unauthenticated
    --memory 512Mi
    --service-account 537446704644-compute@developer.gserviceaccount.com
  scheduler_job: "pipeline-meteo-hourly (0 * * * * Europe/Prague)"
  output_bucket: "gcp-miner-rag-data-01"
  output_master: "master_kbely.md"
  output_dif_pattern: "dif_YYYYMMDDHHMMSS.md"

  api_endpointy_aktivni:
    KLIMA_10M: "https://data-provider.chmi.cz/api/data/tab/meteo/klima-10m/P1PKBE01"
    TEPLOTA_10M: "https://data-provider.chmi.cz/api/data/tab/meteo/teplota-10m/P1PKBE01"

  api_endpointy_zakomentovany:
    SRAZKY_10M: "https://data-provider.chmi.cz/api/data/tab/meteo/srazky-10m/P1PKBE01"
    VITR_10M: "https://data-provider.chmi.cz/api/data/tab/meteo/vitr-10m/P1PKBE01"

  payload_verifikovany:
    filter: null
    sort: null
    columns: []
    paging:
      start: 1
      size: 300
    search:
      columns: []
      text: ""

  response_klic_dat: "data"
  timestamp_format_vstup: "ISO 8601 UTC (2026-03-12T10:30:00Z)"
  timestamp_format_vystup: "ISO 8601 local +offset (2026-03-12T11:30:00+01:00)"
  dedup_regex: '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}'

  zname_bugy_opraveny:
    - "search klíč chyběl v payload (Gemini)"
    - "parser předpokládal '%d. %m. %Y %H:%M' místo ISO 8601 (Gemini)"
    - "klíč 'Datum' místo 'date' v deduplikaci (Gemini)"
    - "klíč 'rows' místo 'data' pro response data (Gemini)"

  diagnosticky_curl: >
    curl -s -X POST "https://data-provider.chmi.cz/api/data/tab/meteo/klima-10m/P1PKBE01"
    -H "Content-Type: application/json"
    -H "Referer: https://www.chmi.cz/"
    -d '{"filter":null,"sort":null,"columns":[],"paging":{"start":1,"size":3},"search":{"columns":[],"text":""}}'
    | python3 -m json.tool | head -40
```

---

*GCP Stack Ingest v3.0 · 2026-03-14 · Zdroj: gcloud CLI + session context · Platnost do: 2026-09-14 · Projekt: PrahaScrapersV1*
