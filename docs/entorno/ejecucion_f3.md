# Ejecución de F3 — Núcleo algorítmico, eficiencia y orientación a objetos

## Requisitos

- Entorno `.venv` del proyecto, Python de la serie 3.13 y dependencias ya fijadas.
- Original local `data/raw/listings.csv.gz` con la huella registrada.
- Base elegible y grupos principal y adicional generados por F2 en `data/processed/`.
- Evidencia `docs/evidencias/preprocesamiento_f2.json` con sus huellas.
- Las carpetas `data/raw/` y `data/processed/` deben continuar excluidas de Git.

No se requieren paquetes nuevos. F3 no reemplaza los notebooks ni los archivos de F2.

## Inicio de la rama

Con el cierre de F1/F2 integrado y el árbol de trabajo limpio:

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/f3-nucleo-algoritmico
```

Copiar las carpetas y el README del paquete en la raíz del proyecto, respetando sus
rutas. No se incluyen archivos de datos ni `.venv`. Si `F3/.gitkeep` existe, eliminarlo
al incorporar el notebook; las carpetas vacías conservan sus marcadores.

## Comprobación previa

Desde la raíz del proyecto, con el entorno activo:

```powershell
python -m unittest discover -s tests
```

El conjunto preparado contiene **29 pruebas**: 18 anteriores y 11 de F3. Las pruebas
automatizadas usan datos sintéticos; la ejecución del notebook agrega el contraste
con el archivo real y con los CSV de F2.

## Notebook

1. Abrir `F3/F3_Nucleo_Algoritmico.ipynb` en VS Code.
2. Seleccionar el kernel de `.venv`, cuya ruta termina en `.venv\Scripts\python.exe`.
3. Ejecutar **Jupyter: Restart Kernel and Run All Cells** y esperar el término.
4. Comprobar diez celdas de código numeradas del 1 al 10 y ausencia de errores.
5. Revisar la equivalencia F2/F3, los casos límite y las mediciones.
6. Guardar con **Ctrl + S**.

Los conteos esperados para el archivo documentado son 27.633 anuncios elegibles,
2.080 en el grupo principal y 5.039 en el adicional. Los tiempos se medirán en el
equipo y pueden diferir de la referencia. Los límites y la ventana aprendidos quedan
registrados; las pruebas verifican que las copias externas no puedan alterarlos.

## Resultados y evidencias

Las salidas individuales se guardan localmente en `data/processed/`, con nombres
terminados en `_f3.csv`; no deben agregarse a Git. Las evidencias agregadas quedan en:

- `docs/evidencias/f3/resultados_f3.json`: entorno, Git, parámetros, controles y decisión.
- `docs/evidencias/f3/mediciones.csv`: tiempo mínimo, mediano y máximo, y pico de memoria.
- `docs/evidencias/f3/repeticiones.csv`: tiempos de cada repetición.
- `docs/evidencias/f3/validacion.csv`: comprobaciones del conjunto real.
- `docs/evidencias/f3/casos_verificacion.csv`: casos normales, límite y excepciones.
- `docs/evidencias/f3/etapas.csv`: filas y columnas por etapa.
- `docs/evidencias/f3/resumen_*.csv`: resúmenes agregados del grupo principal.
- `docs/evidencias/f3/huellas_entradas_f2.csv`: integridad de las referencias.
- `docs/evidencias/f3/pruebas_f3.txt`: salida de las pruebas.

La subcarpeta `docs/evidencias/f3/referencia_linux/` contiene únicamente la verificación
de preparación. Su método y las diferencias de entorno se explican en su README.
No debe utilizarse para atribuir tiempos al equipo Windows ni sustituir las salidas
principales del notebook.

## Informe y publicación

El informe institucional F3 debe utilizar los resultados locales guardados, incluir
la arquitectura y el patrón aplicado y explicar el compromiso entre tiempo y memoria.
La correspondencia con los once criterios está en `F3/verificacion_rubrica.md`.
Después se registrarán los cambios en la rama y se integrarán a `main` mediante PR.
No se declara completada la fase antes del informe y de esa integración.
