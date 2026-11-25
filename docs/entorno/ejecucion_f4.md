# Ejecución e integración de F4

## Entorno y entradas

F4 utiliza Python 3.13 y la `.venv` del proyecto. Se incorpora Matplotlib 3.10.8 a
las cinco dependencias directas utilizadas en F1–F3. El archivo
`requirements.lock.txt` conserva el inventario histórico de Windows de esas fases;
la instalación actual se realiza desde `requirements.txt`. Cada ejecución de F4
guarda su propio inventario completo en `requirements_ejecucion.txt`.

Desde la raíz del repositorio, con la `.venv` activa:

```powershell
python -m pip install -r requirements.txt
python -m pip check
python -c "import sys, matplotlib; print(sys.executable); print(matplotlib.__version__)"
python -m unittest discover -s tests
```

Se requieren los tres CSV finales de F3 en
`data/processed/` y `docs/evidencias/f3/resultados_f3.json` de la misma ejecución.
Los nombres de los CSV son `base_cotizaciones_f3.csv`, `grupo_principal_f3.csv`
y `grupo_sensibilidad_f3.csv`. El notebook verifica sus huellas antes de graficar.
La falta de un archivo o una discrepancia detiene la ejecución; no se reemplazan
los datos ni se cambian las huellas para eludir la comprobación. Si los CSV no se
conservan, deben recuperarse de la ejecución de F3; F4 no los regenera. El original
no es una entrada obligatoria de F4; si está disponible, se comprueba su huella.

## Notebook en VS Code

1. Abrir `F4/F4_Integracion_Comunicacion.ipynb`.
2. Seleccionar **Select Kernel → Python Environments → .venv** del proyecto.
3. Ejecutar **Jupyter: Restart Kernel and Run All Cells**.
4. Revisar las once celdas de código, las tres figuras, las 42 pruebas y los 20
   controles; las salidas aparecen debajo de cada celda. Un error detiene el cierre.
5. Guardar con **Ctrl+S**, conservando las salidas.

La ejecución habitual usa el modo `proyecto` y la evidencia F3 del equipo.
`MCDI500_F4_MODO` no necesita definirse. Si se había usado una sesión de referencia:

```powershell
Remove-Item Env:MCDI500_F4_MODO -ErrorAction SilentlyContinue
```

## Salidas y conservación

- `docs/datos/f4/`: seis tablas agregadas, incluidos hallazgos y cobertura.
- `docs/figuras/f4/`: tres PNG de 300 dpi, con unidades, leyenda y fuente.
- `docs/evidencias/f4/`: resultados JSON, controles, pruebas, mediciones e inventario
  del entorno de la ejecución habitual.
- `docs/evidencias/f4/referencia_linux/`: evidencia independiente de preparación.

El notebook no escribe en `data/raw/` ni `data/processed/`, no sobrescribe los
notebooks anteriores y comprueba nuevamente las huellas al finalizar. La equivalencia
F2/F3 se consulta en el registro previo, sin repetir el preprocesamiento.
Los gráficos se alimentan de los CSV finales de F3 ya verificados.

Los CSV por anuncio permanecen fuera de Git. Las figuras y tablas publicables no
incluyen identificadores de anuncios o anfitriones, nombres, enlaces de perfiles
ni coordenadas. Las categorías y el precio en ARS permanecen interpretables.

## Identificación de las evidencias incluidas

Las salidas distribuidas de F4 provienen de Linux, Python 3.13.5, y de un proceso
IPython nuevo que ejecutó las once celdas originales en orden. El entorno impidió
iniciar los sockets de Jupyter; esa comprobación no se presenta como ejecución
Jupyter ni como ejecución en Windows. El archivo
`referencia_linux/entradas_f3.json` identifica las huellas efectivas de los CSV
reconstruidos en Linux a partir del mismo original y de las clases de F3.

Las huellas binarias de CSV pueden diferir entre plataformas por serialización;
la equivalencia numérica se comprueba con las tolerancias documentadas en F2.
La evidencia original Windows de F3 se conserva sin modificaciones. El modo
`referencia_linux` identifica este procedimiento de manera explícita y dirige
su evidencia a una subcarpeta diferenciada.
