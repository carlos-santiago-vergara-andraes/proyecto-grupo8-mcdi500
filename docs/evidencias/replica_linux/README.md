# Reproducción independiente de F1 y F2 en Linux

## Origen y alcance

Se clonó la rama `main` del repositorio público del proyecto en un entorno Linux distinto del equipo Windows local. El commit verificado fue `cb2e42e53583430ca717162640be83cf197f5412`, correspondiente a la integración del PR #2 de F2. La verificación se realizó el 24 de noviembre de 2026.

Se creó una `.venv` nueva y se instalaron las cinco dependencias directas fijadas en `requirements.txt`. El intérprete independiente fue Python 3.13.5; el equipo Windows había utilizado Python 3.13.17. pandas 3.1.0, NumPy 2.5.4, ipykernel 7.4.0, JupyterLab 4.6.6 y Notebook 7.6.5 coinciden con las versiones directas declaradas.

La entrada fue una copia con SHA-256 `c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a`. Los datos originales y procesados permanecieron locales y no se incluyen en esta carpeta.

## Método de ejecución

Se ejecutaron secuencialmente todas las celdas de código mediante IPython, con un espacio de nombres nuevo para cada notebook y el directorio de trabajo en la raíz del clon. La verificación comprueba el procesamiento fuera del equipo Windows; no corresponde a una segunda sesión de VS Code ni a un servidor Jupyter. Los notebooks guardados incorporan este método explícitamente en sus metadatos.

- F1: ocho bloques ejecutados sin errores.
- F2: diez bloques ejecutados sin errores.
- Suite: 18 pruebas aprobadas en 0,313 segundos.
- Controles de F2: quince satisfactorios.
- Resultados: 27.633 anuncios elegibles, 2.080 en el grupo principal y 5.039 en la ampliación mensual.
- Las catorce tablas agregadas de F2 coinciden con las de Windows, comparadas con tolerancia relativa 1e-10 y absoluta 1e-8, sin exigir igualdad de tipos de almacenamiento.

La huella de entrada es idéntica. Las huellas de CSV derivados se registran por ejecución; su identidad byte a byte no se presupone entre plataformas con convenciones distintas de salto de línea. La equivalencia de resultados se comprobó mediante tablas y valores numéricos.

## Archivos

- `F1_Definicion.ipynb` y `F2_Preprocesamiento.ipynb`: copias de evidencia de esta ejecución independiente; no sustituyen los notebooks principales de F1/ y F2/.
- `verificacion_reproduccion.json`: commit, método, versiones, entrada y resultados.
- `reconocimiento_f1.json` y `preprocesamiento_f2.json`: evidencia independiente de las funciones ejecutadas.
- `pruebas_preprocesamiento_f2.txt`: salida real de la suite en Linux.
- `requirements_linux.txt`: inventario transitivo específico de este entorno. No reemplaza el inventario Windows del proyecto.

Las evidencias se mantienen separadas para conservar su procedencia y evitar confundir plataformas o intérpretes.
