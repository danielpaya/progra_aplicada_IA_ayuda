"""Análisis Exploratorio de Datos (AED) - Caso Claude: enlaces compartidos en buscadores. DATOS SIMULADOS, fines académicos.
Uso: python src/aed_claude_enlaces.py <carpeta_datos> <carpeta_figuras>
Etapas: 1) preguntas  2) caracterización  3) atípicos e inválidos  4) limpieza  5) patrones + ficha de hechos.
"""
import sys, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = sys.argv[1] if len(sys.argv) > 1 else "datos"
F = sys.argv[2] if len(sys.argv) > 2 else "resultados/figuras"
INC2 = pd.Timestamp("2026-07-25")
CORTE = pd.Timestamp("2026-09-30")
R = {}

# ------------------------------------------------ 1) PREGUNTAS
PREGUNTAS = {
    "P1": "¿Qué explica que un enlace compartido llegue a un buscador: el tipo de contenido o dónde se publicó?",
    "P2": "¿Cuántos enlaces indexados exponían datos sensibles y de qué tipo?",
    "P3": "¿Cuánto tiempo estuvieron visibles y cuántos siguen activos hoy?",
    "P4": "¿Cómo cambiaron el volumen, el tiempo de respuesta y el sentimiento de las menciones tras el 25-jul-2026?",
    "P5": "¿La preocupación se extendió a usuarios que no tenían ningún enlace expuesto?",
}

# ------------------------------------------------ 2) CARACTERIZACIÓN
lk = pd.read_excel(f"{D}/01_Auditoria_Enlaces_Compartidos.xlsx", sheet_name="Enlaces")
mn = pd.read_excel(f"{D}/02_Menciones_y_Soporte_Privacidad.xlsx", sheet_name="Menciones")
kpi = pd.read_excel(f"{D}/03_Serie_KPI_24_meses.xlsx", sheet_name="KPI")
R["bruto"] = {"enlaces": len(lk), "menciones": len(mn), "meses_kpi": len(kpi)}
R["nulos_enlaces"] = {k: int(v) for k, v in lk.isna().sum().items()}
R["nulos_menciones"] = {k: int(v) for k, v in mn.isna().sum().items()}

# ------------------------------------------------ 3) ATÍPICOS E INVÁLIDOS + 4) LIMPIEZA
log = []
n0 = len(lk); lk = lk.drop_duplicates(); log.append(("Enlaces", "Duplicados exactos", n0 - len(lk), "Se eliminan"))
norm = lk["indexado"].astype(str).str.strip().str.lower().map({"sí": "Sí", "si": "Sí", "s": "Sí", "no": "No"})
log.append(("Enlaces", "Etiquetas inconsistentes en 'indexado'", int((norm != lk["indexado"]).sum()), "Se normalizan a Sí / No"))
lk["indexado"] = norm
lk["creado_dt"] = pd.to_datetime(lk["fecha_creacion"], errors="coerce")
fi = lk["creado_dt"].isna() | (lk["creado_dt"] < "2025-05-01") | (lk["creado_dt"] > CORTE)
log.append(("Enlaces", "Fecha de creación imposible", int(fi.sum()), "Se excluyen del análisis temporal; el enlace se conserva"))
neg = lk["horas_visible"] < 0
log.append(("Enlaces", "Horas visibles negativas", int(neg.sum()), "Se toma el valor absoluto (error de signo)"))
lk.loc[neg, "horas_visible"] = lk.loc[neg, "horas_visible"].abs()
vac = int(lk["plan"].isna().sum() + lk["pais"].isna().sum())
log.append(("Enlaces", "Plan o país vacíos", vac, "Se conservan como 'Sin dato'"))
lk[["plan", "pais"]] = lk[["plan", "pais"]].fillna("Sin dato")
for c in ["fecha_aparicion", "fecha_retiro", "fecha_desactivacion"]:
    lk[c] = pd.to_datetime(lk[c], errors="coerce")

n0 = len(mn); mn = mn.drop_duplicates(); log.append(("Menciones", "Duplicados exactos", n0 - len(mn), "Se eliminan"))
mn["fecha_dt"] = pd.to_datetime(mn["fecha"], errors="coerce")
fm = mn["fecha_dt"].isna() | (mn["fecha_dt"] < "2026-06-01") | (mn["fecha_dt"] > CORTE)
log.append(("Menciones", "Fechas imposibles o fuera de periodo", int(fm.sum()), "Se excluyen"))
mn = mn[~fm].copy()
neg = mn["tiempo_respuesta_h"] < 0
log.append(("Menciones", "Tiempo de respuesta negativo", int(neg.sum()), "Se toma el valor absoluto"))
mn.loc[neg, "tiempo_respuesta_h"] = mn.loc[neg, "tiempo_respuesta_h"].abs()
fs = ~mn["sentimiento"].between(-1, 1)
log.append(("Menciones", "Sentimiento fuera de la escala -1 a 1", int(fs.sum()), "Se marca como nulo"))
mn.loc[fs, "sentimiento"] = np.nan
nd = int((mn["relacion_con_enlaces"] == "N/D").sum())
mn["relacion_con_enlaces"] = mn["relacion_con_enlaces"].replace("N/D", "Sin dato")
log.append(("Menciones", "Relación con enlaces 'N/D' (vacío disfrazado)", nd, "Se marca 'Sin dato'"))
log.append(("Menciones", "Canal vacío", int(mn["canal"].isna().sum()), "Se conserva como 'Sin dato'"))
mn["canal"] = mn["canal"].fillna("Sin dato")
R["limpieza"] = [dict(base=a, hallazgo=b, n=int(c), tratamiento=d) for a, b, c, d in log]
R["limpio"] = {"enlaces": len(lk), "menciones": len(mn)}

# atípicos estadísticos (IQR) en el tiempo de respuesta de soporte: se conservan, son la señal de la crisis
t = mn["tiempo_respuesta_h"].dropna()
q1, q3 = t.quantile([.25, .75]); lim = q3 + 1.5 * (q3 - q1)
R["iqr_tiempo"] = {"q1": round(q1, 1), "q3": round(q3, 1), "limite": round(lim, 1), "n_atipicos": int((t > lim).sum()),
                   "pct_atipicos_en_crisis": round(float((mn.loc[mn["tiempo_respuesta_h"] > lim, "fecha_dt"] >= INC2).mean() * 100), 1)}

# ------------------------------------------------ 5) PATRONES
ix = lk[lk["indexado"] == "Sí"].copy()
R["indexados"] = len(ix)
R["pct_indexados"] = round(len(ix) / len(lk) * 100, 1)

# P1 · dónde se publicó vs tipo
tab = lk.pivot_table(index="publicado_en", columns="tipo", values="id_enlace", aggfunc="count", fill_value=0)
tab_ix = ix.pivot_table(index="publicado_en", columns="tipo", values="id_enlace", aggfunc="count", fill_value=0).reindex(tab.index, fill_value=0)
pct = (tab_ix / tab * 100).round(1)
R["pct_indexado_publicacion_tipo"] = {f"{p} · {t}": float(pct.loc[p, t]) for p in pct.index for t in pct.columns}
R["n_publicacion_tipo"] = {f"{p} · {t}": int(tab.loc[p, t]) for p in tab.index for t in tab.columns}
R["indexados_por_publicacion"] = ix["publicado_en"].value_counts().astype(int).to_dict()
priv = ix["publicado_en"].eq("Solo mensajería privada")
R["indexados_publicados_por_usuario_pct"] = round(float((~priv).mean() * 100), 1)
R["indexados_sin_publicacion_publica"] = int(priv.sum())
R["pct_indexado_por_tipo"] = (lk.groupby("tipo")["indexado"].apply(lambda s: (s == "Sí").mean() * 100).round(1)).to_dict()

# P2 · datos sensibles
sens = ix[ix["dato_sensible"] != "Ninguno"]
R["indexados_con_sensibles"] = len(sens)
R["pct_indexados_con_sensibles"] = round(len(sens) / len(ix) * 100, 1)
R["sensibles_por_tipo"] = sens["dato_sensible"].value_counts().astype(int).to_dict()
R["sensibles_nivel_alto"] = int((sens["nivel_sensibilidad"] == "Alto").sum())

# P3 · tiempo visible y enlaces activos
R["dias_visibles_mediana"] = round(float(ix["horas_visible"].median() / 24), 1)
R["dias_visibles_mediana_episodio2"] = round(float(ix.loc[ix["fecha_retiro"] >= "2026-01-01", "horas_visible"].median() / 24), 1)
R["indexados_episodio1"] = int((ix["fecha_retiro"] < "2026-01-01").sum())
R["indexados_episodio2"] = int((ix["fecha_retiro"] >= "2026-01-01").sum())
R["indexados_activos_hoy"] = int((ix["desactivado_por_usuario"] == "No").sum())
R["pct_indexados_activos_hoy"] = round(float((ix["desactivado_por_usuario"] == "No").mean() * 100), 1)
R["indexados_por_buscador"] = ix["buscador"].value_counts().astype(int).to_dict()

# P4 · menciones antes, en crisis (30 días) y después
mn["periodo"] = np.select([mn["fecha_dt"] < INC2, mn["fecha_dt"] <= INC2 + pd.Timedelta(days=30)], ["Antes", "Crisis (30 días)"], "Después")
dias = {"Antes": (INC2 - pd.Timestamp("2026-06-01")).days, "Crisis (30 días)": 31, "Después": (CORTE - INC2).days - 30}
per = mn.groupby("periodo").agg(menciones=("id_mencion", "count"), t_resp_mediana_h=("tiempo_respuesta_h", "median"),
                                sentimiento_medio=("sentimiento", "mean"))
per["por_dia"] = [round(per.loc[i, "menciones"] / dias[i], 2) for i in per.index]
R["periodos"] = per.round(2).reset_index().to_dict("records")
sem = mn.set_index("fecha_dt").resample("W-MON", label="left", closed="left")["id_mencion"].count()
privtipos = ["Queja de privacidad", "Solicitud de retiro o desindexación", "Pregunta: ¿mi chat es público?", "Solicitud de borrado de datos"]
sem_p = mn[mn["tipo"].isin(privtipos)].set_index("fecha_dt").resample("W-MON", label="left", closed="left")["id_mencion"].count().reindex(sem.index, fill_value=0)
R["semanal"] = [{"w": str(k.date()), "total": int(v), "priv": int(sem_p[k])} for k, v in sem.items()]
pre = sem[sem.index < INC2 - pd.Timedelta(days=6)]
R["promedio_semanal_previo"] = round(float(pre.mean()), 1)
R["pico_semanal"] = int(sem.max()); R["semana_pico"] = str(sem.idxmax().date())
R["multiplicador_pico"] = round(float(sem.max() / pre.mean()), 1)

# P5 · contagio: ¿quién preguntó o se quejó durante la crisis?
cr = mn[(mn["periodo"] == "Crisis (30 días)") & mn["tipo"].isin(privtipos + ["Cancelación de suscripción"]) & (mn["relacion_con_enlaces"] != "Sin dato")]
R["contagio"] = cr["relacion_con_enlaces"].value_counts().astype(int).to_dict()
R["pct_sin_enlace_expuesto"] = round(float((cr["relacion_con_enlaces"] != "Tenía un enlace indexado").mean() * 100), 1)
R["pct_nunca_compartio"] = round(float((cr["relacion_con_enlaces"] == "Nunca compartió").mean() * 100), 1)

# tablero: robots.txt al 100 % mientras crecían los enlaces visibles
R["tablero"] = kpi[["mes", "pct_paginas_bloqueadas_robots", "enlaces_muestra_visibles_en_buscadores"]].to_dict("records")

# ficha de hechos (combina hechos públicos verificados y hallazgos de los datos simulados)
R["ficha"] = {
    "confirmado": ["Chats y artefactos compartidos aparecieron en Google y Bing (jul-2026)",
                   "Solo se expuso contenido que alguien había compartido; no hubo acceso a cuentas",
                   "robots.txt bloqueaba /share, pero eso no impide indexar una URL enlazada",
                   "Los resultados se retiraron entre el 26 y el 28 de julio",
                   "Ya había pasado en septiembre de 2025 (cerca de 600 conversaciones)"],
    "por_confirmar": ["Cuántos enlaces quedaron copiados en archivos de terceros"],
    "no_consta": ["Que alguien haya usado las credenciales expuestas", "Que sea culpa de los usuarios",
                  "Que ningún dato sensible haya quedado público"],
}

# ------------------------------------------------ FIGURAS
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False})
ROJO, GRIS, AZUL, VERDE = "#E03A1E", "#9aa0a6", "#2442C9", "#2E7D4F"
def save(n): plt.tight_layout(); plt.savefig(f"{F}/{n}.png"); plt.close()

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(sem.index, sem.values, width=5, color=GRIS, label="Todas"); ax.bar(sem_p.index, sem_p.values, width=5, color=ROJO, label="Privacidad")
ax.axvline(INC2, ls="--", color="k", lw=.8); ax.legend(frameon=False); ax.set_title("Menciones y tickets por semana (jun-sep 2026)")
import matplotlib.dates as mdates; ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b")); ax.tick_params(axis="x", rotation=45); save("fig1_menciones_semanales")

fig, ax = plt.subplots(figsize=(8, 4)); pct.sort_values("Conversación").plot.barh(ax=ax, color=[AZUL, ROJO])
ax.set_xlabel("% de enlaces indexados"); ax.set_title("¿Qué enlaces llegaron a buscadores? Según dónde se publicaron"); save("fig2_indexacion_por_publicacion")

fig, ax = plt.subplots(figsize=(8, 4)); s = ix["dato_sensible"].value_counts().sort_values()
ax.barh(s.index, s.values, color=[GRIS if i == "Ninguno" else ROJO for i in s.index]); ax.set_title(f"Datos sensibles en los {len(ix)} enlaces indexados"); save("fig3_datos_sensibles")

fig, ax = plt.subplots(figsize=(8, 4)); mn.boxplot(column="tiempo_respuesta_h", by="periodo", ax=ax); ax.set_title("Tiempo de respuesta de soporte (h) por periodo"); plt.suptitle(""); save("fig4_tiempo_respuesta")

fig, ax = plt.subplots(figsize=(8, 4)); mn.set_index("fecha_dt").resample("W-MON")["sentimiento"].mean().plot(ax=ax, marker="o", color=AZUL)
ax.axhline(0, color="k", lw=.6); ax.axvline(INC2, ls="--", color="k", lw=.8); ax.set_title("Sentimiento medio semanal (-1 a 1)"); save("fig5_sentimiento")

fig, ax = plt.subplots(figsize=(6, 4)); c = pd.Series(R["contagio"])
ax.pie(c.values, labels=c.index, autopct="%1.0f%%", textprops={"fontsize": 9}, wedgeprops={"edgecolor": "white"}, colors=[ROJO, "#F07A5E", "#151311"][:len(c)], startangle=90); [t.set_color("white") for t in ax.texts if "%" in t.get_text()]; ax.set_title("Quejas y preguntas en la crisis\nsegún la relación del usuario con los enlaces", fontsize=10); save("fig6_contagio")

fig, ax = plt.subplots(figsize=(8, 4)); kk = kpi[~kpi["fase"].str.contains("proyecc")]
ax.bar(kk["mes"], kk["enlaces_muestra_visibles_en_buscadores"], color=ROJO, label="Enlaces de la muestra visibles en buscadores")
ax2 = ax.twinx(); ax2.plot(kk["mes"], kk["pct_paginas_bloqueadas_robots"], color=VERDE, lw=3, label="% páginas bloqueadas en robots.txt"); ax2.set_ylim(0, 110)
ax.tick_params(axis="x", rotation=60, labelsize=7); ax.set_title("El tablero en verde (robots.txt 100 %) y los enlaces visibles", pad=28)
fig.legend(loc="upper center", bbox_to_anchor=(.5, .92), ncol=2, frameon=False, fontsize=8); save("fig7_tablero_vs_visibles")

fig, ax = plt.subplots(figsize=(8, 4)); k2 = kpi.set_index("mes")["indice_confianza_privacidad_0_100"]; proj = kpi["fase"].str.contains("proyecc").values
ax.plot(range(len(k2)), k2.values, color=AZUL, marker="o"); ax.plot([i for i in range(len(k2)) if proj[i]], k2.values[proj], color=GRIS, marker="o", ls="--")
ax.axvspan(4.5, 5.5, color="#eeeeee"); ax.axvspan(14.5, 16.5, color="#f6d5cd"); ax.set_xticks(range(len(k2))); ax.set_xticklabels(k2.index, rotation=60, fontsize=7)
ax.set_ylim(0, 100); ax.set_title("Índice de confianza en la privacidad (0-100) · gris = proyección"); save("fig8_indice_confianza")

with open(f"{F}/resultados_aed.json", "w", encoding="utf8") as fh:
    json.dump({"preguntas": PREGUNTAS, **R}, fh, ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if k not in ("semanal", "tablero", "nulos_enlaces", "nulos_menciones")}, ensure_ascii=False, indent=1, default=str))
