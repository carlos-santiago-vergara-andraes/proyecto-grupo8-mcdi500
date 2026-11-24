# Diccionario de variables: criterios de interpretación

## Alcance

El [diccionario completo](diccionario_variables.csv) describe las **90 columnas originales**, en el orden del archivo `data/raw/listings.csv.gz`. Su elaboración corresponde al reconocimiento inicial de F1: no elimina columnas, no imputa valores y no genera una base procesada.

Las estadísticas corresponden a la copia de referencia descrita en la [ficha de procedencia](fuente_dataset.md). La identidad con el archivo local se comprobará mediante SHA-256. Los tipos leídos se registran con fines informativos: una inferencia automática de pandas no sustituye la interpretación del dato.

## Lectura del archivo

El CSV utiliza **punto y coma** como separador y codificación **UTF-8 con BOM** para facilitar su apertura en Excel. Este separador pertenece al diccionario; el dataset original utiliza coma. Se incluyen los siguientes campos:

| Campo | Contenido |
|---|---|
| `variable` | Nombre completo de la columna original. |
| `descripcion` | Significado operativo del campo. |
| `rol_analitico` | Función o naturaleza conceptual de la variable. |
| `tipo_conceptual` | Representación esperada según su significado; no acredita una conversión realizada. |
| `tipo_leido_en_revision` | Tipo inferido por pandas 2.2.3 en la revisión de referencia. Puede variar con el lector y sus opciones. |
| `unidad` | Unidad, categoría o interpretación pertinente. |
| `n_faltantes` | Cantidad de valores ausentes en la lectura revisada. |
| `porcentaje_faltantes` | Porcentaje sobre 29.753 filas, con cuatro decimales. |
| `estado_observado` | Variación, constancia o ausencia total de valores. |
| `uso_propuesto` | Pertinencia preliminar; la selección final se justificará en F2. |
| `base_definicion` | Grado de respaldo documental según la leyenda siguiente. |
| `observaciones` | Precauciones de interpretación y comprobaciones pendientes. |

### Respaldo de las definiciones

- **O:** campo reconocido en el diccionario oficial v4.3 y con significado respaldado por su documentación. Los roles analíticos y usos propuestos son una interpretación del proyecto.
- **U:** campo listado en la referencia oficial con definición incompleta; se presenta una interpretación operativa del nombre y del contenido observado.
- **P:** campo no cubierto por esa versión del diccionario; interpretación provisional a partir del nombre y, cuando existe, de su contenido. La ausencia de definición no se reemplaza por una afirmación de metodología oficial.

La referencia oficial consultada se identifica como versión 4.3, introducida en agosto de 2022. El archivo de 2026 incorpora campos adicionales, por lo que no se atribuye al diccionario oficial una cobertura completa de esta extracción.

## Revisión de roles automáticos

| Variable o grupo | Interpretación para el proyecto | Implicación |
|---|---|---|
| `id`, `host_id`, `host_profile_id`, `scrape_id` | Identificadores. | No se promedian ni se contabilizan como magnitudes continuas. |
| `price` | Importe monetario, aunque se almacena como texto. | La conversión, la moneda y su correspondencia con la cotización se comprobarán en F2. |
| `neighbourhood_cleansed`, `property_type`, `room_type` | Categorías nominales. | Una cardinalidad elevada no las convierte en texto libre ni en variables cuantitativas. |
| `bedrooms`, `beds`, mínimos y máximos de noches | Conteos discretos. | La lectura como `float64` por presencia de faltantes no cambia su naturaleza. |
| `latitude`, `longitude` | Coordenadas continuas aproximadas. | Su interpretación es espacial y no corresponde a direcciones exactas. |
| `host_is_superhost`, `host_has_profile_pic`, `host_identity_verified` | Variables binarias con dos valores observados. | Acreditan información binaria disponible. |
| `has_availability` | Binaria conceptual, constante entre los no nulos. | No permite comparar ambas categorías en esta copia. |
| `instant_bookable` y otras columnas totalmente vacías | Tipo conceptual sin información observada. | No acreditan diversidad efectiva ni admiten recuperación fiable mediante imputación automática. |
| `review_scores_*` | Puntuaciones agregadas de escala acotada. | Se distinguen de las respuestas ordinales individuales que pudieron originarlas. |
| `estimated_occupancy_l365d`, `estimated_revenue_l365d` | Estimaciones del proveedor. | No se interpretan como reservas ni ingresos efectivamente observados. |

### Diversidad disponible

La revisión identifica coordenadas continuas (`latitude`, `longitude`), conteos (`accommodates`, `beds`), variables nominales (`room_type`, `property_type`, `neighbourhood_cleansed`), binarias (`host_is_superhost`), fechas (`last_scraped`, `last_review`) y texto (`description`, `amenities`). Estos ejemplos corresponden a campos con información observada. El precio aporta una magnitud monetaria que requiere revisión de formato y condiciones antes del análisis.

La presencia de esos roles no implica que todas las variables deban incluirse en la base final. El diccionario complementa el validador y no sustituye la revisión de los demás criterios académicos.

## Variables vinculadas con la pregunta preliminar

- **Respuesta candidata:** `price` o `price_quote_price_per_night`; se elegirá una después de comprobar correspondencia, moneda y diferencias de cobertura.
- **Comparaciones principales:** `neighbourhood_cleansed`, `room_type` y `accommodates`.
- **Condiciones necesarias para interpretar precios:** `last_scraped`, `price_quote_checkin_date`, `price_quote_checkout_date` y moneda extraída de `price_quote_raw`.
- **Trazabilidad:** `id` y, cuando proceda, `host_id` para reconocer anuncios del mismo anfitrión.
- **Contexto complementario sujeto a pertinencia:** `property_type`, `bedrooms`, `beds`, `minimum_nights`, `host_is_superhost` y `review_scores_rating`.

Las fechas y duraciones cotizadas difieren entre anuncios. Antes de cerrar la comparación se evaluará cuántos registros y grupos permanecen al exigir condiciones de estancia compatibles. Las observaciones repetidas por anfitrión y los tamaños desiguales por grupo también deberán considerarse al describir resultados.

## Decisiones reservadas para F2

La exclusión de columnas vacías, la elección del precio, la conversión de tipos, el tratamiento de faltantes y valores extremos y las derivaciones se documentarán con sus efectos sobre filas y variables. Las decisiones consignadas aquí son propuestas; no se presentan como transformaciones ejecutadas.

El resultado del validador sobre el original continúa siendo **CUMPLE, con un aviso**. La elaboración del diccionario no elimina ese aviso ni cambia las 90 columnas de la fuente.

## Referencia

Inside Airbnb. (s. f.). *Inside Airbnb data dictionary* (Versión 4.3) [Diccionario de datos]. https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing
