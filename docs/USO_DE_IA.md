# Bitácora de uso de inteligencia artificial

El taller pide que los datos ficticios «se hagan con la IA». Este registro muestra qué hizo la IA en cada etapa y qué revisó el equipo. Se usó un asistente de IA conversacional (Claude, de Anthropic) como herramienta de trabajo. Las decisiones de enfoque, narrativa y contenido final son del equipo.

| Etapa | Qué hizo la IA | Evidencia en el repositorio | Qué revisó y decidió el equipo |
| --- | --- | --- | --- |
| 1. Lectura del caso | Extrajo los hechos, las cifras y las restricciones de la presentación del caso y sus notas | Informe §1 y §2 · ficha de hechos (§3.6) | Que no se inventaran causas, agentes ni número de afectados |
| 2. Planeación | Redactó un prompt estructurado con el paradigma RISE para resolver los 5 entregables | `docs/prompt_RISE.md` | El paradigma elegido y el alcance del taller |
| 3. Datos ficticios | Escribió el generador de los 3 datasets con las cifras ancla del caso y errores sembrados a propósito | `src/gen_datos.py` · hoja LEEME de cada Excel (con el prompt de generación) | Que las cifras cuadraran con el caso (1.025 PQR, 216 lotes, 1.307 controles, 64 reportes del lote 047) |
| 4. Análisis exploratorio | Escribió el script de limpieza, detección de atípicos (IQR), patrones y figuras | `src/aed_alimenta_familia.py` · `resultados/figuras/` | Las 5 preguntas del análisis y la interpretación de cada patrón |
| 5. Informe | Redactó el borrador por secciones y verificó las cifras contra los datos | `informe/` | El contenido, las conclusiones y el plan de acción |
| 6. Presentación | Construyó la presentación en HTML, CSS y JavaScript y el guion por expositor | `index.html` · `presentacion/` | El orden de los expositores, el enfoque de consultoría, el estilo visual y las correcciones de diseño |
| 7. Auditoría | Revisó la entrega completa: cifras, citas APA, restricciones del caso y coherencia | — | Qué correcciones aplicar antes de entregar |

## Cómo verificar que los datos salen del código generado

```bash
pip install -r requirements.txt
python src/gen_datos.py datos                                # mismos datos siempre (semilla 2026)
python src/aed_alimenta_familia.py datos resultados/figuras  # mismas cifras del informe
```

## Reglas que seguimos

- Todo dato numérico está marcado como **simulado**.
- Lo que el caso no informa se marca como **«no consta»**.
- La IA preparó borradores, código y verificaciones; las personas del equipo decidieron qué se entrega y qué se dice.
