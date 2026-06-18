# Estimasi Random Effect Model & Uji Hipotesis

Model terpilih: **Random Effect Model (REM)**. Data: 162 observasi (winsorized 5%),
54 perusahaan × 3 tahun. Estimasi dilengkapi **robust/clustered standard errors per perusahaan**
untuk mengantisipasi autokorelasi.

## Persamaan Regresi

**Y(ETR) = 0,1782 + 0,0256·X1 + 0,0087·X2 + 0,0523·X3 − 0,0367·X4 − 0,0047·X5 + e**

## Uji t (Parsial) — Robust SE

| Variabel | Koefisien | Std. Error | t | p-value | Keputusan |
|----------|-----------|------------|-----|---------|-----------|
| Konstanta | 0,1782 | 0,0459 | 3,881 | 0,0002 | *** |
| X1 Kepemilikan Institusional | 0,0256 | 0,0264 | 0,970 | 0,3334 | Tidak signifikan |
| X2 Komite Audit | 0,0087 | 0,0077 | 1,134 | 0,2586 | Tidak signifikan |
| X3 Dewan Komisaris Independen | 0,0523 | 0,0477 | 1,096 | 0,2749 | Tidak signifikan |
| X4 Keberagaman Gender | −0,0367 | 0,0284 | −1,295 | 0,1974 | Tidak signifikan |
| X5 Kepemilikan Manajerial | −0,0047 | 0,0385 | −0,122 | 0,9031 | Tidak signifikan |

*** signifikan p<0,01

## Uji F (Simultan) & Koefisien Determinasi

| Ukuran | Nilai | Keterangan |
|--------|-------|------------|
| F-statistic (robust) | 0,724 | p-value = 0,6066 → **tidak signifikan** |
| R-squared | 0,0161 | — |
| R-squared (overall) | 0,0266 | model menjelaskan ±2,7% variasi ETR |

## Perbandingan Konvensional vs Robust SE (ketahanan hasil)

| Var | Koef | p (konvensional) | p (robust) |
|-----|------|------------------|------------|
| X1 | 0,0256 | 0,4090 | 0,3334 |
| X2 | 0,0087 | 0,6393 | 0,2586 |
| X3 | 0,0523 | 0,3549 | 0,2749 |
| X4 | −0,0367 | 0,3621 | 0,1974 |
| X5 | −0,0047 | 0,9268 | 0,9031 |

Kesimpulan sama untuk kedua jenis SE: **tidak ada variabel yang signifikan**, dan uji F simultan
tidak signifikan. Hasil bersifat robust terhadap pilihan standard error.

## Kesimpulan Hipotesis

Secara **parsial** (uji t) maupun **simultan** (uji F), **tidak ada** mekanisme GCG (Kepemilikan
Institusional, Komite Audit, Dewan Komisaris Independen, Keberagaman Gender, Kepemilikan Manajerial)
yang berpengaruh signifikan terhadap penghindaran pajak (ETR) pada perusahaan sektor konsumsi
barang primer di BEI periode 2022–2024.

> **Catatan interpretasi (penting):** variabel dependen adalah **ETR** — ETR yang lebih *tinggi*
> berarti penghindaran pajak yang lebih *rendah*. Karena seluruh koefisien tidak signifikan,
> arah hubungan (tanda + / −) tidak dapat diinterpretasikan sebagai pengaruh nyata.

> **Untuk bab Pembahasan:** hasil "tidak signifikan" adalah temuan yang sah dan perlu dibahas —
> misalnya karena periode pengamatan pendek (3 tahun), karakteristik tata kelola yang relatif
> seragam antar perusahaan (mis. komite audit hampir selalu 3 orang), atau faktor penentu
> penghindaran pajak lebih dipengaruhi variabel di luar model. Bandingkan dengan penelitian
> terdahulu dan jelaskan kemungkinan penyebabnya.

## File terkait
- `data/bersih/estimasi_regresi_rem.csv` — ringkasan hasil
- `scripts/estimasi_regresi_rem.py` — script reprodusibel
