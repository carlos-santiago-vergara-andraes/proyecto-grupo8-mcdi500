# Ejecución del notebook F1

## Archivos requeridos

El notebook se conserva en `F1/F1_Definicion.ipynb` y utiliza las funciones de `src/reconocimiento.py`. También requiere el dataset original, `README.md`, `requirements.txt` y `docs/datos/diccionario_variables.csv`, incorporados en los avances anteriores.

La fuente debe coincidir con la huella SHA-256 documentada en [la ficha del dataset](../datos/fuente_dataset.md). El notebook detiene la ejecución si encuentra un archivo diferente; no descarga ni reemplaza el original.

## Preparación de la terminal

Las operaciones de terminal se ejecutan desde la raíz del proyecto. En PowerShell, el entorno se activa mediante:

```powershell
.\.venv\Scripts\Activate.ps1
python --version
python -c "import sys; print(sys.executable)"
```

La consola del proyecto confirmó Python 3.13.17 y un intérprete ubicado en `.venv\Scripts\python.exe`. El prefijo `(.venv)` indica activación en esa terminal. La selección del kernel del notebook se comprueba por separado.

## Habilitación de Python y Jupyter en VS Code

Las librerías instaladas con pip y las extensiones del editor cumplen funciones diferentes. La presencia de Jupyter en el entorno Python no habilita automáticamente su extensión en VS Code.

1. Abrir `F1/F1_Definicion.ipynb` desde la carpeta completa del proyecto.
2. Pulsar **Select Kernel** en la esquina superior derecha del notebook.
3. Si se muestra **Install/Enable suggested extensions Python + Jupyter**, seleccionar esa opción y completar la instalación o habilitación de las extensiones.
4. Si el editor solicita recargar la ventana, aceptar la recarga y volver al notebook.
5. Pulsar nuevamente **Select Kernel** para abrir las fuentes de kernel disponibles.

El procedimiento contempla tanto extensiones ausentes como deshabilitadas; el aviso de instalación o habilitación no distingue por sí solo ambas situaciones.

## Selección del kernel en VS Code

1. Abrir la carpeta completa del proyecto en VS Code.
2. Abrir **`F1/F1_Definicion.ipynb`** desde el explorador de archivos.
3. En la esquina superior derecha del notebook, seleccionar **Select Kernel → Python Environments → `.venv`**; las etiquetas también pueden mostrarse como **Seleccionar kernel → Entornos de Python**. Si ya aparece un kernel, pulsar su nombre para cambiarlo.
4. Elegir la opción **`.venv (3.13.17)`**, marcada como **Recommended**, cuya ruta es `.venv\Scripts\python.exe`. El selector revisado también muestra una instalación global de Python 3.13.17: la versión por sí sola no identifica el entorno del proyecto.
5. Comprobar que el kernel seleccionado aparece en la barra del notebook. La comprobación del intérprete efectivo se realiza además en su celda de entorno.

Se verificaron tanto la disponibilidad de la `.venv` del proyecto en el selector como su uso efectivo en la celda de entorno del notebook guardado.

## Ejecución y guardado del notebook

1. Con la `.venv` seleccionada, pulsar **Ctrl + Shift + P** para abrir la paleta de comandos. Buscar y seleccionar **Jupyter: Restart Kernel and Run All Cells** y confirmar el reinicio si se solicita. Esta acción reinicia el kernel y ejecuta todas las celdas en orden.
2. En una primera ejecución, **Run All** ejecuta las celdas en orden; para la verificación final se reiniciará el kernel antes de repetir la ejecución completa.
3. Esperar el término de todos los bloques y revisar que no existan celdas con error.
4. Verificar las salidas de entorno, integridad y reconocimiento, y el mensaje final de generación de evidencia.
5. Guardar con **Ctrl + S**, conservando las salidas y los números de ejecución.

El indicador `(.venv)` de la terminal no selecciona por sí solo el kernel del notebook. La comprobación dentro del cuaderno verifica el intérprete efectivo.

## Verificaciones durante la ejecución

El notebook registra la versión real de Python, la ruta del intérprete y la versión de cada dependencia directa de `requirements.txt`. Comprueba que Python pertenece a la serie 3.13, que el kernel usa la `.venv` del proyecto y que `pip check` finaliza correctamente. También contrasta las dependencias fijadas mediante `==` con sus versiones instaladas.

La versión de mantenimiento de Python se conserva en la evidencia. La versión 3.13.17 registrada en la configuración del proyecto debe contrastarse con esa salida; si cambia, se actualizará la documentación del entorno con el motivo.

La ejecución guardada verificó Python 3.13.17, ipykernel 7.4.0, JupyterLab 4.6.6, Notebook 7.6.5, NumPy 2.5.4 y pandas 3.1.0. Todas las importaciones fueron correctas y `pip check` informó `No broken requirements found.`. Esas cinco dependencias directas quedaron fijadas en `requirements.txt` a partir de las versiones observadas. La salida revisada confirmó **cero dependencias directas sin versión fijada**.

Para conservar también el inventario de dependencias transitivas del entorno validado, desde la terminal con `.venv` activada:

```powershell
python -m pip freeze | Set-Content -Encoding UTF8 requirements.lock.txt
```

El inventario debe generarse desde el entorno que ejecuta el notebook. Para reconstruir ese conjunto de versiones en una instalación posterior se utilizará `python -m pip install -r requirements.lock.txt`. El inventario se utilizó para reconstruir la nueva `.venv` durante la comprobación desde un clon limpio.

## Resultados que deben comprobarse

- Ejecución completa, sin celdas con error y con numeración continua.
- Intérprete de `.venv`, importaciones correctas y cumplimiento de las versiones declaradas.
- SHA-256 idéntico antes y después de la lectura.
- 29.753 filas y 90 columnas en la fuente seleccionada.
- Cero duplicados exactos y cero repeticiones de `id` en la copia documentada.
- 14 columnas completamente vacías y 16 columnas con más del 60 % de faltantes.
- Cotizaciones con moneda ARS informada y condiciones de estancia heterogéneas, según los recuentos mostrados.
- Perfil de las 90 variables y correspondencia con el diccionario manual.
- Identificación de la rama y el commit consultados durante la ejecución. Un commit que contenga el notebook guardado se registrará después.

La lectura de fechas y JSON se utiliza exclusivamente para el diagnóstico temporal de F1. No se sustituyen valores ni se agregan columnas al dataset cargado. La selección, imputación y transformación de una base analítica corresponden a F2.

## Pruebas de las funciones

Desde la raíz, con la `.venv` activa:

```powershell
python -m unittest discover -s tests -v
```

Las seis pruebas de `tests/test_reconocimiento.py` utilizan archivos temporales y datos sintéticos. Comprueban entradas normales, archivos ausentes o vacíos, variables sin información, una categoría constante, valores infinitos, diccionarios incompatibles, JSON no válido y fechas inconsistentes. También verifican que la lectura y el diagnóstico no alteren las entradas.

Las dos pruebas adicionales de `tests/test_trazabilidad_git.py` comprueban, mediante respuestas de Git simuladas, la identificación de la raíz con una ruta Unicode y el rechazo de una subcarpeta como raíz. La suite actual contiene **ocho pruebas** y debe finalizar con `OK`. Las pruebas simuladas comprueban el código; la rama y el commit reales se registran desde el notebook.

La ejecución realizada desde la terminal con `.venv` activa finalizó correctamente. Se registró el siguiente resumen:

```text
Ran 8 tests in 0.112s

OK
```

Este resultado corresponde a la suite completa de reconocimiento y trazabilidad ejecutada en la `.venv` del proyecto. La salida del clon nuevo se conserva en [pruebas_clon_limpio_f1.txt](../evidencias/pruebas_clon_limpio_f1.txt). El resultado inicial permanece en su archivo de evidencia anterior.

## Resultado de la ejecución revisada

El notebook guardado contiene ocho bloques de código ejecutados sin errores. Las salidas verifican:

- Kernel de la `.venv` del proyecto, Python 3.13.17 e importaciones correctas.
- Coincidencia del SHA-256 con la fuente documentada.
- 29.753 filas, 90 columnas, cero duplicados exactos y cero identificadores `id` repetidos.
- 14 columnas completamente vacías y 16 con más del 60 % de faltantes.
- 27.760 JSON con moneda ARS informada; 603 JSON sin moneda y 1.390 ausentes.
- Conservación del archivo original y de la tabla en memoria.
- Mensaje de generación de `docs/evidencias/reconocimiento_f1.json`.

### Trazabilidad de Git verificada

La salida actual de la consulta de Git confirmó:

- `disponible`: `True`.
- `rama`: `feature/f1-definicion-entorno`.
- `commit`: `539f48bee8e38d5e2880deee03e577e64b0fa5d1`.
- `cambios_sin_confirmar`: `False` al momento de la consulta en el clon nuevo.

La rama y el commit quedaron identificados desde el notebook. La consulta verifica el árbol de trabajo y su raíz mediante el prefijo relativo de Git. No modifica archivos ni el historial.

El indicador `False` señala que la consulta se realizó sin cambios pendientes en ese momento. Las nuevas salidas se guardaron después y se incorporaron mediante el commit `f368242`, cuyo envío a GitHub quedó confirmado.

La ejecución se guardó con **Ctrl + S** y se registraron los cambios del notebook y del JSON de reconocimiento. La salida del push confirmó el avance remoto de `539f48b` a `f368242`. El [registro de reproducción](../repositorio/reproduccion_clon_limpio_f1.md) documenta la comprobación desde el clon nuevo.

Para conservar la salida después de ejecutar el notebook, que crea la carpeta de evidencias:

```powershell
python -m unittest discover -s tests -v 2>&1 | Out-File -Encoding UTF8 docs/evidencias/pruebas_reconocimiento_f1.txt
Get-Content docs/evidencias/pruebas_reconocimiento_f1.txt
```

## Conservación de evidencias

Al completar todas las comprobaciones se genera `docs/evidencias/reconocimiento_f1.json`, con fecha de ejecución UTC, intérprete, versiones, estado de Git, huella del archivo y diagnósticos. El archivo se genera a partir de los resultados reales de la ejecución.

Guardar el notebook con sus salidas. No borrar los resultados antes de subirlo al repositorio. El notebook y la evidencia contienen información del intérprete y del sistema de archivos; su función es documentar la ejecución técnica, sin incorporar nombres personales a la narración del estudio.

## Resolución de incidencias

| Situación | Comprobación |
|---|---|
| Kernel fuera de `.venv` | Seleccionar el entorno del proyecto en el notebook y reiniciar. |
| Importación fallida o versión distinta | Comprobar el intérprete; instalar las dependencias desde ese entorno y repetir la ejecución completa. |
| Huella distinta | Revisar la procedencia y versión del archivo antes de continuar. |
| Diccionario y columnas diferentes | Confirmar que se usa el dataset y el diccionario del mismo avance. |
| Git no disponible | Comprobar su instalación y que VS Code abrió el repositorio completo; registrar la trazabilidad antes del cierre. |
| Ejecución parcial | Reiniciar el kernel, ejecutar todas las celdas y conservar las salidas nuevas. |

## Cierre del avance

Después de ejecutar y guardar, se registrarán en Git el notebook, las funciones, la documentación actualizada, el inventario de dependencias y la evidencia generada. La rama F1 permanece abierta hasta completar también el mapa conceptual y las verificaciones de la fase.
