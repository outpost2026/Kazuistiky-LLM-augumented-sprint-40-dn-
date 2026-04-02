import os
import datetime
import yaml
import requests
import re
from google.cloud import storage

PROJECT_ID = "project-4ac30110-41b1-4783-a5d"
BUCKET_NAME = "gcp-miner-rag-data-01"
STATION_ID = "P1PKBE01"
BASE_URL = "https://data-provider.chmi.cz"

ENDPOINTS = {
    "KLIMA_10M": f"{BASE_URL}/api/data/tab/meteo/klima-10m/{STATION_ID}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Referer": "https://www.chmi.cz/",
}

PAYLOAD = {
    "filter": None,
    "sort": None,
    "columns": [],
    "paging": {"start": 1, "size": 300},
    "search": {"columns": [], "text": ""}
}

def strip_html(value) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        return str(value)
    clean = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", clean).strip()

def fetch_endpoint(label: str, url: str) -> str | None:
    try:
        r = requests.post(url, json=PAYLOAD, headers=HEADERS, timeout=15)
        r.raise_for_status()
        body = r.json()

        rows = body.get("data")
        if not rows:
            print(f"[!] {label}: prázdné 'data'")
            return None

        total = body.get("header", {}).get("totalCount", "?")
        print(f"[+] {label}: {len(rows)}/{total} záznamů")

        col_names = list(rows[0].keys())

        md = f"## {label}\n\n"
        md += "| " + " | ".join(col_names) + " |\n"
        md += "| " + " | ".join(["---"] * len(col_names)) + " |\n"

        for row in rows:
            cells = [strip_html(row.get(col)) for col in col_names]
            md += "| " + " | ".join(cells) + " |\n"

        return md

    except Exception as e:
        print(f"[!] {label}: {e}")
        return None

def upload_to_gcs(local_path: str):
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob("praha_kbely_detail_master.md")
    blob.upload_from_filename(local_path)
    print(f"[+] Odesláno → gs://{BUCKET_NAME}/praha_kbely_detail_master.md")

def run_pipeline():
    """Entry point pro orchestrátor."""
    output_path = "/tmp/kbely.md"
    tables = []

    print("[*] Spouštím těžbu ČHMÚ...")
    for label, url in ENDPOINTS.items():
        md_table = fetch_endpoint(label, url)
        if md_table:
            tables.append(md_table)

    if not tables:
        raise RuntimeError("Chyba extrakce — žádná data z ČHMÚ API")

    front_matter = {
        "title": "Meteo Data Praha Kbely (API Direct)",
        "source_url": "https://www.chmi.cz/namerena-data/merici-stanice/meteorologicke/p1pkbe01-praha-kbely",
        "scraped_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "topic": "meteo",
        "status": "DETAIL_RAW",
        "endpoints": list(ENDPOINTS.keys()),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(front_matter, f, allow_unicode=True)
        f.write("---\n\n# DATA STANICE KBELY\n\n")
        f.write("\n\n".join(tables))

    upload_to_gcs(output_path)
    print("[*] Těžba ČHMÚ dokončena.")
