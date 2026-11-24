# Ejecución reproducible de F2

## Preparación

F1 se integró a `main` mediante el PR #1. F2 se desarrolla en `feature/f2-preprocesamiento`, desde el clon limpio del proyecto. Se mantienen las dependencias y la `.venv` verificadas en F1.

Copiar los archivos del paquete a la raíz del proyecto, conservando sus rutas. `README.md` actualiza el estado posterior al PR #1. El módulo y las pruebas de F1 se mantienen.

Agregar `/data/processed/` a `.gitignore`. El original continúa localmente en `data/raw/listings.csv.gz`, con la huella documentada. No es necesario volver a descargarlo.

```powershell
if (-not (Select-String -LiteralPath .gitignore -Pattern '^/data/processed/$' -Quiet)) { Add-Content -LiteralPath .gitignore -Value "`n/data/processed/" }
git check-ignore -v -- data/raw/listings.csv.gz data/processed/comprobacion_f2.csv
```

El primer bloque del notebook exige que ambas rutas estén ignoradas y que no existan archivos de datos rastreados, salvo marcadores `.gitkeep`.

## Ejecución en VS Code

1. Abrir `F2/F2_Preprocesamiento.ipynb`.
2. Seleccionar la `.venv` del proyecto como kernel, igual que en F1. La activación en la terminal no sustituye la selección del kernel.
3. Abrir **Ctrl + Shift + P** y ejecutar **Jupyter: Restart Kernel and Run All Cells**.
4. Esperar todas las celdas; las salidas aparecen debajo de cada bloque de código.
5. Revisar que los controles indiquen `True`, que la suite termine en `OK` y que la fuente permanezca inmutable.
6. Guardar el notebook con **Ctrl + S**, conservando sus salidas.

La suite se ejecuta desde el notebook y conserva su salida en un archivo. Incluye las ocho pruebas de F1 y diez adicionales de F2; si se mantienen todas, el total esperado es 18.

El flujo no utiliza muestreo ni operaciones aleatorias: las reglas y los desempates son deterministas.

## Salidas

| Ruta | Contenido | Distribución |
| --- | --- | --- |
| `data/processed/base_cotizaciones_f2.csv` | Cotizaciones elegibles con variables analíticas y marcas. | Local; fuera de Git. |
| `data/processed/cohorte_principal_f2.csv` | Fecha exacta y duración elegidas por cobertura. | Local; fuera de Git. |
| `data/processed/cohorte_sensibilidad_f2.csv` | Mismo mes y duración para sensibilidad. | Local; fuera de Git. |
| `data/processed/indicadores_tipo_f2.csv` | Id e indicadores one-hot del tipo de alojamiento. | Local; fuera de Git. |
| `docs/datos/preprocesamiento_f2.md` | Resultados, decisiones, límites y relación con objetivos. | Git. |
| `docs/datos/f2/` | Tablas agregadas de diagnóstico, cobertura y validación. | Git. |
| `docs/evidencias/preprocesamiento_f2.json` | Versiones, Git, controles y huellas de salidas locales. | Git. |
| `docs/evidencias/pruebas_preprocesamiento_f2.txt` | Salida real de la suite ejecutada en el proyecto. | Git. |

El informe de referencia incluido en el paquete se obtuvo en el entorno de preparación, con Python 3.12.14, pandas 2.2.3 y NumPy 2.3.5, sobre una copia con el mismo SHA-256. No sustituye la ejecución en Windows con Python 3.13.17 ni sus salidas.

## Verificación antes de registrar el avance

```powershell
git status --short
git ls-files -- data/raw/ data/processed/
```

La segunda consulta no debe listar archivos de datos; puede conservar marcadores `.gitkeep`. No se usa `git add .` para este avance.

Tras comprobar las salidas, actualizar el estado de F2 en el README a «ejecutada y verificada localmente», sin declarar terminados el informe, F3 ni F4. Registrar el avance en un commit descriptivo e integrarlo a main mediante PR al cerrar F2.
