# Reproducción de F1 desde un clon limpio

## Alcance de la comprobación

Se clonó la rama `feature/f1-definicion-entorno` después de la limpieza histórica y se creó una nueva `.venv` desde Python 3.13. Las dependencias se instalaron utilizando `requirements.lock.txt`. La comprobación corresponde a un clon y un entorno independientes en el mismo equipo Windows.

El dataset se conservó como archivo local en `data/raw/listings.csv.gz`. La comprobación de exclusión mostró la regla `/data/raw/` del `.gitignore`; su presencia en el disco no implica su publicación en GitHub. El notebook utiliza la huella SHA-256 documentada para identificar la fuente.

## Pruebas de las funciones

Se ejecutó desde el nuevo proyecto:

```powershell
python -m unittest discover -s tests -v
```

Resultado registrado:

```text
Ran 8 tests in 0.112s

OK
```

La [salida completa](../evidencias/pruebas_clon_limpio_f1.txt) conserva los ocho casos. Los casos de Git incluyen respuestas simuladas para comprobar la lógica del código; la identificación del repositorio real se verificó mediante la celda de trazabilidad del notebook.

## Ejecución y trazabilidad

Se ejecutó `F1/F1_Definicion.ipynb` siguiendo el procedimiento de reiniciar el kernel y ejecutar todas las celdas. La consulta de Git registró:

- `disponible`: `True`.
- `rama`: `feature/f1-definicion-entorno`.
- `commit`: `539f48bee8e38d5e2880deee03e577e64b0fa5d1`.
- `cambios_sin_confirmar`: `False` al momento de esa consulta.

La comprobación de Git ocurre antes de guardar las nuevas salidas y de generar el JSON final. Después de guardar se identificaron dos archivos modificados: el notebook y `docs/evidencias/reconocimiento_f1.json`. Ambos se registraron en el commit `f368242`, con mensaje `test(f1): registrar reproducción desde clon limpio`.

La salida del push confirmó el avance remoto de `539f48b` a `f368242` en la rama F1. Por ello, el commit consultado durante la ejecución y el commit que conserva sus resultados son referencias distintas y coherentes con el orden de trabajo.

## Evidencias conservadas

- [Notebook F1 ejecutado](../../F1/F1_Definicion.ipynb).
- [JSON de reconocimiento](../evidencias/reconocimiento_f1.json).
- [Salida de las ocho pruebas en el clon nuevo](../evidencias/pruebas_clon_limpio_f1.txt).
- [Inventario de dependencias](../../requirements.lock.txt).
- [Registro del retiro del dataset del historial](retiro_dataset_historial.md).

## Continuidad

La reproducción de F1 desde el nuevo entorno quedó registrada. El mapa conceptual, su vinculación técnica y los registros de cierre se incorporarán en un commit posterior. La integración a `main` se realizará mediante Pull Request. La preparación del dataset y la comparación de precios pertenecen a F2; las fases posteriores se desarrollarán conforme a sus instrucciones.
