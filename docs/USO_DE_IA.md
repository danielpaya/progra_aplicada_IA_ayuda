# Bitácora de uso de inteligencia artificial

El taller pide que los datos ficticios «se hagan con la IA». Este registro muestra qué hizo la IA en cada etapa y qué revisó el equipo. Se usó un asistente de IA conversacional (Claude, de Anthropic) como herramienta de trabajo. Que el asistente sea de la misma empresa del caso no cambia el análisis: los hechos salen de fuentes de prensa citadas y las cifras son simuladas y están marcadas como tales. Las decisiones de enfoque, narrativa y contenido final son del equipo.

| Etapa | Qué hizo la IA | Evidencia en el repositorio | Qué revisó y decidió el equipo |
| --- | --- | --- | --- |
| 1. Investigación del caso | Buscó y resumió las fuentes públicas sobre los dos episodios (sep-2025 y jul-2026) y la documentación de Google sobre robots.txt | Informe, «Qué pasó» y Referencias | Usar solo hechos con fuente y marcar lo demás como «no consta» |
| 2. Planeación | Redactó un prompt estructurado con el paradigma RISE para resolver los 5 entregables | `docs/prompt_RISE.md` | El paradigma elegido y el alcance del taller |
| 3. Datos ficticios | Escribió el generador de los 3 datasets, coherente con los hechos públicos y con errores sembrados a propósito | `src/gen_datos.py` · hoja LEEME de cada Excel (con el prompt de generación) | Que ninguna cifra simulada se presente como dato real de Anthropic |
| 4. Análisis exploratorio | Escribió el script de limpieza, detección de atípicos (IQR), patrones y figuras | `src/aed_claude_enlaces.py` · `resultados/figuras/` | Las 5 preguntas del análisis y la interpretación de cada patrón |
| 5. Informe | Redactó el borrador por secciones y verificó las cifras contra los datos | `informe/` | El contenido, las conclusiones y el plan de acción |
| 6. Presentación | Construyó la presentación en HTML, CSS y JavaScript; las cifras salen de los datos con `src/build_data_js.py` | `index.html` · `presentacion/` | El orden de los expositores, el enfoque de propuesta y el estilo visual |
| 7. Verificación | Cruzó las cifras del informe, la presentación y los datos, y revisó cada diapositiva | — | Qué correcciones aplicar antes de entregar |

## Cómo verificar que los datos salen del código generado

```bash
pip install -r requirements.txt
python src/gen_datos.py datos                               # mismos datos siempre (semilla 2026)
python src/aed_claude_enlaces.py datos resultados/figuras   # mismas cifras del informe
python src/build_data_js.py                                 # mismas cifras de la presentación
```

## Reglas que seguimos

- Los hechos públicos van con su fuente; todo dato numérico interno está marcado como **simulado**.
- No le atribuimos a Anthropic ninguna métrica, OKR ni decisión que no sea pública. Los OKR «de antes» son ilustrativos.
- Lo que no consta en fuentes públicas se marca como **«no consta»**.
- La IA preparó borradores, código y verificaciones; las personas del equipo decidieron qué se entrega y qué se dice.
