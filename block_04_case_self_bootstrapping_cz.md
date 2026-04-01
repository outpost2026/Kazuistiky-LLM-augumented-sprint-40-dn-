# Case Study: Můj kód je lepší nákupčí než já: Jak mi Python sehnal Dell za 2 000 Kč

**Stručný příběh o tom, jak správně nastavená automatizace přestává být jen nástrojem a stává se generátorem reálných zdrojů.**

---

## Co je to „Self-bootstrapping“?

Většinou vnímáme vývoj lineárně: něco se naučíme, napíšeme kód a ten nám vrátí nějaký výsledek. Tento příběh je ale o **uzavřené smyčce**.

Sledoval jsem cestu, kde:

1.  **Systém** vygeneroval fyzické zdroje (zde hardware).
2.  Tyto **zdroje** umožnily další, pokročilejší vývoj.
3.  Tento **vývoj** vytvořil ochranu pro majetek vysoké hodnoty.

Celý tento kruh se uzavřel za necelé dva dny od spuštění.

---

##  Jak to celé začalo (Setup)

Na začátku stála jednoduchá potřeba: levně sehnat materiál na stavbu off-grid dílny. Místo ručního prohledávání inzerátů vznikl automatický „slídil“ (scraper), který hlídal [Bazoš.cz](http://bazos.cz).

**Technické pozadí (zjednodušeně):**

-   Každých 6 hodin se v cloudu probudil skript.
-   Prohledal inzeráty a pomocí klíčových slov vybral ty zajímavé.
-   Pokud něco našel, poslal okamžitě zprávu na Telegram.
-   Modifikace produkčního “slídila” z těžby materiálů na nové téma - kvalitní notebooky za hubičku

**Náklady?** Téměř nulové díky bezplatným limitům v cloudu (GCP) a dvěma dnům práce.

---

## Zlomový okamžik: Po 48 hodinách

Třetí den v produkci systém „pípl“. Objevil se inzerát na výprodej firemních notebooků Dell Latitude 5590 v Praze.

-   **Cena:** 2 000 Kč
-   **Výsledek:** Notebook, který odpracoval zbývající část vývojového sprintu, si systém v podstatě našel a „koupil“ sám.

### Vyplatilo se to? (Ekonomika automatizace)

| Položka | Hodnota |
| --- | --- |
| **Investice** | ~2 dny času + 0 Kč za provoz |
| **Pořízený HW** | Dell Latitude 5590 za 2 000 Kč |
| **Ušetřené peníze** | **odhad 2000 – 8 000 Kč** (oproti nákupu nového HW) |

Tento scraper na sebe vydělal dřív, než skončil první týden projektu.

---

## Smyčka pokračuje: Ochrana baterie

Nový notebook nebyl jen na psaní kódů. Umožnil vyvinout telemetrický systém pro **16 kWh LiFePO4 baterii**, která napájí celou dílnu.

Předtím byla baterie „černá skříňka“ – pokud by se přehřála nebo se rozjely charakteristiky jednotlivých článku, dozvěděl bych se to, až když by přestala fungovat (škoda cca 50 000 Kč).

**Dnes díky automatizaci:**

-   Mám data v reálném čase přes ESP32 a Cloud.
-   Jakákoliv chyba spustí okamžitý alarm na Telegramu.
-   **Scraper** sehnal hardware -> **Hardware** umožnil vývoj -> **Vývoj** chrání drahé baterie.

---

## Hlavní ponaučení: Nepište jen skripty, stavte aktiva

Hlavní rozdíl není v tom, jak složitý je váš kód, ale jak ho **nasadíte**.

-   **Obyčejný skript:** Spustíte ho, když si vzpomenete. Často vám utečou ty nejlepší příležitosti (jako inzerát v 6 ráno).
-   **Produkční automatizace:** Běží v cloudu, nespí, hlídá chyby a upozorní vás jen, když se něco děje.

> **Zlaté pravidlo:** I u malých nástrojů se vyplatí stavět je od začátku v „produkční kvalitě“. Rozdíl v nákladech je minimální, ale rozdíl v přínosu může být obrovský.

---

## Kde to můžete využít i vy?

Tento princip funguje všude, kde se dají sledovat příležitosti:

-   **E-commerce:** Sledování cen konkurence nebo dostupnosti zboží.
-   **Reality:** Hlídání nových nabídek k pronájmu či prodeji.
-   **Výroba:** Monitoring cen vstupních surovin a dodavatelů.

Stačí najít malý, opakující se problém, automatizovat ho a nechat ho, aby si na sebe (a na váš další rozvoj) vydělal.

---

*Tento dokument je součástí série kazuistik o efektivním self-learningu a automatizaci.*
```
