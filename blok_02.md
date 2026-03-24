# Pět principů, díky kterým tento sprint fungoval

Toto nejsou pravidla vymyšlená předem. Jsou to vzorce extrahované ze 40 dnů produkčních dat – z organicky vzniklé historie verzí, post-mortem logů a analýz selhání. Každý princip vzešel z konkrétního selhání, které mu předcházelo.

---

## Princip 1 — Kontroluj předtím, než programuješ (RAW FIRST)

**Problém, který to řeší:** LLM generují na pohled uvěřitelný kód proti API, které ve skutečnosti nikdy nevolaly. Kód je syntakticky správný, ale sémanticky chybný (halucinace). Systém selhává bez chybové hlášky nebo vrací prázdné výsledky. Toto selhání vypadá jako problém v kódu, i když se ve skutečnosti jedná o problém s daty, která neodpovídají předpokladům.

**Praxe:** Před napsáním jakéhokolliv parseru, klienta nebo integrace ověřte realitu:

```bash
curl -s -X POST "[https://api.example.com/endpoint](https://api.example.com/endpoint)" \
  -H "Content-Type: application/json" \
  -d '{"your": "payload"}' | python3 -m json.tool | head -40
```

Zkontrolujte surovou odpověď (*raw response*). Ověřte skutečné názvy klíčů. Potvrďte skutečné datové typy. **Až potom** požádejte LLM o napsání parseru se skutečnou odpovědí vloženou přímo do promptu.

**Důkaz ze sprintu:** Čtyři samostatné chyby v meteorologické pipeline byly způsobeny tím, že LLM předpokládalo strukturu odpovědi odlišnou od reality API. Klíče `data` byly mylně považovány za `rows`, časová razítka ISO 8601 za formát `%d. %m. %Y %H:%M`. Všechny chyby byly eliminovány poté, co se RAW FIRST stal povinným prvním krokem.

**Přenositelnost (Transfer):** Tento princip platí pro jakoukoliv externí závislost — binární protokoly (BMS UART), dodavatelská API či databázová schémata. Ověřte skutečný výstup předtím, než nad ním postavíte abstrakci.

---

## Princip 2 — Jeden segment po druhém (Fractional compilation)

**Problém, který to řeší:** Požádat LLM o vygenerování kompletní pipeline v jediném promptu produkuje kód, který se obtížně ladí, **snadno degraduje** a u kterého je téměř nemožné přiřadit selhání konkrétním komponentám.

**Praxe:** Rozložte každý úkol na nejmenší nezávisle ověřitelnou jednotku. Sestavte, otestujte a potvrďte každou jednotku předtím, než si vyžádáte další.

Příklad segmentace pro scraping pipeline:
1. HTTP požadavek + výpis surové odpovědi do konzole.
2. HTML parser extrahující jedno cílové pole.
3. Validace pole a konverze datového typu.
4. Zápis do úložiště s ošetřením chybových stavů.
5. Integrace scheduleru (cron job).

Každý krok produkuje ověřitelný artefakt. Pokud krok 3 selže, víte přesně, kde je chyba. Nemusíte ji hledat ve 200řádkovém monolitu.

**Důkaz ze sprintu:** Verzovací řady `sonda_db_v1` → `v6` a `kategorizace_v1` → `v5` dokumentují tento vzorec. Každá verze přidala maximálně dvě funkce. Post-mortem analýza (viz `DEVELOPMENT_NOTES.md`) identifikuje monolitické promptování jako primární příčinu ztráty architektonické koherence modelu Gemini po 5. iteraci.

---

## Princip 3 — Selhání jsou data. Ne překážky (Post-Mortem kultura)

**Problém, který to řeší:** Při samostatném vývoji bez týmu se chyby často opakují. LLM nemá paměť na to, co se v minulé session pokazilo, a vývojář zapomíná. Stejná příčina pak produkuje stejné selhání i o několik týdnů později.

**Praxe:** Každé netriviální selhání vyžaduje písemný záznam: symptom, pokus o opravu, hlavní příčina, řešení a odvozené pravidlo.

Ukázka z diagnostického logu („pitevní kniha“):

```text
ZÁZNAM 047
Symptom: Cloud Run vrací 200, ale zápis do GCS tiše selhává.
Pokus: Přidán logging, žádný výstup.
Příčina: Service account nemá oprávnění storage.objects.create.
Řešení: Přidána role roles/storage.objectCreator k SA.
Pravidlo: Ověř IAM oprávnění před debugováním aplikační logiky.
```

> **Poznámka:** Tento konkrétní směr byl nakonec vyhodnocen jako **slepá ulička** (Google API neumožňuje přímé volání na Google Drive z této služby), následoval pivot k Telegram API.

Více než 70 záznamů za 40 dní vytvořilo prohledávatelnou bázi znalostí. Vzorce se staly viditelnými a stejná chyba se neopakovala dvakrát.

**Přenositelnost (Transfer):** Standardní praxe v inženýrství (hlášení incidentů) a medicíně (konference o mortalitě). V samostatném vývoji softwaru je vzácná, ale právě ona vytváří asymetrii ve výsledcích.

---

## Princip 4 — Model je nástroj, ne orákulum

**Problém, který to řeší:** LLM produkují sebevědomý a dobře naformátovaný výstup bez ohledu na jeho správnost. Model se chová identicky, ať už je řešení geniální, nebo nenápadně chybné. Nekritické přijímání výstupu vede k neodhaleným regresím.

**Praxe:** Během sprintu byla důsledně aplikována tři pravidla:
1. **Nikdy nepřijímej výstup bez ověřitelného testu.** Každá funkce byla před integrací spuštěna proti známému vstupu.
2. **Křížově validuj napříč modely.** Primární vývoj v Claude, nezávislá revize v Gemini či Deepseek. Odchylka v návrhu signalizuje potenciální problém.
3. **Ignoruj hodnotící jazyk.** Fráze jako „toto je elegantní řešení“ nenesou žádnou informaci. Je to vlastnost RLHF tréninku, nikoliv technické zhodnocení.

**Důkaz ze sprintu:** Případ degradace Gemini ukázal, že model pokračoval v produkci sebevědomého výstupu i v momentě, kdy logika skriptu zcela kolabovala. Faktická správnost a míra přesvědčivosti modelu jsou dvě zcela nezávislé proměnné.

---

## Princip 5 — Kontext je infrastruktura

**Problém, který to řeší:** LLM začínají každé sezení s čistým štítem. Bez explicitních informací model neví o předchozích architektonických rozhodnutích nebo specifických omezeních projektu.

**Praxe:** Přistupujte ke kontextovým dokumentům jako k infrastruktuře (code-as-context). Každý projekt udržuje stavový dokument s YAML hlavičkou, který se aktualizuje po každém sezení.

Příklad minimálního kontextového dokumentu:
```yaml
---
projekt: "meteo-pipeline"
stack: "Cloud Run, GCS, europe-west1"
opravene_chyby:
  - "chybějící search klíč v payloadu"
  - "ISO 8601 parsování namísto strptime"
omezeni:
  - "RAW FIRST před každým novým endpointem"
  - "žádný VM, pouze serverless"
naposledy_overeno: "2026-03-14"
---
```

Tento dokument je vložen na začátek každé relevantní session. Model díky tomu pracuje s plným kontextem projektu od první zprávy.

**Důkaz ze sprintu:** Používání dokumentů `gcp_stack_ingest_v3.md` a profilů operátora měřitelně zlepšilo soudržnost sezení. RAG indexer v tomto repozitáři byl postaven právě proto, aby tuto „injekci kontextu“ umožnil škálovat.
