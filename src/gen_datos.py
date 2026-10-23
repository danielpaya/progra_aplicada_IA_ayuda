"""Generador de DATOS SIMULADOS - Caso Claude (Anthropic): enlaces compartidos que aparecieron en buscadores.
Fines académicos. Los HECHOS del caso (fechas, comunicados) son públicos y están citados en el informe;
las CIFRAS de estas tablas son simuladas con IA y no son datos reales de Anthropic.

Produce 3 libros Excel:
  01 Auditoría simulada de enlaces públicos (muestra de 2.400 enlaces + errores sembrados)
  02 Menciones en redes y tickets de soporte sobre privacidad (jun-sep 2026)
  03 Serie mensual de KPI (abr-2025 a mar-2027, con proyección)
Errores intencionales documentados en la hoja LEEME de cada libro.
Uso: python src/gen_datos.py datos
"""
import sys, random
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
rng = np.random.default_rng(2026)
random.seed(2026)
AVISO = ("DATO SIMULADO – Fines académicos. Caso Claude (Anthropic): enlaces compartidos en buscadores. "
         "Las cifras NO son datos reales de Anthropic. Universidad de La Sabana.")

INCIDENTE_1 = date(2025, 9, 8)    # Google retira ~600 conversaciones indexadas (Forbes, 2025)
INCIDENTE_2 = date(2026, 7, 25)   # publicación en r/ClaudeAI con la búsqueda site:claude.ai/share
CORTE = date(2026, 9, 30)         # fecha de corte de la auditoría simulada


def rdate(a, b):
    return a + timedelta(days=int(rng.integers(0, (b - a).days + 1)))


def pick(opts):
    k, p = zip(*opts.items())
    return k[int(rng.choice(len(k), p=np.array(p) / sum(p)))]


# ================================================================ 1) ENLACES PÚBLICOS (2.400)
PUBLICADO = {"Solo mensajería privada": 78, "Reddit": 5, "X (Twitter)": 5, "Foro o Discord público": 4,
             "Blog o sitio web": 4, "Repositorio GitHub": 4}
P_INDEX = {"Solo mensajería privada": .004, "Reddit": .32, "X (Twitter)": .18, "Foro o Discord público": .25,
           "Blog o sitio web": .40, "Repositorio GitHub": .22}
TEMAS = {"Programación": 30, "Trabajo y documentos": 20, "Escritura creativa": 14, "Educación": 10,
         "Asuntos personales": 8, "Salud": 6, "Finanzas y cripto": 6, "Legal": 6}
SENS = {  # probabilidad de cada tipo de dato sensible según el tema
    "Programación": {"Credenciales, llaves o cripto": .14},
    "Trabajo y documentos": {"Documentos internos de empresa": .45, "Datos personales de contacto": .08},
    "Escritura creativa": {"Datos personales de contacto": .02},
    "Educación": {"Datos de menores de edad": .12, "Datos personales de contacto": .06},
    "Asuntos personales": {"Datos personales de contacto": .40},
    "Salud": {"Datos de salud": .65},
    "Finanzas y cripto": {"Credenciales, llaves o cripto": .45},
    "Legal": {"Datos personales de contacto": .45},
}
NIVEL = {"Credenciales, llaves o cripto": "Alto", "Datos de salud": "Alto", "Datos de menores de edad": "Alto",
         "Datos personales de contacto": "Medio", "Documentos internos de empresa": "Medio", "Ninguno": "Bajo"}
PAISES = {"Estados Unidos": 30, "India": 10, "Reino Unido": 8, "Brasil": 7, "Alemania": 6, "México": 6,
          "España": 5, "Colombia": 5, "Argentina": 4, "Francia": 4, "Otro": 15}

links = []
for i in range(2400):
    tipo = "Artefacto" if rng.random() < .30 else "Conversación"
    pub = pick(PUBLICADO)
    tema = pick(TEMAS)
    s = "Ninguno"
    for k, p in SENS.get(tema, {}).items():
        if rng.random() < p:
            s = k
            break
    creado = rdate(date(2025, 5, 1), date(2026, 7, 20))
    p_idx = P_INDEX[pub] * (1.3 if tipo == "Artefacto" and pub != "Solo mensajería privada" else 1)
    idx = rng.random() < p_idx
    ap = ret = None
    buscador = None
    if idx:
        buscador = pick({"Google": 55, "Bing": 25, "Google y Bing": 15, "Brave": 5})
        if creado < INCIDENTE_1 - timedelta(days=7):            # primer episodio (2025)
            ap = min(creado + timedelta(days=int(rng.gamma(2, 6)) + 2), INCIDENTE_1 - timedelta(days=1))
            ret = INCIDENTE_1 + timedelta(days=int(rng.integers(0, 3)))
        elif creado > INCIDENTE_1:                               # se acumulan hasta el segundo episodio (2026)
            ap = min(creado + timedelta(days=int(rng.integers(2, 21))), INCIDENTE_2 - timedelta(days=1))
            lo, hi = (1, 4) if tipo == "Conversación" else (2, 11)
            ret = INCIDENTE_2 + timedelta(days=int(rng.integers(lo, hi + 1)))
        else:                                                    # creado justo durante el primer retiro: no alcanza a indexarse
            idx, buscador = False, None
    desact = rng.random() < (.37 if idx else .12)
    f_des = None
    if desact:
        f_des = (INCIDENTE_2 + timedelta(days=int(rng.integers(1, 27)))) if idx else rdate(creado, CORTE)
    links.append(dict(
        id_enlace=f"{'AR' if tipo == 'Artefacto' else 'SH'}-{i + 1:05d}", tipo=tipo, fecha_creacion=creado,
        plan=pick({"Free": 52, "Pro": 36, "Max": 12}), pais=pick(PAISES), publicado_en=pub, tema=tema,
        dato_sensible=s, nivel_sensibilidad=NIVEL[s], indexado="Sí" if idx else "No", buscador=buscador,
        fecha_aparicion=ap, fecha_retiro=ret,
        horas_visible=round((ret - ap).days * 24 + float(rng.uniform(-6, 6)), 1) if idx else None,
        desactivado_por_usuario="Sí" if desact else "No", fecha_desactivacion=f_des,
    ))

# errores intencionales
L = links
ix = rng.choice(len(L), 60, replace=False)
for i in ix[:15]:
    L[i]["plan"] = None                                              # vacío
for i in ix[15:27]:
    L[i]["pais"] = None                                              # vacío
for i in ix[27:35]:
    L[i]["fecha_creacion"] = random.choice(["2062-07-25", "2025-02-30", "1999-09-08"])   # imposible
idx_ix = [i for i, r in enumerate(L) if r["indexado"] == "Sí"]
for i in rng.choice(idx_ix, 9, replace=False):
    L[i]["horas_visible"] = -abs(L[i]["horas_visible"])              # negativo (error de signo)
for i in ix[35:42]:
    L[i]["indexado"] = random.choice(["si", "SI ", "S"]) if L[i]["indexado"] == "Sí" else random.choice(["no", "NO "])  # etiqueta inconsistente
dups = [dict(L[i]) for i in rng.choice(len(L), 30, replace=False)]   # 30 duplicados exactos
df_links = pd.DataFrame(L + dups).sample(frac=1, random_state=7).reset_index(drop=True)
for c in ["fecha_creacion", "fecha_aparicion", "fecha_retiro", "fecha_desactivacion"]:
    df_links[c] = df_links[c].map(lambda v: None if v is None or (isinstance(v, float) and np.isnan(v)) else str(v))

# ================================================================ 2) MENCIONES Y SOPORTE (jun-sep 2026)
INI, FIN = date(2026, 6, 1), date(2026, 9, 30)
TIPO_BASE = {"Pregunta general de privacidad": 30, "Solicitud de borrado de datos": 15, "Queja de privacidad": 15,
             "Otro tema (no privacidad)": 40}
TIPO_CRISIS = {"Queja de privacidad": 30, "Solicitud de retiro o desindexación": 20, "Pregunta: ¿mi chat es público?": 22,
               "Cancelación de suscripción": 8, "Defensa: «es comportamiento esperado»": 10, "Consulta de empresa o cumplimiento": 10}
CANAL = {"Reddit": 25, "X (Twitter)": 25, "Soporte (ticket)": 30, "Foro de desarrolladores": 8, "Prensa": 4, "LinkedIn": 8}
RELACION = {"Tenía un enlace indexado": 22, "Compartió, sin indexar": 32, "Nunca compartió": 46}

men = []
d = INI
while d <= FIN:
    t = (d - INCIDENTE_2).days
    lam = 5.5 + (120 * np.exp(-t / 6) if t >= 0 else 0)
    for _ in range(int(rng.poisson(lam))):
        crisis = 0 <= t <= 30
        tipo = pick(TIPO_CRISIS) if (t >= 0 and rng.random() < np.exp(-t / 25)) else pick(TIPO_BASE)
        canal = pick(CANAL)
        if crisis:
            base_s = .2 if tipo.startswith("Defensa") else -.6
        else:
            base_s = -.05 if t < 0 else -.22
        tr = None
        if canal == "Soporte (ticket)":
            tr = round(float(rng.gamma(4, 5 if t < 0 else (15.5 if crisis else 3.8))), 1)
        priv = tipo not in ("Otro tema (no privacidad)",)
        rel = pick(RELACION) if (priv and t >= 0) else ("Nunca compartió" if not priv else pick({"Compartió, sin indexar": 40, "Nunca compartió": 60}))
        men.append(dict(fecha=d, canal=canal, tipo=tipo, plan=pick({"Free": 50, "Pro": 34, "Max": 10, "Team/Enterprise": 6}),
                        pais=pick(PAISES), sentimiento=round(float(np.clip(rng.normal(base_s, .22), -1, 1)), 2),
                        tiempo_respuesta_h=tr, relacion_con_enlaces=rel,
                        estado=random.choice(["Cerrado", "Cerrado", "Cerrado", "En gestión"]) if d < date(2026, 9, 15) else random.choice(["Abierto", "En gestión"])))
    d += timedelta(days=1)
men.sort(key=lambda r: r["fecha"])
for i, r in enumerate(men, 1):
    r["id_mencion"] = f"M-{i:05d}"
men_limpio = [dict(r) for r in men]
ix = rng.choice(len(men), 50, replace=False)
for i in ix[:10]:
    men[i]["canal"] = None                                           # vacío
for i in ix[10:19]:
    men[i]["fecha"] = random.choice(["2026-07-32", "2062-07-25", "2016-07-25"])   # imposible
tk = [i for i, r in enumerate(men) if r["tiempo_respuesta_h"] is not None and i not in ix[:19]]
for i in rng.choice(tk, 6, replace=False):
    men[i]["tiempo_respuesta_h"] = -men[i]["tiempo_respuesta_h"]     # negativo
for i in ix[19:24]:
    men[i]["sentimiento"] = random.choice([3.5, -7.0])                # fuera de la escala -1..1
for i in ix[24:32]:
    men[i]["relacion_con_enlaces"] = "N/D"                            # vacío disfrazado
dups = [dict(men[i]) for i in rng.choice(len(men), 20, replace=False)]
men += dups
cols = ["id_mencion", "fecha", "canal", "tipo", "plan", "pais", "sentimiento", "tiempo_respuesta_h",
        "relacion_con_enlaces", "estado"]
df_men = pd.DataFrame(men)[cols].sample(frac=1, random_state=3).reset_index(drop=True)
df_men["fecha"] = df_men["fecha"].astype(str)

# ================================================================ 3) SERIE KPI (abr-2025 a mar-2027)
meses = pd.period_range("2025-04", "2027-03", freq="M")


def fase(m):
    if m < pd.Period("2025-09", "M"): return "Antes"
    if m == pd.Period("2025-09", "M"): return "Incidente 1"
    if m < pd.Period("2026-07", "M"): return "Entre incidentes"
    if m <= pd.Period("2026-08", "M"): return "Crisis"
    if m == pd.Period("2026-09", "M"): return "Contención"
    return "Plan (proyección)"


# enlaces de la muestra visibles en buscadores durante cada mes (se calcula desde la tabla 1, sin errores)
vis = []
for m in meses:
    a, b = m.start_time.date(), m.end_time.date()
    vis.append(sum(1 for r in links if r["fecha_aparicion"] and r["fecha_aparicion"] <= b and r["fecha_retiro"] >= a))

curve = {  # 24 valores por indicador · abr-25 … mar-27 · simulados
    "indice_confianza_privacidad_0_100": [81, 82, 81, 83, 82, 66, 70, 73, 75, 76, 77, 78, 78, 79, 80, 49, 41, 52, 57, 62, 66, 69, 72, 75],
    "nps":                               [44, 45, 43, 46, 45, 21, 26, 30, 33, 34, 36, 37, 37, 38, 38, -6, -14, -2, 5, 11, 17, 22, 27, 32],
    "pct_usuarios_que_comparten":        [9.8, 10.1, 10.4, 10.9, 11.2, 9.0, 9.6, 10.2, 10.8, 11.1, 11.5, 11.8, 12.0, 12.2, 12.4, 7.1, 6.2, 7.4, 8.3, 9.2, 10.0, 10.7, 11.3, 12.0],
    "pct_paginas_bloqueadas_robots":     [100] * 24,
    "pct_paginas_noindex_legible":       [0] * 18 + [40, 100, 100, 100, 100, 100],
    "tiempo_desindexacion_h":            [None] * 5 + [96] + [None] * 9 + [72, 60, 30, 12, 6, 5, 4, 4, 4],
    "tiempo_respuesta_soporte_h":        [21, 20, 22, 20, 21, 48, 26, 23, 22, 21, 20, 21, 20, 21, 20, 63, 41, 17, 12, 12, 12, 12, 12, 12],
    "pct_enlaces_escaneo_sensibles":     [0] * 18 + [0, 25, 60, 90, 100, 100],
    "pct_mensajes_auditados":            [0] * 15 + [10, 55, 100, 100, 100, 100, 100, 100, 100],
    "ratio_hechos_promesas":             [None] * 15 + [0.4, 0.8, 1.6, 2.0, 2.4, 2.7, 3.0, 3.2, 3.4],
}
# jun-sep 2026: el tiempo de respuesta mensual sale de los tickets simulados del libro 02 (antes de sembrar errores)
for k, m in enumerate(meses):
    if pd.Period("2026-06", "M") <= m <= pd.Period("2026-09", "M"):
        v = [r["tiempo_respuesta_h"] for r in men_limpio if r["tiempo_respuesta_h"] is not None
             and pd.Period(r["fecha"], "M") == m]
        curve["tiempo_respuesta_soporte_h"][k] = round(float(np.median(v)))
df_kpi = pd.DataFrame({"mes": meses.astype(str), "fase": [fase(m) for m in meses],
                       "enlaces_muestra_visibles_en_buscadores": vis, **curve})
df_kpi.loc[df_kpi["fase"] == "Plan (proyección)", "enlaces_muestra_visibles_en_buscadores"] = 0

# ================================================================ escribir
PROMPT_LNK = ("Genera una auditoría simulada de 2.400 enlaces públicos de Claude (conversaciones y artefactos) creados entre "
              "may-2025 y jul-2026, con dónde se publicó cada enlace, tema, dato sensible, si fue indexado, en qué buscador, "
              "fechas de aparición y retiro, y si el usuario lo desactivó. La probabilidad de indexación depende de dónde se "
              "publicó el enlace (robots.txt bloquea el rastreo pero no impide indexar una URL enlazada). Los retiros ocurren "
              "tras los dos episodios públicos (8-sep-2025 y 25-jul-2026). Siembra errores y documéntalos.")
PROMPT_MEN = ("Genera menciones en redes y tickets de soporte simulados sobre privacidad de Claude entre jun y sep de 2026: "
              "volumen base de ~5,5 por día y un pico tras el 25-jul-2026 que decae en unas 6 semanas; tipo, canal, plan, "
              "sentimiento (-1 a 1), tiempo de respuesta para tickets y relación del usuario con los enlaces (si tenía uno "
              "indexado, si compartió sin indexar o si nunca compartió). Siembra errores y documéntalos.")
PROMPT_KPI = ("Genera una serie mensual simulada (abr-2025 a mar-2027) de KPI de confianza, operación y uso para la función "
              "Compartir de Claude, con las fases Antes, Incidente 1, Entre incidentes, Crisis, Contención y Plan (proyección).")


def leeme(prompt, errores, extra=""):
    return pd.DataFrame({"campo": ["AVISO", "Prompt de generación (IA)", "Errores intencionales", "Notas"],
                         "valor": [AVISO, prompt, errores, extra]})


with pd.ExcelWriter(f"{OUT}/01_Auditoria_Enlaces_Compartidos.xlsx") as w:
    leeme(PROMPT_LNK, "30 duplicados exactos; 15 planes vacíos; 12 países vacíos; 8 fechas de creación imposibles "
                      "(p. ej. 2025-02-30); 9 horas visibles negativas; 7 etiquetas inconsistentes en 'indexado' (si, SI, S, no).",
          "Las fechas se guardan como texto a propósito, para conservar las fechas imposibles. Según la prensa, las cuentas "
          "Team y Enterprise no pueden compartir públicamente, por eso la muestra solo incluye Free, Pro y Max."
          ).to_excel(w, sheet_name="LEEME", index=False)
    df_links.to_excel(w, sheet_name="Enlaces", index=False)
with pd.ExcelWriter(f"{OUT}/02_Menciones_y_Soporte_Privacidad.xlsx") as w:
    leeme(PROMPT_MEN, "20 duplicados exactos; 10 canales vacíos; 9 fechas imposibles; 6 tiempos de respuesta negativos; "
                      "5 sentimientos fuera de la escala -1 a 1; 8 relaciones 'N/D'.",
          "tiempo_respuesta_h solo aplica a los tickets de soporte.").to_excel(w, sheet_name="LEEME", index=False)
    df_men.to_excel(w, sheet_name="Menciones", index=False)
with pd.ExcelWriter(f"{OUT}/03_Serie_KPI_24_meses.xlsx") as w:
    leeme(PROMPT_KPI, "Sin errores intencionales.",
          "Oct-2026 a mar-2027 = proyección del plan. 'enlaces_muestra_visibles_en_buscadores' se calcula desde el libro 01. "
          "Indicadores ilustrativos: no son métricas oficiales de Anthropic.").to_excel(w, sheet_name="LEEME", index=False)
    df_kpi.to_excel(w, sheet_name="KPI", index=False)
print("enlaces", len(df_links), "| indexados", sum(r["indexado"] == "Sí" for r in links), "| menciones", len(df_men), "| kpi", len(df_kpi))
