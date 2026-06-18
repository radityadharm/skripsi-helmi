import csv, numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson, jarque_bera
from scipy import stats

# --- load data winsorized ---
rows=[]
with open("data/bersih/data_panel_winsorized.csv",encoding="utf-8") as fh:
    for r in csv.DictReader(fh): rows.append(r)
Xcols=["X1_KepInstitusional","X2_KomiteAudit","X3_DewanKomInd","X4_KeberagamanGender","X5_KepManajerial"]
names=["X1","X2","X3","X4","X5"]
X=np.array([[float(r[c]) for c in Xcols] for r in rows])
y=np.array([float(r["Y_ETR"]) for r in rows])
Xc=sm.add_constant(X)
model=sm.OLS(y,Xc).fit()
resid=model.resid

print("="*70); print("UJI ASUMSI KLASIK (data winsorized, 162 observasi)"); print("="*70)
print("Model: Y(ETR) = a + b1.X1 + b2.X2 + b3.X3 + b4.X4 + b5.X5 + e\n")

# 1) NORMALITAS
print("-"*70); print("1. UJI NORMALITAS (residual)"); print("-"*70)
jb,jbp,skew,kurt=jarque_bera(resid)
ks,ksp=stats.kstest((resid-resid.mean())/resid.std(ddof=0),'norm')
sw,swp=stats.shapiro(resid)
print(f"  Jarque-Bera      : stat={jb:.3f}, p-value={jbp:.4f}  -> {'NORMAL' if jbp>0.05 else 'TIDAK normal'}")
print(f"  Kolmogorov-Smir. : stat={ks:.3f}, p-value={ksp:.4f}  -> {'NORMAL' if ksp>0.05 else 'TIDAK normal'}")
print(f"  Shapiro-Wilk     : stat={sw:.3f}, p-value={swp:.4f}  -> {'NORMAL' if swp>0.05 else 'TIDAK normal'}")
print(f"  (Skewness={skew:.3f}, Kurtosis={kurt:.3f}; syarat normal jika p>0,05)")

# 2) MULTIKOLINEARITAS
print("\n"+"-"*70); print("2. UJI MULTIKOLINEARITAS (VIF & Tolerance)"); print("-"*70)
print(f"  {'Variabel':<8}{'VIF':>10}{'Tolerance':>12}   Keterangan")
for i,nm in enumerate(names):
    v=variance_inflation_factor(Xc,i+1)
    print(f"  {nm:<8}{v:>10.3f}{1/v:>12.3f}   {'OK (VIF<10)' if v<10 else 'MULTIKOL'}")

# 3) HETEROSKEDASTISITAS
print("\n"+"-"*70); print("3. UJI HETEROSKEDASTISITAS"); print("-"*70)
bp=het_breuschpagan(resid,Xc); wh=het_white(resid,Xc)
print(f"  Breusch-Pagan    : LM={bp[0]:.3f}, p-value={bp[1]:.4f}  -> {'BEBAS hetero' if bp[1]>0.05 else 'ADA hetero'}")
print(f"  White            : LM={wh[0]:.3f}, p-value={wh[1]:.4f}  -> {'BEBAS hetero' if wh[1]>0.05 else 'ADA hetero'}")
# Glejser
ag=sm.OLS(np.abs(resid),Xc).fit()
print(f"  Glejser (uji F)  : F={ag.fvalue:.3f}, p-value={ag.f_pvalue:.4f}  -> {'BEBAS hetero' if ag.f_pvalue>0.05 else 'ADA hetero'}")

# 4) AUTOKORELASI
print("\n"+"-"*70); print("4. UJI AUTOKORELASI"); print("-"*70)
dw=durbin_watson(resid)
bg=acorr_breusch_godfrey(model,nlags=1)
print(f"  Durbin-Watson    : DW={dw:.3f}  (mendekati 2 = bebas autokorelasi)")
print(f"  Breusch-Godfrey  : LM={bg[0]:.3f}, p-value={bg[1]:.4f}  -> {'BEBAS autokorelasi' if bg[1]>0.05 else 'ADA autokorelasi'}")

# simpan ringkasan CSV
with open("data/bersih/uji_asumsi_klasik.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh)
    w.writerow(["Uji","Metode","Statistik","p-value","Kesimpulan"])
    w.writerow(["Normalitas","Jarque-Bera",round(jb,3),round(jbp,4),"Normal" if jbp>0.05 else "Tidak normal"])
    w.writerow(["Normalitas","Kolmogorov-Smirnov",round(ks,3),round(ksp,4),"Normal" if ksp>0.05 else "Tidak normal"])
    w.writerow(["Normalitas","Shapiro-Wilk",round(sw,3),round(swp,4),"Normal" if swp>0.05 else "Tidak normal"])
    for i,nm in enumerate(names):
        v=variance_inflation_factor(Xc,i+1)
        w.writerow(["Multikolinearitas",f"VIF {nm}",round(v,3),"",("OK" if v<10 else "Multikol")])
    w.writerow(["Heteroskedastisitas","Breusch-Pagan",round(bp[0],3),round(bp[1],4),"Bebas" if bp[1]>0.05 else "Ada hetero"])
    w.writerow(["Heteroskedastisitas","White",round(wh[0],3),round(wh[1],4),"Bebas" if wh[1]>0.05 else "Ada hetero"])
    w.writerow(["Heteroskedastisitas","Glejser",round(ag.fvalue,3),round(ag.f_pvalue,4),"Bebas" if ag.f_pvalue>0.05 else "Ada hetero"])
    w.writerow(["Autokorelasi","Durbin-Watson",round(dw,3),"","DW="+str(round(dw,3))])
    w.writerow(["Autokorelasi","Breusch-Godfrey",round(bg[0],3),round(bg[1],4),"Bebas" if bg[1]>0.05 else "Ada autokorelasi"])
print("\nRingkasan disimpan: data/bersih/uji_asumsi_klasik.csv")
