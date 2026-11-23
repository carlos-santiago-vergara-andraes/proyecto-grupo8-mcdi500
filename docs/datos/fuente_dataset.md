# Ficha de procedencia del dataset

## Identificación y origen

El proyecto utiliza el archivo detallado de anuncios de Inside Airbnb para Buenos Aires, Argentina. Cada fila corresponde a un anuncio incluido en la extracción del proveedor. La copia revisada contiene 29.753 anuncios y no presenta identificadores `id` repetidos ni filas duplicadas exactas.

| Elemento | Registro |
|---|---|
| Proveedor | Inside Airbnb |
| Ámbito geográfico | Buenos Aires, Argentina |
| Archivo | `listings.csv.gz` |
| Ruta del original en el proyecto | `data/raw/listings.csv.gz` |
| Formato | CSV comprimido mediante gzip; separador coma; lectura UTF-8 |
| Dimensión | 29.753 filas × 90 columnas |
| Tamaño comprimido de la copia revisada | 18.108.998 bytes; aproximadamente 17,3 MiB |
| Fecha identificadora de la descarga del proveedor | 23 de septiembre de 2026, según la ruta del recurso |
| Fechas observadas en `last_scraped` | Del 25 al 27 de septiembre de 2026 |
| Descarga en el equipo de trabajo | 22 de noviembre de 2026, 23:27:27; fecha y hora locales informadas |
| Licencia indicada por el proveedor | Creative Commons Attribution 4.0 International (CC BY 4.0) |

La fecha de la ruta del recurso, las fechas de extracción por anuncio y la fecha de descarga local se registran por separado. La discrepancia entre la fecha de la ruta y `last_scraped` se conserva como característica de la fuente, sin sustituir un dato por otro. La hora de descarga no acredita una zona horaria del archivo.

- [Recurso original seleccionado](https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz).
- [Catálogo y condiciones de uso](https://insideairbnb.com/get-the-data/).
- [Diccionario oficial de variables](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing).
- [Supuestos y limitaciones del proveedor](https://insideairbnb.com/data-assumptions/).

## Integridad y conservación

El archivo original se conserva comprimido y sin modificaciones. La documentación de F1 describe su contenido; la selección, limpieza y transformación se justificarán y ejecutarán en F2. Los productos derivados se guardarán en `data/processed/`.

La huella SHA-256 calculada sobre la copia de referencia examinada es:

```text
c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a
```

Esta huella permite comparar el archivo del repositorio con la copia revisada. La coincidencia del archivo local permanece pendiente de comprobación; no se infiere únicamente de su nombre o de sus dimensiones. Desde la raíz del proyecto en PowerShell:

```powershell
Get-FileHash .\data\raw\listings.csv.gz -Algorithm SHA256
```

Si ambas huellas coinciden, se acredita identidad de contenido entre esas copias. Si difieren, se deberá revisar la versión antes de trasladar los resultados de esta ficha al archivo local. La fecha de descarga se mantiene como registro de procedencia y no como prueba criptográfica.

## Validación inicial

La ejecución local comunicada del validador sobre las 90 columnas originales produjo el resultado **CUMPLE los requisitos mínimos, con un aviso**. El informe se conserva en [validacion_dataset.md](validacion_dataset.md).

La copia revisada presenta 14 columnas completamente vacías. Además, `source` y `license` superan el 60 % de faltantes. Estos campos se documentan en el diccionario; su exclusión de una futura base analítica deberá justificarse en F2. El archivo original no se modifica para eliminar el aviso.

El resultado del script comprueba sus criterios automáticos. La adecuación al estudio requiere también revisar el significado de las variables y el alcance académico. Los identificadores no se consideran magnitudes numéricas por el hecho de estar almacenados como números.

## Precio y comparabilidad

La pregunta preliminar compara el precio anunciado por noche según barrio, tipo de alojamiento y capacidad. La revisión de las cotizaciones del archivo permite precisar las siguientes condiciones:

| Comprobación sobre la copia revisada | Resultado |
|---|---|
| `price` sin información | 2.119 anuncios |
| `price_quote_price_per_night` sin información | 2.120 anuncios |
| `price_quote_raw` sin información | 1.390 anuncios |
| JSON de cotización presentes | 28.363; todos pudieron leerse |
| JSON con `quote.currency` igual a `ARS` | 27.760 |
| JSON sin valor informado en `quote.currency` | 603 |
| Otras monedas identificadas en ese campo | Ninguna |
| Intervalo de entrada solicitada | 25 de septiembre de 2026 a 22 de septiembre de 2027 |
| Intervalo de salida solicitada | 26 de septiembre de 2026 a 26 de septiembre de 2027 |
| Duración observada de la estancia cotizada | Entre 1 y 365 noches |

La moneda ARS queda confirmada para las cotizaciones que la informan; el símbolo `$` por sí solo no acredita moneda. Existe un anuncio con `price` informado cuya cotización no permite confirmar moneda. Su tratamiento se decidirá en F2.

Los importes corresponden a condiciones de estancia heterogéneas. La fecha, la duración y la composición de la muestra pueden influir en las diferencias descriptivas. En F2 se comprobará la correspondencia entre `price` y `price_quote_price_per_night`, se elegirá una variable de respuesta y se evaluará el alcance de comparaciones con condiciones de estancia compatibles. Ambas variables no se tratarán como medidas independientes sin comprobar su relación.

El análisis no acreditará tarifas efectivamente pagadas, rentabilidad ni efectos causales del barrio o de otras características. Los campos `estimated_occupancy_l365d` y `estimated_revenue_l365d` son estimaciones del proveedor y quedan fuera de la pregunta principal.

## Cobertura y límites de uso

La fuente representa anuncios capturados en una extracción, sin garantizar cobertura de todo el mercado de alojamientos. Las coordenadas son aproximadas; los días no disponibles no distinguen reservas de bloqueos del anfitrión. La ausencia de reseñas tampoco demuestra, por sí sola, ausencia de actividad.

El archivo incluye campos públicos de perfil. Los nombres, fotografías, enlaces personales y textos de presentación del anfitrión no forman parte de las variables explicativas propuestas. Los resultados se comunicarán mediante comparaciones agregadas, sin atribuir conclusiones individuales a personas.

La licencia del dataset indicada en el catálogo es CC BY 4.0 y requiere atribución. El campo `license` del CSV corresponde al permiso o registro del alojamiento, no a la licencia de uso del conjunto de datos.

## Documentación vinculada

- [Criterios del diccionario de variables](diccionario_variables.md).
- [Diccionario completo de las 90 variables](diccionario_variables.csv).
- [Informe del validador](validacion_dataset.md).

## Referencias

Inside Airbnb. (2026). *Buenos Aires: Detailed listings* [Conjunto de datos; recurso identificado como 2026-09-23]. https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz

Inside Airbnb. (s. f.). *Get the data*. Recuperado el 23 de noviembre de 2026, de https://insideairbnb.com/get-the-data/

Inside Airbnb. (s. f.). *Inside Airbnb data dictionary* (Versión 4.3) [Diccionario de datos]. https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?usp=sharing

Inside Airbnb. (s. f.). *Data assumptions*. https://insideairbnb.com/data-assumptions/
