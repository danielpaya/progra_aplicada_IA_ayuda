"""Genera presentacion/assets/data.js desde los resultados del AED y la serie KPI (DATOS SIMULADOS).
Uso: python src/build_data_js.py
Así las cifras de las diapositivas salen de los datos y no se escriben a mano.
"""
import json
import pandas as pd

R = json.load(open("resultados/figuras/resultados_aed.json", encoding="utf8"))
kpi = pd.read_excel("datos/03_Serie_KPI_24_meses.xlsx", sheet_name="KPI")
kpi = kpi.astype(object).where(pd.notna(kpi), None)

ROWS = ["Blog o sitio web", "Reddit", "Foro o Discord público", "Repositorio GitHub", "X (Twitter)", "Solo mensajería privada"]
COLS = ["Conversación", "Artefacto"]
heat = {"rows": ROWS, "cols": COLS,
        "pct": [[R["pct_indexado_publicacion_tipo"][f"{r} · {c}"] for c in COLS] for r in ROWS],
        "n": [[R["n_publicacion_tipo"][f"{r} · {c}"] for c in COLS] for r in ROWS]}
DATA = {
    "semanas": R["semanal"],
    "heat": heat,
    "contagio": R["contagio"],
    "sensibles": R["sensibles_por_tipo"],
    "resumen": {k: R[k] for k in ["indexados", "indexados_con_sensibles", "pct_indexados_activos_hoy", "multiplicador_pico",
                                  "pico_semanal", "promedio_semanal_previo", "pct_sin_enlace_expuesto", "pct_nunca_compartio",
                                  "indexados_publicados_por_usuario_pct", "dias_visibles_mediana", "limpio", "bruto"]},
    "periodos": R["periodos"],
    "confianza": [{"m": r["mes"], "v": r["indice_confianza_privacidad_0_100"], "fase": r["fase"]} for r in kpi.to_dict("records")],
    "kpi": kpi.to_dict("records"),
}
with open("presentacion/assets/data.js", "w", encoding="utf8") as f:
    f.write("// Generado por src/build_data_js.py desde resultados/figuras/resultados_aed.json y datos/03_Serie_KPI_24_meses.xlsx (DATOS SIMULADOS)\n")
    f.write("window.DATA = " + json.dumps(DATA, ensure_ascii=False, default=str) + ";\n")
print("data.js ok ·", len(DATA["kpi"]), "meses ·", len(DATA["semanas"]), "semanas")
