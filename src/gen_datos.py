"""Generador de DATOS SIMULADOS - Caso Alimenta Familia (fines académicos).
Produce 3 libros Excel coherentes con las cifras ancla del caso:
  PQR 1.025 registros brutos | 216 lotes | 1.307 controles brutos | lote VEG-BP-2026-047 con 64 reportes únicos de salud.
Errores intencionales documentados en la hoja LEEME de cada libro.
"""
import sys, random
from datetime import date, timedelta
import numpy as np
import pandas as pd

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
rng = np.random.default_rng(2026)
random.seed(2026)
AVISO = "DATO SIMULADO – Fines académicos. Caso Alimenta Familia (Universidad de La Sabana)."

CRISIS = date(2026, 4, 14)          # noche de la crisis
LOTE_CRITICO = "VEG-BP-2026-047"

# ---------------------------------------------------------------- productos
VEG = {"BP": "Bebida proteica vegana", "GA": "Galletas veganas de avena", "HA": "Hamburguesa vegetal",
       "YO": "Yogur vegetal de coco", "LE": "Bebida de almendras", "QU": "Queso vegetal",
       "BA": "Barra de cereal vegana", "MA": "Mayonesa vegana", "PA": "Pan integral vegano",
       "CH": "Chocolate vegano"}
OTR = {("LAC", "LE"): "Leche entera", ("LAC", "QC"): "Queso campesino", ("LAC", "KU"): "Kumis",
       ("PAN", "TA"): "Tostadas", ("PAN", "PT"): "Pan tajado", ("CER", "GR"): "Granola",
       ("CER", "AV"): "Avena en hojuelas", ("CER", "AR"): "Arepas de maíz"}
PLANTAS = ["Planta Chía", "Planta Funza", "Planta Rionegro"]
TURNOS = ["Mañana", "Tarde", "Noche"]
PROV = ["Proteínas del Sur S.A.S.", "Agroinsumos Sabana", "Cooperativa Campo Vivo",
        "Molinos del Valle", "Lácteos La Pradera", "Frutos Secos Andinos"]
CEDI = ["CEDI Bogotá", "CEDI Medellín", "CEDI Bucaramanga", "CEDI Cali", "CEDI Barranquilla"]
DISTR = ["Distribuidora El Ahorro", "Supermercados La Canasta", "Mayorista Central",
         "Tiendas Barrio Unido", "Cadena Mercafamilia", "Minimercados Asociados"]

def rdate(a, b):
    return a + timedelta(days=int(rng.integers(0, (b - a).days + 1)))

# ---------------------------------------------------------------- 216 lotes
lotes = []
for k, nom in VEG.items():                       # 10 productos x 12 lotes = 120
    start = 40 if k == "BP" else int(rng.integers(10, 60))
    for j in range(12):
        lotes.append(dict(lote=f"VEG-{k}-2026-{start + j:03d}", producto=nom, linea="Vegana"))
for (ln, k), nom in OTR.items():                 # 8 productos x 12 lotes = 96
    start = int(rng.integers(100, 300))
    for j in range(12):
        lotes.append(dict(lote=f"{ln}-{k}-2026-{start + j:03d}", producto=nom,
                          linea={"LAC": "Lácteos", "PAN": "Panadería", "CER": "Cereales"}[ln]))
assert len(lotes) == 216
for L in lotes:
    L["fecha_produccion"] = rdate(date(2026, 1, 5), date(2026, 6, 30))
    L["planta"] = random.choice(PLANTAS)
    L["turno"] = random.choice(TURNOS)
    L["proveedor_principal"] = random.choice(PROV)
    L["cedi"] = random.choice(CEDI)
    L["distribuidor"] = random.choice(DISTR)
    L["unidades"] = int(rng.integers(4000, 18000))
# anclas del caso
fix = {
    "VEG-BP-2026-046": dict(fecha_produccion=date(2026, 3, 30), planta="Planta Chía", turno="Tarde"),
    "VEG-BP-2026-047": dict(fecha_produccion=date(2026, 4, 2), planta="Planta Chía", turno="Noche",
                             proveedor_principal="Proteínas del Sur S.A.S.", cedi="CEDI Bogotá", unidades=12600),
    "VEG-BP-2026-048": dict(fecha_produccion=date(2026, 4, 6), planta="Planta Chía", turno="Mañana"),
}
ga = [L for L in lotes if L["lote"].startswith("VEG-GA")][-1]   # lote de la "segunda prueba"
ga.update(fecha_produccion=date(2026, 5, 16), planta="Planta Chía", turno="Noche", cedi="CEDI Bucaramanga",
          distribuidor="Minimercados Asociados")
LOTE_GA = ga["lote"]
for L in lotes:
    if L["lote"] in fix:
        L.update(fix[L["lote"]])
    # garantizar sesgo: los lotes BP 040-051 salen de Chía, la línea crítica
    L["fecha_despacho"] = L["fecha_produccion"] + timedelta(days=int(rng.integers(2, 9)))
ga["fecha_despacho"] = date(2026, 5, 21)
ga["fecha_recibo_tienda"] = date(2026, 5, 27)
for L in lotes:
    L.setdefault("fecha_recibo_tienda", L["fecha_despacho"] + timedelta(days=int(rng.integers(2, 7))))

OTROS = ["VEG-BP-2026-046", "VEG-BP-2026-048", "VEG-BP-2026-049"] + [L["lote"] for L in lotes if L["linea"] == "Vegana" and not L["lote"].startswith("VEG-BP")][:20]
PROTEGIDOS = set(OTROS) | {LOTE_CRITICO, LOTE_GA}
# ---------------------------------------------------------------- 1.307 controles
CONTROLES = [("Bacillus cereus", "UFC/g", 0, 100), ("Salmonella spp.", "presencia/25g", 0, 0),
             ("Alérgenos (trazas leche/huevo)", "ppm", 0, 5),
             ("Composición declarada (proteína)", "g/100g", None, None),
             ("Humedad / pH", "%", 0, 12), ("Etiquetado", "check", None, None)]
RESP = ["Analista A. Rojas", "Analista M. Pardo", "Analista J. Gómez", "Lab. externo BioAndes"]
ctrl = []
cid = 1
for L in lotes:
    fp = L["fecha_produccion"]
    pre = fp < CRISIS
    riesgo = 0.14 if (pre and L["planta"] == "Planta Chía" and L["turno"] == "Noche") else (0.025 if pre else 0.0)
    for (c, u, lo, hi) in CONTROLES:
        res, val = "Conforme", None
        if c == "Bacillus cereus":
            val = float(rng.integers(5, 60))
        elif c == "Salmonella spp.":
            val = 0.0
        elif c.startswith("Alérgenos"):
            val = round(float(rng.uniform(0, 2.5)), 2)
        elif c.startswith("Composición"):
            decl = 20.0 if "BP" in L["lote"] else 8.0
            val = round(decl * float(rng.normal(1, 0.025)), 2)
        elif c.startswith("Humedad"):
            val = round(float(rng.uniform(3, 9)), 2)
        if rng.random() < riesgo:
            res, val = "No realizado", None
        elif rng.random() < 0.015:
            res = "No conforme"
        ctrl.append(dict(id_control=f"C{cid:05d}", lote=L["lote"], control=c, unidad=u, valor_medido=val,
                         resultado=res, fecha_control=fp + timedelta(days=int(rng.integers(0, 3))),
                         responsable=random.choice(RESP)))
        cid += 1
# lote crítico: controles omitidos + composición no conforme
for r in ctrl:
    if r["lote"] == LOTE_CRITICO:
        if r["control"] in ("Bacillus cereus", "Alérgenos (trazas leche/huevo)"):
            r.update(resultado="No realizado", valor_medido=None)
        elif r["control"].startswith("Composición"):
            r.update(resultado="No conforme", valor_medido=14.2)
        else:
            r["resultado"] = "Conforme"
    if r["lote"] in PROTEGIDOS and r["lote"] != LOTE_CRITICO:
        if r["resultado"] != "Conforme":
            r["resultado"] = "Conforme"
            if r["valor_medido"] is None and not r["control"] in ("Etiquetado",):
                r["valor_medido"] = 20.1 if r["control"].startswith("Comp") else 1.0
assert len(ctrl) == 1296
# errores intencionales
idx = rng.choice([i for i, r in enumerate(ctrl) if r["lote"] not in PROTEGIDOS], 18, replace=False)
for i in idx[:9]:
    ctrl[i]["resultado"] = None                                         # vacío
for i in idx[9:14]:
    L = next(l for l in lotes if l["lote"] == ctrl[i]["lote"])
    ctrl[i]["fecha_control"] = L["fecha_produccion"] - timedelta(days=int(rng.integers(20, 60)))  # imposible
for i in idx[14:18]:
    ctrl[i]["valor_medido"] = random.choice([-3.5, 999.0])              # fuera de rango
dups = [dict(ctrl[i]) for i in rng.choice(len(ctrl), 11, replace=False)]  # duplicados exactos
ctrl += dups
assert len(ctrl) == 1307
df_ctrl = pd.DataFrame(ctrl).sample(frac=1, random_state=7).reset_index(drop=True)
df_lotes = pd.DataFrame(lotes)

# ---------------------------------------------------------------- 1.025 PQR
CIUD = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Chía", "Pereira", "Cartagena"]
CANAL = ["Línea de atención", "Correo", "WhatsApp", "Redes sociales", "Web", "Punto de venta"]
prod_of = {L["lote"]: (L["producto"], L["linea"]) for L in lotes}
all_prod = [(n, "Vegana") for n in VEG.values()] + [(n, {"LAC": "Lácteos", "PAN": "Panadería", "CER": "Cereales"}[k[0]]) for k, n in OTR.items()]

def fecha_pqr(tipo):
    """Fechas 2026-01-02 a 2026-09-30 con pico posterior a la crisis."""
    if tipo in ("Etiquetado", "Consulta de seguridad", "Rumor / desinformación") and rng.random() < 0.75:
        return CRISIS + timedelta(days=int(abs(rng.normal(0, 18))))
    return rdate(date(2026, 1, 2), date(2026, 9, 30))

def t_resp(f):
    if f < CRISIS:
        return round(float(rng.gamma(4, 7)), 1)          # ~28 h
    if f < CRISIS + timedelta(days=60):
        return round(float(rng.gamma(5, 14)), 1)         # ~70 h
    return round(float(rng.gamma(4, 4)), 1)              # ~16 h

def sent(f, tipo):
    base = -0.1 if f < CRISIS else (-0.65 if f < CRISIS + timedelta(days=60) else -0.25)
    if tipo == "Salud":
        base -= 0.2
    return round(float(np.clip(rng.normal(base, 0.2), -1, 1)), 2)

pqr = []
def add(tipo, lote=None, f=None, sev=None, desc="", prod=None):
    if lote:
        prod = prod_of[lote]
    prod = prod or random.choice(all_prod)
    f = f or fecha_pqr(tipo)
    pqr.append(dict(fecha=f, canal=random.choice(CANAL), ciudad=random.choice(CIUD), producto=prod[0],
                    linea=prod[1], lote=lote, tipo=tipo,
                    severidad=sev or int(rng.integers(1, 4)), descripcion=desc,
                    estado=None, tiempo_respuesta_h=t_resp(f), sentimiento=sent(f, tipo)))

SINT = ["náuseas", "vómito", "dolor abdominal", "diarrea", "reacción alérgica leve", "malestar general"]
# 64 reportes únicos de salud del lote crítico
for _ in range(64):
    f = CRISIS + timedelta(days=int(np.clip(rng.gamma(2, 4) - 2, -2, 26)))
    add("Salud", LOTE_CRITICO, f, int(rng.choice([3, 4, 5], p=[.45, .4, .15])),
        f"Reporta {random.choice(SINT)} tras consumir la bebida proteica")
# 23 reportes de salud que mencionan otros lotes sin respaldo de laboratorio
otros = OTROS
for i in range(23):
    lt = otros[i % 3] if i < 12 else random.choice(otros[3:])
    add("Salud", lt, CRISIS + timedelta(days=int(rng.integers(0, 40))), int(rng.choice([2, 3, 4])),
        f"Menciona {random.choice(SINT)}; no hay muestra analizada")
# 14 reportes de salud previos/independientes, leves
for _ in range(14):
    add("Salud", None, None, int(rng.choice([1, 2, 3])), "Malestar leve, sin lote identificado")
# segunda prueba (15-ago)
add("Salud", LOTE_GA, date(2026, 8, 15), 2, "Malestar leve tras comer galletas veganas; pregunta si su lote está bien")
# resto
dist = {"Etiquetado": 118, "Calidad sensorial": 250, "Empaque": 140, "Consulta de seguridad": 210,
        "Rumor / desinformación": 46, "Felicitación": 41, "Disponibilidad en tienda": 93}
DESC = {"Etiquetado": "Duda sobre cantidades declaradas en la etiqueta",
        "Calidad sensorial": "Sabor o textura diferente a lo habitual", "Empaque": "Empaque defectuoso o abierto",
        "Consulta de seguridad": "Pregunta si los demás productos son seguros",
        "Rumor / desinformación": "Comparte documento que circula en redes",
        "Felicitación": "Felicita por la atención recibida", "Disponibilidad en tienda": "No encuentra la línea vegana"}
for t, n in dist.items():
    for _ in range(n):
        lote = random.choice([L["lote"] for L in lotes]) if rng.random() < 0.55 else None
        add(t, lote, None, 1 if t == "Felicitación" else None, DESC[t])
assert len(pqr) == 1000, len(pqr)
for p in pqr:
    p["estado"] = random.choice(["Cerrado", "Cerrado", "Cerrado", "En gestión"]) if p["fecha"] < date(2026, 9, 1) else random.choice(["Abierto", "En gestión"])
pqr.sort(key=lambda p: p["fecha"])
for i, p in enumerate(pqr, 1):
    p["id_pqr"] = f"PQR-{i:05d}"
# errores intencionales
ix = rng.choice([i for i, p in enumerate(pqr) if p["tipo"] != "Salud"], 70, replace=False)
for i in ix[:12]:
    pqr[i]["ciudad"] = None
for i in ix[12:20]:
    pqr[i]["canal"] = None
for i in ix[20:26]:
    pqr[i]["fecha"] = random.choice(["2062-04-15", "1999-04-14", "2026-13-02"])   # imposibles
for i in ix[26:33]:
    pqr[i]["tiempo_respuesta_h"] = -abs(pqr[i]["tiempo_respuesta_h"])            # negativo
for i in ix[33:38]:
    pqr[i]["severidad"] = 9                                                      # escala 1-5
for i in ix[38:48]:
    if pqr[i]["tipo"] != "Salud":
        pqr[i]["lote"] = "N/D"                                                   # vacío disfrazado
dup_src = [i for i in range(len(pqr)) if pqr[i]["lote"] == LOTE_CRITICO][:9] + list(rng.choice([i for i, p in enumerate(pqr) if p["tipo"] != "Salud"], 16, replace=False))
dups = [dict(pqr[i]) for i in dup_src]                                           # 25 duplicados (mismo id)
pqr += dups
assert len(pqr) == 1025
cols = ["id_pqr", "fecha", "canal", "ciudad", "producto", "linea", "lote", "tipo", "severidad", "descripcion",
        "estado", "tiempo_respuesta_h", "sentimiento"]
df_pqr = pd.DataFrame(pqr)[cols].sample(frac=1, random_state=3).reset_index(drop=True)
df_pqr["fecha"] = df_pqr["fecha"].astype(str)

# ---------------------------------------------------------------- serie KPI 18 meses
meses = pd.period_range("2025-10", "2027-03", freq="M")
def fase(m):
    if m < pd.Period("2026-04", "M"): return "Antes"
    if m <= pd.Period("2026-06", "M"): return "Crisis"
    if m <= pd.Period("2026-09", "M"): return "Recuperación"
    return "Recuperación (proyección)"
curve = {  # valores por mes, simulados
    "indice_confianza_0_100":    [78,79,78,80,79,80, 41,38,45, 52,57,61, 64,67,69,71,73,75],
    "sentimiento_neto_pct":      [34,36,33,35,37,36,-48,-55,-31,-18,-6,3, 9,14,18,21,24,27],
    "nps":                       [46,47,45,48,47,49,-12,-18,-5, 8,15,21, 25,29,32,35,37,40],
    "ventas_linea_vegana_mm_cop":[0,0,0,0,180,410, 120,60,95, 150,210,265, 300,330,360,385,405,430],
    "pct_controles_realizados":  [96.8,97.1,96.5,96.9,97.2,96.4, 99.1,100,100, 100,100,100, 100,100,100,100,100,100],
    "tiempo_rastreo_lote_h":     [72,72,70,72,74,72, 60,36,20, 12,8,6, 5,5,4,4,4,4],
    "tiempo_respuesta_pqr_h":    [29,28,30,27,28,29, 71,74,52, 31,22,17, 15,14,13,12,12,12],
    "pct_distribuidores_activos":[100,100,100,100,100,100, 72,58,61, 70,79,85, 88,90,92,94,95,96],
    "pct_mensajes_auditados":    [0,0,0,0,0,0, 40,95,100, 100,100,100, 100,100,100,100,100,100],
    "ratio_hechos_promesas":     [None]*6 + [0.6,0.9,1.3, 1.5,2.1,2.6, 2.8,3.0,3.1,3.2,3.3,3.4],
    "recompra_pct":              [41,42,41,43,42,43, 22,19,24, 28,31,34, 36,37,38,39,40,41],
}
df_kpi = pd.DataFrame({"mes": meses.astype(str), "fase": [fase(m) for m in meses], **curve})
df_kpi.loc[df_kpi["ventas_linea_vegana_mm_cop"] == 0, "ventas_linea_vegana_mm_cop"] = None  # línea lanzada feb-26

# ---------------------------------------------------------------- escribir
PROMPT_PQR = ("Genera un dataset simulado de 1.025 PQR de Alimenta Familia (ene-sep 2026) con las columnas indicadas; "
              "incluye 64 reportes únicos de salud del lote VEG-BP-2026-047 concentrados tras el 14-abr-2026, 23 reportes "
              "de salud que mencionan otros lotes sin respaldo de laboratorio, y errores intencionales documentados "
              "(25 duplicados, vacíos, fechas imposibles, tiempos negativos, severidad fuera de escala).")
PROMPT_TRZ = ("Genera la trazabilidad simulada de 216 lotes (10 productos veganos y 8 de otras líneas) y 1.307 registros de "
              "control de calidad (6 controles por lote + 11 duplicados). El lote VEG-BP-2026-047 (Planta Chía, turno noche) "
              "tiene Bacillus cereus y alérgenos 'No realizado' y la proteína declarada 20 g frente a 14,2 g medidos. Los lotes "
              "046 y 048 son conformes. Incluye resultados vacíos, fechas de control previas a la producción y valores fuera de rango.")
PROMPT_KPI = ("Genera una serie mensual simulada de 18 meses (oct-2025 a mar-2027) con los KPI de confianza, operación y "
              "comercial de Alimenta Familia, marcando las fases Antes, Crisis (abr-jun 2026) y Recuperación.")

def leeme(prompt, errores):
    return pd.DataFrame({"campo": ["AVISO", "Prompt de generación (IA)", "Errores intencionales"],
                         "valor": [AVISO, prompt, errores]})

with pd.ExcelWriter(f"{OUT}/01_Registro_PQR_y_Reclamos_Alimenta_Familia.xlsx") as w:
    leeme(PROMPT_PQR, "25 duplicados exactos; 12 ciudades vacías; 8 canales vacíos; 10 lotes 'N/D'; 6 fechas imposibles; "
                      "7 tiempos de respuesta negativos; 5 severidades = 9 (escala 1-5). La columna fecha se guarda como texto a propósito, para conservar las fechas imposibles (p. ej. 2026-13-02).").to_excel(w, sheet_name="LEEME", index=False)
    df_pqr.to_excel(w, sheet_name="PQR", index=False)
with pd.ExcelWriter(f"{OUT}/02_Trazabilidad_de_Lotes_y_Controles_de_Calidad.xlsx") as w:
    leeme(PROMPT_TRZ, "11 controles duplicados; 9 resultados vacíos; 5 fechas de control anteriores a la producción; "
                      "4 valores medidos fuera de rango (-3,5 o 999).").to_excel(w, sheet_name="LEEME", index=False)
    df_lotes.to_excel(w, sheet_name="Lotes", index=False)
    df_ctrl.to_excel(w, sheet_name="Controles", index=False)
with pd.ExcelWriter(f"{OUT}/03_Serie_KPI_18_meses.xlsx") as w:
    leeme(PROMPT_KPI, "Sin errores intencionales. Oct-2026 a mar-2027 = proyección simulada.").to_excel(w, sheet_name="LEEME", index=False)
    df_kpi.to_excel(w, sheet_name="KPI", index=False)
print("PQR", len(df_pqr), "| lotes", len(df_lotes), "| controles", len(df_ctrl), "| kpi", len(df_kpi), "| lote GA", LOTE_GA)
