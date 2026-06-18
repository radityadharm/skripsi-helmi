import csv, numpy as np, pandas as pd
from linearmodels.panel import RandomEffects
import statsmodels.api as sm
import warnings; warnings.filterwarnings("ignore")

df=pd.read_csv("data/bersih/data_panel_winsorized.csv").rename(columns={
    "X1_KepInstitusional":"X1","X2_KomiteAudit":"X2","X3_DewanKomInd":"X3",
    "X4_KeberagamanGender":"X4","X5_KepManajerial":"X5","Y_ETR":"Y"})
df=df.set_index(["Kode","Tahun"])
y=df["Y"]; X=sm.add_constant(df[["X1","X2","X3","X4","X5"]])

# Random Effects + robust (clustered per entitas) SE
re=RandomEffects(y,X).fit(cov_type="clustered",cluster_entity=True)

label={"const":"Konstanta","X1":"X1 Kepemilikan Institusional","X2":"X2 Komite Audit",
       "X3":"X3 Dewan Komisaris Independen","X4":"X4 Keberagaman Gender","X5":"X5 Kepemilikan Manajerial"}

print("="*78)
print("ESTIMASI RANDOM EFFECT MODEL (robust/clustered SE per perusahaan)")
print("="*78)
print(f"Observasi: {re.nobs} | Entitas: 54 | Periode: 3\n")

# persamaan
b=re.params
print("PERSAMAAN REGRESI:")
print(f"  Y = {b['const']:.4f} "
      + " ".join([f"{'+' if b[v]>=0 else '-'} {abs(b[v]):.4f}{v}" for v in ['X1','X2','X3','X4','X5']])
      + " + e\n")

# tabel koefisien (uji t parsial)
print("-"*78); print("UJI t (PARSIAL)"); print("-"*78)
print(f"  {'Variabel':<32}{'Koef.':>10}{'Std.Err':>10}{'t':>8}{'p-value':>10}  Sig.")
for v in ['const','X1','X2','X3','X4','X5']:
    coef=re.params[v]; se=re.std_errors[v]; t=re.tstats[v]; p=re.pvalues[v]
    sig="***" if p<0.01 else "**" if p<0.05 else "*" if p<0.10 else "ns"
    print(f"  {label[v]:<32}{coef:>10.4f}{se:>10.4f}{t:>8.3f}{p:>10.4f}  {sig}")
print("  Sig.: *** p<0,01  ** p<0,05  * p<0,10  ns = tidak signifikan")

# uji F simultan, R2
print("\n"+"-"*78); print("UJI F (SIMULTAN) & KOEFISIEN DETERMINASI"); print("-"*78)
print(f"  F-statistic (robust) = {re.f_statistic_robust.stat:.4f}, p-value = {re.f_statistic_robust.pval:.4f}"
      f"  -> {'SIGNIFIKAN' if re.f_statistic_robust.pval<0.05 else 'tidak signifikan'}")
print(f"  R-squared          = {re.rsquared:.4f}")
print(f"  R-squared (overall)= {re.rsquared_overall:.4f}")

# kesimpulan hipotesis per variabel (arah thd ETR)
print("\n"+"-"*78); print("RINGKASAN HIPOTESIS (Y = ETR; ETR naik = penghindaran pajak TURUN)"); print("-"*78)
rowsout=[]
for v in ['X1','X2','X3','X4','X5']:
    coef=re.params[v]; p=re.pvalues[v]
    sig = p<0.05
    arah = "positif" if coef>0 else "negatif"
    if sig:
        efek = "menurunkan penghindaran pajak" if coef>0 else "meningkatkan penghindaran pajak"
        ket=f"Signifikan ({arah}) -> {efek}"
    else:
        ket="Tidak signifikan -> tidak berpengaruh"
    print(f"  {label[v]:<32}: koef={coef:+.4f}, p={p:.4f}  =>  {ket}")
    rowsout.append([label[v],round(coef,4),round(re.std_errors[v],4),round(re.tstats[v],3),round(p,4),
                    ("Signifikan" if sig else "Tidak signifikan"),arah])

with open("data/bersih/estimasi_regresi_rem.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh)
    w.writerow(["Variabel","Koefisien","Std.Error","t-stat","p-value","Kesimpulan","Arah"])
    w.writerow(["Konstanta",round(re.params['const'],4),round(re.std_errors['const'],4),
                round(re.tstats['const'],3),round(re.pvalues['const'],4),"",""])
    for r in rowsout: w.writerow(r)
    w.writerow([])
    w.writerow(["F-statistic (robust)",round(re.f_statistic_robust.stat,4),"p-value",round(re.f_statistic_robust.pval,4),"",""])
    w.writerow(["R-squared",round(re.rsquared,4),"R-squared overall",round(re.rsquared_overall,4),"",""])
print("\nRingkasan disimpan: data/bersih/estimasi_regresi_rem.csv")
