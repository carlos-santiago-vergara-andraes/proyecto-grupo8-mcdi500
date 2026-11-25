# F2 — Preprocesamiento y decisiones verificadas

## Procedencia y ejecución

SHA-256 de la fuente: `c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a`.

Python 3.13.17; pandas 3.1.0; NumPy 2.5.4.

Rama y commit consultados al iniciar: `{'disponible': True, 'rama': 'feature/f2-preprocesamiento', 'commit': '3a004826bc9765fcc5c9e88e9384faba9af2d6ba', 'cambios_sin_confirmar': True}`. La referencia identifica el estado consultado; los archivos guardados se incorporan en un commit posterior.

Ámbito de ejecución: Ejecución local del notebook con kernel .venv del proyecto..

## Elección de precio

`price_quote_price_per_night` es la variable principal: evita interpretar separadores monetarios y se coteja con `quote.price_per_night`. Se exige moneda ARS comprobada en el JSON. `price` se utiliza como contraste; su ausencia no se rellena ni se fusionan importes sin comprobación.

La concordancia se evalúa con tolerancia absoluta de 0,01 ARS y tolerancia relativa cero, sobre pares finitos. Los precios no se imputan.

| indicador | valor |
| --- | --- |
| anuncios_totales | 29753 |
| price_presente_original | 27634 |
| price_numerico_finito | 27634 |
| price_presente_no_interpretable | 0 |
| precio_quote_presente_original | 27633 |
| precio_quote_numerico_finito | 27633 |
| ambos_numericos_finitos | 27633 |
| solo_price_finito | 1 |
| solo_precio_quote_finito | 0 |
| coinciden_tolerancia_0_01_ARS | 27633 |
| difieren_mas_0_01_ARS | 0 |
| porcentaje_coincidencia_entre_ambos | 100 |
| diferencia_absoluta_maxima_ARS | 0 |
| cotizacion_precio_coincide_JSON | 27633 |
| cotizacion_total_coincide_JSON | 27633 |

## Condiciones comparables

Se seleccionó entrada **2026-09-27**, estancia de **1 noche(s)**: **2080 anuncios**, de 27633 elegibles (7.53 %).

La regla selecciona la combinación fecha exacta–duración con mayor cobertura, antes de comparar precios por barrio. El desempate utiliza fecha y duración crecientes. Se conserva la tabla completa de cobertura para reproducir la decisión.

La sensibilidad amplía las entradas al mes 2026-09 y conserva la duración: 5039 anuncios. No representa una corrección por inflación. Las fechas de estancia solicitadas no son fechas de transacciones ni una serie histórica de precios.

Se informa la composición del grupo y sus diferencias con la base elegible. Los grupos pequeños se identifican; no se presentan como referencias estables. La selección limita la generalización al mercado completo.

| entrada | noches | n_anuncios |
| --- | --- | --- |
| 2026-09-27 00:00:00 | 1 | 2080 |
| 2026-09-28 00:00:00 | 2 | 1279 |
| 2026-09-27 00:00:00 | 2 | 1244 |
| 2026-09-28 00:00:00 | 1 | 1057 |
| 2026-09-26 00:00:00 | 1 | 894 |
| 2026-09-27 00:00:00 | 3 | 640 |
| 2026-09-29 00:00:00 | 2 | 618 |
| 2026-09-29 00:00:00 | 1 | 526 |
| 2026-09-26 00:00:00 | 2 | 521 |
| 2026-09-28 00:00:00 | 3 | 521 |

## Faltantes y reglas de limpieza

La tabla siguiente describe las variables inspeccionadas antes de transformar. La ausencia de precio, moneda o condiciones verificables impide formar la base principal. Los motivos pueden superponerse; solo la columna secuencial se suma para explicar la pérdida total.

| variable | tipo_original | n_faltantes | porcentaje_faltantes | n_distintos |
| --- | --- | --- | --- | --- |
| id | int64 | 0 | 0 | 29753 |
| host_id | int64 | 0 | 0 | 14623 |
| last_scraped | str | 0 | 0 | 3 |
| neighbourhood_cleansed | str | 0 | 0 | 47 |
| room_type | str | 0 | 0 | 4 |
| accommodates | int64 | 0 | 0 | 16 |
| price | str | 2119 | 7.122 | 11775 |
| price_quote_price_per_night | float64 | 2120 | 7.1253 | 11775 |
| price_quote_total_price | float64 | 2120 | 7.1253 | 10072 |
| price_quote_checkin_date | str | 1390 | 4.6718 | 325 |
| price_quote_checkout_date | str | 1390 | 4.6718 | 355 |
| price_quote_raw | str | 1390 | 4.6718 | 24755 |
| bedrooms | float64 | 13 | 0.0437 | 20 |
| beds | float64 | 522 | 1.7544 | 33 |
| review_scores_rating | float64 | 3479 | 11.6929 | 141 |

| regla | n_con_motivo_en_fuente | n_excluidos_en_este_paso | n_restantes |
| --- | --- | --- | --- |
| id_ausente | 0 | 0 | 29753 |
| moneda_no_ARS | 1993 | 1993 | 27760 |
| precio_no_positivo_o_no_finito | 2120 | 127 | 27633 |
| precio_no_coincide_JSON | 2120 | 0 | 27633 |
| fechas_no_validas | 1390 | 0 | 27633 |
| fechas_no_coinciden_JSON | 1390 | 0 | 27633 |
| capacidad_no_entera_positiva | 0 | 0 | 27633 |
| barrio_ausente | 0 | 0 | 27633 |
| tipo_no_reconocido | 0 | 0 | 27633 |

## Alternativas para variables complementarias

Se compararon casos completos, media, mediana global y mediana por tipo con respaldo global en dormitorios y camas. Se midieron cobertura, valores fraccionarios y cambio de desviación poblacional. Ninguna de estas variables determina el grupo principal; se conservan sus faltantes, con indicadores, para evitar alterar la cobertura o crear conteos artificiales. Los importes principales tampoco se rellenan.

| variable | alternativa | n_original | n_ausentes_o_invalidos | n_resultante | n_rellenos | media_resultante | mediana_resultante | desviacion_poblacional | cambio_porcentual_desviacion | n_valores_fraccionarios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dormitorios | casos_completos | 27633 | 13 | 27620 | 0 | 1.1539 | 1 | 0.95 | 0 | 0 |
| dormitorios | media_global | 27633 | 13 | 27633 | 13 | 1.1539 | 1 | 0.9497 | -0.0235 | 13 |
| dormitorios | mediana_global | 27633 | 13 | 27633 | 13 | 1.1538 | 1 | 0.9497 | -0.0229 | 0 |
| dormitorios | mediana_por_tipo_con_respaldo_global | 27633 | 13 | 27633 | 13 | 1.1538 | 1 | 0.9497 | -0.0229 | 0 |
| camas | casos_completos | 27633 | 478 | 27155 | 0 | 1.9428 | 1 | 1.5983 | 0 | 0 |
| camas | media_global | 27633 | 478 | 27633 | 478 | 1.9428 | 1 | 1.5844 | -0.8687 | 478 |
| camas | mediana_global | 27633 | 478 | 27633 | 478 | 1.9265 | 1 | 1.5891 | -0.5708 | 0 |
| camas | mediana_por_tipo_con_respaldo_global | 27633 | 478 | 27633 | 478 | 1.9426 | 1 | 1.5847 | -0.8479 | 0 |

| variable | faltantes_antes | invalidos_convertidos_a_faltante |
| --- | --- | --- |
| dormitorios | 13 | 0 |
| camas | 478 | 0 |
| valoracion | 3077 | 0 |

## Transformaciones y atípicos

Los identificadores se tratan como etiquetas; las fechas se interpretan como fechas y la capacidad y duración como enteros. Se conserva el precio en ARS. `precio_log1p` permite inspeccionar asimetría y su reversibilidad se valida. `precio_ars_por_plaza` normaliza por capacidad anunciada: no describe un cobro por persona ni sustituye el precio por anuncio.

Los indicadores one-hot del tipo de alojamiento no imponen orden a la variable nominal. Se exportan separados, con cuatro categorías declaradas, y se verifica una pertenencia por fila. El barrio conserva su etiqueta para las comparaciones descriptivas.

Los precios fuera de 1,5 IQR se marcan dentro de cada tipo; permanecen en la base. Se informa una comparación con y sin estas marcas como sensibilidad, sin identificar automáticamente precios altos con errores.

| tipo_alojamiento | n | n_marcados |
| --- | --- | --- |
| Entire home/apt | 24919 | 2004 |
| Hotel room | 126 | 2 |
| Private room | 2437 | 196 |
| Shared room | 151 | 7 |

| alternativa | n | mediana_ARS | q1_ARS | q3_ARS |
| --- | --- | --- | --- | --- |
| principal_completa | 2080 | 114662 | 90811.5975 | 160526 |
| principal_sin_marcas_IQR | 1902 | 110075 | 87142.58 | 145238 |

## Composición y sensibilidad temporal

| tipo_alojamiento | n_exacta | mediana_ARS_exacta | q1_ARS_exacta | q3_ARS_exacta | grupo_menor_30_exacta | n_mismo_mes | mediana_ARS_mismo_mes | q1_ARS_mismo_mes | q3_ARS_mismo_mes | grupo_menor_30_mismo_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Entire home/apt | 1692 | 120800 | 98302.9475 | 166640.85 | False | 3981 | 125000 | 99110 | 175814 | False |
| Hotel room | 40 | 253784 | 199257 | 298822.25 | False | 105 | 253784 | 195171 | 316465 | False |
| Private room | 329 | 69000 | 47000 | 107018 | False | 856 | 70326 | 47355.195 | 115516.5575 | False |
| Shared room | 19 | 35775 | 24431 | 42654 | True | 97 | 32106 | 26651.39 | 50451 | False |

Las diferencias entre el grupo exacto y la ampliada pueden reflejar cambios de composición y de condiciones de oferta; no se atribuyen causalmente a la fecha o la inflación.

## Validación y exportación local

| control | cumple |
| --- | --- |
| base_no_vacia | True |
| id_unico_y_presente | True |
| precio_finito_positivo | True |
| moneda_ARS | True |
| fechas_y_duracion_coherentes | True |
| capacidad_entera_positiva | True |
| grupos_principales_presentes | True |
| tipos_reconocidos | True |
| log_precio_reversible | True |
| razon_por_plaza_coherente | True |
| sin_nombres_URL_texto_libre_coordenadas | True |
| archivo_original_inmutable | True |
| tabla_original_inmutable | True |
| tres_CSV_releidos_y_cotejados | True |
| indicadores_tipo_releidos_y_cotejados | True |

La fuente original permanece inmutable. Los CSV por anuncio se guardan localmente en `data/processed/`, excluido de Git. El repositorio conserva el código, los informes agregados y las evidencias de ejecución. La exportación se relee y se coteja con la tabla en memoria.

## Correspondencia con objetivos

| Objetivo | Sección de F2_Preprocesamiento.ipynb | Evidencia |
| --- | --- | --- |
| 1. Calidad y cobertura | 1. Obtención; 2. Exploración; 3. Limpieza. | Huella, faltantes, cotejo de precios y JSON, reglas de elegibilidad. |
| 2. Base trazable | 3. Limpieza; 5. Transformación; 6. Validación y exportación. | Conteos secuenciales, alternativas de faltantes, variables derivadas y relectura verificada. |
| 3. Descripción por grupos | 5. Transformación: Resúmenes iniciales y sensibilidad temporal. | n, mediana y cuartiles por barrio, tipo y capacidad. Los gráficos y su interpretación siguen pendientes en la fase analítica. |
| 4. Estabilidad | 4. Condiciones comparables; 5. Transformación y revisión de atípicos. | Grupo exacto, ampliación al mismo mes, composición y contraste con/sin marcas IQR. |

Este registro técnico no sustituye el informe sumativo en la plantilla institucional ni las referencias APA 7 del entregable.
