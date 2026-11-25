# Proyecto MCDI500 — Airbnb Buenos Aires

Proyecto en desarrollo para la asignatura **Programación para la Ciencia de Datos** del Magíster en Ciencia de Datos e Inteligencia Artificial de la Universidad Andrés Bello.

## Integrante

- Carlos Vergara Andraes (@carlos-santiago-vergara-andraes).

## Problema y pregunta de análisis

El proyecto estudiará las diferencias en los precios cotizados de alojamientos de Airbnb en Buenos Aires, considerando su ubicación, tipo y capacidad. El análisis busca aportar referencias descriptivas para comparar tarifas de oferta entre alojamientos con características y condiciones de estancia similares.

**Pregunta:** ¿Cómo varía el precio cotizado por noche en ARS según el barrio, el tipo de alojamiento y la capacidad de los anuncios de Airbnb de Buenos Aires, considerando la fecha y la duración de la estancia cotizada?

El alcance será descriptivo y observacional. Las cotizaciones corresponden a distintas fechas y duraciones de estancia; las comparaciones se delimitarán según la cobertura de condiciones compatibles. Los resultados no acreditarán tarifas efectivamente pagadas, rentabilidad ni relaciones causales.

[Consultar la definición del problema y el plan de análisis](F1/definicion_problema.md).

## Objetivos

**Objetivo general:** caracterizar las diferencias del precio cotizado por noche en ARS entre barrios, tipos de alojamiento y capacidades de los anuncios de Airbnb de Buenos Aires, mediante un análisis descriptivo reproducible que considere la fecha y la duración de las estancias cotizadas.

Los objetivos específicos son:

1. Evaluar la calidad y la cobertura de las variables necesarias, verificando identificadores, faltantes, formatos, moneda y coherencia de las cotizaciones.
2. Preparar una base analítica trazable con reglas justificadas y efectos documentados sobre los anuncios y los grupos.
3. Describir la distribución del precio por barrio, tipo y capacidad mediante tamaños de grupo, mediana, cuartiles y gráficos.
4. Evaluar la estabilidad de las diferencias al considerar condiciones de estancia comparables y decisiones de preprocesamiento, comunicando cobertura y limitaciones.

La evaluación de calidad y el preprocesamiento se ejecutaron en F1 y F2. Las comparaciones descriptivas y el análisis de estabilidad se completarán en las fases siguientes.

## Dataset

| Característica | Información |
|---|---|
| Fuente | Inside Airbnb |
| Ciudad | Buenos Aires, Argentina |
| Archivo original | `listings.csv.gz` |
| Ubicación local, excluida de Git | `data/raw/listings.csv.gz` |
| Registros | 29.753 |
| Variables | 90 |
| Tamaño comprimido | Aproximadamente 17,3 MB, según el validador |
| Licencia indicada por el proveedor | Creative Commons Attribution 4.0 International — CC BY 4.0 |

- [Descarga del archivo original](https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz).
- [Fuente y condiciones de uso](https://insideairbnb.com/get-the-data/).

El archivo original se conserva localmente, comprimido y sin modificaciones en `data/raw/`, que está excluido de Git mediante `.gitignore`. La reproducción requiere obtener el archivo desde el proveedor y comprobar su huella. Los resultados verificados del preprocesamiento se conservan localmente en `data/processed/`, excluido de Git. La descarga local se registró el **22 de noviembre de 2026 a las 23:27:27**. La [ficha de procedencia](docs/datos/fuente_dataset.md) distingue esa fecha de las fechas de extracción e incluye la huella SHA-256 cotejada con el archivo local durante la ejecución de F1.

## Obtención local y distribución de los datos

El original contiene nombres públicos, enlaces y datos de perfiles de anfitriones. Su distribución se realiza desde el recurso oficial de Inside Airbnb; el repositorio conserva el código, la documentación y las evidencias agregadas del análisis.

- Recurso exacto: https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz
- Licencia indicada por el proveedor: **Creative Commons Attribution 4.0 International (CC BY 4.0)**, con atribución a Inside Airbnb.
- Condiciones de uso: https://insideairbnb.com/get-the-data/
- Ruta local: `data/raw/listings.csv.gz`, excluida de Git.
- SHA-256 verificado:

```text
c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a
```

En un clon limpio, antes de abrir los notebooks:

```powershell
New-Item -ItemType Directory -Force .\data\raw | Out-Null
Invoke-WebRequest -Uri "https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz" -OutFile .\data\raw\listings.csv.gz
$huellaEsperadaDataset = "c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a"
$huellaObtenidaDataset = (Get-FileHash .\data\raw\listings.csv.gz -Algorithm SHA256).Hash
if ($huellaObtenidaDataset -ne $huellaEsperadaDataset) { throw "La huella del dataset no coincide con la fuente documentada." }
```

Si el archivo ya está disponible, se comprueba su huella sin volver a descargarlo ni reemplazarlo. El [procedimiento de obtención](docs/datos/obtencion_dataset.md) desarrolla la conservación local, la verificación y los criterios de distribución.

Se verificaron la exclusión de Git, la conservación del archivo local y la retirada de `data/raw/` del historial filtrado. Al publicar la limpieza se verificó la concordancia de las ramas con la copia filtrada: `539f48bee8e38d5e2880deee03e577e64b0fa5d1` para F1 y `1bcf2be00feb2596e4e3e6d65983feb409beb8c6` para `main`. El [registro del retiro histórico](docs/repositorio/retiro_dataset_historial.md) documenta el respaldo, el método y las verificaciones. Posteriormente se registró y envió la reproducción desde un clon limpio en `f368242`. F1 se integró posteriormente a `main` mediante el [Pull Request #1](https://github.com/carlos-santiago-vergara-andraes/proyecto-grupo8-mcdi500/pull/1).

## Validación inicial del dataset

Se ejecutó `validar_dataset.py` sobre el archivo original desde la raíz del proyecto:

```powershell
python validar_dataset.py data/raw/listings.csv.gz --sep "," --informe docs/datos/validacion_dataset.md
```

**Resultado: CUMPLE los requisitos mínimos del validador, con un aviso.**

La validación registró:

- 29.753 filas y 90 columnas.
- Diversidad de roles analíticos y presencia de variables numéricas y categóricas.
- Presencia de fechas, texto y valores faltantes.
- Ninguna fila duplicada exacta.
- Un aviso por columnas con más del 60 % de valores faltantes: 14 columnas completamente vacías, además de `source` y `license`, con 92,9 % y 98,3 % de faltantes, respectivamente.

El resultado corresponde a las **90 columnas originales**. La selección de variables y el tratamiento de faltantes se documentaron en F2, conservando la fuente original.

La clasificación automática se contrastó con el significado de las variables en el diccionario de datos. Por ejemplo, `host_id` y `host_profile_id` son identificadores, aunque el validador los clasifique como variables continuas. El diccionario de datos documenta estas diferencias y distingue los campos con definición provisional. El cumplimiento del script constituye una comprobación inicial y se complementará con la revisión de los requisitos académicos de la actividad.

[Consultar el informe de validación](docs/datos/validacion_dataset.md).

## Organización del proyecto

| Ubicación | Contenido |
|---|---|
| `F1/` | Definición del problema, entorno y reconocimiento inicial del dataset. |
| `F2/` | Obtención, exploración, limpieza, transformación y validación de datos. |
| `F3/` | Núcleo algorítmico, clases, equivalencia F2/F3 y mediciones de eficiencia. |
| `src/` | Funciones Python reutilizables. |
| `tests/` | Pruebas de lectura, diagnóstico, trazabilidad de Git, preprocesamiento y conservación de los datos. |
| `data/raw/` | Datos originales locales, inmutables y excluidos de Git. |
| `data/processed/` | Resultados locales del preprocesamiento, excluidos de Git. |
| `docs/entorno/` | Instalación, configuración y reproducción del entorno. |
| `docs/repositorio/` | Creación y organización del repositorio. |
| `docs/datos/` | Documentación de fuente, diccionario de variables e informes de validación. |
| `docs/mapas/` | Mapa conceptual y su archivo editable. |
| `docs/informes/` | Plantilla de formato e informes técnicos. |
| `docs/evidencias/` | Evidencias de ejecución y verificaciones. |

Esta organización identifica la función de cada carpeta. La ubicación prevista de un producto no implica que su elaboración esté finalizada.

## Documentación disponible

- [Problema, pregunta, objetivos y alcance](F1/definicion_problema.md).
- [Notebook F1](F1/F1_Definicion.ipynb): ejecutado en la `.venv` del proyecto, con reconocimiento del dataset y trazabilidad de Git verificados.
- [Instrucciones de ejecución de F1](docs/entorno/ejecucion_f1.md).
- [Mapa conceptual editable](docs/mapas/mapa_conceptual.md).
- [Mapa conceptual en PDF](docs/mapas/mapa_conceptual.pdf).
- [Vinculación del mapa con el avance](docs/mapas/vinculacion_mapa_f1.md).
- [Reproducción desde un clon limpio](docs/repositorio/reproduccion_clon_limpio_f1.md).
- [Creación del repositorio](docs/repositorio/creacion_repositorio.md).
- [Configuración del entorno](docs/entorno/instalacion_entorno.md).
- [Validación inicial del dataset](docs/datos/validacion_dataset.md).
- [Ficha de procedencia](docs/datos/fuente_dataset.md).
- [Obtención local y verificación del dataset](docs/datos/obtencion_dataset.md).
- [Retiro del dataset del historial publicado](docs/repositorio/retiro_dataset_historial.md).
- [Criterios del diccionario de variables](docs/datos/diccionario_variables.md).
- [Diccionario completo de las 90 variables](docs/datos/diccionario_variables.csv).

- [Notebook F2](F2/F2_Preprocesamiento.ipynb): ejecutado y guardado en la `.venv` local, integrado a `main` mediante PR #2.
- [Instrucciones y salidas de F2](docs/entorno/ejecucion_f2.md).
- [Criterios de preprocesamiento de F2](F2/decisiones_preprocesamiento.md).

- [Resultados y decisiones de F2](docs/datos/preprocesamiento_f2.md).
- [Informe sumativo F1 y F2 en PDF](docs/informes/MCDI500_Informe_F1_F2_Precios_Airbnb_Buenos_Aires.pdf).
- [Informe editable en DOCX](docs/informes/MCDI500_Informe_F1_F2_Precios_Airbnb_Buenos_Aires.docx).
- [Reproducción independiente en Linux](docs/evidencias/replica_linux/README.md).

## Entorno de trabajo

Se utiliza **Python 3.13.17**, con un entorno virtual `.venv` dentro del proyecto. Las dependencias se declaran en `requirements.txt`. El entorno virtual se excluye del control de versiones.

Para preparar el entorno desde la raíz del repositorio en Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

La versión y la ubicación del intérprete se comprueban mediante:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

El notebook F1 verificó el kernel de la `.venv` del proyecto, Python 3.13.17 y las importaciones de las cinco dependencias directas. `pip check` finalizó sin incompatibilidades. Las versiones observadas se fijaron en `requirements.txt`: ipykernel 7.4.0, JupyterLab 4.6.6, Notebook 7.6.5, NumPy 2.5.4 y pandas 3.1.0. El inventario de dependencias transitivas se conserva en `requirements.lock.txt` y se utilizó para reconstruir la `.venv` del clon nuevo.

## Ejecución del notebook F1

1. Abrir `F1/F1_Definicion.ipynb` en VS Code.
2. Si VS Code solicita **Install/Enable suggested extensions Python + Jupyter**, completar la instalación o habilitación y recargar el editor si se solicita.
3. Seleccionar **Select Kernel → Python Environments → `.venv (3.13.17)`**, con ruta `.venv\Scripts\python.exe`, marcada como **Recommended** en el selector revisado.
4. Pulsar **Ctrl + Shift + P**, buscar y seleccionar **Jupyter: Restart Kernel and Run All Cells** y confirmar el reinicio si se solicita. Esperar la ejecución de todas las celdas.
5. Comprobar las salidas del entorno, la huella del archivo, el perfil de variables y la referencia de Git.
6. Guardar el notebook con **Ctrl + S**, conservando sus salidas, y revisar `docs/evidencias/reconocimiento_f1.json`, generado al completar las comprobaciones.

El notebook utiliza `src/reconocimiento.py` para verificar el entorno, leer y reconocer los datos sin limpiarlos ni transformarlos. Su ejecución se detiene si se utiliza otro entorno, no se cumplen las dependencias fijadas o el archivo difiere de la copia de referencia. La selección, imputación y transformación de una base analítica corresponden a F2.

Para conservar las versiones efectivamente instaladas, después de verificar el entorno:

```powershell
python -m pip freeze | Set-Content -Encoding UTF8 requirements.lock.txt
```

El notebook guardado registró la generación de `docs/evidencias/reconocimiento_f1.json` en el entorno del proyecto. La consulta de Git ya identifica la rama y el commit; la ejecución guardada desde el clon nuevo se registró junto con el JSON de reconocimiento en el commit `f368242`. El inventario completo de dependencias transitivas se conserva en `requirements.lock.txt`.

F1 incorporó ocho pruebas: seis de lectura, diagnóstico y conservación de datos, y dos de trazabilidad de Git mediante respuestas simuladas. Cubren archivos comprimidos, faltantes, infinitos, diccionarios incoherentes, JSON no válido, fechas inconsistentes, rutas Unicode y detección de subcarpetas. Se ejecutan desde la raíz, con la `.venv` activa:

```powershell
python -m unittest discover -s tests -v
```

En la verificación histórica de F1 desde el clon nuevo, las **8 pruebas finalizaron en 0,112 segundos con resultado `OK`**. Con las diez pruebas incorporadas en F2, la suite de F2 alcanzó **18 pruebas**. F3 incorpora once pruebas adicionales; la suite completa preparada para F3 contiene **29 pruebas**. La salida se conserva en [la evidencia del clon limpio](docs/evidencias/pruebas_clon_limpio_f1.txt); el resultado inicial permanece en su archivo de evidencia anterior. El notebook guardado confirma ocho bloques ejecutados sin errores, la `.venv` correcta, 29.753 filas, 90 columnas, la huella esperada y la conservación de los datos. La consulta posterior de Git confirmó la identificación de la rama y el commit. Los pasos completos se documentan en [la guía de ejecución de F1](docs/entorno/ejecucion_f1.md).

## Control de versiones

F1 se desarrolló en `feature/f1-definicion-entorno` y se integró a `main` mediante el Pull Request #1. F2 se desarrolló en `feature/f2-preprocesamiento` y se integró a `main` mediante el Pull Request #2. Los cambios se registran mediante commits descriptivos y cada fase se integra a `main` antes de la entrega.

La consulta de trazabilidad realizada desde el notebook registró:

- Repositorio disponible: `True`.
- Rama: `feature/f1-definicion-entorno`.
- Commit de referencia: `539f48bee8e38d5e2880deee03e577e64b0fa5d1`.
- Cambios sin confirmar durante la consulta en el clon nuevo: `False`.

El último indicador describe el estado de los archivos de trabajo en ese momento. Después de guardar las nuevas salidas se registraron el notebook y el JSON de reconocimiento en el commit `f368242`, con mensaje `test(f1): registrar reproducción desde clon limpio`. El push confirmó su envío a la rama F1. La integración de F1 a `main` se completó mediante el Pull Request #1.

La reescritura histórica cambió los identificadores de los commits afectados. El registro del retiro histórico documenta la correspondencia entre las referencias anteriores y posteriores a la limpieza. Los commits citados como evidencias identifican momentos concretos de ejecución y no necesariamente el estado actual de `main`.

F1 y F2 están integradas en `main` mediante los PR #1 y #2. El commit de integración de F2 verificado desde un clon independiente es `cb2e42e53583430ca717162640be83cf197f5412`; incluye el avance registrado en `23ab86c`. El informe y su documentación de cierre se incorporan en un avance posterior. La versión evaluable deberá quedar en `main` antes de la entrega.

## Ejecución del notebook F2

1. Mantener el archivo original en `data/raw/listings.csv.gz` y excluir también `/data/processed/` en `.gitignore`.
2. Abrir `F2/F2_Preprocesamiento.ipynb` y seleccionar la misma `.venv` verificada en F1.
3. Ejecutar **Jupyter: Restart Kernel and Run All Cells** y esperar la finalización completa.
4. Revisar las salidas de precios, faltantes, grupos, validación y pruebas; guardar con **Ctrl + S**.
5. Consultar `docs/datos/preprocesamiento_f2.md`, `docs/datos/f2/`, `docs/evidencias/preprocesamiento_f2.json` y `docs/evidencias/pruebas_preprocesamiento_f2.txt`.

Las salidas por anuncio se conservan localmente en `data/processed/`; Git conserva el notebook, el código y las evidencias agregadas. No se publica el original ni se agregan archivos de `data/raw/` o `data/processed/` al commit. Las dependencias de F1 son suficientes.

La ejecución local de F2 registró **18 pruebas aprobadas en 0,656 segundos y 15 controles de validación satisfactorios**. Las [evidencias de pruebas](docs/evidencias/pruebas_preprocesamiento_f2.txt) y el [registro de validación](docs/evidencias/preprocesamiento_f2.json) conservan los resultados.

Para comparar precios, se seleccionó un grupo de **2.080 anuncios** con entrada el **27 de septiembre de 2026**, salida el **28 de septiembre de 2026** y duración de **una noche**. El grupo adicional de **5.039 anuncios** mantiene una noche y amplía las entradas a septiembre de 2026; permite evaluar la sensibilidad temporal, sin constituir un ajuste por inflación. Los grupos seleccionados no representan toda la oferta y las fechas de estancia no acreditan una misma fecha de fijación del precio.

Se compararon `price` y `price_quote_price_per_night`: el primero presenta **27.634 valores** y el segundo **27.633**. Ambos están disponibles simultáneamente en **27.633 anuncios**, sin diferencias numéricas observadas. Se seleccionó `price_quote_price_per_night`, contrastado con el JSON de cotización y limitado a moneda ARS, fechas y duración válidas. Los [resultados de comparación](docs/datos/f2/comparacion_precios.csv) y las [decisiones de F2](docs/datos/preprocesamiento_f2.md) documentan la elección.

## Ejecución del notebook F3

F3 reorganiza las funciones de F2 mediante una clase base, tres clases hijas y un
orquestador por composición. Las reglas de datos de F2 se mantienen. Se comparan
resúmenes por bucle y agrupamiento vectorizado, con mediciones de tiempo y memoria.

1. Conservar el original y los tres CSV locales de F2 con sus huellas registradas.
2. Abrir `F3/F3_Nucleo_Algoritmico.ipynb` y seleccionar la `.venv` del proyecto.
3. Ejecutar **Jupyter: Restart Kernel and Run All Cells** y esperar las diez celdas.
4. Revisar equivalencia, casos límite, controles y métricas; guardar con **Ctrl + S**.
5. Consultar `docs/evidencias/f3/resultados_f3.json` y las tablas generadas en esa carpeta.

No se requieren dependencias nuevas. Los resultados por anuncio se conservan en
`data/processed/`, fuera de Git. Los módulos de F3 están en `src/f3_*.py` y las pruebas
en `tests/test_f3.py`; las 18 pruebas previas se complementan con once nuevas.

- [Arquitectura y decisiones de F3](F3/arquitectura_y_decisiones.md).
- [Correspondencia con la rúbrica oficial de F3](F3/verificacion_rubrica.md).
- [Instrucciones completas de ejecución de F3](docs/entorno/ejecucion_f3.md).
- [Verificación de preparación de F3 en Linux](docs/evidencias/f3/referencia_linux/README.md).

## Estado del proyecto

- **F1 técnica integrada a `main` mediante PR #1:** notebook ejecutado, ocho pruebas aprobadas, fuente fuera de Git e historial limpiado; mapa conceptual en Markdown y PDF.
- **F2 ejecutada, verificada e integrada a main mediante PR #2:** notebook ejecutado en la `.venv` del proyecto con Python 3.13.17, 18 pruebas aprobadas y 15 controles de validación satisfactorios. Se generaron una base elegible de 27.633 anuncios, un grupo principal de 2.080 y un grupo adicional de 5.039 para evaluar la sensibilidad temporal. Las decisiones y evidencias quedaron documentadas; los datos procesados se conservan localmente, fuera de Git.
- **Informe sumativo F1 y F2 elaborado:** DOCX y PDF con plantilla institucional, resultados verificados, tabla de faltantes, relación objetivos–secciones de notebook, mapa y referencias APA 7.
- **F3 preparada:** módulos orientados a objetos, notebook y once pruebas adicionales. La verificación de preparación conserva los resultados de F2; falta ejecutar y guardar el notebook en el entorno local, completar el informe institucional y registrar la integración de F3 a `main`.
- **F4 pendiente.**

La guía de F2 documenta las salidas y las comprobaciones de reproducción. La evidencia Windows se conserva como ejecución principal. La verificación independiente en Linux parte de un clon de main, utiliza Python 3.13.5 y las mismas cinco dependencias directas fijadas, y ejecuta todas las celdas mediante IPython. Reprodujo los conteos, los quince controles, las dieciocho pruebas y las catorce tablas agregadas de F2. El inventario Linux y el método se documentan por separado; los notebooks de evidencia no sustituyen a los principales de F1/ y F2/.
