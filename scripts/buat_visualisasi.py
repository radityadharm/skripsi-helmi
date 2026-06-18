import csv, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({"figure.dpi":130,"font.size":10,"axes.titleweight":"bold"})

OUT="visualisasi"
# --- load panel ---
rows=[]
with open("data/bersih/data_panel.csv",encoding="utf-8") as fh:
    for r in csv.DictReader(fh): rows.append(r)
def f(r,k): return float(r[k])
vars_=[("X1_KepInstitusional","X1\nKep. Institusional"),
       ("X2_KomiteAudit","X2\nKomite Audit"),
       ("X3_DewanKomInd","X3\nDewan Kom. Ind."),
       ("X4_KeberagamanGender","X4\nKeberagaman Gender"),
       ("X5_KepManajerial","X5\nKep. Manajerial"),
       ("Y_ETR","Y\nETR (Penghindaran Pajak)")]
data={k:np.array([f(r,k) for r in rows]) for k,_ in vars_}
tahun=np.array([int(r["Tahun"]) for r in rows])

# ===== 1. Distribusi (histogram + KDE) =====
fig,axes=plt.subplots(2,3,figsize=(14,8))
for ax,(k,lab) in zip(axes.flat,vars_):
    sns.histplot(data[k],kde=True,ax=ax,color="#2c6fbb",edgecolor="white")
    ax.set_title(lab); ax.set_xlabel(""); ax.set_ylabel("Frekuensi")
fig.suptitle("Distribusi Tiap Variabel (162 Observasi)",fontsize=14,fontweight="bold")
fig.tight_layout(); fig.savefig(f"{OUT}/01_distribusi_variabel.png",bbox_inches="tight"); plt.close(fig)

# ===== 2. Boxplot deteksi outlier (skala dinormalkan z-score agar sebanding) =====
fig,ax=plt.subplots(figsize=(11,6))
zd=[ (data[k]-data[k].mean())/data[k].std(ddof=0) for k,_ in vars_]
bp=ax.boxplot(zd,tick_labels=[l.replace(chr(10)," ") for _,l in vars_],patch_artist=True,showfliers=True)
for patch in bp['boxes']: patch.set_facecolor("#9ecae1")
ax.set_title("Boxplot Standardisasi (z-score) — Deteksi Outlier")
ax.set_ylabel("Nilai standar (z)"); ax.axhline(0,color="grey",lw=.8,ls="--")
plt.xticks(rotation=20,ha="right")
# anotasi outlier Y tertinggi
yi=np.argmax(data["Y_ETR"]); kode=rows[yi]["Kode"]
fig.tight_layout(); fig.savefig(f"{OUT}/02_boxplot_outlier.png",bbox_inches="tight"); plt.close(fig)

# ===== 3. Heatmap korelasi =====
M=np.column_stack([data[k] for k,_ in vars_])
corr=np.corrcoef(M.T)
labels=[l.split("\n")[0] for _,l in vars_]
fig,ax=plt.subplots(figsize=(8,6.5))
sns.heatmap(corr,annot=True,fmt=".2f",cmap="RdBu_r",center=0,vmin=-1,vmax=1,
            xticklabels=labels,yticklabels=labels,square=True,linewidths=.5,
            cbar_kws={"label":"Koefisien korelasi Pearson"},ax=ax)
ax.set_title("Matriks Korelasi Antar Variabel")
fig.tight_layout(); fig.savefig(f"{OUT}/03_heatmap_korelasi.png",bbox_inches="tight"); plt.close(fig)

# ===== 4. Scatter X1-X5 vs Y dengan garis regresi =====
fig,axes=plt.subplots(2,3,figsize=(14,8))
xs=[v for v in vars_ if v[0]!="Y_ETR"]
y=data["Y_ETR"]
for ax,(k,lab) in zip(axes.flat,xs):
    sns.regplot(x=data[k],y=y,ax=ax,scatter_kws={"alpha":.5,"s":28,"color":"#2c6fbb"},
                line_kws={"color":"#d62728"})
    r=np.corrcoef(data[k],y)[0,1]
    ax.set_title(f"{lab.split(chr(10))[0]} vs Y  (r={r:.2f})")
    ax.set_xlabel(lab.replace("\n"," ")); ax.set_ylabel("Y (ETR)")
axes.flat[-1].axis("off")
fig.suptitle("Hubungan Variabel Independen terhadap Penghindaran Pajak (Y)",fontsize=14,fontweight="bold")
fig.tight_layout(); fig.savefig(f"{OUT}/04_scatter_X_vs_Y.png",bbox_inches="tight"); plt.close(fig)

# ===== 5. Tren rata-rata per tahun =====
years=[2022,2023,2024]
fig,axes=plt.subplots(1,2,figsize=(14,5.2))
for k,lab in xs:
    means=[data[k][tahun==yr].mean() for yr in years]
    axes[0].plot(years,means,marker="o",label=lab.split("\n")[0])
axes[0].set_title("Rata-rata Variabel GCG per Tahun"); axes[0].set_xticks(years)
axes[0].set_ylabel("Rata-rata"); axes[0].legend(fontsize=8)
ymeans=[data["Y_ETR"][tahun==yr].mean() for yr in years]
axes[1].plot(years,ymeans,marker="o",color="#d62728",lw=2)
axes[1].set_title("Rata-rata Penghindaran Pajak (Y/ETR) per Tahun")
axes[1].set_xticks(years); axes[1].set_ylabel("Rata-rata ETR")
for x,v in zip(years,ymeans): axes[1].annotate(f"{v:.3f}",(x,v),textcoords="offset points",xytext=(0,8),ha="center")
fig.tight_layout(); fig.savefig(f"{OUT}/05_tren_per_tahun.png",bbox_inches="tight"); plt.close(fig)

# ===== 6. Top & Bottom 10 perusahaan by rata-rata Y =====
from collections import defaultdict
agg=defaultdict(list)
for r in rows: agg[r["Kode"]].append(f(r,"Y_ETR"))
avg={k:np.mean(v) for k,v in agg.items()}
srt=sorted(avg.items(),key=lambda x:x[1])
bottom=srt[:10]; top=srt[-10:]
fig,axes=plt.subplots(1,2,figsize=(14,5.5))
axes[0].barh([k for k,_ in top],[v for _,v in top],color="#d62728")
axes[0].set_title("10 Tertinggi ETR\n(beban pajak relatif besar / penghindaran rendah)")
axes[0].set_xlabel("Rata-rata ETR 2022-2024")
axes[1].barh([k for k,_ in bottom],[v for _,v in bottom],color="#2ca02c")
axes[1].set_title("10 Terendah ETR\n(indikasi penghindaran pajak lebih tinggi)")
axes[1].set_xlabel("Rata-rata ETR 2022-2024")
fig.tight_layout(); fig.savefig(f"{OUT}/06_peringkat_perusahaan.png",bbox_inches="tight"); plt.close(fig)

print("Outlier Y tertinggi:",kode,round(data['Y_ETR'][yi],3))
print("Selesai membuat 6 grafik.")
