import csv, numpy as np, pandas as pd
from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects
from scipy import stats
import warnings; warnings.filterwarnings("ignore")

# --- load ---
df=pd.read_csv("data/bersih/data_panel_winsorized.csv")
df=df.rename(columns={"X1_KepInstitusional":"X1","X2_KomiteAudit":"X2",
    "X3_DewanKomInd":"X3","X4_KeberagamanGender":"X4","X5_KepManajerial":"X5","Y_ETR":"Y"})
df=df.set_index(["Kode","Tahun"])
exog=df[["X1","X2","X3","X4","X5"]]
import statsmodels.api as sm
exog_c=sm.add_constant(exog)
y=df["Y"]

pooled=PooledOLS(y,exog_c).fit()
fe=PanelOLS(y,exog_c,entity_effects=True).fit()
re=RandomEffects(y,exog_c).fit()

print("="*70); print("PEMILIHAN MODEL REGRESI DATA PANEL"); print("="*70)
print(f"Entitas (perusahaan): {df.index.get_level_values(0).nunique()}, "
      f"Periode: {df.index.get_level_values(1).nunique()}, Observasi: {len(df)}\n")

# ---------- 1. UJI CHOW (Common vs Fixed) ----------
# F = ((RSS_pooled - RSS_fe)/(N-1)) / (RSS_fe/(NT-N-K))
N=df.index.get_level_values(0).nunique()
T=df.index.get_level_values(1).nunique()
K=exog.shape[1]
rss_p=float((pooled.resids**2).sum()); rss_fe=float((fe.resids**2).sum())
df1=N-1; df2=N*T-N-K
F_chow=((rss_p-rss_fe)/df1)/(rss_fe/df2)
p_chow=stats.f.sf(F_chow,df1,df2)
print("-"*70); print("1. UJI CHOW  (H0: Common Effect | H1: Fixed Effect)"); print("-"*70)
print(f"  F-stat = {F_chow:.4f}, df=({df1},{df2}), p-value = {p_chow:.4f}")
chow_pick="Fixed Effect" if p_chow<0.05 else "Common Effect"
print(f"  => p {'<' if p_chow<0.05 else '>'} 0,05 -> pilih {chow_pick}")

# ---------- 2. UJI HAUSMAN (Fixed vs Random) ----------
b_fe=fe.params.drop("const"); b_re=re.params.drop("const")
cov_fe=fe.cov.drop("const").drop("const",axis=1)
cov_re=re.cov.drop("const").drop("const",axis=1)
diff=b_fe-b_re; covdiff=cov_fe-cov_re
chi2=float(diff.values.T @ np.linalg.pinv(covdiff.values) @ diff.values)
dfh=len(diff); p_haus=stats.chi2.sf(chi2,dfh)
print("\n"+"-"*70); print("2. UJI HAUSMAN  (H0: Random Effect | H1: Fixed Effect)"); print("-"*70)
print(f"  Chi-square = {chi2:.4f}, df={dfh}, p-value = {p_haus:.4f}")
haus_pick="Fixed Effect" if p_haus<0.05 else "Random Effect"
print(f"  => p {'<' if p_haus<0.05 else '>'} 0,05 -> pilih {haus_pick}")

# ---------- 3. UJI LM Breusch-Pagan (Common vs Random) ----------
# LM = (NT/(2(T-1))) * [ (sum_i (sum_t e_it)^2) / (sum e_it^2) - 1 ]^2
e=pooled.resids.copy()
tmp=pd.DataFrame({"e":e.values},index=df.index)
group_sum=tmp.groupby(level=0)["e"].sum()
num=(group_sum**2).sum()
den=(tmp["e"]**2).sum()
LM=(N*T/(2*(T-1)))*((num/den)-1)**2
p_lm=stats.chi2.sf(LM,1)
print("\n"+"-"*70); print("3. UJI LAGRANGE MULTIPLIER  (H0: Common Effect | H1: Random Effect)"); print("-"*70)
print(f"  LM-stat = {LM:.4f}, df=1, p-value = {p_lm:.4f}")
lm_pick="Random Effect" if p_lm<0.05 else "Common Effect"
print(f"  => p {'<' if p_lm<0.05 else '>'} 0,05 -> pilih {lm_pick}")

# ---------- KESIMPULAN ----------
print("\n"+"="*70); print("KESIMPULAN PEMILIHAN MODEL"); print("="*70)
print(f"  Uji Chow    : {chow_pick}")
print(f"  Uji Hausman : {haus_pick}")
print(f"  Uji LM      : {lm_pick}")
# logika keputusan
if chow_pick=="Common Effect" and lm_pick=="Common Effect":
    final="Common Effect Model (CEM)"
elif haus_pick=="Fixed Effect":
    final="Fixed Effect Model (FEM)"
else:
    final="Random Effect Model (REM)"
print(f"\n  >>> MODEL TERPILIH: {final}")

with open("data/bersih/pemilihan_model_panel.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh)
    w.writerow(["Uji","H0","H1","Statistik","p-value","Keputusan"])
    w.writerow(["Chow","Common Effect","Fixed Effect",round(F_chow,4),round(p_chow,4),chow_pick])
    w.writerow(["Hausman","Random Effect","Fixed Effect",round(chi2,4),round(p_haus,4),haus_pick])
    w.writerow(["Lagrange Multiplier","Common Effect","Random Effect",round(LM,4),round(p_lm,4),lm_pick])
    w.writerow(["","","","","","MODEL TERPILIH: "+final])
print("\nRingkasan disimpan: data/bersih/pemilihan_model_panel.csv")
