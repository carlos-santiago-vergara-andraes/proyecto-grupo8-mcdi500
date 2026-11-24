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

Los objetivos orientan las próximas actividades; su formulación no implica que el preprocesamiento o las comparaciones ya estén ejecutados.

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

El archivo original se conserva localmente, comprimido y sin modificaciones en `data/raw/`, que está excluido de Git mediante `.gitignore`. La reproducción requiere obtener el archivo desde el proveedor y comprobar su huella. Los resultados del preprocesamiento se generarán en `data/processed/` durante F2. La descarga local se registró el **22 de noviembre de 2026 a las 23:27:27**. La [ficha de procedencia](docs/datos/fuente_dataset.md) distingue esa fecha de las fechas de extracción e incluye la huella SHA-256 cotejada con el archivo local durante la ejecución de F1.

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

La exclusión de Git y la retirada del índice están preparadas. La limpieza de las referencias históricas se completará y verificará por separado antes de integrar a `main`.

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

El resultado corresponde a las **90 columnas originales**. La selección de variables y el tratamiento de los faltantes se justificarán en F2, conservando la fuente original.

La clasificación automática se contrastó con el significado de las variables en el diccionario de datos. Por ejemplo, `host_id` y `host_profile_id` son identificadores, aunque el validador los clasifique como variables continuas. El diccionario de datos documenta estas diferencias y distingue los campos con definición provisional. El cumplimiento del script constituye una comprobación inicial y se complementará con la revisión de los requisitos académicos de la actividad.

[Consultar el informe de validación](docs/datos/validacion_dataset.md).

## Organización del proyecto

| Ubicación | Contenido |
|---|---|
| `F1/` | Definición del problema, entorno y reconocimiento inicial del dataset. |
| `F2/` | Obtención, exploración, limpieza, transformación y validación de datos. |
| `src/` | Funciones Python reutilizables. |
| `tests/` | Pruebas de lectura, diagnóstico y conservación de los datos. |
| `data/raw/` | Datos originales locales, inmutables y excluidos de Git. |
| `data/processed/` | Resultados generados durante el preprocesamiento. |
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
- [Creación del repositorio](docs/repositorio/creacion_repositorio.md).
- [Configuración del entorno](docs/entorno/instalacion_entorno.md).
- [Validación inicial del dataset](docs/datos/validacion_dataset.md).
- [Ficha de procedencia](docs/datos/fuente_dataset.md).
- [Obtención local y verificación del dataset](docs/datos/obtencion_dataset.md).
- [Criterios del diccionario de variables](docs/datos/diccionario_variables.md).
- [Diccionario completo de las 90 variables](docs/datos/diccionario_variables.csv).

Los enlaces al notebook F2, al mapa vigente y al informe técnico se incorporarán a medida que esos productos estén preparados y verificados.

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

El notebook F1 verificó el kernel de la `.venv` del proyecto, Python 3.13.17 y las importaciones de las cinco dependencias directas. `pip check` finalizó sin incompatibilidades. Las versiones observadas se fijaron en `requirements.txt`: ipykernel 7.4.0, JupyterLab 4.6.6, Notebook 7.6.5, NumPy 2.5.4 y pandas 3.1.0. El inventario de dependencias transitivas y la reproducción desde un clon limpio se completarán durante el cierre técnico.

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

El notebook guardado registró la generación de `docs/evidencias/reconocimiento_f1.json` en el entorno del proyecto. La consulta de Git ya identifica la rama y el commit; al guardar la ejecución actualizada se revisará que esa referencia quede conservada también en la evidencia generada al final. El inventario completo de dependencias transitivas permanece pendiente de generación.

La suite incluye ocho pruebas: seis de lectura, diagnóstico y conservación de datos, y dos de trazabilidad de Git mediante respuestas simuladas. Cubren archivos comprimidos, faltantes, infinitos, diccionarios incoherentes, JSON no válido, fechas inconsistentes, rutas Unicode y detección de subcarpetas. Se ejecutan desde la raíz, con la `.venv` activa:

```powershell
python -m unittest discover -s tests -v
```

La suite completa finalizó localmente con **8 pruebas en 0,206 segundos y resultado `OK`**. La salida se conserva en [la evidencia de pruebas](docs/evidencias/pruebas_reconocimiento_f1.txt). El notebook guardado confirma ocho bloques ejecutados sin errores, la `.venv` correcta, 29.753 filas, 90 columnas, la huella esperada y la conservación de los datos. La consulta posterior de Git confirmó la identificación de la rama y el commit. Los pasos completos se documentan en [la guía de ejecución de F1](docs/entorno/ejecucion_f1.md).

## Control de versiones

El desarrollo actual se realiza en la rama `feature/f1-definicion-entorno`. Los cambios se registran mediante commits específicos que describen el trabajo realizado.

La consulta de trazabilidad realizada desde el notebook registró:

- Repositorio disponible: `True`.
- Rama: `feature/f1-definicion-entorno`.
- Commit de referencia: `6cf6cd89e194303f92e172cf6a587bb0b1e0bd1c`.
- Cambios sin confirmar durante la consulta: `True`.

El último indicador describe el estado de los archivos de trabajo en ese momento. El commit que incorpore el notebook, sus salidas y la documentación actualizados será posterior a la referencia consultada. Esta consulta no acredita un push ni la integración a `main`.

Al completar y verificar F1, la rama se integrará a `main` mediante un Pull Request. F2 se desarrollará posteriormente en su propia rama. La versión evaluable del proyecto deberá quedar integrada en `main` antes de la entrega.

## Estado del proyecto

**Fase 1 en desarrollo.**

### Avances realizados

- Configuración inicial del entorno virtual de Python.
- Organización de las carpetas de documentación.
- Obtención local y reconocimiento del dataset original.
- Ejecución de la validación inicial y generación de su informe.
- Registro de procedencia y fecha real de descarga del dataset.
- Elaboración del diccionario de las 90 variables y revisión de sus roles analíticos.
- Definición del problema, la pregunta, los objetivos, el alcance, los supuestos y las restricciones del análisis.
- Preparación del notebook F1 y de funciones reutilizables para el reconocimiento inicial.
- Ejecución local satisfactoria de las ocho pruebas de reconocimiento y trazabilidad de F1.
- Identificación de la `.venv` con Python 3.13.17 en el selector de kernel de VS Code.
- Ejecución y guardado del notebook F1 sin errores, con verificación efectiva del kernel y las versiones.
- Coincidencia de la huella del archivo y comprobación de conservación del dataset.
- Fijación de las cinco dependencias directas según las versiones verificadas.
- Verificación de Git desde el notebook, con identificación de la rama y el commit de referencia.

### Pendientes de F1

- Registrar el ajuste de distribución del dataset y completar la limpieza del historial con respaldo.

- Guardar el notebook actualizado y comprobar que conserva las salidas completas y la numeración desde 1 tras reiniciar el kernel.
- Revisar la evidencia generada y conservar el inventario completo de dependencias.
- Revisar el mapa conceptual y su correspondencia con el proyecto.

### Continuidad hacia F2 y la entrega sumativa

- Implementar el preprocesamiento con decisiones justificadas y funciones reutilizables.
- Ejecutar y documentar el notebook F2, conservando sus salidas y verificaciones.
- Generar los archivos procesados y comprobar su lectura y consistencia.
- Redactar el informe técnico con las evidencias obtenidas y los apartados exigidos.
- Verificar la reproducción desde un clon limpio e integrar los cambios en `main`.

## Referencia del dataset

Inside Airbnb. (2026). *Buenos Aires: Detailed listings* [Conjunto de datos; recurso identificado como 2026-09-23]. https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz
