# Retiro del dataset original del historial publicado

## Propósito y alcance

Se ajustó la distribución de la fuente de Inside Airbnb conforme a la retroalimentación docente. El archivo original incluye nombres públicos, enlaces e información de perfiles de anfitriones. Su obtención se mantiene desde el proveedor; el repositorio conserva el código, la documentación y las evidencias agregadas.

El ajuste comprende la exclusión de `data/raw/`, la retirada del CSV del índice y la reescritura de las referencias históricas que contenían esa ruta. La fecha de registro del procedimiento es el 24 de noviembre de 2026.

## Conservación y respaldo

Antes de la reescritura se creó un respaldo fuera del repositorio publicado:

- Archivo `repositorio.bundle`, verificado mediante `git bundle verify`.
- Resultado de la verificación: respaldo válido, con historial completo disponible en el momento de su creación y cinco referencias registradas.
- Copia adicional del archivo original `listings.csv.gz`.

Se comprobó que el CSV permanecía en el equipo mediante `Test-Path`, con resultado `True`. La regla `/data/raw/` quedó incorporada al `.gitignore`; `git check-ignore -v` confirmó su aplicación. La retirada del índice se realizó mediante `git rm --cached`, conservando el archivo local.

El respaldo contiene el historial previo y se mantiene fuera del repositorio publicado. No debe incorporarse mediante otra rama, etiqueta o archivo de respaldo en GitHub.

## Método aplicado

La limpieza se realizó en un clon independiente creado mediante `git clone --mirror`, con git-filter-repo 2.47.0 instalado en un entorno auxiliar separado del entorno científico del proyecto.

Se aplicó el filtrado por ruta:

```text
git-filter-repo --invert-paths --path data/raw/
```

El filtro reescribió las referencias afectadas sin incorporar la ruta excluida. La herramienta informó que procesó 14 commits y terminó la reescritura y compactación sin errores. Las ramas `main` y `feature/f1-definicion-entorno` se conservaron.

## Referencias antes y después

### Rama `feature/f1-definicion-entorno`

- Antes del filtrado: `e9cb2dc1fec8ed72c2b4193d0833933f5dfe4eda`.
- Después del filtrado: `539f48bee8e38d5e2880deee03e577e64b0fa5d1`.

### Rama `main`

- Antes del filtrado: `8666070d18ce7f433e9afee20873285a09bbc7c0`.
- Después del filtrado: `1bcf2be00feb2596e4e3e6d65983feb409beb8c6`.

Los identificadores cambiaron por la reescritura del historial. Los identificadores anteriores conservados en registros de ejecución corresponden al estado previo del repositorio y se interpretan en ese contexto. La evidencia posterior debe registrar las referencias efectivas de la nueva ejecución.

## Comprobaciones realizadas

1. En la copia filtrada, `git log --all --oneline -- data/raw/` no devolvió resultados.
2. `git show-ref --heads` mostró las dos ramas con sus nuevas referencias.
3. Después de publicar el historial corregido, `git ls-remote --heads origin` mostró los mismos identificadores para ambas ramas:

```text
539f48bee8e38d5e2880deee03e577e64b0fa5d1 refs/heads/feature/f1-definicion-entorno
1bcf2be00feb2596e4e3e6d65983feb409beb8c6 refs/heads/main
```

Estas comprobaciones acreditan la concordancia entre las ramas locales filtradas y las ramas publicadas consultadas. No equivalen a una revisión de copias ajenas, bifurcaciones o vistas en caché del servicio de alojamiento.

## Reproducción y continuidad

El trabajo continuará desde un clon nuevo del historial corregido. El archivo original se copiará desde la fuente local conservada o se descargará siguiendo [obtencion_dataset.md](../datos/obtencion_dataset.md). Antes de ejecutar los notebooks se comprobará su SHA-256:

```text
c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a
```

La reproducción se realizó en un clon nuevo del mismo equipo, con un entorno virtual reconstruido desde `requirements.lock.txt`. Las ocho pruebas finalizaron con `OK` en 0,112 segundos y la ejecución actualizada de F1 se registró y envió a GitHub mediante el commit `f368242`. El [registro de reproducción](reproduccion_clon_limpio_f1.md) identifica las evidencias correspondientes.

La limpieza histórica no integra el contenido de F1 a `main`: esa integración sigue pendiente y se realizará mediante Pull Request antes de la entrega. Los cambios posteriores de documentación se registrarán mediante un nuevo commit.

## Síntesis para comunicar el ajuste

Se excluyó el dataset original del control de versiones y se conservó localmente. El README documenta el recurso exacto de descarga, la licencia y la huella SHA-256. Se limpió la ruta `data/raw/` del historial en una copia independiente, con respaldo verificado, y se comprobó que las referencias publicadas de ambas ramas coinciden con la versión filtrada. La reproducción desde un clon limpio quedó registrada en `f368242`. La integración mediante Pull Request permanece pendiente para el cierre de F1.

## Referencias

GitHub. (s. f.). *Removing sensitive data from a repository*. https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

Newren, E. (s. f.). *git-filter-repo documentation*. https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt
