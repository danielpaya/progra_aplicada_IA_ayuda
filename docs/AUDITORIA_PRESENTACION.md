# Auditoría y rediseño de la presentación

Presentación auditada: versión «tablero» de 17 diapositivas. Resultado: versión «collage + datos» de 43 diapositivas principales y un anexo opcional de 8.

## 1. Hallazgos

| Severidad | Problema | Impacto en la audiencia | Solución aplicada |
| --- | --- | --- | --- |
| Crítico | Cada tablero cargaba de 4 a 6 ideas | La Junta no sabe dónde mirar y deja de escuchar mientras lee | Una idea por diapositiva: una frase y un elemento visual dominante. De 17 a 43 diapositivas de 15–30 s |
| Crítico | Textos de 12–15 px | Ilegibles en un proyector a 6 m | Mínimo de 22–28 px en el cuerpo y cifras héroe de 96–240 px |
| Alto | Paleta verde, rojo, azul, ámbar y morado sobre negro, sin significado fijo | Parecía software financiero; el rojo, usado para todo, dejó de sonar a alarma | Paleta semántica de 6 tonos, cada uno con un solo significado (sección 2) |
| Alto | Sin movimiento: solo un fundido entre diapositivas | La información llega toda de golpe y no hay ritmo | Pasos con →, contadores, gráficos que se dibujan, recortes que entran con rebote y cortinas de sección |
| Alto | Sin identidad visual («sin alma») | No se recuerda al día siguiente | Collage editorial: papel con grano, semitonos, letras recortadas, sellos, cinta adhesiva, estallidos e íconos en semitono |
| Medio | La portada tenía anillos estáticos | Se perdía la metáfora principal | Ondas de luz que salen en bucle del lote 047 hacia «Organización». El cierre repite las ondas en verde |
| Medio | La causa raíz se mostraba con todo a la vez | Se perdía el «momento wow» | Dos diapositivas: primero el medidor en verde (96,8 %), después el mapa de calor con el sello «Aquí salió el lote 047» |
| Medio | La matriz decía «4 victorias rápidas», pero los puntajes daban 5 | Contradicción visible si alguien cuenta | Corregido: 5 victorias rápidas y 3 proyectos estratégicos |
| Medio | Las fuentes de Google fallan sin internet | Cambio de tipografía en el salón | Respaldo con fuentes del sistema (Impact, Georgia, Segoe UI) que conservan la jerarquía |
| Medio | La explicación de los datos simulados se había quitado | Riesgo si el profesor la pide | Anexo de 8 diapositivas, oculto por defecto, con el botón «Datos» o la tecla D |

## 2. Sistema de diseño

**Paleta semántica.** El color cuenta la historia: arranca en rojo (crisis) y termina en verde (confianza).

| Color | Hex | Significado único |
| --- | --- | --- |
| Papel crema | `#F2EBDC` | Fondo · cercanía, alimento casero |
| Tinta | `#151311` | Texto y recortes en semitono |
| Rojo tomate | `#E03A1E` | Solo crisis, riesgo y pérdida |
| Verde hoja | `#2E7D4F` | Solo recuperación y confianza |
| Mostaza | `#F2B705` | Solo decisión humana y acciones |
| Azul riso | `#2442C9` | Solo la IA |

Cada sección tiene su color dominante: Camilo en rojo, Daniel en tinta y rojo, Laura en azul, Mateo en mostaza y Valerie en verde. La barra de progreso cambia de color con la sección.

**Tipografía.**
- Titulares: Anton (respaldo: Impact), en mayúsculas y condensada.
- Frases: Fraunces (respaldo: Georgia).
- Datos y etiquetas: Inter (respaldo: Segoe UI).

**Componentes:**
- Recorte de papel con sombra dura (`.cut`) y cinta adhesiva (`.tape`).
- Sello (`.stamp`) y sticker (`.sticker`).
- Estallido (`data-burst`) y letras recortadas (`data-ransom`).
- Gráfico de puntos (`data-waffle`), medidor (`.meter`) y barras de avance hacia la meta.
- Íconos en semitono: tienda, megáfono, bombillo, candado, IA, persona y botella.
- Cortina de sección por expositor y grano de papel sobre todas las diapositivas.

**Animaciones:**
- Entrada: `up`, `pop`, `left`, `right`, `tilt`, `stamp`, `fade`.
- Gráficos: `grow` y `growx` para barras; `draw` para líneas que se dibujan.
- Continuas: ondas, pulso, giro del reloj y flotación.
- Pasos con → (`data-b`), contadores, un camión que recorre la ruta del lote y un terminal que se escribe solo.
- Duraciones de 0,35 a 0,8 s con curvas *ease-out* y rebote.
- Si el sistema tiene activado «reducir movimiento» (`prefers-reduced-motion`), las animaciones se desactivan.

## 3. Storyboard

| # | Expositor | Intención | Frase en pantalla | Visual · animación | s |
| --- | --- | --- | --- | --- | --- |
| 1 | Camilo | Abrir | Recuperar la confianza | Ondas de luz desde el lote 047 | 25 |
| 2 | Camilo | Enganchar | ¿Cuánto cuesta perder la confianza de una familia? | Letras recortadas | 10 |
| 3 | Camilo | Dimensionar | 1.560 millones de pesos | Contador sobre fondo rojo · estallido «6 meses» | 20 |
| 4 | Camilo | Dimensionar | La confianza cayó a la mitad en un mes | 79 → línea que se dibuja → 38 | 15 |
| 5 | Camilo | Dimensionar | De recomendarnos a pedir que nos eviten | Aguja del NPS que baja de +47 a −18 | 15 |
| 6 | Camilo | Dimensionar | 4 de cada 10 distribuidores sacaron la línea | 10 tiendas; se tachan 4 | 15 |
| 7 | Camilo | Dimensionar | Solo 19 de cada 100 volvieron a comprar | Gráfico de puntos · → 23 se van | 20 |
| 8 | Camilo | Contar | Seis momentos que nos trajeron aquí | Línea de tiempo · 6 pasos | 40 |
| 9 | Camilo | Explicar | El lote se quedó quieto. La desconfianza, no | Escalera que crece | 20 |
| 10 | Camilo | Nombrar | No falló un producto. Se rompió la confianza | Tipografía gigante sobre tinta | 20 |
| 11 | Camilo | Nombrar | Un lote, cuatro heridas | 4 recortes · 4 pasos | 30 |
| 12 | Camilo | Revelar | El tablero decía: todo bien | Medidor verde 96,8 % | 15 |
| 13 | Camilo | Revelar (wow) | Un turno omitía 1 de cada 7 controles | Mapa de calor · sello «Aquí salió el lote 047» | 25 |
| 14 | Daniel | Sección | 02 · El diagnóstico | Cortina de tinta | 5 |
| 15 | Daniel | Medir | ×11 más reclamos | Barras semanales que crecen | 20 |
| 16 | Daniel | Medir | 64 h | Reloj que gira · contador | 15 |
| 17 | Daniel | Medir | El ánimo del cliente se desplomó | Aguja de −0,10 a −0,69 | 15 |
| 18 | Daniel | Separar | 64 de 102: un solo lote | 102 puntos, 64 rojos | 20 |
| 19 | Daniel | Separar | El miedo llegó a las líneas sanas | Dona del 44 % | 20 |
| 20 | Daniel | Cerrar | Lo que no consta, no se dice | 3 sellos · 3 pasos | 25 |
| 21 | Laura | Sección | 03 · La solución | Cortina azul | 5 |
| 22 | Laura | Proponer | La IA verifica. Las personas deciden | Íconos de IA y persona flotando | 15 |
| 23 | Laura | Explicar | De datos dispersos a evidencia por público | 5 columnas · 5 pasos | 35 |
| 24 | Laura | Explicar | Del primer día al primer año | 6 fases en cascada | 25 |
| 25 | Laura | Probar valor | El comunicado | Frase tachada → sello → versión aprobada | 20 |
| 26 | Laura | Probar valor | La entrevista | Megáfono · 1/5 → 5/5 | 20 |
| 27 | Laura | Probar valor | La promesa | La frase se separa en hecho y promesa | 20 |
| 28 | Laura | Tranquilizar | Lo que la IA nunca hace | 3 sellos «Nunca» | 15 |
| 29 | Mateo | Sección | 04 · Las acciones críticas | Cortina mostaza | 5 |
| 30 | Mateo | Priorizar | 8 acciones críticas | Matriz de impacto y esfuerzo | 20 |
| 31 | Mateo | Proponer | 6/6 | Candado y 6 casillas que se marcan | 20 |
| 32 | Mateo | Proponer | Responder rápido, con una sola voz | 4 recortes (acciones 2–5) | 25 |
| 33 | Mateo | Proponer | Demostrar el cambio, no solo anunciarlo | 3 recortes azules (acciones 6–8) | 20 |
| 34 | Mateo | Comprometer | Cada acción tiene fecha y dueño | Gantt que crece | 20 |
| 35 | Mateo | Probar | Un nuevo reporte, resuelto en horas | Ruta con camión animado | 25 |
| 36 | Mateo | Probar | 72 h → 6 h | Contador regresivo sobre verde | 15 |
| 37 | Valerie | Sección | 05 · Los resultados | Cortina verde | 5 |
| 38 | Valerie | Cambiar | Dejamos de medir promedios | OKR tachados → OKR nuevos | 25 |
| 39 | Valerie | Mostrar | La confianza vuelve: 38 → 61 → 75 | Línea que se dibuja y proyección | 20 |
| 40 | Valerie | Mostrar | La operación ya responde | 4 barras frente a la meta | 20 |
| 41 | Valerie | Retorno | +165 millones al mes | Ventas que crecen hasta mar-27 | 20 |
| 42 | Valerie | Pedir | Tres decisiones | 3 recortes · 3 pasos | 30 |
| 43 | Valerie | Cerrar | Confianza = mensaje + evidencia + consistencia + acción | Ondas verdes desde «Hechos» | 20 |

**Anexo** (oculto; se activa con el botón de la diapositiva de cierre, el botón «Datos» o la tecla D; sin expositor asignado):

| A | Expositor | Frase | Visual |
| --- | --- | --- | --- |
| 0 | Equipo | Anexo · Datos simulados | Cortina azul |
| 1 | Equipo | El caso no traía datos. Los creamos | 2 recortes |
| 2 | Equipo | Un prompt estructurado (RISE) | 4 bloques R-I-S-E |
| 3 | Equipo | Tres bases, coherentes con el caso | Contadores 1.025 · 1.307 · 18 |
| 4 | Equipo | Datos sucios, como en la vida real | 4 sellos: 36 · 39 · 11 · 16 |
| 5 | Equipo | La IA encontró y reportó cada error | Contadores 1.025 → 994 y 1.307 → 1.296 |
| 6 | Equipo | Cualquiera puede regenerar los mismos datos | Terminal que se escribe solo |
| 7 | Equipo | Dato simulado | Sello gigante |

## 4. Mejoras adicionales

- **Notas con pasos:** el panel de notas (tecla N) marca dónde decir [→] y en qué paso va el expositor.
- **Barra de progreso por sección:** cambia de color con cada expositor, para que el equipo sepa cuánto falta.
- **Retroceso inteligente:** con ← se deshacen los pasos uno a uno, y al volver a la diapositiva anterior aparece completa.
- **Tema noche (tecla L):** respaldo si el proyector se ve lavado. Mantiene el significado de los colores.
- **Cifras calculadas desde `data.js`:** las ventas perdidas, la recuperación y las barras de avance se calculan, no se escriben a mano, así que no pueden contradecir los datos.
- **Accesibilidad:** contraste alto sobre papel crema y respeto a la preferencia de «reducir movimiento».
- **Corrección de contenido:** cinco victorias rápidas, no cuatro.
