# Data Penelitian Skripsi — Helmi Irsyadi

**Judul (tema):** Pengaruh Mekanisme *Good Corporate Governance* terhadap Penghindaran Pajak (*Tax Avoidance*)
**Objek:** Perusahaan sektor **Konsumsi Barang Primer** yang terdaftar di **Bursa Efek Indonesia (BEI)**
**Periode:** 2022–2024 (3 tahun)
**Sampel:** 54 perusahaan × 3 tahun = **162 observasi** (balanced panel)

## Model Penelitian

| Kode | Variabel | Jenis | Pengukuran |
|------|----------|-------|------------|
| X1 | Kepemilikan Institusional | Independen | Saham Institusional ÷ Saham Beredar |
| X2 | Komite Audit | Independen | Jumlah anggota Komite Audit |
| X3 | Dewan Komisaris Independen | Independen | Komisaris Independen ÷ Total Dewan Komisaris |
| X4 | Keberagaman Gender | Independen | Direksi Perempuan ÷ Total Direksi |
| X5 | Kepemilikan Manajerial | Independen | Saham Manajemen ÷ Saham Beredar |
| Y | Penghindaran Pajak (CETR/ETR) | Dependen | Beban Pajak ÷ Laba Sebelum Pajak |

## Struktur Folder

```
skripsi-helmi/
├── README.md                         <- dokumen ini
├── data/
│   ├── raw/                          <- DATA ASLI (jangan diubah)
│   │   └── Tabulasi_Data_Asli_Revisi_bu_Eny_27April2026.xlsx
│   ├── bersih/                       <- DATA HASIL PERAPIAN
│   │   ├── Tabulasi_Data_Bersih.xlsx <- workbook rapi multi-sheet (utama)
│   │   ├── data_panel.csv            <- 162 observasi, nilai final X1-X5 & Y
│   │   ├── data_komponen.csv         <- rincian input mentah tiap variabel
│   │   └── data_spss.csv             <- numerik saja, siap impor SPSS
│   └── seleksi/                      <- proses pemilihan sampel
│       ├── rekap_seleksi_sampel.csv
│       └── daftar_perusahaan_sampel.csv
└── docs/
    ├── kamus_data.md                 <- definisi & rumus variabel
    └── catatan_kualitas_data.md      <- anomali & catatan pembersihan
```

## Catatan Singkat Perapian

- Data dirapikan dari file asli (16 sheet, banyak sel gabung & format tidak konsisten) menjadi format **tidy** yang siap analisis.
- Seluruh rasio (X1, X3, X4, X5, Y) telah **divalidasi ulang** dari input mentah — cocok 100%.
- Nilai final diambil presisi penuh dari sheet `Hasil` file asli.
- Detail anomali & keputusan pembersihan ada di [`docs/catatan_kualitas_data.md`](docs/catatan_kualitas_data.md).

> File asli di `data/raw/` sengaja **tidak diubah** sebagai arsip/backup. Semua hasil perapian ada di `data/bersih/`.
