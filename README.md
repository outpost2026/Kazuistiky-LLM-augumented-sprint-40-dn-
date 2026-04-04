# Outpost SOC Predictor

>Produkční systém pro predikci stavu nabití (SOC) LFP baterie na základě meteodat a přesného modelu terénu.

---

### Účel projektu

**Outpost SOC Predictor** predikuje denní přírůstek stavu nabití (ΔSOC) LiFePO₄ baterií kombinací meteorologických dat s pokročilým algoritmem teréního stínění. Systém poskytuje aktuální předpovědi ve strukturované podobě (CSV, JSON nebo formátované tabulky) na **N dní dopředu**.

**Co je na tomto projektu specifické**

Klíčová inovace je **maska horizontu** — LiDAR-odvozený profil terénu, který zohledňuje reálné stínění topografií a vegetací. To umožňuje predikci **čistého ΔSOC** (výroby minus spotřebu), což je přesně veličina, kterou vidí Battery Management System. **Výsledek:** Korelace maskovaného záření se skutečným ΔSOC vzrostla na **r = 0,953** oproti standardním DEM modelům.

---

## Oblasti použití

- **Ostrovní systémy**: Predikce kdy bude baterie plná nebo kriticky vybita
- **Hybridní systémy s úložištěm**: Předpověď dostupné energie pro řízení zátěže
- **Mikrosítě**: Plánování na více dní pro řízení na straně poptávky
- **Plánování údržby**: Optimalizace cyklů střídače podle předpovídaného nabíjení

---

### *Setup pro replikaci celé architektury v jednoho souboru json*
- universální použití (libovolná topologie, lokalita, FV, bms a další proměnné)
- stačí stáhnout jeden json soubor **[Setup_pipeline_soc_prediction.json](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/LFP_soc_predict_pipeline/Setup_pipeline_soc_prediction.json)** - obsahuje celou kuchařku s postupem

---

##  Architektura systému

Pipeline se skládá ze tří hlavních produkčních skriptů:

| Skript | Účel | Vstup | Výstup |
|--------|------|-------|--------|
| **`outpost_meteo_etl_v3.py`** | ETL: stažení dat počasí, výpočet sluneční polohy, aplikace masky horizontu | Open-Meteo API | `outpost_meteo_forecast.csv` |
| **`soc_predict.py`** | Predikce SOC kombinací BMS dat a maskovaných meteodat | BMS CSV + forecast | Tabulka / JSON / CSV |
| **`horizon_profile_outpost.py`** | *Jednorázové nastavení* — vygeneruje profil horizontu z LiDAR dat | LAZ (DMR 5G) | `horizon_profile.json` |

**⚠️ Poznámka:** Skript `data_ingestion_bridge.py` (automatizace BMS) je ve vývoji; sběr dat probíhá zatím manuálně přes BLE/USB.

---

## Technické pozadí: Maska horizontu

### Proč je vlastně použit složitý model stínění

Standardní modely nadmořské výšky (DEM) selhávají v komplexním terénu s vegetací. Nemohou vidět stromy ani protější svahy. Řešení využívá **LiDAR-odvozené profily terénu** pro aplikaci realistického stínění.

### Data a metoda

- **Zdroj:** [Nástroj Atom](https://ags.cuzk.gov.cz/geoprohlizec/?atom=dmr5g) — Digitální model reliéfu ČR 5. generace (DMR 5G) + Digitální model povrchu (DMP)
- **Zpracování:** Vlastní skript `horizon_profile_outpost.py` konvertuje LAZ → JSON
- **Implementace:** Ray-casting ze středu FV pole, rozlišení 1° azimutu
- **Přínos:** Vylepšená korelace maskovaného záření ze základní úrovně na **r = 0,953** se skutečnými daty ΔSOC

### Matematika

Pro každý azimut α (0°–359°):
1. Vyslání paprsku ze středu FV pole
2. Nalezení prvního průsečíku s terénem
3. Výpočet úhlu elevace θ(α)
4. Uložení jako součást masky horizontu

Během předpovědi se hodinové záření vynuluje pro azimuty, kde je sluneční altituda < θ(α).

---

## Lineární model (Kalibrace v3.0)

Nakalibrován na datech z března 2026 (srovnání denního součtu záření vs. naměřený ΔSOC).

### Modelová rovnice

```
ΔSOC [%] = 0,00776 × rad_sum [Wh/m²] − 9,55
```

### Metriky výkonu

| Metrika | Hodnota |
|---------|---------|
| **R²** | 0,907 |
| **Min. denní záření pro nabíjení** | ~1230 Wh/m² |
| **Korelace (maskované záření vs. ΔSOC)** | r = 0,953 |

---

## Hardwarový kontext

| Komponenta | Specifikace |
|------------|-------------|
| **Fotovoltaika** | 2300 Wp, azimut 173° (JJV), dočasná zemní montáž |
| **Baterie** | LiFePO₄, 630 Ah nominál (491 Ah využitelných) |
| **BMS** | JK BMS — zaznamenává čistý proud na svorkách |
| **Střídač** | POW-HVM3.2H (plánovaná integrace v4.0) |
| **Lokalita** | Praha-okolí, jižní svah, extrémní stínění (terén + vegetace) |

---


### Základní použití

```bash
# (Volitelné) Vygenerování masky horizontu z LiDAR dat
python horizon_profile_outpost.py --laz /cesta/k/dmr5g.laz --output horizon_profile.json

# Stažení předpovědi počasí a aplikace teréní masky
python outpost_meteo_etl_v3.py --days 7 --output outpost_meteo_forecast.csv

# Predikce SOC na příštích 7 dní
python soc_predict.py \
  --bms bms_data.csv \
  --meteo outpost_meteo_forecast.csv \
  --days 7 \
  --format table
```

### Příkazové řádkové volby

```
usage: soc_predict.py [-h] [--bms BMS_PATH] [--meteo METEO_PATH] 
                      [--days DAYS] [--format {table,json,csv}] 
                      [--no-api]

volitelné argumenty:
  -h, --help              Zobrazit nápovědu
  --bms BMS_PATH          Cesta k datům z BMS (CSV)
  --meteo METEO_PATH      Cesta k předpovědi počasí (musí obsahovat 
                          sloupec 'shortwave_radiation_masked')
  --days DAYS             Počet dní předpovědi (výchozí: 7)
  --format {table,json,csv}
                          Formát výstupu (výchozí: table)
  --no-api                Vynutit offline režim pouze s lineárním modelem
```

### Příklad výstupu
- zde [reálný výstup predikce - forecast.csv](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/LFP_soc_predict_pipeline/forecast.csv)

## Závislosti

- `pvlib-python` — Výpočty sluneční polohy
- `pandas` — Manipulace s daty
- `requests` — Volání Open-Meteo API
- `numpy` — Numerické operace

---

### Sezónní rekalibraci (Kritické)

Model je kalibrován na datech z března 2026. **Sezónní drift vyžaduje rekalibraci každých 14+ dní** kvůli:
- Měnící se sluneční deklinaci
- Sezónnímu růstu vegetace
- Vlivu teploty na účinnost baterie


### Konfigurace montáže (Kritické)

Kalibrace je specifická pro **dočasnou zemní montáž na azimutu 173° JJV**. Přemístění zařízení na střechu zneplatní všechny modely.

---

## ⚠️ Známá omezení a plán vývoje

### Kritické problémy

- ✋ **Sezónní drift**: Model vyžaduje přetrénování každých 2 týdnů
- ✋ **Závislost na montáži**: Přemístění zařízení vyžaduje úplnou rekalibraci
- 🔴 **Manuální sběr BMS dat**: Sběr přes BLE/USB; bez real-time integrace

### Status v3.0

- ✅ Teréní maskování s LiDAR daty
- ✅ Offline lineární predikční model
- ✅ Multi-formátový výstup (tabulka, CSV, JSON)
- ⏳ Ošetření chyb a validace vstupů (částečné)
- ⏳ Integrace střídače (POW-HVM3.2H)

### Plánováno pro v4.0

- [ ] Integrace měření živého výkonu střídače
- [ ] Automatizovaný sběr dat z BMS přes `data_ingestion_bridge.py`
- [ ] XGBoost ensemble model s intervaly spolehlivosti předpovědi
- [ ] Webový dashboard pro vizualizaci předpovědi
- [ ] Podpora více lokalit
- [ ] Automatizovaná sezónní rekalibraci

---

## Licence

MIT License — Viz soubor [LICENSE](LICENSE) pro detaily.

---

## 🔗 Reference a zdroje dat

- **Open-Meteo API:** [open-meteo.com](https://open-meteo.com/)
- **LiDAR Data:** [Atom - Digitální model reliéfu ČR DMR 5G](https://ags.cuzk.gov.cz/geoprohlizec/?atom=dmr5g)
- **Výpočty sluneční polohy:** [pvlib-python](https://pvlib-python.readthedocs.io/)
- **Chemie baterií:** Efektivnostní křivky LiFePO₄ a teplotní vlivy

---

## 🎓 Citace

Pokud tento systém používáte v publikacích, prosím citujte:

```bibtex
@software{outpost_soc_2026,
  title={Outpost SOC Predictor: Predikce nabíjení LiFePO₄ s teréním maskováním},
  author={[Ondřej Soušek]},
  year={2026},
  url={https://github.com/outpost2026}
}
```

---

**Poslední aktualizace:** Březen 2026 | **Aktuální verze:** v3.0 | 
