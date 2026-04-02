import os
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from google.cloud import storage

# ── KONFIGURACE GCP & CESTY ──────────────────────────────────────────────────
# SPRÁVNĚ: Hledáme klíč "TELEGRAM_TOKEN", pokud není, použijeme ten dlouhý řetězec
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8725468950:AAH19oZ28SiZeaxILLdRLbMQLhJSpcnrA-I")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1341669174")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "gcp-miner-rag-data-01")

# PROČ: V GCP lze zapisovat pouze do složky /tmp, zbytek disku je uzamčen.
TMP_DIR        = "/tmp"
MASTER_NAME    = "notebooky_rag_master.md"
MASTER_FILE    = f"{TMP_DIR}/{MASTER_NAME}"
DIFF_FILE      = f"{TMP_DIR}/dif_index.md"

TARGET_PSC     = "18000"
TARGET_RADIUS  = "25"
MIN_PRICE      = 800
MAX_PRICE      = 4000
DAYS_BACK      = 10

# Sémantické filtry (v6 standard)
BLACKLIST = ["stojan", "pouzdro", "obal", "brašna", "kabel", "adaptér", "nabíječka", 
             "deska", "board", "panty", "šasi", "display", "lcd", "apple", "macbook",
             # CPU generační disqualifiery — nulové false positive riziko
             "core 2 duo", "core 2 quad", "core2duo", "core2quad",
             # Celeron/Atom N-series — tablet třída v x86 těle (slovní forma)
             "celeron n", "atom n", "intel n100", "intel n200",
             ]
IDENTITY  = ["notebook", "laptop", "thinkpad", "latitude", "precision", "probook",
             "elitebook",  # FIX: chyběl — HP EliteBook řada business class
             ]
HW_REGEX  = r'\b(8|12|16|24|32|64)\s*(gb|g)\b|\b(ssd|nvme|m2)\b'

# N-series regex pro titulky formátu "N4020", "N5100" bez slova Celeron
_N_SERIES_RE = re.compile(r'\b[Nn](100|200|4\d{3}|5\d{3})\b')
# 4GB filtr: zahazuj pokud POUZE 4GB zmíněno, bez jakéhokoli 8GB+
_FOUR_GB_RE   = re.compile(r'\b4\s*gb\b', re.IGNORECASE)
_EIGHT_GB_RE  = re.compile(r'\b(8|12|16|24|32|64)\s*(gb|g)\b', re.IGNORECASE)

# ── GCS FUNKCE (PROTI AMNÉZII KONTEJNERU) ─────────────────────────────────────
def download_master_gcs():
    """Stáhne historickou databázi z bucketu do /tmp/, aby skript nezačínal od nuly."""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MASTER_NAME)
        if blob.exists():
            blob.download_to_filename(MASTER_FILE)
            print("[i] Stažen existující master z GCS.")
        else:
            Path(MASTER_FILE).write_text("--- Init databáze ---\n", encoding="utf-8")
            print("[i] Master na GCS nenalezen, vytvořen nový lokální.")
    except Exception as e:
        print(f"[!] Chyba při stahování z GCS: {e}")
        Path(MASTER_FILE).write_text("--- Init databáze ---\n", encoding="utf-8")

def upload_master_gcs():
    """Zálohuje aktualizovanou databázi zpět do bucketu."""
    if os.path.exists(MASTER_FILE):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MASTER_NAME)
        blob.upload_from_filename(MASTER_FILE)
        print("[i] Nahrán aktualizovaný master do GCS.")

# ── TELEGRAM HELPERS ──────────────────────────────────────────────────────────
def send_telegram_doc(file_path, caption):
    # FIX P0: Odstraněn duplicitní dispatch blok za try/except.
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

# ── POMOCNÉ FUNKCE ────────────────────────────────────────────────────────────
def load_known_urls(file_path):
    if not Path(file_path).exists():
        return set()
    content = Path(file_path).read_text(encoding="utf-8")
    return set(re.findall(r'(?:url|source_url):\s*"([^"]+)"', content))

def parse_bazos_date(date_str):
    try:
        match = re.search(r'(\d{1,2})\.(\d{1,2})\.\s?(\d{4})', date_str)
        if match:
            d, m, y = match.groups()
            return datetime(int(y), int(m), int(d))
        return datetime.now()
    except: return datetime.now()

def evaluate(title, desc, price_raw):
    full_text = f"{title} {desc}".lower()
    try:
        price = int(re.sub(r'\D', '', price_raw))
        if price < MIN_PRICE or price > MAX_PRICE: return 0, price
    except: return 0, 0

    if any(x in full_text for x in BLACKLIST): return 0, price
    if not any(x in full_text for x in IDENTITY): return 0, price
    if not re.search(HW_REGEX, full_text): return 0, price
    # 4GB filtr: explicitní 4GB bez zmínky 8GB+ → zahazuj
    if _FOUR_GB_RE.search(full_text) and not _EIGHT_GB_RE.search(full_text): return 0, price
    # N-series regex (zachytí "N4020", "N100" v titulku bez slova Celeron)
    if _N_SERIES_RE.search(f"{title} {desc}"): return 0, price
    
    score = 100 - (price / 50)
    if "thinkpad" in full_text: score += 30
    if "16gb" in full_text: score += 40
    return round(score, 1), price

# ── ENGINE (MODUL) ────────────────────────────────────────────────────────────

def run_pipeline():
    """
    Přejmenováno z main(). Tuto funkci bude volat náš Orchestrátor z main.py.
    """
    print(f"[*] Inicializace Notebook-Mineru v GCP...")
    
    # 1. Obnova paměti z cloudu
    download_master_gcs()
    known_urls = load_known_urls(MASTER_FILE)
    print(f"[i] V Masteru nalezeno {len(known_urls)} známých inzerátů.")

    Path(DIFF_FILE).write_text(f"# Nové inzeráty ({datetime.now().strftime('%d.%m. %H:%M')})\n\n", encoding="utf-8")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    limit_date = datetime.now() - timedelta(days=DAYS_BACK)
    new_count = 0

    # FIX P1: Flag pro čisté ukončení obou smyček při dosažení historického limitu.
    stop_scraping = False

    for page in range(20):
        if stop_scraping:
            break

        offset = page * 20
        url = f"https://pc.bazos.cz/notebook/{offset}/?hledat=&hlokalita={TARGET_PSC}&humkreis={TARGET_RADIUS}&cenaod={MIN_PRICE}&cenado={MAX_PRICE}&order="
        
        try:
            r = session.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            ads = soup.find_all("div", class_="inzeraty")
            if not ads: break

            print(f"  [>] Strana {page + 1}...")

            for ad in ads:
                if ad.find_parent("div", class_="podobne"): continue
                
                loc_div = ad.find("div", class_="inzeratylok")
                date_span = loc_div.find("span", class_="velikost10") if loc_div else None
                ad_date = parse_bazos_date(date_span.get_text()) if date_span else datetime.now()
                
                if "topovany" not in str(ad) and ad_date < limit_date:
                    print(f"  [!] Historický limit {DAYS_BACK} dní dosažen. Končím cyklus.")
                    stop_scraping = True
                    break

                a = ad.find("h2", class_="nadpis").find("a")
                link = "https://pc.bazos.cz" + a["href"]
                if link in known_urls:
                    continue
                
                title = a.get_text(strip=True)
                desc  = ad.find("div", class_="popis").get_text(strip=True)
                price_raw = ad.find("div", class_="inzeratycena").get_text(strip=True)
                
                score, price_val = evaluate(title, desc, price_raw)
                
                if score > 40:
                    # PROČ: Striktní RAG formátování YAML hlavičky, jak sis přál
                    output = (
                        f"---\n"
                        f"title: \"{title}\"\n"
                        f"source_url: \"{link}\"\n"
                        f"scraped_at: \"{datetime.now().isoformat()}\"\n"
                        f"topic: \"IT_Hardware\"\n"
                        f"data_type: \"market_leads\"\n"
                        f"price: \"{price_val} Kč\"\n"
                        f"score: {score}\n"
                        f"---\n\n"
                        f"# {title}\n{desc[:400]}...\n\nLokalita: {loc_div.get_text(strip=True) if loc_div else ''} | [Link]({link})\n\n***\n\n"
                    )
                    
                    with open(MASTER_FILE, "a", encoding="utf-8") as f_m, \
                         open(DIFF_FILE, "a", encoding="utf-8") as f_d:
                        f_m.write(output)
                        f_d.write(output)
                    
                    known_urls.add(link)
                    new_count += 1
                    print(f"    [+] NOVÝ: {score} pts | {title[:40]}")

            time.sleep(random.uniform(1.5, 3.0))
        except Exception as e:
            print(f"  [!] Chyba Bazoš cyklu: {e}")
            break

    print(f"[*] Skript dokončen. Nových inzerátů: {new_count}")
    
    # 2. Zálohování paměti zpět do cloudu po dokončení těžby
    upload_master_gcs()
    
    # 3. Odeslání do Telegramu
    if new_count > 0:
        send_telegram_doc(DIFF_FILE, f"💻 Notebooky: {new_count} nových leadů.")
        print("[OK] Odesláno do Telegramu.")
    else:
        print("[INFO] Žádné nové notebooky. Telegram mlčí.")

# Pokud testuješ skript samostatně z terminálu
if __name__ == "__main__":
    run_pipeline()