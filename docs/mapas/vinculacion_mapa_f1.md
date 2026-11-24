# Vinculación del mapa conceptual con el avance de F1

El mapa organiza el flujo reproducible de Airbnb Buenos Aires. Sus versiones [Markdown](mapa_conceptual.md) y [PDF](mapa_conceptual.pdf) contienen los mismos conceptos y relaciones. La representación conserva el carácter conceptual de la Fase 1 y anticipa el trabajo posterior. La tabla siguiente distingue esa planificación de las evidencias técnicas disponibles.

## Correspondencia entre planificación e implementación

| Tipo de elemento | Componente del mapa | Estado del avance | Evidencia o producto previsto |
|---|---|---|---|
| Herramientas | Python, `.venv`, pandas, NumPy, Jupyter, Git y GitHub. | Verificados en F1; versiones directas fijadas. | [Notebook F1](../../F1/F1_Definicion.ipynb), [dependencias](../../requirements.txt), [inventario](../../requirements.lock.txt) y [guía de ejecución](../entorno/ejecucion_f1.md). |
| Procesos | Adquisición, carga, perfil, preparación, validación y análisis. | Fuente y reconocimiento implementados; preparación y análisis proyectados. | [Ficha de procedencia](../datos/fuente_dataset.md), [validación inicial](../datos/validacion_dataset.md) y [funciones de reconocimiento](../../src/reconocimiento.py). Los productos de F2 se incorporarán cuando estén ejecutados. |
| Flujo reproducible | Original inmutable, entorno declarado, diagnóstico y datos derivados. | Original local, integridad y reproducción desde clon limpio verificados; base procesada pendiente. | `data/raw/listings.csv.gz`, `docs/evidencias/reconocimiento_f1.json` y archivos de dependencias. `data/processed/` recibirá el resultado de F2. |
| Decisiones técnicas | Roles semánticos, faltantes y cotizaciones comparables. | Identificadores y roles documentados; los tratamientos se justificarán en F2. | [Definición del problema](../../F1/definicion_problema.md) y [diccionario](../datos/diccionario_variables.md). No se imputarán precios en la comparación principal. |
| Organización del repositorio | F1/, F2/, src/, tests/, data/ y docs/. | Estructura y funciones de F1 incorporadas; integración a main pendiente. | [README](../../README.md), [pruebas](../../tests/test_reconocimiento.py), [trazabilidad de Git](../../tests/test_trazabilidad_git.py) y [evidencia de pruebas](../evidencias/pruebas_reconocimiento_f1.txt). |
| Estructura del notebook | Narrativa, código modular, resultados y referencias. | Notebook F1 ejecutado; notebook F2 proyectado. | [F1_Definicion.ipynb](../../F1/F1_Definicion.ipynb): problema, entorno, Git, integridad, perfil, cotizaciones y evidencia. El informe se redactará con los resultados comprobados de ambas fases. |

## Justificación de la correspondencia

La preservación del original y su huella permiten reconocer la misma entrada; el entorno y las dependencias permiten reconstruir las herramientas; el notebook y los registros explican los procedimientos. Git conserva las versiones y GitHub aloja los cambios enviados. Estas funciones son complementarias: la documentación científica explica el razonamiento y la trazabilidad vincula ese razonamiento con archivos y revisiones.

La limpieza permanece en F2 porque requiere contrastar alternativas y medir sus consecuencias. La disponibilidad de cotizaciones con distintas fechas y duraciones impide interpretar toda diferencia como efecto de una característica del alojamiento. Los retornos del mapa representan la revisión de la pregunta a partir del diagnóstico y la revisión de las reglas a partir de la validación.

## Estado de versionamiento

La fuente original está excluida de Git. Se retiró `data/raw/` del historial en una copia independiente, con respaldo, y se verificaron las nuevas referencias publicadas. El [registro del retiro](../repositorio/retiro_dataset_historial.md) conserva las referencias antes y después del filtrado.

La ejecución desde el clon nuevo consultó el commit `539f48bee8e38d5e2880deee03e577e64b0fa5d1`. Sus resultados se registraron y enviaron mediante el commit `f368242`, con mensaje `test(f1): registrar reproducción desde clon limpio`. Las ocho pruebas finalizaron con `OK` en 0,112 segundos. El [registro de reproducción](../repositorio/reproduccion_clon_limpio_f1.md) identifica las evidencias.

El mapa y este documento son un avance posterior que deberá registrarse en su propio commit. La integración a `main` mediante Pull Request sigue pendiente. Los commits de F2 descritos en el mapa son ejemplos proyectados, no registros de trabajo ya ejecutado.

## Uso y mantenimiento

El Markdown conserva el texto y el diagrama Mermaid para revisión en GitHub. El PDF conserva la presentación de dos páginas tamaño carta horizontal, con tipografía Arial y la jerarquía de color de las guías. Cualquier cambio en conceptos, relaciones, leyenda o referencias debe reflejarse en ambas versiones antes de entregar.

El contenido técnico se redacta en forma impersonal. El PDF se utilizará en la actividad del mapa y se incorporará o referenciará en la entrega sumativa según sus instrucciones; los archivos fuente se conservarán en GitHub.
