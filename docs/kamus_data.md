# Kamus Data (Data Dictionary)

## Identitas Observasi

| Kolom | Keterangan |
|-------|------------|
| No | Nomor urut observasi (1–162) |
| Kode | Kode emiten di BEI (mis. AALI, ADES) |
| Nama Perusahaan | Nama lengkap emiten |
| Tahun | Tahun pengamatan (2022, 2023, 2024) |

## Variabel Penelitian

| Kode | Nama Variabel | Jenis | Rumus | Rentang Wajar |
|------|---------------|-------|-------|---------------|
| **X1** | Kepemilikan Institusional | Independen | Jumlah Saham Institusional ÷ Jumlah Saham Beredar | 0 – 1 |
| **X2** | Komite Audit | Independen | Jumlah anggota Komite Audit (hitungan) | bilangan bulat, umumnya ≥ 2 |
| **X3** | Dewan Komisaris Independen | Independen | Jumlah Komisaris Independen ÷ Total Dewan Komisaris | 0 – 1 |
| **X4** | Keberagaman Gender | Independen | Jumlah Direksi Perempuan ÷ Total Direksi | 0 – 1 |
| **X5** | Kepemilikan Manajerial | Independen | Jumlah Saham Manajemen ÷ Total Saham Beredar | 0 – 1 |
| **Y** | Penghindaran Pajak (CETR/ETR) | Dependen | Beban Pajak ÷ Laba Sebelum Pajak | umumnya 0 – 1 |

## Kolom pada `data_komponen.csv` (input mentah)

| Kolom | Dipakai untuk |
|-------|---------------|
| Saham Institusional, Saham Beredar | menghitung X1 |
| Total Komite Audit (X2) | nilai X2 |
| Jml Komisaris Independen, Total Dewan Komisaris | menghitung X3 |
| Direksi Perempuan, Total Direksi | menghitung X4 |
| Saham Manajemen, Saham Beredar (KM) | menghitung X5 |
| Beban Pajak, Laba Sebelum Pajak | menghitung Y |

> Catatan: nilai X1–X5 & Y pada file komponen sengaja disamakan (presisi penuh) dengan `data_panel.csv` agar konsisten.
