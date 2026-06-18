# Catatan Kualitas & Pembersihan Data

Dokumen ini mencatat semua temuan dan keputusan saat merapikan data dari file asli
(`data/raw/Tabulasi_Data_Asli_Revisi_bu_Eny_27April2026.xlsx`) menjadi data bersih
di `data/bersih/`.

## 1. Validasi perhitungan (hasil: LULUS)

Seluruh rasio dihitung ulang dari input mentahnya dan dibandingkan dengan nilai pada
sheet `Hasil`:

- X1 = Saham Institusional / Saham Beredar ✅
- X3 = Komisaris Independen / Total Dewan Komisaris ✅
- X4 = Direksi Perempuan / Total Direksi ✅
- X5 = Saham Manajemen / Saham Beredar ✅
- Y  = Beban Pajak / Laba Sebelum Pajak ✅

Tidak ditemukan kesalahan perhitungan. Selisih yang muncul hanya akibat pembulatan
tampilan di sheet asli (mis. 0,79685 vs 0,7968471…). Versi bersih memakai **presisi penuh**.

## 2. Nilai kosong yang ditangani

**Kepemilikan Manajerial (X5):** 11 observasi tidak memiliki angka "Saham Manajemen"
di file asli. Ini menandakan perusahaan **tanpa kepemilikan saham oleh manajemen**,
sehingga diisi **0** (konsisten dengan nilai X5 = 0 pada sheet `Hasil`).
Perusahaan terkait antara lain: AALI (2022), STTP (2022), TBLA, UNSP, UNVR.

## 3. Outlier yang perlu diperhatikan (BELUM diubah)

**ETR (Y) > 1 — MLPL tahun 2022: Y = 1,667.**
Artinya beban pajak melebihi laba sebelum pajak pada tahun tersebut. Nilai ini valid
secara hitung, tetapi merupakan outlier. Keputusan penanganan (dibiarkan / winsorize /
trimming) sebaiknya ditentukan pada tahap analisis, bukan saat perapian. **Saat ini
nilai dibiarkan apa adanya.**

## 4. Perbaikan label & konsistensi istilah

- Sheet asli `ETR` memberi judul kolom hasil **"HASIL X2"** — ini **typo**; yang benar
  adalah variabel **Y (CETR)**. Sudah dibetulkan pada versi rapi.
- Penyebutan sektor tidak konsisten di file asli: "sektor riil strategis" (sheet `Sampel`)
  vs "konsumsi barang primer" (sheet `Kriteria Sampel`). Diseragamkan menjadi
  **"Konsumsi Barang Primer"**.

## 5. Hal yang TIDAK diubah

- File asli di `data/raw/` dibiarkan utuh sebagai arsip.
- Tidak ada observasi yang dihapus; jumlah tetap 162 (balanced panel).
- Tidak dilakukan transformasi statistik (log, winsorize, standardisasi) — itu masuk tahap analisis.

## Ringkasan rentang nilai (162 observasi)

| Variabel | Min | Maks | Catatan |
|----------|-----|------|---------|
| X1 | 0,0019 | 1,0000 | wajar |
| X2 | (hitungan) | — | bilangan bulat |
| X3 | 0,2857 | 0,8333 | wajar |
| X4 | 0,0000 | 0,6000 | wajar |
| X5 | 0,0000 | 0,7651 | wajar |
| Y  | 0,0174 | 1,6670 | ada 1 outlier (MLPL 2022) |
