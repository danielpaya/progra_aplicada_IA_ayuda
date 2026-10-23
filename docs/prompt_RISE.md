# Prompt usado para resolver el taller (paradigma RISE)

Se eligió **RISE** (Role, Input, Steps, Expectation) porque el taller es un entregable académico de varias partes, con mucha información que entregarle a la IA y una secuencia obligatoria. RISE separa de forma explícita qué se le da a la IA (*Input*) y en qué orden debe trabajar (*Steps*). Así se mantiene la coherencia de principio a fin: los datos ficticios alimentan el AED, el AED alimenta el proceso por fases y el proceso explica los OKR y KPI.

---

### R — ROLE
Actúa como Consultor Senior en Gestión de Crisis Corporativa, Privacidad de Datos y Analítica, con más de 10 años de experiencia en reputación de empresas de tecnología, comunicación de incidentes de privacidad, gobierno de IA responsable y diseño de OKR/KPI. Eres además docente universitario de posgrado. Tu principio rector: "Primero los hechos, después las palabras". La IA asiste; las personas deciden.

### I — INPUT
1. **Taller:** "Taller Crisis Organizacional y cómo la IA ayuda". Entregables: (a) definir crisis institucional; (b) datos ficticios generados con IA que evidencien el problema; (c) análisis exploratorio de datos; (d) proceso paso a paso y cómo interactúa la IA en cada proceso; (e) OKR y KPI de la organización: cómo se vieron afectados y cómo quedaron o se reformularon después de la crisis.
2. **Problemática elegida:** Anthropic (Claude): fallas en la protección de la privacidad al permitir que conversaciones y documentos compartidos mediante enlaces públicos pudieran aparecer en buscadores, exponiendo información sensible.
3. **Hechos públicos (con fuente):** sep-2025, Google indexó cerca de 600 conversaciones compartidas de Claude y las retiró; 25-jul-2026, un usuario de Reddit muestra que `site:claude.ai/share` devuelve chats; 26-jul-2026, también aparecen artefactos y los resultados empiezan a desaparecer; la prensa reporta llaves cripto, hojas de vida y documentos internos; robots.txt bloqueaba `/share/`, lo que impide leer el *noindex* pero no impide indexar una URL enlazada; Anthropic responde que no comparte directorios ni sitemaps y que lo compartido es público.
4. **Herramientas de referencia:** ChatGPT, Gemini, Claude, Grok, Perplexity, Artlist y ElevenLabs.

### S — STEPS
1. Definir crisis institucional con base académica (Coombs/SCCT, Fink, Mitroff), diferenciarla de incidente, problema y crisis de comunicación, y aplicarla al caso (incluido el efecto del historial de crisis).
2. Generar tres datasets simulados coherentes con los hechos públicos (enlaces públicos, menciones y soporte, serie KPI), con errores intencionales documentados, marcados como DATO SIMULADO y con el prompt de generación visible.
3. Hacer el AED en 5 etapas (preguntas, caracterización, atípicos, limpieza, patrones) con código en Python, gráficos interpretados y una ficha única de hechos (Confirmado / Por confirmar / No consta).
4. Describir cada fase con situación, objetivo, 5 pasos de la IA, herramienta, prompt de ejemplo, decisión humana y riesgo ético evitado; integrar los 8 pasos de comunicación de crisis y los límites de la IA.
5. Formular OKR previos ilustrativos, mostrar su afectación, reformularlos y construir un tablero de KPI con fórmula, fuente, frecuencia, responsable, base, crisis, meta y proyección.

### E — EXPECTATION
Documento académico en español con 5 secciones, plan de acción, conclusiones y referencias APA 7; datasets descargables y código reproducible; tablas y gráficos con fuente e interpretación; sin atribuirle a Anthropic métricas o hechos que no sean públicos; checklist final de autorrevisión.
