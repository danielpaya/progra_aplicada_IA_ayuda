# Guion de la exposición

Caso Claude · Propuesta académica a la dirección de Anthropic · 43 diapositivas · ≈ 18–20 minutos. Las notas se ven en la presentación con la tecla **N**.

**Cómo leer este guion:** cada **[→]** indica que hay que pulsar → para revelar el siguiente elemento antes de seguir hablando.

Hilo: **el problema** (Camilo) → **el diagnóstico** (Daniel) → **la solución** (Laura) → **las acciones** (Mateo) → **los resultados y la decisión** (Valery).


## Camilo · El problema

**1. Portada**  
Buenas. Soy Camilo y con Daniel, Laura, Mateo y Valery analizamos un caso real: conversaciones y documentos de Claude que la gente compartió con un enlace terminaron apareciendo en Google. Miren el centro: un solo enlace. Las ondas son lo que pasó después: la duda salió del enlace y llegó hasta Anthropic como empresa.

**2. La pregunta**  
Empiezo con una pregunta: ¿qué pasa cuando el botón de compartir termina publicando tu conversación? Eso fue lo que pasó.

**3. Dos veces**  
Pasó dos veces en diez meses. En septiembre de 2025 Google tenía indexadas cerca de 600 conversaciones de Claude. En julio de 2026 volvió a pasar, y esta vez también aparecieron los artefactos. Que se repita es lo que convierte un error en una crisis.

**4. Confianza a la mitad**  
En nuestro escenario simulado, el índice de confianza en la privacidad estaba en 80 en junio. En agosto cayó a 41: casi la mitad.

**5. NPS**  
El NPS mide si los usuarios recomendarían Claude. Estaba en más 38. Pasó a menos 14: hay más usuarios que lo desaconsejan que usuarios que lo recomiendan.

**6. Dejaron de compartir**  
La mitad de los usuarios que compartían dejaron de hacerlo: pasamos de 12,4 % a 6,2 %. Cuando la gente no confía en una función, simplemente deja de usarla.

**7. Siguen vivos**  
Y algo que poca gente sabe: sacar un enlace de Google no lo apaga. En nuestros datos, de cada 100 enlaces que llegaron a un buscador, 60 siguen activos. Solo 40 dueños los desactivaron.

**8. Qué pasó**  
Seis momentos, todos públicos. [→] En 2024 llegan los artefactos, que también se comparten con un enlace. [→] En septiembre de 2025 Google tenía cerca de 600 chats indexados y los retira. [→] Anthropic responde que no comparte directorios ni sitemaps con los buscadores. [→] El 25 de julio de 2026, en Reddit, alguien busca site dos puntos claude punto ai barra share y aparecen chats. [→] Al día siguiente aparecen también artefactos, y los resultados empiezan a desaparecer. [→] Y el 27 la prensa reporta llaves de billeteras cripto, hojas de vida y documentos internos.

**9. El contagio**  
El problema técnico fue un enlace. Pero la duda subió: a la conversación, a la función de compartir, a Claude y, al final, a Anthropic como empresa.

**10. Crisis institucional**  
Esto no es solo un error técnico. Es una crisis institucional: lo que está en duda es si una empresa que se presenta como de seguridad de IA cumple lo que promete. Según la teoría de Coombs, un error accidental que se repite se juzga como prevenible: ya no basta con explicar, hay que demostrar el cambio.

**11. Cuatro capas**  
Un enlace abrió cuatro heridas. [→] De privacidad: 56 de los 154 enlaces indexados tenían datos sensibles. [→] Técnica: ninguna página tenía un noindex que el buscador pudiera leer. [→] Informacional: el 94 % los publicó su propio dueño, sin saber que eso los volvía buscables. [→] Y reputacional: casi la mitad de las quejas vino de personas que nunca compartieron nada.

**12. Todo en verde**  
Y aquí está la causa raíz. Este era el indicador: el cien por ciento de las páginas compartidas estaba bloqueado en robots.txt, el archivo que les dice a los buscadores qué no rastrear. Meta cumplida, todo en verde.

**13. La causa raíz**  
Pero Google lo dice en su propia documentación: una página bloqueada en robots.txt se puede indexar igual si otros sitios la enlazan. Y como el buscador no puede entrar, nunca lee el noindex. Miren: los artefactos publicados en blogs llegaron a Google el 60 % de las veces; los que solo se mandaron por mensaje privado, menos del 1 %. No fue solo culpa de los usuarios: fue un tablero que medía lo equivocado. Daniel les muestra lo que dicen los datos.


## Daniel · El diagnóstico

**14. Sección · Diagnóstico**  
Soy Daniel. Les muestro qué dicen los datos.

**15. ×11**  
La semana del 27 de julio llegaron 404 menciones y tickets, once veces el promedio de 35. Las rojas son de privacidad. El volumen tardó casi un mes en volver a lo normal.

**16. 56 horas**  
Y el soporte colapsó. Responder un ticket pasó de 20 a 56 horas: más de dos días esperando para alguien que quiere saber si su conversación está en Google.

**17. Sentimiento**  
El tono de los mensajes pasó de neutral, menos 0,04, a muy negativo: menos 0,53.

**18. Datos sensibles**  
Cada punto es un enlace que llegó a un buscador. 56 de 154 tenían datos sensibles: datos de contacto, documentos internos de empresas, llaves y credenciales, y datos de salud. Más de un tercio.

**19. Los no afectados**  
Y el miedo no se quedó en los afectados. El 78 % de las quejas y preguntas vino de personas sin ningún enlace expuesto, y casi la mitad nunca había compartido nada. Eso es el contagio en datos.

**20. Ficha de hechos**  
Todo esto termina en una ficha única de hechos. [→] Cinco datos confirmados por fuentes públicas. [→] Uno por confirmar: cuántas copias quedaron en archivos de terceros. [→] Y tres que no constan: que alguien haya usado las llaves expuestas, que sea culpa de los usuarios y que no haya habido datos sensibles. Lo que no consta no se dice en público. Laura les presenta la solución.


## Laura · La solución

**21. Sección · Solución**  
Soy Laura. Les presento la solución.

**22. La propuesta**  
Nuestra propuesta se llama Compartir con Privacidad Verificable, y se resume en una frase: la IA verifica, las personas deciden.

**23. Cómo funciona**  
Funciona así. [→] Entran los datos que hoy están dispersos: los enlaces públicos, lo que muestran los buscadores y lo que dicen los usuarios. [→] La IA detecta datos sensibles, verifica si algo está indexado y contrasta cada frase. [→] Sale una sola ficha de hechos. [→] Con ella deciden las personas: Privacidad, Legal y la vocera. [→] Y cada público recibe la evidencia que necesita.

**24. Seis fases**  
El sistema trabaja en seis fases, desde la primera hora hasta el primer año. En azul, lo que hace la IA; en amarillo, lo que decide siempre una persona.

**25. Error 1: el comunicado**  
Tres errores que el sistema detiene. El primero: un comunicado que dice que no hubo datos sensibles. [→] La IA lo bloquea: esa parte no tiene respaldo en la ficha. [→] La versión aprobada dice solo lo que consta. Eso evita un problema legal y otra pérdida de credibilidad.

**26. Error 2: la entrevista**  
El segundo: la entrevista. La IA hace de periodista hostil y pregunta si fue culpa de los usuarios. [→] Responder que sí se califica con 1 sobre 5: culpa a la víctima. [→] La respuesta entrenada saca 5 sobre 5: asume la parte que le toca a la empresa.

**27. Error 3: la promesa**  
El tercero: mezclar lo hecho con lo prometido. Ya pasó dos veces; si la promesa falla una tercera, no hay vuelta atrás. [→] La IA separa el hecho, que tiene evidencia, de la promesa. Solo se anuncia lo hecho.

**28. Límites de la IA**  
Y tiene reglas claras. [→] La IA nunca publica sola, [→] nunca borra el contenido de un usuario sin su permiso [→] y nunca decide. Siempre firma una persona. Mateo les presenta las acciones.


## Mateo · Las acciones críticas

**29. Sección · Acciones**  
Soy Mateo. Les presento las acciones de los próximos 90 días.

**30. Ocho acciones**  
Proponemos ocho acciones, ubicadas por impacto y esfuerzo. Cinco son victorias rápidas: alto impacto, poco esfuerzo, todas en los primeros 45 días. Tres son proyectos estratégicos para el día 90.

**31. Acción 1**  
La acción número uno: ninguna página compartida se publica sin sus seis verificaciones: noindex en la cabecera y en la página, rastreo permitido para que el buscador lo lea, fuera de los mapas del sitio, prueba en buscadores y registro en el panel del usuario. Esto ataca directamente la causa raíz que mostró Camilo.

**32. Victorias rápidas**  
Las otras cuatro victorias rápidas: la ficha de hechos con auditoría de cada mensaje, avisar y atender con una persona a cada afectado, un monitor que revise los buscadores todos los días, y un aviso claro al compartir con un panel para ver y apagar tus enlaces.

**33. Proyectos estratégicos**  
Y tres proyectos estratégicos: que la IA avise antes de compartir una llave o un dato de salud, que los enlaces venzan y se abran solo con invitación, y una auditoría externa con un reporte público de transparencia.

**34. Hoja de ruta**  
Así se ve en el tiempo. En 10 días ninguna página sale sin un noindex que se pueda leer. En 45, un monitor revisa los buscadores todos los días. En 90, los enlaces vencen y una auditoría externa publica lo que encontró. Cada acción tiene un responsable.

**35. El simulacro**  
Y lo probamos en un simulacro. Un usuario va a compartir una conversación que tiene una llave de API. La IA la detecta y le avisa; el usuario la borra. Después publica el enlace en un foro. El rastreador sí puede leer el noindex, y el buscador no muestra nada. La llave nunca se publicó.

**36. 72 h → 6 h**  
En julio, sacar los enlaces de los buscadores tomó cerca de 72 horas. En el simulacro, 6. La meta del día 90 es 4 horas. Valery les muestra los resultados.


## Valery · Resultados y cierre

**37. Sección · Resultados**  
Soy Valery. Les muestro qué se gana con el plan.

**38. Nuevos OKR**  
Proponemos cambiar lo que se mide. Los OKR de antes, que planteamos como ejemplo, medían crecimiento y un bloqueo que no protegía. [→] Los nuevos miden privacidad que se puede verificar: cero páginas indexadas revisadas cada día, todos los enlaces revisados por datos sensibles, aviso a un afectado en menos de 72 horas y más hechos que promesas.

**39. La confianza vuelve**  
El indicador central: la confianza tocó fondo en 41, en septiembre va en 52 y con el plan proyectamos 75 en marzo de 2027, la meta. Fíjense que después de 2025 se recuperó sola, pero no llegó a su nivel anterior. Por eso no basta con esperar.

**40. La respuesta mejora**  
Lo que depende de la empresa mejora rápido: el soporte responde en 12 horas y se auditan todos los mensajes. Sacar un enlace de los buscadores todavía toma 30 horas, frente a una meta de 4. Y lo que depende del público, como el NPS, avanza más lento.

**41. El retorno**  
Y el uso. Hoy comparte el 7,4 % de los usuarios. Con el plan proyectamos 12 % en marzo: 62 % más, casi el nivel de antes de la crisis. La gente vuelve a usar una función cuando confía en ella.

**42. Las tres decisiones**  
Para cerrar, le pedimos a la dirección tres decisiones. [→] Aprobar esta semana el noindex que se pueda verificar. [→] Nombrar un dueño de la ficha de hechos. [→] Y financiar el escaneo de datos sensibles y la caducidad de los enlaces, para que ningún dato sensible quede público sin aviso.

**43. Cierre**  
La confianza no la devuelve un comunicado. Es mensaje, evidencia, consistencia y acción. Ahora las ondas son verdes: la confianza también se contagia, pero solo con hechos. Muchas gracias.


## Anexo · Datos simulados (opcional · solo si el profesor lo pide · lo puede presentar cualquier integrante)

Se activa de tres formas: el botón azul **▤ Anexo** de la diapositiva de cierre, el botón **▤ Datos** de los controles (arriba a la izquierda) o la tecla **D**. Aparece al final de la presentación.

**A0. Anexo · Datos simulados**  
Anexo opcional, solo si el profesor lo pide. Lo puede presentar cualquier integrante del equipo: explica cómo creamos y limpiamos los datos simulados.

**A1. Por qué simulamos**  
Los hechos del caso son públicos, pero las métricas internas de Anthropic no. Las simulamos con IA, coherentes con lo que reportó la prensa, y les metimos errores a propósito, porque en una crisis real los datos llegan sucios.

**A2. El prompt**  
Usamos un prompt con el paradigma RISE: rol, insumos, pasos y expectativa. Está completo en docs/prompt_RISE.md y en la hoja LEEME de cada Excel.

**A3. Tres bases**  
Tres bases: 2.430 enlaces auditados, 1.428 menciones y tickets, y 24 meses de indicadores.

**A4. Errores sembrados**  
Sembramos 50 duplicados, 45 vacíos, 17 fechas imposibles, 20 valores fuera de rango y 7 etiquetas inconsistentes, sumando las dos bases.

**A5. Limpieza**  
Después de limpiar quedaron 2.400 enlaces y 1.399 menciones. Los atípicos de tiempo de respuesta no se borraron, porque son justamente la señal de la crisis.

**A6. Reproducible**  
Todo es reproducible: con dos comandos en Python, y con semilla fija, cualquiera obtiene exactamente los mismos datos y gráficos.

**A7. Ética**  
Y lo más importante: los hechos públicos van con su fuente, las cifras simuladas van marcadas, y no le atribuimos a Anthropic ninguna métrica real.
