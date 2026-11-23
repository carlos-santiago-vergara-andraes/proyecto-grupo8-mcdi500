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
| Ubicación en el repositorio | `data/raw/listings.csv.gz` |
| Registros | 29.753 |
| Variables | 90 |
| Tamaño comprimido | Aproximadamente 17,3 MB, según el validador |
| Licencia indicada por el proveedor | Creative Commons Attribution 4.0 International — CC BY 4.0 |

- [Descarga del archivo original](https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz).
- [Fuente y condiciones de uso](https://insideairbnb.com/get-the-data/).

El archivo original se conserva comprimido y sin modificaciones en `data/raw/`. Los resultados del preprocesamiento se generarán en `data/processed/` durante F2. La descarga local se registró el **22 de noviembre de 2026 a las 23:27:27**. La [ficha de procedencia](docs/datos/fuente_dataset.md) distingue esa fecha de las fechas de extracción e incluye una huella SHA-256 de referencia, pendiente de cotejo con el archivo local.

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
| `data/raw/` | Datos originales sin modificaciones. |
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
- [Creación del repositorio](docs/repositorio/creacion_repositorio.md).
- [Configuración del entorno](docs/entorno/instalacion_entorno.md).
- [Validación inicial del dataset](docs/datos/validacion_dataset.md).
- [Ficha de procedencia](docs/datos/fuente_dataset.md).
- [Criterios del diccionario de variables](docs/datos/diccionario_variables.md).
- [Diccionario completo de las 90 variables](docs/datos/diccionario_variables.csv).

Los enlaces a los notebooks ejecutados, el mapa vigente y el informe técnico se incorporarán a medida que esos productos estén preparados y verificados.

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

En los notebooks se seleccionará el kernel asociado a la `.venv` del proyecto. La verificación desde el propio kernel, la fijación completa de las versiones utilizadas y la ejecución desde un clon limpio se documentarán durante el cierre de F1 y F2.

## Control de versiones

El desarrollo actual se realiza en la rama `feature/f1-definicion-entorno`. Los cambios se registran mediante commits específicos que describen el trabajo realizado.

Al completar y verificar F1, la rama se integrará a `main` mediante un Pull Request. F2 se desarrollará posteriormente en su propia rama. La versión evaluable del proyecto deberá quedar integrada en `main` antes de la entrega.

## Estado del proyecto

**Fase 1 en desarrollo.**

### Avances realizados

- Configuración inicial del entorno virtual de Python.
- Organización de las carpetas de documentación.
- Incorporación del dataset original al repositorio.
- Ejecución de la validación inicial y generación de su informe.
- Registro de procedencia y fecha real de descarga del dataset.
- Elaboración del diccionario de las 90 variables y revisión de sus roles analíticos.
- Definición del problema, la pregunta, los objetivos y el alcance del análisis.

### Pendientes de F1

- Cotejar la huella SHA-256 del archivo local con la copia de referencia documentada.
- Completar el notebook F1 y ejecutarlo desde un kernel reiniciado.
- Revisar el mapa conceptual y su correspondencia con el proyecto.

### Continuidad hacia F2 y la entrega sumativa

- Implementar el preprocesamiento con decisiones justificadas y funciones reutilizables.
- Ejecutar y documentar el notebook F2, conservando sus salidas y verificaciones.
- Generar los archivos procesados y comprobar su lectura y consistencia.
- Redactar el informe técnico con las evidencias obtenidas y los apartados exigidos.
- Verificar la reproducción desde un clon limpio e integrar los cambios en `main`.
