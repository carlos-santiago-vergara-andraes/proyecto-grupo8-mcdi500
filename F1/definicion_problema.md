# Definición del problema y orientación del estudio

## Contexto y problema

La comparación de precios de alojamientos de corta estancia requiere distinguir ofertas con características y condiciones de reserva diferentes. Una tarifa anunciada para un alojamiento completo, una determinada capacidad y ciertas fechas de estancia no representa necesariamente una referencia comparable para otro tipo de oferta.

El proyecto estudiará los anuncios de Airbnb de Buenos Aires disponibles en el archivo detallado de Inside Airbnb identificado en su ruta como `2026-09-23`. La copia revisada contiene 29.753 anuncios y 90 variables. El validador del curso informó cumplimiento de sus requisitos mínimos, con un aviso por valores faltantes. La [ficha de procedencia](../docs/datos/fuente_dataset.md) y el [diccionario de variables](../docs/datos/diccionario_variables.md) documentan las características y las limitaciones de esta fuente.

El problema de análisis consiste en establecer referencias descriptivas de precio por barrio, tipo de alojamiento y capacidad, considerando que las cotizaciones del archivo corresponden a distintas fechas y duraciones de estancia. Las diferencias observadas pueden reflejar tanto las características de los anuncios como la composición de los grupos y las condiciones cotizadas.

## Pregunta de análisis

**¿Cómo varía el precio cotizado por noche en ARS según el barrio, el tipo de alojamiento y la capacidad de los anuncios de Airbnb de Buenos Aires, considerando la fecha y la duración de la estancia cotizada?**

La pregunta se refiere a diferencias descriptivas entre los anuncios incluidos en la extracción. No plantea identificar efectos causales ni estimar el precio de una reserva efectivamente realizada.

## Objetivo general

**Caracterizar las diferencias del precio cotizado por noche en ARS entre barrios, tipos de alojamiento y capacidades de los anuncios de Airbnb de Buenos Aires, mediante un análisis descriptivo reproducible que considere la fecha y la duración de las estancias cotizadas.**

## Objetivos específicos

1. **Evaluar la calidad y la cobertura de las variables necesarias para el análisis**, verificando identificadores, faltantes, formatos, moneda y coherencia de las fechas y los importes de las cotizaciones.
2. **Preparar una base analítica trazable**, mediante reglas justificadas de selección, conversión y tratamiento de registros, documentando sus efectos sobre el número de anuncios y la composición de los grupos.
3. **Describir la distribución del precio cotizado por noche según barrio, tipo de alojamiento y capacidad**, mediante el tamaño de cada grupo, la mediana, los cuartiles y representaciones gráficas pertinentes.
4. **Evaluar la estabilidad de las diferencias descriptivas al considerar condiciones de estancia comparables y decisiones de preprocesamiento**, comunicando la cobertura, las limitaciones y el alcance de las referencias obtenidas.

## Utilidad prevista

Los resultados podrán apoyar una comparación inicial de tarifas de oferta para anfitriones o gestores de alojamientos, mediante rangos y medianas de segmentos con características similares. Cada referencia deberá acompañarse de su tamaño de muestra, condiciones de estancia y limitaciones de cobertura.

Este aporte corresponde a una referencia descriptiva de oferta. El dataset no permite acreditar ingresos efectivamente percibidos, demanda realizada, rentabilidad ni un precio comercial óptimo.

## Alcance y unidad de análisis

| Componente | Delimitación |
|---|---|
| Ámbito geográfico | Buenos Aires, Argentina, según la cobertura del archivo seleccionado. |
| Unidad de análisis | Anuncio identificado por `id`; no corresponde a una persona, reserva ni transacción. |
| Fuente | Archivo original `data/raw/listings.csv.gz`, conservado sin modificaciones. |
| Identificación de la extracción | Ruta del proveedor con fecha `2026-09-23`; `last_scraped` observado entre el 25 y el 27 de septiembre de 2026. |
| Perspectiva temporal | Una extracción de anuncios con cotizaciones de fechas de estancia heterogéneas; no constituye una serie histórica de precios. |
| Variable de respuesta | Precio cotizado por noche en ARS, cuya representación se elegirá después de cotejar `price` y `price_quote_price_per_night`. |
| Comparaciones principales | Barrio, tipo de alojamiento y capacidad. |
| Condiciones de comparabilidad | Fecha de entrada, fecha de salida, duración de estancia y moneda confirmada. |
| Tipo de estudio | Descriptivo y observacional. |
| Población descrita | Anuncios de la extracción que satisfagan las reglas documentadas; no se presupone representatividad de todo el mercado. |

Se utiliza Buenos Aires como ámbito específico por la disponibilidad de un archivo abierto con suficiente volumen y variables pertinentes para la pregunta. Las conclusiones se limitarán a esta ciudad y a la extracción seleccionada.

## Variables y función prevista

| Función | Variables originales | Consideración metodológica |
|---|---|---|
| Precio | `price`, `price_quote_price_per_night` | Se cotejarán cobertura y concordancia; se elegirá una representación principal y se documentarán las diferencias. |
| Barrio | `neighbourhood_cleansed` | Variable nominal; su cardinalidad no la convierte en magnitud numérica. |
| Tipo de alojamiento | `room_type` | Se distinguirá de `property_type`, que describe la clase de propiedad. |
| Capacidad | `accommodates` | Conteo de personas; se comprobarán integridad y dominio. |
| Fechas cotizadas | `price_quote_checkin_date`, `price_quote_checkout_date` | Permiten reconocer fecha de entrada y duración; su lectura no equivale a observar reservas. |
| Moneda y detalle de cotización | `price_quote_raw` | Se comprobará `quote.currency`; el símbolo `$` no basta para identificar ARS. |
| Trazabilidad | `id`, `host_id`, `last_scraped` | Se conservarán para identificar registros y reconocer anuncios del mismo anfitrión. Los identificadores no se promedian. |
| Contexto complementario | `property_type`, `bedrooms`, `beds`, `minimum_nights`, `host_is_superhost`, `review_scores_rating` | Se utilizarán únicamente cuando aporten información pertinente y su cobertura permita interpretarlos. |

Las variables adicionales de cotización no están definidas en la versión 4.3 del diccionario oficial consultado. Su interpretación operativa se documenta como provisional y se contrastará con el JSON de cada registro antes de utilizarlas en la base analítica.

## Supuestos de interpretación

- Un `id` identifica un anuncio dentro del archivo; su ausencia o repetición se comprobará antes de usarlo para trazar registros.
- La moneda ARS se reconocerá mediante `quote.currency`, sin deducirla únicamente del símbolo monetario. Los importes sin moneda comprobable no se equipararán automáticamente con los demás.
- Las fechas de entrada y salida describen la estancia solicitada para una cotización. No acreditan que esa estancia se haya reservado o realizado.
- Las categorías de barrio y tipo de alojamiento se interpretan según la clasificación de la fuente; su significado y cobertura se revisarán antes de comparar grupos.
- La falta de información no representa un cero. Tampoco se presupone que los anuncios con precio informado tengan la misma composición que los anuncios sin precio.
- Las comparaciones describirán anuncios observados en condiciones documentadas. No se presupone representatividad del mercado ni independencia entre anuncios del mismo anfitrión.

Las comprobaciones que contradigan estos supuestos se cuantificarán y darán lugar a reglas o limitaciones explícitas, sin modificar silenciosamente la interpretación del estudio.

## Plan de análisis

### Reconocimiento inicial en F1

Se documentarán el origen del archivo, el entorno, las dimensiones, el esquema, los faltantes y la diversidad de variables. También se comprobará la integridad del archivo y se reconocerán las condiciones de las cotizaciones. Estas tareas describen la fuente y orientan las reglas de F2, sin modificar el original ni producir una base limpiada.

### Preparación y comprobaciones en F2

La preparación aplicará reglas explícitas sobre identificadores, formatos y valores relevantes. Para el análisis principal se requerirán un importe por noche finito y positivo, moneda ARS confirmada, barrio y tipo informados, capacidad válida y fechas de estancia coherentes. Se contabilizará y justificará cada exclusión, incluyendo su efecto por grupo. Las reglas constituyen el plan del estudio y no se presentan como operaciones ya ejecutadas.

Los precios ausentes no se sustituirán por importes imputados en la comparación principal. El tratamiento de faltantes en variables complementarias se evaluará por su significado y cobertura; si se comparan métodos de imputación, los resultados se distinguirán de los valores observados. Las columnas completamente vacías no se completarán mediante supuestos sin respaldo.

Los importes extremos se marcarán y examinarán. Su magnitud no bastará para eliminarlos: se distinguirán posibles errores, condiciones de reserva particulares y valores plausibles. Cualquier exclusión o escenario de sensibilidad deberá conservar su justificación y sus efectos cuantificados.

Las verificaciones se implementarán mediante funciones reutilizables y comprobaciones pertinentes de entradas válidas, casos límite y errores. La base procesada se exportará a `data/processed/` y se releerá para comprobar su consistencia.

### Descripción y comparabilidad

La distribución de precios se describirá mediante frecuencias, mediana, cuartiles y gráficos. Los resultados por barrio, tipo y capacidad incluirán el número de anuncios que sustenta cada resumen. Los cruces entre variables se realizarán cuando exista información suficiente; no se supondrá que todas las combinaciones tienen cobertura equivalente.

Se examinará la cobertura por fecha de entrada y duración de estancia para establecer segmentos comparables. La definición de esos segmentos se justificará antes de interpretar diferencias de precios y quedará registrada en el notebook. La comparación por condiciones de estancia reduce heterogeneidad observable, sin acreditar un control completo de los factores que intervienen en el precio.

Se contrastarán los resúmenes generales con los segmentos de condiciones más homogéneas y, cuando corresponda, con escenarios de tratamiento de valores extremos. Si las restricciones dejan grupos con información insuficiente, se comunicará esa limitación y se reducirá el alcance de la comparación. La presencia de varios anuncios de un mismo anfitrión también se informará como característica de la muestra.

## Evidencias previstas para los objetivos

| Objetivo | Evidencia esperada | Comprobación de cumplimiento |
|---|---|---|
| 1. Calidad y cobertura | Perfil inicial en F1 y controles de campos necesarios en F2. | Dimensiones, faltantes, identificadores y recuentos de registros que satisfacen cada comprobación. |
| 2. Base trazable | Notebook F2, funciones reutilizables y archivo procesado. | Registro de reglas y efectos; consistencia del archivo exportado y releído. |
| 3. Distribuciones por segmento | Tablas y gráficos con explicación en el notebook. | Mediana, cuartiles y número de anuncios identificados para cada comparación presentada. |
| 4. Estabilidad y alcance | Comparaciones por condiciones de estancia y discusión de sensibilidad. | Cobertura y cambios de los resúmenes cuantificados; limitaciones explícitas y conclusiones coherentes con las observaciones. |

La tabla define cómo se verificará el trabajo; no acredita resultados ya obtenidos. La cobertura de la entrega sumativa se revisará además contra sus criterios de entorno, herramientas, código, documentación, mapa conceptual y referencias.

## Reproducibilidad y comunicación

El notebook de F1 integrará esta definición con el reconocimiento de los datos, la verificación del intérprete y las referencias. El notebook de F2 documentará decisiones y resultados del preprocesamiento. Ambos deberán ejecutarse en orden desde un kernel reiniciado y conservar las salidas pertinentes.

El mapa conceptual representará la relación entre problema, datos, herramientas, documentación y fases del flujo reproducible. Su versión editable se conservará en Markdown y su versión de entrega en PDF. El informe técnico utilizará los resultados comprobados de los notebooks y los enlaces a los productos correspondientes.

Los cambios se registrarán mediante commits específicos en la rama de la fase y se integrarán a `main` mediante Pull Request. El repositorio y el informe mantendrán una distinción explícita entre decisiones planificadas y procedimientos ejecutados.

## Restricciones

La fuente puede presentar omisiones, anuncios desactualizados y diferencias entre las condiciones cotizadas. La extracción es observacional y no corresponde a una muestra probabilística del mercado. Los faltantes y las reglas de selección pueden modificar la composición de los grupos. Además, las ubicaciones son aproximadas y los datos de disponibilidad no distinguen todas las causas de bloqueo del calendario.

La disponibilidad de una sola extracción limita el análisis de cambios históricos y estacionalidad. Las variables de cotización adicionales requieren validación de su contenido porque no están cubiertas por la versión del diccionario oficial consultada. La reconstrucción del entorno depende de la disponibilidad de las versiones declaradas y de la verificación del kernel empleado.

El tiempo disponible para esta entrega limita la incorporación y validación de fuentes adicionales. El trabajo se organiza con las herramientas del curso y se concentra en el archivo seleccionado. Estas condiciones se distinguen de las decisiones de alcance: ciudad, segmentos de comparación y tipo de análisis.

Las estimaciones de ocupación e ingresos del proveedor quedan fuera del análisis principal. Tampoco se realizarán predicciones de rentabilidad ni recomendaciones automáticas de tarifas. Los resultados comunicarán diferencias descriptivas junto con su cobertura y sus limitaciones.

## Referencias

Inside Airbnb. (2026). *Buenos Aires: Detailed listings* [Conjunto de datos; recurso identificado como 2026-09-23]. https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz

Inside Airbnb. (s. f.). *Inside Airbnb data dictionary* (Versión 4.3) [Diccionario de datos]. https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing

Inside Airbnb. (s. f.). *Data assumptions*. https://insideairbnb.com/data-assumptions/
