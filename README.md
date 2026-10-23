# Taller: Crisis organizacional y cómo la IA ayuda

**Caso Claude (Anthropic): conversaciones compartidas que aparecieron en buscadores** · Programación aplicada · Universidad de La Sabana · Octubre de 2026

**Equipo:** Camilo Andres Alvarez Penate · Valery Andrea Gomez Torres · Mateo Laguna Sanchez · Laura Sofia Noy Nino · Daniel Felipe Pallares Kelin  
**Docente:** Julian Obando Scarpetta

> ⚠️ Los **hechos** del caso son públicos y están citados en el informe. Las **cifras** de este repositorio son **simuladas con fines académicos**: se generaron con IA de forma coherente con esos hechos y **no son datos reales de Anthropic**. Trabajo académico, no afiliado a Anthropic.

## La problemática

Anthropic (Claude): fallas en la protección de la privacidad al permitir que conversaciones y documentos compartidos mediante enlaces públicos pudieran aparecer en buscadores, exponiendo información sensible. Pasó en septiembre de 2025 (cerca de 600 conversaciones) y otra vez en julio de 2026, esta vez con artefactos incluidos.

## Qué contiene

| Entregable del taller | Dónde está |
| --- | --- |
| 1. Definir crisis institucional | [`informe/`](informe/), sección 1 |
| 2. Datos ficticios hechos con IA que evidencian el problema | [`datos/`](datos/) (3 libros Excel) + [`src/gen_datos.py`](src/gen_datos.py) + bitácora [`docs/USO_DE_IA.md`](docs/USO_DE_IA.md) |
| 3. Análisis exploratorio de datos | [`src/aed_claude_enlaces.py`](src/aed_claude_enlaces.py) + [`resultados/figuras/`](resultados/figuras/) + informe, sección 3 |
| 4. Proceso paso a paso y cómo interactúa la IA | Informe, sección 4 |
| 5. OKR y KPI antes, durante y después | [`datos/03_Serie_KPI_24_meses.xlsx`](datos/) + informe, secciones 5 y 6 (plan de acción) |
| Exposición | [`index.html`](index.html) (raíz, lista para GitHub Pages) + [`presentacion/GUION.md`](presentacion/GUION.md) |

```
├── datos/                 01 Enlaces (2.430) · 02 Menciones y soporte (1.428) · 03 KPI (24 meses)
├── src/                   gen_datos.py (genera los datos) · aed_claude_enlaces.py (análisis + figuras) · build_data_js.py (cifras de la presentación)
├── resultados/figuras/    8 figuras PNG + resultados_aed.json
├── informe/               Informe en PDF, Word y Markdown
├── index.html             La presentación (se abre directo en GitHub Pages)
├── presentacion/          Estilos, código, datos y fuentes de la presentación + guion de los expositores
├── docs/                  Prompt RISE, bitácora de uso de IA y auditoría de la presentación
└── LICENSE                MIT (código) · datos simulados con fines académicos
```

## Cómo reproducir los datos y el análisis

Requiere Python 3.10 o superior.

```bash
pip install -r requirements.txt
python src/gen_datos.py datos                               # regenera los 3 Excel (semilla 2026: siempre los mismos datos)
python src/aed_claude_enlaces.py datos resultados/figuras   # limpieza, patrones y figuras
python src/build_data_js.py                                 # actualiza las cifras de la presentación
```

Cada libro Excel tiene una hoja **LEEME** con el prompt usado para generarlo y la lista de errores sembrados a propósito (duplicados, vacíos, fechas imposibles, valores fuera de rango y etiquetas inconsistentes).

## Cómo usar la presentación

La exposición es una **propuesta académica a la dirección de Anthropic**, con estilo de collage editorial: 43 diapositivas de una sola idea cada una, animadas y con revelación por pasos. El sello del pie de cada diapositiva indica si muestra un **hecho público**, un **dato simulado** o una **propuesta del equipo**.

Abre `index.html` (en la raíz) en Chrome o Edge. **Funciona sin internet**: las fuentes vienen incluidas en `presentacion/assets/fonts/`.

**GitHub Pages:** en el repositorio ve a *Settings → Pages*, elige *Deploy from a branch*, la rama `main` y la carpeta `/ (root)`. La presentación queda en `https://<usuario>.github.io/<repositorio>/`. El archivo `.nojekyll` evita que GitHub procese los archivos.

| Tecla | Acción |
| --- | --- |
| `→` `Espacio` | Avanza; si la diapositiva tiene pasos, primero los revela uno por uno |
| `←` | Retrocede (deshace los pasos uno a uno) |
| `1` a `5` | Saltar a Camilo, Daniel, Laura, Mateo o Valery |
| `D` | Mostrar u ocultar el **anexo de datos simulados** (también con el botón **▤ Datos**) |
| `N` | Notas del expositor: qué decir, cuándo pulsar [→] y quién sigue |
| `L` | Tema noche, si el proyector se ve lavado |
| `O` · `F` | Vista general · pantalla completa |
| `T` / `R` | Cronómetro / reiniciar |

Los controles aparecen arriba a la izquierda al mover el mouse.

### Anexo de datos simulados (opcional)

Son 8 diapositivas que explican cómo se generaron y limpiaron los datos con IA. Están **ocultas por defecto**: no cuentan en la numeración ni en la navegación, y no tienen un expositor asignado (las puede presentar cualquiera). Para mostrarlas, usa el botón azul **▤ Anexo** de la diapositiva de cierre, el botón **▤ Datos** de los controles o la tecla `D`. La elección se recuerda entre aperturas. También se puede abrir directo con `index.html?anexo=1`.

### Reparto de la exposición (≈ 18–20 min)

| Expositor | Diapositivas | Rol en la historia |
| --- | --- | --- |
| **Camilo** | 1–13 | Abre y presenta **el problema**: qué pasó, por qué es una crisis institucional y la causa raíz |
| Daniel | 14–20 | **Diagnóstico** con datos: pico de quejas, colapso del soporte, datos sensibles y contagio |
| Laura | 21–28 | **La solución**: Compartir con Privacidad Verificable, cómo funciona y qué errores evita |
| Mateo | 29–36 | **Acciones críticas**: priorización, acción 1, hoja de ruta de 90 días y simulacro |
| Valery | 37–43 | **Resultados**: nuevos OKR, confianza, uso de Compartir y las tres decisiones |

El guion completo, con las marcas [→], está en [`presentacion/GUION.md`](presentacion/GUION.md).

## Hallazgos principales (datos simulados)

- De 2.400 enlaces públicos auditados, **154** llegaron a un buscador; el **93,5 %** lo había publicado su dueño en un sitio público, y **56** contenían datos sensibles.
- Mientras el indicador «páginas bloqueadas en robots.txt» marcaba **100 %**, los enlaces visibles en buscadores pasaron de 16 a **111**: bloquear el rastreo no impide indexar una URL enlazada.
- La semana del 27 de julio llegaron **11 veces** más menciones que el promedio, el soporte pasó de 20 a **56 horas** y el **78 %** de las quejas vino de usuarios sin ningún enlace expuesto.
- El índice de confianza en la privacidad cayó de **80 a 41**. Va en 52 y se proyecta en 75 a marzo de 2027.
