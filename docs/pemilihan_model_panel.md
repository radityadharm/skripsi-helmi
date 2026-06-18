# Pemilihan Model Regresi Data Panel

Data: 162 observasi (winsorized) — 54 perusahaan × 3 tahun.
Tiga model dibandingkan: **Common Effect (CEM)**, **Fixed Effect (FEM)**, **Random Effect (REM)**.

## Hasil Uji

| Uji | H0 | H1 | Statistik | p-value | Keputusan |
|-----|----|----|-----------|---------|-----------|
| **Chow** | Common Effect | Fixed Effect | F = 4,2353 | 0,0000 | Fixed Effect |
| **Hausman** | Random Effect | Fixed Effect | χ² = 3,1589 | 0,6755 | **Random Effect** |
| **Lagrange Multiplier** | Common Effect | Random Effect | LM = 42,2484 | 0,0000 | **Random Effect** |

## Alur Keputusan

1. **Uji Chow** (CEM vs FEM): p = 0,0000 < 0,05 → **Fixed Effect** lebih baik daripada Common Effect.
2. **Uji Hausman** (FEM vs REM): p = 0,6755 > 0,05 → gagal tolak H0 → **Random Effect** lebih tepat daripada Fixed Effect.
3. **Uji LM** (CEM vs REM): p = 0,0000 < 0,05 → **Random Effect** lebih baik daripada Common Effect.

## Kesimpulan

> **Model terpilih: Random Effect Model (REM).**

Ketiga uji konsisten: FEM mengalahkan CEM (Chow), REM mengalahkan FEM (Hausman), dan REM
mengalahkan CEM (LM). Maka estimasi akhir dan pengujian hipotesis menggunakan **Random Effect Model**.

> Karena pada uji asumsi klasik terdeteksi indikasi autokorelasi, estimasi REM sebaiknya
> dilengkapi **robust/clustered standard errors (per perusahaan)** agar inferensi (uji t & F)
> tetap valid.

## File terkait
- `data/bersih/pemilihan_model_panel.csv` — ringkasan hasil
- `scripts/pemilihan_model_panel.py` — script reprodusibel
