# Configuración del entorno de desarrollo — Grupo 8 MCDI500

## 1. Propósito

Se configuró un entorno de desarrollo para el proyecto de la asignatura Programación para la Ciencia de Datos (MCDI500). La preparación comprendió la creación de un entorno virtual, la instalación de las dependencias y la comprobación del intérprete y las librerías de análisis de datos.

Fecha de registro: 20 de noviembre de 2026.

## 2. Configuración del proyecto

Se utiliza Windows PowerShell como terminal y Visual Studio Code como editor. El entorno virtual `.venv` se encuentra en la raíz de `proyecto-grupo8-mcdi500`.

| Componente | Configuración registrada |
|---|---|
| Python | 3.13.17 |
| Entorno virtual | `.venv` |
| Intérprete del proyecto | `.venv\Scripts\python.exe` |
| pip | 26.2.2, según el registro de instalación |
| NumPy | 2.5.4 |
| pandas | 3.1.0 |
| ipykernel | 7.4.0 |
| JupyterLab | 4.6.6 |
| Notebook | 7.6.5 |

Las versiones de las dependencias se obtuvieron del registro de instalación. Las versiones de NumPy y pandas se comprobaron adicionalmente mediante su importación desde el intérprete del entorno virtual.

## 3. Creación y activación del entorno virtual

Desde la raíz del proyecto se ejecutaron los siguientes comandos:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

El entorno virtual mantiene las dependencias del proyecto aisladas de las bibliotecas instaladas en otros entornos. Su configuración se apoya en la instalación base de Python utilizada para crearlo.

La activación incorpora el indicador `(.venv)` a la terminal y prioriza los ejecutables del entorno. Para comprobar la versión y la ubicación del intérprete se ejecutó:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

Se obtuvo Python 3.13.17 y una ruta correspondiente a `.venv\Scripts\python.exe` dentro del proyecto.

La activación se realiza en cada nueva sesión de PowerShell que deba utilizar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

La desactivación se realiza mediante:

```powershell
deactivate
```

## 4. Selección del intérprete en Visual Studio Code

Se seleccionó `.venv` como entorno de Python del proyecto en Visual Studio Code. La selección de `.venv\Scripts\python.exe` permite utilizar Python 3.13.17 y las dependencias instaladas para el proyecto.

La selección se realizó mediante la paleta de comandos:

1. Apertura de la paleta con Ctrl + Shift + P.
2. Ejecución de **Python: Select Interpreter**.
3. Selección de `.venv\Scripts\python.exe`.

La configuración del intérprete del editor y la selección del kernel de un notebook son independientes. La comprobación del kernel se realizará cuando se ejecute el cuaderno correspondiente.

## 5. Instalación y verificación de dependencias

Las dependencias declaradas en `requirements.txt` se instalaron desde el entorno virtual:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

La instalación finalizó con el mensaje `Successfully installed`. La comprobación de dependencias produjo el siguiente resultado:

```text
No broken requirements found.
```

Este resultado indica que pip no detectó conflictos en las dependencias declaradas por los paquetes instalados. La verificación funcional del análisis de datos requiere ejecutar posteriormente los scripts y notebooks del proyecto.

Para comprobar las importaciones y las versiones principales se ejecutó:

```powershell
python -c "import sys, pandas, numpy; print(sys.executable); print('pandas:', pandas.__version__); print('NumPy:', numpy.__version__)"
```

La ruta del intérprete correspondió al entorno virtual del proyecto. Las versiones informadas fueron:

```text
pandas: 3.1.0
NumPy: 2.5.4
```

Las dos bibliotecas se importaron sin errores.

## 6. Reconstrucción del entorno

La carpeta `.venv` se reconstruye en cada equipo. Su exclusión del control de versiones debe indicarse mediante la entrada `.venv/` en el archivo `.gitignore`.

Con Python 3.13 disponible, la preparación del entorno desde la raíz del proyecto se realiza mediante:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

En el archivo de dependencias registrado, NumPy y pandas tienen versiones fijadas. Las entradas de ipykernel, JupyterLab y Notebook no incluyen una versión específica. El inventario del anexo identifica las versiones instaladas durante la preparación.

Para conservar un archivo adicional con las versiones de los paquetes instalados puede ejecutarse:

```powershell
python -m pip freeze > requirements-lock.txt
```

La reconstrucción a partir de ese archivo, una vez generado y versionado, se realiza mediante:

```powershell
python -m pip install -r requirements-lock.txt
```

Estos comandos se incluyen como procedimiento de reproducción. La generación de `requirements-lock.txt` y la ejecución en un segundo equipo no se registran como verificaciones realizadas.

## 7. Estado de la configuración

La configuración base del entorno quedó preparada para ejecutar scripts Python desde la terminal del proyecto. Se comprobaron:

- Python 3.13.17 y la ruta del intérprete dentro de `.venv`.
- La creación y activación del entorno virtual.
- La selección del intérprete del proyecto en Visual Studio Code.
- La instalación de las dependencias.
- La comprobación de dependencias mediante `pip check`.
- La importación de pandas 3.1.0 y NumPy 2.5.4.

La incorporación del dataset y la ejecución de `validar_dataset.py` corresponden a la siguiente etapa. La ejecución del notebook con el kernel del proyecto y la reproducción en otro equipo se comprobarán durante el desarrollo de los entregables.

## Anexo. Inventario de dependencias instaladas

El registro de instalación identificó 93 paquetes, incluidas las dependencias directas y auxiliares.


| Paquete | Versión instalada |
|---|---|
| anyio | 4.16.0 |
| argon2-cffi | 25.1.0 |
| argon2-cffi-bindings | 26.2.0 |
| arrow | 1.4.0 |
| asttokens | 3.0.2 |
| async-lru | 2.4.0 |
| attrs | 26.1.0 |
| babel | 2.18.0 |
| beautifulsoup4 | 4.15.0 |
| bleach | 6.4.0 |
| certifi | 2026.10.23 |
| cffi | 2.1.1 |
| charset_normalizer | 3.5.2 |
| colorama | 0.4.6 |
| comm | 0.2.3 |
| debugpy | 1.8.22 |
| defusedxml | 0.7.1 |
| executing | 2.3.0 |
| fastjsonschema | 2.22.3 |
| fqdn | 1.6.0 |
| h11 | 0.16.0 |
| httpcore | 1.0.9 |
| httpx | 0.28.1 |
| idna | 3.20 |
| ipykernel | 7.4.0 |
| ipython | 9.18.1 |
| ipython-pygments-lexers | 1.1.1 |
| isoduration | 20.11.0 |
| jedi | 0.20.1 |
| jinja2 | 3.1.6 |
| json5 | 0.17.3 |
| jsonpointer | 3.12 |
| jsonschema | 4.26.0 |
| jsonschema-specifications | 2025.9.1 |
| jupyter-builder | 1.3.0 |
| jupyter-client | 8.10.0 |
| jupyter-core | 5.9.1 |
| jupyter-events | 0.12.1 |
| jupyter-lsp | 2.3.1 |
| jupyter-server | 2.21.1 |
| jupyter-server-terminals | 0.5.4 |
| jupyterlab | 4.6.6 |
| jupyterlab-pygments | 0.3.0 |
| jupyterlab-server | 2.28.1 |
| lark | 1.3.1 |
| MarkupSafe | 3.0.4 |
| matplotlib-inline | 0.2.2 |
| mistune | 3.4.0 |
| nbclient | 0.11.0 |
| nbconvert | 7.17.2 |
| nbformat | 5.11.1 |
| nest-asyncio2 | 1.7.4 |
| notebook | 7.6.5 |
| notebook-shim | 0.2.4 |
| numpy | 2.5.4 |
| packaging | 26.3 |
| pandas | 3.1.0 |
| pandocfilters | 1.5.1 |
| parso | 0.8.7 |
| platformdirs | 4.14.7 |
| prometheus-client | 0.26.0 |
| prompt_toolkit | 3.0.53 |
| psutil | 7.2.2 |
| pure-eval | 0.2.4 |
| pycparser | 3.12 |
| pygments | 2.21.0 |
| python-dateutil | 4.0.0 |
| python-json-logger | 4.2.0 |
| pywinpty | 3.1.2 |
| pyyaml | 6.0.3 |
| pyzmq | 27.3.0 |
| referencing | 0.37.0 |
| requests | 2.34.2 |
| rfc3339-validator | 0.1.4 |
| rfc3986-validator | 0.1.1 |
| rfc3987-syntax | 1.1.0 |
| rpds-py | 2026.9.1 |
| send2trash | 2.2.0 |
| six | 1.17.0 |
| soupsieve | 4.1.2 |
| stack_data | 0.6.3 |
| terminado | 0.18.1 |
| tinycss2 | 1.5.1 |
| tornado | 6.6.1 |
| traitlets | 5.16.1 |
| typing_extensions | 4.16.0 |
| tzdata | 2026.6 |
| uri-template | 1.3.0 |
| urllib3 | 2.8.0 |
| wcwidth | 0.9.4 |
| webcolors | 25.10.0 |
| webencodings | 0.6.1 |
| websocket-client | 1.9.2 |

## Referencias técnicas

- Python Software Foundation. *venv — Creation of virtual environments*. https://docs.python.org/3.13/library/venv.html
- Python Software Foundation. *Using Python on Windows*. https://docs.python.org/3.13/using/windows.html
- NumPy. *NumPy 2.5.4*. https://pypi.org/project/numpy/2.5.4/
- pandas. *pandas 3.1.0*. https://pypi.org/project/pandas/3.1.0/
- Project Jupyter. *ipykernel*. https://pypi.org/project/ipykernel/
- Project Jupyter. *JupyterLab*. https://pypi.org/project/jupyterlab/
- Project Jupyter. *Notebook*. https://pypi.org/project/notebook/
