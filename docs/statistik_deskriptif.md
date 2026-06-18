# Statistik Deskriptif

Data: 162 observasi (54 perusahaan × 3 tahun, 2022–2024).
Penanganan outlier: **Winsorize 5%** (persentil 5 & 95) untuk variabel kontinu.
**X2 (Komite Audit) tidak di-winsorize** karena merupakan variabel hitungan (count, 2–4 orang);
jika di-winsorize nilainya kolaps menjadi konstan 3 sehingga tak bisa dipakai regresi.

## Tabel 1 — Sebelum Winsorize (162 observasi)

| Variabel | N | Min | Maks | Mean | Median | Std. Dev | Skewness | Kurtosis |
|----------|---|-----|------|------|--------|----------|----------|----------|
| X1 Kepemilikan Institusional | 162 | 0,002 | 1,000 | 0,732 | 0,805 | 0,258 | −1,48 | 1,61 |
| X2 Komite Audit | 162 | 2,000 | 4,000 | 3,006 | 3,000 | 0,208 | 0,60 | 20,11 |
| X3 Dewan Komisaris Independen | 162 | 0,286 | 0,833 | 0,444 | 0,400 | 0,116 | 1,27 | 1,82 |
| X4 Keberagaman Gender | 162 | 0,000 | 0,600 | 0,126 | 0,000 | 0,162 | 1,13 | 0,44 |
| X5 Kepemilikan Manajerial | 162 | 0,000 | 0,765 | 0,074 | 0,000 | 0,175 | 2,66 | 6,10 |
| Y Penghindaran Pajak (ETR) | 162 | 0,017 | 1,667 | 0,255 | 0,225 | 0,144 | 6,62 | 57,75 |

## Tabel 2 — Sesudah Winsorize 5% (162 observasi)

| Variabel | N | Min | Maks | Mean | Median | Std. Dev | Skewness | Kurtosis |
|----------|---|-----|------|------|--------|----------|----------|----------|
| X1 Kepemilikan Institusional | 162 | 0,068 | 0,990 | 0,735 | 0,805 | 0,251 | −1,41 | 1,35 |
| X2 Komite Audit | 162 | 2,000 | 4,000 | 3,006 | 3,000 | 0,208 | 0,60 | 20,11 |
| X3 Dewan Komisaris Independen | 162 | 0,333 | 0,667 | 0,439 | 0,400 | 0,101 | 0,69 | −0,38 |
| X4 Keberagaman Gender | 162 | 0,000 | 0,453 | 0,121 | 0,000 | 0,150 | 0,86 | −0,55 |
| X5 Kepemilikan Manajerial | 162 | 0,000 | 0,545 | 0,067 | 0,000 | 0,151 | 2,37 | 4,30 |
| Y Penghindaran Pajak (ETR) | 162 | 0,168 | 0,389 | 0,241 | 0,225 | 0,058 | 1,34 | 1,13 |

## Batas Winsorize & Nilai yang Terpotong

| Variabel | Batas Bawah (p5) | Batas Atas (p95) | Dipotong Bawah | Dipotong Atas |
|----------|------------------|------------------|----------------|---------------|
| X1 | 0,0679 | 0,9900 | 9 | 9 |
| X2 | (tidak di-winsorize) | — | 0 | 0 |
| X3 | 0,3333 | 0,6667 | 1 | 5 |
| X4 | 0,0000 | 0,4532 | 0 | 9 |
| X5 | 0,0000 | 0,5447 | 0 | 9 |
| Y | 0,1678 | 0,3893 | 9 | 9 |

## Interpretasi Ringkas

- **Y (Penghindaran Pajak / ETR):** rata-rata ≈ 0,24 setelah winsorize. Nilai ini mendekati tarif
  pajak badan, artinya secara umum perusahaan tidak terlalu agresif menghindari pajak. Outlier
  MLPL 2022 (ETR 1,667) tertangani — kurtosis turun dari 57,75 menjadi 1,13 (jauh lebih normal).
- **X1 (Kepemilikan Institusional):** mean 0,74 dan skewness negatif — mayoritas perusahaan
  dimiliki institusi dalam proporsi besar.
- **X2 (Komite Audit):** hampir seragam di angka 3 anggota (median = 3), sesuai ketentuan minimum OJK.
- **X4 & X5 (Keberagaman Gender & Kepemilikan Manajerial):** median = 0 — banyak perusahaan tanpa
  direksi perempuan dan tanpa kepemilikan manajerial; distribusi miring ke kanan.

## File terkait
- `data/bersih/statistik_deskriptif_sebelum.csv`
- `data/bersih/statistik_deskriptif_winsorized.csv`
- `data/bersih/data_panel_winsorized.csv` — dataset winsorized untuk analisis lanjut
- `data/bersih/data_spss_winsorized.csv` — versi numerik siap impor SPSS
