# F3 — Verificación de preparación en Linux

Esta carpeta registra la verificación del código preparado para F3. No sustituye
la ejecución principal del notebook en el equipo Windows del proyecto.

## Método y alcance

- Punto de partida: `main` en `06a4c5a66b5cd7b59e463c4144b0cc66dcae3643`.
- Fuente original con SHA-256 `c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a`.
- Python 3.13.5, pandas 3.1.0 y NumPy 2.5.4; dependencias directas de `requirements.txt`.
- Diez celdas de código ejecutadas en orden mediante IPython, sin servidor Jupyter
  ni interfaz VS Code. No se presenta como Restart Kernel and Run All Cells.
- El entorno Python disponible para la verificación se reutilizó; no se afirma
  que esta prueba haya instalado un entorno nuevo.
- Los tres CSV de referencia se reprodujeron con las funciones originales de F2
  sobre la misma fuente, en Linux. Sus huellas están en `insumos_f2_reproducidos.json`.
  No son los bytes originales de los CSV Windows. Las diferencias de serialización
  y finales de línea pueden producir otras huellas entre sistemas.
- El notebook de referencia cambia únicamente el destino de evidencias, la ruta
  del manifiesto de esos insumos y la descripción del contexto de ejecución.
- No se modificaron los archivos ni las evidencias de F1/F2 del repositorio.

## Resultados observados

- Base elegible: 27.633 anuncios; grupo principal: 2.080; grupo adicional: 5.039.
- Vista y base idénticas en memoria a las producidas por las funciones de F2.
- Los tres resultados coinciden con los CSV F2 reproducidos, con las tolerancias
  de lectura declaradas en F2.
- 29 pruebas aprobadas y 23 controles satisfactorios.
- La versión vectorizada fue seleccionada con las mediciones de este entorno;
  las métricas completas se conservan en `mediciones.csv` y `repeticiones.csv`.

Los importes de los resúmenes se cotejan con `rtol=0` y tolerancia absoluta de
`1e-7 ARS` por diferencias de redondeo binario en los cuartiles. Los grupos, conteos
y su orden se verifican exactamente; no se redondean precios antes del cálculo.

La suite, el notebook ejecutado, los parámetros, las tablas agregadas y el inventario
Linux se conservan en esta carpeta. Los datos por anuncio permanecen fuera de Git.
La ejecución local pendiente generará las evidencias principales directamente en
`docs/evidencias/f3/` y podrá producir otros tiempos.
