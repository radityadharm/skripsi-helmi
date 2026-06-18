# Uji Asumsi Klasik

Data: 162 observasi (winsorized 5%). Model dasar (pooled OLS):
**Y(ETR) = α + β₁X1 + β₂X2 + β₃X3 + β₄X4 + β₅X5 + e**

> Catatan: uji ini dijalankan pada residual regresi OLS gabungan (pooled) sebagai
> pemeriksaan awal. Pada pendekatan **data panel**, sebagian asumsi (autokorelasi &
> heteroskedastisitas) lazimnya ditangani pada tahap estimasi model terpilih (FEM/REM)
> melalui *robust/clustered standard errors*.

## Ringkasan Hasil

| Uji | Metode | Statistik | p-value | Kesimpulan |
|-----|--------|-----------|---------|------------|
| **Normalitas** | Jarque-Bera | 49,785 | 0,0000 | ❌ Tidak normal |
| | Kolmogorov-Smirnov | 0,178 | 0,0001 | ❌ Tidak normal |
| | Shapiro-Wilk | 0,863 | 0,0000 | ❌ Tidak normal |
| **Multikolinearitas** | VIF X1 | 1,420 | — | ✅ OK (<10) |
| | VIF X2 | 1,030 | — | ✅ OK |
| | VIF X3 | 1,004 | — | ✅ OK |
| | VIF X4 | 1,055 | — | ✅ OK |
| | VIF X5 | 1,355 | — | ✅ OK |
| **Heteroskedastisitas** | Breusch-Pagan | 8,531 | 0,1293 | ✅ Bebas |
| | White | 30,062 | 0,0510 | ✅ Bebas |
| | Glejser (uji F) | 2,039 | 0,0761 | ✅ Bebas |
| **Autokorelasi** | Durbin-Watson | 1,221 | — | ⚠️ Indikasi autokorelasi positif |
| | Breusch-Godfrey | 24,772 | 0,0000 | ❌ Ada autokorelasi |

## Interpretasi

✅ **Multikolinearitas — TERPENUHI.** Semua VIF < 10 (tertinggi X1 = 1,42), Tolerance > 0,1.
Tidak ada korelasi kuat antar variabel independen.

✅ **Heteroskedastisitas — TERPENUHI.** Ketiga uji (Breusch-Pagan, White, Glejser) p-value > 0,05.
Varians residual konstan (homoskedastis).

❌ **Normalitas — BELUM terpenuhi.** Residual tidak berdistribusi normal (skewness 1,26; kurtosis 4,03).

❌ **Autokorelasi — BELUM terpenuhi.** DW = 1,221 (di bawah batas bawah) dan Breusch-Godfrey
signifikan. Perlu dicatat: nilai DW pada data panel yang disusun bertumpuk (per perusahaan lalu
per tahun) sering bias, sehingga interpretasinya tidak seketat data deret waktu murni.

## Opsi Penanganan (untuk didiskusikan dengan pembimbing)

**Untuk normalitas:**
1. *Central Limit Theorem* — dengan n = 162 (>30), estimasi OLS tetap relatif robust; banyak
   skripsi cukup mencantumkan argumen ini.
2. Transformasi variabel (mis. log/akar pada Y) — bisa memperbaiki normalitas, tetapi mengubah
   interpretasi koefisien.
3. Outlier sudah ditangani via winsorize; pengetatan lebih lanjut (mis. winsorize 1%/99% atau
   trimming) bisa dipertimbangkan.

**Untuk autokorelasi:**
1. Pada regresi data panel, gunakan **standard error robust (clustered per perusahaan)** saat
   estimasi FEM/REM — ini cara standar mengatasi autokorelasi & heteroskedastisitas sekaligus.
2. Model **FGLS** atau **Driscoll-Kraay** untuk panel.

> Rekomendasi: lanjutkan ke **pemilihan model panel (Uji Chow → Hausman → LM)**, lalu pada
> estimasi akhir terapkan *robust standard errors* agar isu autokorelasi tertangani secara metodologis.

## File terkait
- `data/bersih/uji_asumsi_klasik.csv` — ringkasan hasil
- `scripts/uji_asumsi_klasik.py` — script reprodusibel
