# F2 — Criterios de preprocesamiento

## Orden y fundamento

1. Verificar la fuente por SHA-256, el entorno y la exclusión de datos de Git.
2. Medir faltantes originales y concordancia entre `price`, `price_quote_price_per_night` y el JSON. Tolerancia absoluta: 0,01 ARS; relativa: cero.
3. Elegir el precio numérico por noche, con moneda ARS y contraste con `quote.price_per_night`. No imputar precios ni inferir moneda por `$`.
4. Construir una base elegible con reglas explícitas. Los id repetidos detienen el flujo. Contar motivos superpuestos y pérdidas secuenciales por separado.
5. Comparar alternativas para faltantes de camas y dormitorios. Mantenerlos en la base con indicadores porque no determinan los grupos principales; no introducir conteos no observados.
6. Elegir la combinación de fecha exacta de entrada y noches con mayor cobertura. Desempatar por fecha temprana y duración menor. No elegir según la mediana u otro resultado de precios.
7. Medir cambios de composición respecto de la base elegible y construir una sensibilidad con entradas del mismo mes e idéntica duración. No tratar esa ampliación como corrección por inflación.
8. Conservar el precio en ARS. Derivar log1p para inspección de asimetría y precio/capacidad anunciada como referencia normalizada por plazas; no interpretar esa razón como cobro por persona. Codificar el tipo nominal con indicadores one-hot, preservando sus etiquetas.
9. Marcar atípicos de precio por 1,5 IQR dentro de cada tipo. Conservarlos y medir sensibilidad con/sin marcas; no declarar errores a partir de la magnitud solamente.
10. Validar dominios, fechas, categorías, invariantes, conservación de la fuente y relectura de los CSV. Conservar salidas de las pruebas.

## Resultados y estado

Los conteos definitivos del entorno local se escribirán al ejecutar `F2_Preprocesamiento.ipynb`, en `docs/datos/preprocesamiento_f2.md` y `docs/datos/f2/`. La comprobación de referencia se conserva por separado en `docs/evidencias/referencia_preprocesamiento_f2.md` e identifica sus versiones.

La cohorte exacta limita la generalización; no representa todo el mercado ni todas las fechas. Los resúmenes por tipo y capacidad pueden mantener diferencias de composición por barrio. Las cotizaciones no son reservas realizadas y las diferencias descriptivas no acreditan causalidad.

Los archivos locales conservan id de anuncio y anfitrión para trazabilidad. No se publican esos archivos; el repositorio conserva evidencia agregada. El informe institucional sigue pendiente.
