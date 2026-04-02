import os
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import re
from datetime import datetime
from urllib.parse import urlparse, urlunparse
from google.cloud import storage
import traceback

# ── KONFIGURACE PRO GCP ───────────────────────────────────────────────────────
# SPRÁVNĚ: Hledáme klíč "TELEGRAM_TOKEN", pokud není, použijeme ten dlouhý řetězec
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8725468950:AAH19oZ28SiZeaxILLdRLbMQLhJSpcnrA-I")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1341669174")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "gcp-miner-rag-data-01")

# PROČ BASE_DIR: V cloudu nevíme, v jaké složce přesně kontejner běží. 
# Toto dynamicky najde cestu k CSV souborům, které leží vedle tohoto skriptu.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_CSV = os.path.join(BASE_DIR, "categories.csv")
TOPICS_CSV     = os.path.join(BASE_DIR, "topics.csv")

# PROČ /tmp: Linux Bridge - Zápis je v GCP povolen pouze do efemérní RAM.
TMP_DIR = "/tmp"
TMP_MASTER = os.path.join(TMP_DIR, "material_master.md")
TMP_DIFF   = os.path.join(TMP_DIR, f"diff_material_{datetime.now().strftime('%Y%m%d_%H%M')}.md")
GCS_MASTER_NAME = "material_master.md" # Přejmenováno z "master.md" kvůli prevenci kolizí v bucketu

# Nastavení těžby
MAX_PAGES      = 20
DELAY_MIN      = 1.0
DELAY_MAX      = 2.5
TARGET_PSC     = "18000"
TARGET_RADIUS  = "25"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

# ── GCP PERSISTENTNÍ VRSTVA (BUCKET) ─────────────────────────────────────────
def download_master():
    """Zabrání amnézii kontejneru stažením historie z GCS."""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_MASTER_NAME)
        if blob.exists():
            blob.download_to_filename(TMP_MASTER)
            print(f"[OK] {GCS_MASTER_NAME} stažen z GCS.")
        else:
            with open(TMP_MASTER, "w", encoding="utf-8") as f:
                f.write("--- Init databáze materiálů ---\n")
            print(f"[INFO] Nový {GCS_MASTER_NAME} vytvořen v /tmp.")
    except Exception as e:
        print(f"[!] Chyba při stahování z GCS: {e}")
        with open(TMP_MASTER, "w", encoding="utf-8") as f:
            f.write("--- Init databáze materiálů ---\n")

def upload_master():
    """Zálohuje nabyté vědomosti zpět do cloudu."""
    if os.path.exists(TMP_MASTER):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_MASTER_NAME)
        blob.upload_from_filename(TMP_MASTER)
        print(f"[OK] {GCS_MASTER_NAME} nahrán do GCS.")

# ── TELEGRAM HELPERS ──────────────────────────────────────────────────────────
def send_telegram_doc(file_path, caption):
    if not TELEGRAM_TOKEN:
        print("[!] Telegram Error: Token je prázdný!")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(url, files={'document': f}, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption})
        
        if r.status_code != 200:
            print(f"[!] Telegram API Error {r.status_code}: {r.text}")
        else:
            print(f"[OK] Telegram úspěšně přijal soubor.")
    except Exception as e:
        print(f"[!] Kritická chyba při spojení s Telegramem: {e}")

def send_telegram_alert(text):
    if not TELEGRAM_TOKEN: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text[:4000]})

# ── LOGIKA TĚŽBY ──────────────────────────────────────────────────────────────
def validate_location(loc_text, target_psc):
    """Local Guard: Ochrana proti Topovaným inzerátům z jiných krajů."""
    if not loc_text: return True 
    zip_match = re.search(r'(\d{3})\s?(\d{2})', loc_text)
    if zip_match:
        found_zip_prefix = zip_match.group(1) 
        if target_psc.startswith("1"):
            return found_zip_prefix.startswith(("1", "2"))
    return True

def make_session():
    s = requests.Session()
    s.headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return s

def get_soup(session, url):
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[!] Chyba stahování {url}: {e}")
        return None

def load_csv(path):
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception as e:
        print(f"[!] Nelze načíst {path}: {e}")
    return rows

def build_page_url(base_url, page_index):
    if page_index == 0:
        return base_url
    parsed = urlparse(base_url)
    path = parsed.path.rstrip('/')
    offset = page_index * 20
    new_path = f"{path}/{offset}/"
    return urlunparse(parsed._replace(path=new_path))

def load_known_urls(filepath):
    known = set()
    if not os.path.exists(filepath):
        return known
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        urls = re.findall(r'(?:url|source_url):\s*"([^"]+)"', content)
        for u in urls:
            known.add(u)
    return known

def parse_topics(raw_topics):
    parsed = []
    for row in raw_topics:
        tid = row.get("topic_id", "").strip()
        tlabel = row.get("topic_label", "").strip()
        must_inc = [x.strip().lower() for x in row.get("must_include", "").split(",") if x.strip()]
        should_inc = [x.strip().lower() for x in row.get("should_include", "").split(",") if x.strip()]
        must_exc = [x.strip().lower() for x in row.get("must_exclude", "").split(",") if x.strip()]
        parsed.append({"id": tid, "label": tlabel, "must_inc": must_inc, "should_inc": should_inc, "must_exc": must_exc})
    return parsed

def match_topics(text, topics):
    text_lower = text.lower()
    best_topic = None
    best_score = 0.0
    for t in topics:
        if t["must_inc"]:
            missing_must = [m for m in t["must_inc"] if m not in text_lower]
            if missing_must:
                continue
        if t["must_exc"]:
            found_exc = [e for e in t["must_exc"] if e in text_lower]
            if found_exc:
                continue
        score = 1.0
        if t["should_inc"]:
            matches = sum(1 for s in t["should_inc"] if s in text_lower)
            score += matches * 0.5
        if score > best_score:
            best_score = score
            best_topic = t
    return best_topic, best_score

def format_lead_block(title, link, price, loc, desc, topic_label, score, category_name):
    """PROČ: Formátuje výstup přesně podle RAG standardu (YAML front-matter)."""
    return (
        f"---\n"
        f"title: \"{title}\"\n"
        f"source_url: \"{link}\"\n"
        f"scraped_at: \"{datetime.now().isoformat()}\"\n"
        f"topic: \"{topic_label}\"\n"
        f"data_type: \"market_leads\"\n"
        f"score: {score}\n"
        f"category: \"{category_name}\"\n"
        f"---\n\n"
        f"# {title}\n"
        f"**Lokalita:** {loc} | **Cena:** {price} | [Odkaz na Bazoš]({link})\n\n"
        f"{desc}\n\n***\n\n"
    )

def base_origin(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def scrape_index(category, topics, session, known_urls, new_leads):
    cat_url = category.get("url")
    cat_name = category.get("name")
    origin = base_origin(cat_url)
    print(f"[*] Skenuji: {cat_name} -> {cat_url}")

    for page_idx in range(MAX_PAGES):
        page_url = build_page_url(cat_url, page_idx)
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
        
        soup = get_soup(session, page_url)
        if not soup: break

        form = soup.find("form", id="formular")
        if form:
            soup = get_soup(session, f"{page_url}?hledat=&rubriky=dum&hlokalita={TARGET_PSC}&humkreis={TARGET_RADIUS}&cenaod=&cenado=&Submit=Hledat")
            if not soup: break

        ads = soup.find_all("div", class_="inzeraty inzeratyflex")
        if not ads: break

        for ad in ads:
            title_el = ad.find("h2", class_="nadpis")
            if not title_el: continue
            a_tag = title_el.find("a")
            if not a_tag: continue
            
            title = a_tag.text.strip()
            href = a_tag["href"]
            link = href if href.startswith("http") else origin + href

            if link in known_urls: continue

            loc_el = ad.find("div", class_="inzeratylok")
            loc = loc_el.text.strip() if loc_el else ""
            
            if not validate_location(loc, TARGET_PSC): continue

            price_el = ad.find("div", class_="inzeratycena")
            price = price_el.text.strip() if price_el else ""
            desc_el = ad.find("div", class_="popis")
            desc = desc_el.text.strip() if desc_el else ""

            full_text = f"{title} {desc}"
            matched_topic, score = match_topics(full_text, topics)

            if matched_topic:
                block = format_lead_block(title, link, price, loc, desc, matched_topic["label"], score, cat_name)
                new_leads.append(block)
                # Průběžný zápis do lokální /tmp/ paměti
                with open(TMP_MASTER, "a", encoding="utf-8") as f:
                    f.write(block)
                known_urls.add(link)
                print(f"    [+] NOVÝ LEAD: {title[:40]}")

def write_diff(filepath, new_leads, topics):
    """Zápis denního přehledu pro Telegram."""
    run_ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"---\n")
        f.write(f"title: \"Bazoš Diff - Materiál\"\n")
        f.write(f"source_url: \"bazos.cz\"\n")
        f.write(f"scraped_at: \"{datetime.now().isoformat()}\"\n")
        f.write(f"topic: \"Offgrid_Material_Report\"\n")
        f.write(f"data_type: \"daily_diff\"\n")
        f.write(f"---\n\n")
        f.write(f"# Nové inzeráty ({run_ts})\n")
        f.write(f"Filtr: PSČ {TARGET_PSC} (+{TARGET_RADIUS} km)\n\n")
        if new_leads:
            f.writelines(new_leads)
        else:
            f.write("_Žádné nové inzeráty nezachyceny._\n")

# ── VSTUPNÍ BOD PRO MODUL (VOLÁ ORCHESTRÁTOR) ─────────────────────────────────
def run_pipeline():
    """
    PROČ: Zmizel argument 'request'. Tuto funkci volá náš hlavní orchestrátor
    v main.py čistě jako Python modul. Nepracuje s HTTP protokolem.
    """
    try:
        print("[*] Startuje RAG pipeline: Materiál...")
        download_master()
        
        categories = [c for c in load_csv(CATEGORIES_CSV) if c.get("active", "0").strip() == "1"]
        topics = parse_topics(load_csv(TOPICS_CSV))
        
        if not categories or not topics:
            raise ValueError("CSV soubory nebyly nalezeny nebo jsou prázdné.")

        known_urls = load_known_urls(TMP_MASTER)
        session = make_session()
        new_leads = []

        for cat in categories:
            scrape_index(cat, topics, session, known_urls, new_leads)

        write_diff(TMP_DIFF, new_leads, topics)
        upload_master()

        if new_leads:
            send_telegram_doc(TMP_DIFF, f"🎯 Těžba materiálu: {len(new_leads)} nových leadů.")
            print(f"[OK] Odesláno do Telegramu: {len(new_leads)} leadů.")
        else:
            print("[INFO] Žádné nové inzeráty. Telegram mlčí.")

    except Exception as e:
        # Pád probublá do main.py, který zaloguje chybu a vrátí HTTP 500
        raise RuntimeError(f"Chyba materiálového scraperu: {str(e)}")