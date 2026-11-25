# Ejecución reproducible de F2

## Preparación

F1 y F2 se integraron a `main` mediante los PR #1 y #2. F2 se desarrolló en `feature/f2-preprocesamiento`, desde el clon limpio del proyecto. Se mantienen las dependencias y la `.venv` verificadas en F1.

Clonar la rama main y mantener las rutas del repositorio. Los módulos y pruebas de F1 se reutilizan en F2.

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
| `data/processed/grupo_principal_f2.csv` | Fecha exacta y duración elegidas por cobertura. | Local; fuera de Git. |
| `data/processed/grupo_sensibilidad_f2.csv` | Mismo mes y duración para sensibilidad. | Local; fuera de Git. |
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

## Estado verificado

F2 se ejecutó en Windows con Python 3.13.17, pandas 3.1.0 y NumPy 2.5.4. Los diez bloques finalizaron en orden, con 18 pruebas aprobadas en 0,656 segundos y quince controles satisfactorios. Se conservaron 27.633 anuncios elegibles, 2.080 en el grupo exacto y 5.039 en la ampliación mensual. El avance se registró en 23ab86c y se integró mediante PR #2.

La reproducción independiente desde main en Linux ejecutó todas las celdas de ambos notebooks mediante IPython, con un espacio de nombres nuevo por notebook y las mismas dependencias directas. Su método, inventario y salidas se conservan en docs/evidencias/replica_linux/. F3 y F4 permanecen pendientes.
