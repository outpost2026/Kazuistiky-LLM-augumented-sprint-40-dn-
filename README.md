## Obsah
- **[bms.csv](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/LFP_soc_predict_pipeline/bms.csv)** obsahuje agregovaná vyčištěná data z logu BMS LFP baterie - vstupní soubor pro predikční skript
- **[meteo.csv](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/LFP_soc_predict_pipeline/meteo.csv)** vstupní data z openmeteo.com očištěná pomocí profilu horizontu z LIDAR transformace, předpověď relevantních dat 7 dní zpět, 7 dní dopředu pro fotovoltaický systém a baterie LFP
- **[forecast.csv](https://github.com/outpost2026/Kazuistiky-LLM-sprint/blob/LFP_soc_predict_pipeline/forecast.csv)** - finální výstupní soubor s predikcí úrovně nabití baterie pro zadaný počet dní, standardně 5 dnů. Odchylka predikce od pozorované reálné kapacity na další den v intervalu 5 %
