# Creación del repositorio — Grupo 8 MCDI500

Se creó el repositorio proyecto-grupo8-mcdi500 para organizar el proyecto de la asignatura Programación para la Ciencia de Datos de la Universidad Andrés Bello. El procedimiento se realizó desde PowerShell en Windows.

## Inicialización local

Se ingresó a la carpeta del proyecto y se inicializó Git con la rama principal main.

```powershell
cd proyecto-grupo8-mcdi500
git init -b main
```

Se configuraron el nombre y el correo del autor para este repositorio.

```powershell
git config --local user.name "Carlos Vergara Andraes"
git config --local user.email "carlos.santiago.vergara.andraes@gmail.com"
```

Se verificaron la identidad del autor y la cuenta autenticada en GitHub.

```powershell
git config --get user.name
git config --get user.email
gh api user --jq .login
```

La cuenta autenticada correspondía a carlos-santiago-vergara-andraes.

## Estructura inicial

Se incorporaron las carpetas F1, F2, F3 y F4 para organizar las fases del proyecto. Los directorios `data/raw` y `data/processed` se destinaron a los datos originales y procesados. Las carpetas docs y src se reservaron para documentación y módulos de Python.

Se agregaron archivos `.gitkeep` vacíos para registrar las carpetas sin contenido. También se incorporaron `README.md`, `.gitignore`, `requirements.txt` y `validar_dataset.py`.

Durante la revisión de src, PowerShell informó que `src/.gitkeep` ya existía. Se conservó el archivo y se agregó al área de preparación con `git add src/.gitkeep`.

## Primer commit

Se revisó el estado del repositorio y se prepararon los archivos para el primer commit.

```powershell
git status
git add .
git diff --cached --stat
git status
```

Se registró la estructura inicial.

```powershell
git commit -m "docs: creación estructura inicial proyecto grupo 8 MCDI500"
```

El commit recibió el identificador abreviado `8666070`. Se incorporaron 12 archivos y 261 líneas. La consulta posterior con `git status` indicó que el directorio de trabajo estaba limpio.

## Creación del repositorio remoto

Se ejecutó el asistente de GitHub CLI.

```powershell
gh repo create
```

Se creó un repositorio privado llamado proyecto-grupo8-mcdi500 bajo la cuenta carlos-santiago-vergara-andraes. La descripción utilizada fue “Proyecto académico MCDI500 — Análisis de datos con Python, Jupyter y Git.”

Se seleccionó la creación sin README ni `.gitignore` remotos, dado que ambos archivos estaban registrados localmente. Se omitió la clonación porque la carpeta de trabajo ya existía.

## Publicación del primer commit

Se conectó el repositorio local con el remoto origin y se publicó la rama main.

```powershell
git remote add origin https://github.com/carlos-santiago-vergara-andraes/proyecto-grupo8-mcdi500.git
git branch -M main
git push -u origin main
```

La salida confirmó la publicación de main y su configuración para seguir a `origin/main`.

El repositorio quedó disponible en la siguiente dirección.

https://github.com/carlos-santiago-vergara-andraes/proyecto-grupo8-mcdi500

Las versiones del software, la instalación de dependencias y las comprobaciones del entorno se registrarán conforme se realicen esas actividades.
