# Decisiones de análisis y visualización de F4

El cierre se preparó sobre `main` en `4cd0c4c`, que integra F3 mediante PR #4.
La guía de Semana 3 se consultó en `cceae874db0dcb6ad6429480a8a4fd987e536c83`.
La fase agrega comunicación y validación; conserva las reglas y ventanas de F2/F3.

## Contrato y flujo

El notebook consulta la evidencia F1/F2 y la equivalencia ya registrada en F3;
verifica el entorno y las tres huellas F3; carga esos CSV, comprueba sus subconjuntos,
agrega precios interpretables y exporta tres figuras. La normalización de categorías,
conversión de moneda, tratamiento de faltantes y selección temporal ya corresponden
a F2/F3. F4 no ejecuta nuevamente el preprocesamiento. La integridad se comprueba
sobre los artefactos de entrada, sin reconstruir el pipeline.

`src/f4_analisis.py` separa carga, contrato, agregación y comprobación. Se reutiliza
`resumen_vectorizado` de F3. `src/f4_visualizacion.py` recibe las tablas verificadas
y dibuja, sin modificar datos ni aprender parámetros. Esta separación permite
cambiar un gráfico en un solo módulo sin alterar el preprocesamiento.

## Elección de figuras

| Figura | Objetivo | Selección y medida | Justificación y límite |
|---|---|---|---|
| 1. Cajas por tipo | OE3 | Los 2.080 anuncios principales; mediana, cuartiles y extremos | Escala logarítmica explícita para conservar extremos y comparar distribuciones. Los grupos difieren en barrio y capacidad; compartidas n=19. |
| 2. Puntos por barrio | OE3–OE4 | Completos, capacidad 2, estancia principal; seis barrios con n ≥ 30 | Se fijan condiciones observadas; puntos y Q1–Q3 evitan confundir dispersión con incertidumbre. Quedan otras diferencias entre inmuebles. |
| 3. Barras por capacidad | OE3–OE4 | Completos, una noche; capacidades 2–6 con n ≥ 30 en ambos grupos | Barras desde cero, medianas y cuartiles. La ampliación mensual contiene al principal y no ajusta inflación. |

El umbral de 30 se fija por cobertura antes de interpretar precios; no demuestra
precisión o representatividad. Las tablas conservan también los grupos no mostrados.
Los seis barrios reúnen 514 de los 713 completos de capacidad 2 (72,09 %).
La matriz de indicadores y `precio_log1p` permanecen separadas de los datos que se
grafican; no se aplican escalamiento ni imputaciones adicionales.

## Interpretación y calidad

El precio corresponde a una cotización, no a una transacción. Se confirma ARS
mediante el JSON en F2. Entrada y salida describen la estancia solicitada, no la
fecha efectiva de fijación del precio. La ampliación mensual es sensibilidad
descriptiva, sin contraste inferencial entre muestras independientes.

Las cajas usan bigotes calculados en el grupo graficado; esa convención visual
no cambia las marcas IQR aprendidas en F3 sobre la base elegible. Los extremos
continúan en los datos. Las mediciones de F3 evalúan los resúmenes, no el flujo
completo. F4 conserva ese alcance y almacena sus nuevas mediciones por separado.

Los recuentos se comprueban por selección directa; los cuartiles con NumPy se
contrastan con los agregados de pandas (rtol=0; atol=1e-7 ARS). Las comprobaciones
de los CSV mantienen las tolerancias de serialización de F2. Las pruebas cubren
casos normales, entradas ausentes, alteraciones, grupos pequeños y no mutación.

## Fuentes técnicas

Se aplican los criterios de la [guía de F4](https://github.com/magistercienciadatos/Material_Didactico_Semana_3/blob/cceae874db0dcb6ad6429480a8a4fd987e536c83/3_Guias_de_Apoyo/Guia_apoyo_Sumativa3_Fase4.docx)
y el [apunte de F4](https://github.com/magistercienciadatos/Material_Didactico_Semana_3/blob/cceae874db0dcb6ad6429480a8a4fd987e536c83/3_Guias_de_Apoyo/MCDI500_Apunte_Fase4.pdf).
La implementación utiliza [Matplotlib 3.10.8](https://matplotlib.org/3.10.8/)
y [pandas GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html).
