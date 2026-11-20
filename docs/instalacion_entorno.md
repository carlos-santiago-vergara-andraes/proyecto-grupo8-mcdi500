# Preparación del entorno de desarrollo — Grupo 8 MCDI500

## Revisión inicial

El 20 de noviembre de 2026 se revisaron las instalaciones de Python disponibles en el equipo desde Windows PowerShell, antes de preparar el entorno del proyecto.

Se ejecutaron los siguientes comandos.

```powershell
py --list-paths
python --version
python -m pip --version
python -m pip list
git --version
gh --version
```

El lanzador identificó instalaciones de Python 3.14 y Python 3.12. El comando `python` ejecutaba Python 3.14.7 y utilizaba pip 26.2.1. En esa instalación estaban disponibles NumPy 2.5.2 y pandas 3.0.5.

| Componente | Resultado observado |
|---|---|
| Python activo | 3.14.7 |
| Python adicional | Serie 3.12; versión de mantenimiento sin comprobar |
| pip asociado a Python 3.14 | 26.2.1 |
| NumPy asociado a Python 3.14 | 2.5.2 |
| pandas asociado a Python 3.14 | 3.0.5 |
| Git | 2.34.1.windows.1 |
| GitHub CLI | 2.32.1 |

## Editor de desarrollo

Se utiliza Visual Studio Code (VS Code) para editar los archivos del proyecto, trabajar con la terminal integrada y revisar la documentación Markdown. Su versión está pendiente de registrar.

Para trabajar con los notebooks se comprobarán las extensiones Python y Jupyter de Microsoft, el intérprete seleccionado y el kernel de cada cuaderno.

| Componente | Estado |
|---|---|
| Visual Studio Code | En uso; versión pendiente de registrar |
| Extensión Python de Microsoft | Instalación y versión pendientes de comprobar |
| Extensión Jupyter de Microsoft | Instalación y versión pendientes de comprobar |
| Intérprete del proyecto en VS Code | Pendiente de seleccionar y verificar |
| Kernel de los notebooks | Pendiente de seleccionar y verificar |

La versión de VS Code se consultará en Ayuda → Acerca de. Las versiones de las extensiones se consultarán en su panel de detalles.

## Decisión de configuración

Se decidió preparar una instalación limpia y conservar una única versión de Python en el equipo para simplificar la selección del intérprete, la instalación de dependencias y la configuración del kernel de Jupyter.

Se mantiene la serie Python 3.13, utilizada en el ejemplo de ejecución de la guía docente. La propuesta de pasar a Python 3.14 se revisó al comprobar que las dependencias fijadas también publican paquetes para Python 3.13 en Windows de 64 bits.

Python 3.13.17 dispone de un instalador oficial de Windows de 64 bits. Python 3.13.18 es posterior e incorpora correcciones de seguridad; su página oficial indica que se distribuye únicamente como código fuente. Se registra Python 3.13.17 como candidato para la instalación mediante el ejecutable oficial y se deja constancia de que existe una versión de mantenimiento posterior.

La versión finalmente instalada se registrará después de ejecutar el instalador y comprobar el intérprete.
El script `validar_dataset.py` utiliza pandas para leer, perfilar y evaluar el conjunto de datos. También emplea `pd.to_datetime` con `format="mixed"`, disponible desde pandas 2.0. La comprobación del validador se realizará con las dependencias declaradas en el proyecto y un archivo de datos real.

La compatibilidad del entorno completo se confirmará mediante la instalación de dependencias, sus importaciones y la ejecución del validador.

## Instalación prevista

Se retirarán las instalaciones anteriores desde la administración de aplicaciones de Windows. Se prevé utilizar el instalador oficial de Python 3.13.17 de 64 bits, con pip y el lanzador de Python habilitados. La versión instalada se confirmará desde la consola.

Tras la instalación se registrarán la fecha, la ruta del intérprete y las versiones obtenidas mediante los siguientes comandos.

```powershell
py --list-paths
py -3.13 --version
py -3.13 -m pip --version
```

Se creará un entorno virtual `.venv` dentro del proyecto. Las dependencias y Jupyter se instalarán en ese entorno, y el kernel del notebook se configurará para utilizar su intérprete.

## Registro de la instalación y las verificaciones

Al completar la instalación se incorporarán los resultados observados en la siguiente tabla.

| Comprobación | Resultado |
|---|---|
| Fecha de instalación | Pendiente |
| Versiones anteriores retiradas | Pendiente de verificar |
| Versión completa de Python instalada | Pendiente |
| Arquitectura de Python | Pendiente |
| Ruta de instalación de Python | Pendiente |
| Opciones seleccionadas en el instalador | Pendiente |
| Comandos de creación y activación de `.venv` | Pendiente de registrar |
| Ruta del intérprete de `.venv` | Pendiente |
| Versión de pip dentro de `.venv` | Pendiente |
| Versiones de las dependencias instaladas | Pendiente |
| Importación de las librerías del proyecto | Pendiente |
| Comprobación de dependencias con `python -m pip check` | Pendiente |
| Ejecución de una celda en Jupyter con el kernel del proyecto | Pendiente |
| Ejecución de `validar_dataset.py` y archivo utilizado | Pendiente |
| Informe generado por el validador | Pendiente |

Las versiones efectivamente instaladas se reflejarán también en `requirements.txt`. Las instrucciones de reconstrucción del entorno se incorporarán al README. Se registrarán los ajustes aplicados, su motivo y la comprobación posterior.

La ejecución del validador se documentará indicando si logró leer y evaluar el archivo, junto con los requisitos cumplidos y los avisos detectados. La evaluación del dataset y la comprobación de funcionamiento del entorno tendrán sus respectivos resultados.

## Comprobación previa de disponibilidad y dependencias

Se consultó el instalador oficial `python-3.13.17-amd64.exe`. El servidor respondió HTTP 200 y declaró un tamaño de 29.941.280 bytes.

Se realizó una resolución simulada con pip para CPython 3.13, plataforma win_amd64 y paquetes binarios, usando las cinco dependencias del requirements.txt. La resolución finalizó con código de salida 0 y seleccionó los siguientes paquetes principales.

| Paquete | Versión seleccionada en la simulación |
|---|---|
| ipykernel | 7.4.0 |
| jupyterlab | 4.6.6 |
| notebook | 7.6.5 |
| numpy | 2.5.4 |
| pandas | 3.1.0 |

La simulación se realizó desde un entorno distinto al equipo Windows de desarrollo. La disponibilidad de paquetes y la resolución comprobadas respaldan la instalación propuesta. El conjunto final de dependencias, incluidas las específicas de Windows, se confirmará durante la instalación real. La ejecución de Jupyter, las importaciones y el validador siguen pendientes.

## Estado del registro

La revisión inicial y la decisión de configuración están documentadas. La desinstalación de las versiones anteriores, la instalación de Python 3.13, la creación del entorno virtual y las comprobaciones del validador están pendientes de confirmación.

Este documento se actualizará con los resultados de cada paso realizado.

## Incorporación al informe técnico

Este registro respalda el apartado de reproducibilidad técnica del informe. La siguiente redacción describe el estado actual del trabajo.

Durante la preparación del entorno se identificaron instalaciones de Python 3.14 y 3.12 en el equipo. El intérprete activo correspondía a Python 3.14.7, con pip 26.2.1, NumPy 2.5.2 y pandas 3.0.5. Se mantiene la serie Python 3.13 y se verificó la disponibilidad del instalador oficial de Python 3.13.17 de 64 bits, junto con paquetes de NumPy 2.5.4 y pandas 3.1.0 para esa serie. Se registró que Python 3.13.18 es posterior y se publica como código fuente. Se utiliza Visual Studio Code como editor y se prevé configurar sus extensiones Python y Jupyter para trabajar con el entorno virtual del proyecto. El funcionamiento se comprobará mediante importaciones, la selección del kernel de Jupyter y la ejecución de `validar_dataset.py` sobre el conjunto de datos seleccionado. Los resultados de estas verificaciones se incorporarán al informe una vez completadas.

Al cerrar la instalación, este párrafo se actualizará con las versiones confirmadas, las pruebas ejecutadas y sus resultados. Los campos pendientes conservarán ese estado hasta completar su comprobación.

## Referencias técnicas

Python Software Foundation. Python 3.13.17.

https://www.python.org/downloads/release/python-31317/

Python Software Foundation. Python 3.13.18.

https://www.python.org/downloads/release/python-31318/

NumPy. Distribuciones de NumPy 2.5.4.

https://pypi.org/project/numpy/2.5.4/

pandas. Distribuciones de pandas 3.1.0.

https://pypi.org/project/pandas/3.1.0/

Python Software Foundation. Using Python on Windows.

https://docs.python.org/3.13/using/windows.html

The pandas development team. What’s new in pandas 2.0.0.

https://pandas.pydata.org/docs/whatsnew/v2.0.0.html

Project Jupyter. Paquetes de ipykernel, JupyterLab y Notebook.

https://pypi.org/project/ipykernel/

https://pypi.org/project/jupyterlab/

https://pypi.org/project/notebook/
