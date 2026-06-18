import csv, numpy as np

cols=[("X1_KepInstitusional","X1 Kepemilikan Institusional"),
      ("X2_KomiteAudit","X2 Komite Audit"),
      ("X3_DewanKomInd","X3 Dewan Komisaris Independen"),
      ("X4_KeberagamanGender","X4 Keberagaman Gender"),
      ("X5_KepManajerial","X5 Kepemilikan Manajerial"),
      ("Y_ETR","Y Penghindaran Pajak (ETR)")]

rows=[]
with open("data/bersih/data_panel.csv",encoding="utf-8") as fh:
    for r in csv.DictReader(fh): rows.append(r)
data={k:np.array([float(r[k]) for r in rows]) for k,_ in cols}
N=len(rows)

def winsorize(a,p=5):
    lo,hi=np.percentile(a,p),np.percentile(a,100-p)
    return np.clip(a,lo,hi),lo,hi

def desc(a):
    return dict(N=len(a),Min=a.min(),Maks=a.max(),Mean=a.mean(),
                Median=np.median(a),StdDev=a.std(ddof=1),
                Skew=float(((a-a.mean())**3).mean()/a.std()**3),
                Kurt=float(((a-a.mean())**4).mean()/a.std()**4-3))

def table(dataset,title):
    print(f"\n{'='*90}\n{title}\n{'='*90}")
    hdr=f"{'Variabel':<32}{'N':>4}{'Min':>9}{'Maks':>9}{'Mean':>9}{'Median':>9}{'Std':>9}{'Skew':>8}{'Kurt':>8}"
    print(hdr); print("-"*len(hdr))
    out=[]
    for k,lab in cols:
        d=desc(dataset[k])
        print(f"{lab:<32}{d['N']:>4}{d['Min']:>9.3f}{d['Maks']:>9.3f}{d['Mean']:>9.3f}{d['Median']:>9.3f}{d['StdDev']:>9.3f}{d['Skew']:>8.2f}{d['Kurt']:>8.2f}")
        out.append([lab,d['N'],d['Min'],d['Maks'],d['Mean'],d['Median'],d['StdDev'],d['Skew'],d['Kurt']])
    return out

orig=table(data,"STATISTIK DESKRIPTIF — SEBELUM WINSORIZE (162 observasi)")

# winsorize
wdata={}; bounds={}
SKIP={"X2_KomiteAudit"}  # variabel hitungan, tidak diwinsorize
for k,_ in cols:
    if k in SKIP:
        wdata[k]=data[k].copy(); bounds[k]=(data[k].min(),data[k].max())
    else:
        wdata[k],lo,hi=winsorize(data[k],5); bounds[k]=(lo,hi)
wins=table(wdata,"STATISTIK DESKRIPTIF — SESUDAH WINSORIZE 5% (162 observasi)")

# berapa nilai yang terpotong
print(f"\n{'='*90}\nBATAS WINSORIZE & JUMLAH NILAI TERPOTONG (persentil 5 & 95)\n{'='*90}")
print(f"{'Variabel':<32}{'Batas Bawah':>14}{'Batas Atas':>14}{'Dipotong Bwh':>14}{'Dipotong Ats':>14}")
for k,lab in cols:
    lo,hi=bounds[k]
    nlo=int((data[k]<lo).sum()); nhi=int((data[k]>hi).sum())
    print(f"{lab:<32}{lo:>14.4f}{hi:>14.4f}{nlo:>14}{nhi:>14}")

# ---- simpan output ----
def writecsv(path,rows):
    with open(path,"w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh)
        w.writerow(["Variabel","N","Minimum","Maksimum","Mean","Median","Std. Deviasi","Skewness","Kurtosis"])
        for r in rows: w.writerow([r[0]]+[round(x,4) if isinstance(x,float) else x for x in r[1:]])
writecsv("data/bersih/statistik_deskriptif_sebelum.csv",orig)
writecsv("data/bersih/statistik_deskriptif_winsorized.csv",wins)

# simpan dataset winsorized (panel + spss)
with open("data/bersih/data_panel_winsorized.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh)
    w.writerow(["No","Kode","Nama Perusahaan","Tahun"]+[k for k,_ in cols])
    for i,r in enumerate(rows):
        w.writerow([r["No"],r["Kode"],r["Nama Perusahaan"],r["Tahun"]]+[round(wdata[k][i],10) for k,_ in cols])
with open("data/bersih/data_spss_winsorized.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow([k.split("_")[0] for k,_ in cols])
    for i in range(N): w.writerow([round(wdata[k][i],10) for k,_ in cols])
print("\nFile tersimpan: statistik_deskriptif_*.csv, data_panel_winsorized.csv, data_spss_winsorized.csv")
