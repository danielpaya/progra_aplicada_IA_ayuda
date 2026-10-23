"""Análisis Exploratorio de Datos (AED) - Caso Alimenta Familia. DATOS SIMULADOS, fines académicos.
Uso: python aed_alimenta_familia.py <carpeta_datos> <carpeta_figuras>
Etapas: 1) preguntas  2) caracterización  3) atípicos  4) limpieza  5) patrones + ficha de hechos.
"""
import sys, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1] if len(sys.argv) > 1 else "out"
F = sys.argv[2] if len(sys.argv) > 2 else "fig"
LOTE = "VEG-BP-2026-047"
CRISIS = pd.Timestamp("2026-04-14")
R = {}  # resultados para el informe

# ------------------------------------------------ 1) PREGUNTAS
PREGUNTAS = {
    "P1": "¿Los reportes de salud se concentran en un lote o se distribuyen en el portafolio?",
    "P2": "¿Qué controles de calidad se omitieron y en qué planta/turno ocurre con más frecuencia?",
    "P3": "¿Existe evidencia de laboratorio para los reportes que mencionan otros lotes?",
    "P4": "¿Cómo cambiaron el volumen, el tiempo de respuesta y el sentimiento de las PQR tras la crisis?",
    "P5": "¿La desconfianza se extendió a productos y líneas no afectados técnicamente?",
}

# ------------------------------------------------ 2) CARACTERIZACIÓN
pqr = pd.read_excel(f"{D}/01_Registro_PQR_y_Reclamos_Alimenta_Familia.xlsx", sheet_name="PQR")
lotes = pd.read_excel(f"{D}/02_Trazabilidad_de_Lotes_y_Controles_de_Calidad.xlsx", sheet_name="Lotes")
ctrl = pd.read_excel(f"{D}/02_Trazabilidad_de_Lotes_y_Controles_de_Calidad.xlsx", sheet_name="Controles")
kpi = pd.read_excel(f"{D}/03_Serie_KPI_18_meses.xlsx", sheet_name="KPI")
R["bruto"] = {"pqr": len(pqr), "lotes": len(lotes), "controles": len(ctrl)}
R["nulos_pqr"] = pqr.isna().sum().to_dict()

# ------------------------------------------------ 3) DETECCIÓN DE ATÍPICOS / INVÁLIDOS
log = []
n0 = len(pqr)
pqr = pqr.drop_duplicates()
log.append(("PQR", "Duplicados exactos", n0 - len(pqr), "Se eliminan"))
pqr["fecha_dt"] = pd.to_datetime(pqr["fecha"], errors="coerce")
fecha_inv = pqr["fecha_dt"].isna() | (pqr["fecha_dt"] < "2026-01-01") | (pqr["fecha_dt"] > "2026-09-30")
log.append(("PQR", "Fechas imposibles o fuera de periodo", int(fecha_inv.sum()), "Se excluyen del análisis temporal"))
neg = pqr["tiempo_respuesta_h"] < 0
log.append(("PQR", "Tiempo de respuesta negativo", int(neg.sum()), "Se toma valor absoluto (error de signo)"))
sev = ~pqr["severidad"].between(1, 5)
log.append(("PQR", "Severidad fuera de escala 1-5", int(sev.sum()), "Se marca como nula"))
# IQR en tiempo de respuesta (atípicos estadísticos, no errores)
t = pqr.loc[~neg, "tiempo_respuesta_h"]
q1, q3 = t.quantile([.25, .75]); lim = q3 + 1.5 * (q3 - q1)
R["iqr_tiempo"] = {"q1": round(q1, 1), "q3": round(q3, 1), "limite": round(lim, 1), "n_atipicos": int((t > lim).sum())}

# ------------------------------------------------ 4) LIMPIEZA
pqr.loc[pqr["tiempo_respuesta_h"] < 0, "tiempo_respuesta_h"] = pqr["tiempo_respuesta_h"].abs()
pqr.loc[~pqr["severidad"].between(1, 5), "severidad"] = np.nan
nd = (pqr["lote"] == "N/D").sum()
pqr["lote"] = pqr["lote"].replace("N/D", np.nan)
log.append(("PQR", "Lote 'N/D' (vacío disfrazado)", int(nd), "Se convierte a nulo"))
log.append(("PQR", "Ciudad o canal vacíos", int(pqr["ciudad"].isna().sum() + pqr["canal"].isna().sum()), "Se conservan como 'Sin dato'"))
pqr[["ciudad", "canal"]] = pqr[["ciudad", "canal"]].fillna("Sin dato")
pqr = pqr[~(pqr["fecha_dt"].isna() | (pqr["fecha_dt"] < "2026-01-01") | (pqr["fecha_dt"] > "2026-09-30"))]

n0 = len(ctrl)
ctrl = ctrl.drop_duplicates()
log.append(("Controles", "Duplicados exactos", n0 - len(ctrl), "Se eliminan"))
vac = ctrl["resultado"].isna().sum()
ctrl["resultado"] = ctrl["resultado"].fillna("Sin registro")
log.append(("Controles", "Resultado vacío", int(vac), "Se marca 'Sin registro' (no se asume conforme)"))
ctrl = ctrl.merge(lotes, on="lote", how="left")
ctrl["fecha_control"] = pd.to_datetime(ctrl["fecha_control"]); ctrl["fecha_produccion"] = pd.to_datetime(ctrl["fecha_produccion"])
fc = ctrl["fecha_control"] < ctrl["fecha_produccion"]
log.append(("Controles", "Fecha de control anterior a la producción", int(fc.sum()), "Se marca para verificación con Calidad"))
fr = (ctrl["valor_medido"] < 0) | (ctrl["valor_medido"] >= 999)
log.append(("Controles", "Valor medido fuera de rango", int(fr.sum()), "Se anula el valor; se conserva el resultado"))
ctrl.loc[fr, "valor_medido"] = np.nan
R["limpieza"] = [dict(base=a, hallazgo=b, n=c, tratamiento=d) for a, b, c, d in log]
R["limpio"] = {"pqr": len(pqr), "controles": len(ctrl)}

# ------------------------------------------------ 5) PATRONES
salud = pqr[pqr["tipo"] == "Salud"]
por_lote = salud.groupby("lote").size().sort_values(ascending=False)
R["salud_total"] = len(salud)
R["salud_lote047"] = int(por_lote.get(LOTE, 0))
R["salud_otros_lotes"] = int(salud["lote"].notna().sum() - por_lote.get(LOTE, 0))
R["salud_sin_lote"] = int(salud["lote"].isna().sum())
R["top_lotes_salud"] = por_lote.head(8).astype(int).to_dict()

# P3: evidencia de laboratorio para otros lotes
otros = salud[salud["lote"].notna() & (salud["lote"] != LOTE)]["lote"].unique()
c_otros = ctrl[ctrl["lote"].isin(otros)]
R["otros_lotes_mencionados"] = len(otros)
R["otros_lotes_no_conformes"] = int(c_otros[c_otros["resultado"].isin(["No conforme"])]["lote"].nunique())

# P2: omisiones por planta/turno (antes de la crisis)
ctrl["pre"] = ctrl["fecha_produccion"] < CRISIS
om = ctrl[ctrl["pre"]].assign(omit=lambda x: x["resultado"] == "No realizado").groupby(["planta", "turno"])["omit"].mean().mul(100).round(1)
R["omision_planta_turno_pre"] = {f"{p} · {t}": v for (p, t), v in om.items()}
R["omision_post"] = round(float((ctrl.loc[~ctrl["pre"], "resultado"] == "No realizado").mean() * 100), 2)
R["ficha_047"] = ctrl[ctrl["lote"] == LOTE][["control", "valor_medido", "resultado"]].to_dict("records")
R["lotes_046_048"] = pd.crosstab(ctrl.loc[ctrl["lote"].isin(["VEG-BP-2026-046", "VEG-BP-2026-048"]), "lote"], ctrl["resultado"]).to_dict("index")

# P4: antes vs después
pqr["periodo"] = np.select([pqr["fecha_dt"] < CRISIS, pqr["fecha_dt"] < CRISIS + pd.Timedelta(days=60)],
                           ["Antes", "Crisis (60 días)"], "Después")
per = pqr.groupby("periodo").agg(pqr=("id_pqr", "count"), t_resp_mediana_h=("tiempo_respuesta_h", "median"),
                                 sentimiento_medio=("sentimiento", "mean"))
dias = {"Antes": (CRISIS - pd.Timestamp("2026-01-02")).days, "Crisis (60 días)": 60,
        "Después": (pd.Timestamp("2026-09-30") - CRISIS).days - 60 + 1}
per["pqr_por_dia"] = [round(per.loc[i, "pqr"] / dias[i], 2) for i in per.index]
R["periodos"] = per.round(2).reset_index().to_dict("records")

# P5: contagio a otras líneas
pqr["mes"] = pqr["fecha_dt"].dt.to_period("M").astype(str)
consult = pqr[pqr["tipo"].isin(["Consulta de seguridad", "Rumor / desinformación", "Etiquetado"])]
R["contagio_por_linea"] = consult.groupby("linea").size().astype(int).to_dict()
sem = pqr.set_index("fecha_dt").resample("W-MON")["id_pqr"].count()
R["semanal_pqr"] = {str(k.date()): int(v) for k, v in sem.items()}
sem_s = salud.assign(f=pd.to_datetime(salud["fecha"])).set_index("f").resample("W-MON")["id_pqr"].count()
R["semanal_salud"] = {str(k.date()): int(v) for k, v in sem_s.items()}

# ------------------------------------------------ FIGURAS (6)
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False})
GRIS, AZUL = "#9aa0a6", "#1a73e8"
def save(n): plt.tight_layout(); plt.savefig(f"{F}/{n}.png"); plt.close()

fig, ax = plt.subplots(figsize=(8, 4)); sem.plot(ax=ax, color=GRIS); sem_s.reindex(sem.index, fill_value=0).plot(ax=ax, color=AZUL)
ax.axvline(CRISIS, ls="--", color="k", lw=.8); ax.set_title("PQR semanales: total (gris) y salud (azul)"); ax.set_xlabel(""); save("fig1_pqr_semanales")
fig, ax = plt.subplots(figsize=(8, 4)); top = por_lote.head(8)[::-1]
ax.barh(top.index, top.values, color=[AZUL if i == LOTE else GRIS for i in top.index]); ax.set_title("Reportes de salud por lote (top 8)"); save("fig2_salud_por_lote")
fig, ax = plt.subplots(figsize=(8, 4)); om.unstack().plot.bar(ax=ax, rot=0, color=["#c6dafc", "#8ab4f8", AZUL]); ax.set_ylabel("% controles no realizados")
ax.set_title("Controles omitidos antes de la crisis, por planta y turno"); save("fig3_omision_planta_turno")
fig, ax = plt.subplots(figsize=(8, 4)); pqr.boxplot(column="tiempo_respuesta_h", by="periodo", ax=ax); ax.set_title("Tiempo de respuesta PQR (h) por periodo"); plt.suptitle(""); save("fig4_tiempo_respuesta")
fig, ax = plt.subplots(figsize=(8, 4)); pqr.groupby("mes")["sentimiento"].mean().plot(ax=ax, marker="o", color=AZUL); ax.axhline(0, color="k", lw=.6)
ax.set_title("Sentimiento medio de las PQR por mes (-1 a 1)"); save("fig5_sentimiento")
fig, ax = plt.subplots(figsize=(8, 4)); pd.crosstab(consult["mes"], consult["linea"]).plot.bar(stacked=True, ax=ax, rot=45); ax.set_title("Consultas de seguridad, rumores y etiquetado por línea"); save("fig6_contagio_lineas")

fig, ax = plt.subplots(figsize=(8, 4)); k2 = kpi.set_index("mes")["indice_confianza_0_100"]; proj = kpi["fase"].str.contains("proyecc").values
ax.plot(range(len(k2)), k2.values, color=AZUL, marker="o"); ax.plot([i for i in range(len(k2)) if proj[i]], k2.values[proj], color=GRIS, marker="o", ls="--")
ax.axvspan(5.5, 8.5, color="#eeeeee"); ax.axhline(k2.values[:6].mean(), ls="--", color="k", lw=.6); ax.set_xticks(range(len(k2))); ax.set_xticklabels(k2.index, rotation=60, fontsize=7)
ax.set_ylim(0, 100); ax.set_title("Índice de confianza (0-100): antes, crisis y recuperación (gris = proyección)"); save("fig7_indice_confianza")

with open(f"{F}/resultados_aed.json", "w", encoding="utf8") as fh:
    json.dump({"preguntas": PREGUNTAS, **R}, fh, ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
