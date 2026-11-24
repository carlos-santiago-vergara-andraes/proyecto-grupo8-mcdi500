# Obtención local y verificación del dataset

## Política de distribución

El dataset original de Inside Airbnb se conserva localmente en `data/raw/listings.csv.gz` y no se distribuye dentro del repositorio. El archivo incluye nombres públicos, enlaces e información de perfiles que no son necesarios para difundir el código y la documentación del estudio. El repositorio conserva la procedencia, licencia, huella de integridad, diccionario y resultados agregados de reconocimiento.

Esta política corresponde al ajuste solicitado en la retroalimentación docente. Su implementación se verificará mediante el estado de Git y la revisión del historial; este documento no acredita que la limpieza ya esté ejecutada.

## Recurso seleccionado

- Proveedor: Inside Airbnb.
- Ámbito: Buenos Aires, Argentina.
- Archivo: `listings.csv.gz`.
- Recurso identificado por la ruta: `2026-09-23`.
- Descarga local registrada: 22 de noviembre de 2026, 23:27:27.
- Licencia indicada por el proveedor: Creative Commons Attribution 4.0 International (CC BY 4.0), con atribución.
- Catálogo y licencia: https://insideairbnb.com/get-the-data/
- Enlace exacto: https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz

SHA-256 comprobado en el reconocimiento de F1:

```text
c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a
```

## Descarga en un clon limpio

Desde la raíz del proyecto en Windows PowerShell, cuando el archivo todavía no existe:

```powershell
New-Item -ItemType Directory -Force .\data\raw | Out-Null
Invoke-WebRequest -Uri "https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz" -OutFile .\data\raw\listings.csv.gz
$huellaEsperadaDataset = "c8db6461c06c0de3efbdda6821d6d28c9aef7dff3c6fde64ac4fd3661e15b78a"
$huellaObtenidaDataset = (Get-FileHash .\data\raw\listings.csv.gz -Algorithm SHA256).Hash
if ($huellaObtenidaDataset -ne $huellaEsperadaDataset) { throw "La huella del dataset no coincide con la fuente documentada." }
```

Si el archivo ya se encuentra disponible, basta con comprobar su huella; no se vuelve a descargar ni se reemplaza el original:

```powershell
Get-FileHash .\data\raw\listings.csv.gz -Algorithm SHA256
```

Después de la verificación se reconstruye la `.venv` y se ejecuta el notebook siguiendo [ejecucion_f1.md](../entorno/ejecucion_f1.md). La creación de `data/raw/` forma parte de la obtención local, ya que una carpeta ignorada no se incorpora al clonar el repositorio.

## Ajuste de Git

Se añadirá esta regla al `.gitignore` existente, conservando sus demás reglas:

```gitignore
/data/raw/
```

La retirada del índice conserva el archivo en el equipo. Antes de aplicarla se revisará `git status` y se confirmarán las rutas seguidas por Git. La eliminación del archivo del índice y su exclusión futura son distintas de la limpieza histórica.

La limpieza del historial se realizará sobre una copia de trabajo preparada para ese fin, con un respaldo fuera del repositorio publicado. Se identificarán las ramas y etiquetas afectadas y las rutas anteriores del archivo, si las hubiera. El archivo también debe desaparecer de esas referencias; limpiar únicamente la rama actual no permite acreditar la retirada histórica completa.

Los identificadores de commits afectados cambian al reescribir el historial. Las referencias de ejecución previas se conservarán como registros históricos y se contrastarán con las nuevas referencias. Después de la limpieza se volverá a ejecutar F1 y se revisarán las salidas antes de integrar a `main` mediante Pull Request. No se reutilizarán copias antiguas para volver a publicar el historial retirado.

## Verificación de cierre

- El dataset permanece disponible localmente y su SHA-256 coincide.
- Git ignora `data/raw/` y no sigue el archivo original.
- El historial de las ramas y etiquetas publicadas se revisó tras la limpieza.
- Los notebooks y archivos de documentación no muestran nombres, enlaces de perfiles ni registros individuales de anfitriones.
- Un clon limpio obtiene el archivo desde el recurso oficial y ejecuta F1.
- La evidencia actualizada identifica las referencias reales posteriores a la limpieza.

La retirada de las referencias publicadas no demuestra por sí sola que desaparezcan copias ajenas o vistas conservadas por el servicio de alojamiento. Cualquier referencia adicional encontrada se tratará conforme a la documentación de GitHub.

## Texto para incorporar al README

El siguiente bloque se incorporará en la sección del dataset, sustituyendo las afirmaciones que indiquen que el original se distribuye con Git:

> El archivo original se conserva localmente en `data/raw/listings.csv.gz` y se excluye del control de versiones. Se obtiene desde el recurso oficial de Inside Airbnb para Buenos Aires identificado como `2026-09-23`. La reproducción requiere descargarlo y verificar el SHA-256 documentado antes de ejecutar los notebooks. El procedimiento y las condiciones de uso se describen en [Obtención local del dataset](docs/datos/obtencion_dataset.md).

En el README también deberán figurar el enlace exacto de descarga, la huella completa y la licencia CC BY 4.0 indicados en este documento. La política se marcará como implementada después de comprobar el índice y el historial, sin anticipar esa verificación.

## Criterios que se aplicarán en F2

La comparación de `price` y `price_quote_price_per_night` registrará el número de anuncios con cada campo, el solapamiento, las diferencias de cobertura y la concordancia tras interpretar el formato monetario. La elección de una variable se justificará con esos resultados y con la confirmación de moneda.

Las comparaciones de precios en ARS se delimitarán por fecha de estancia cotizada y duración. Se evaluará la cobertura de una misma ventana y duración o, si corresponde, se presentarán resultados separados por tramos de fecha. No se considerarán equivalentes cotizaciones temporalmente heterogéneas. La ventana se elegirá documentando soporte de muestra y cobertura, sin seleccionarla a partir de un resultado de precios preferido.

El informe incluirá el perfil de faltantes de las variables efectivamente utilizadas y una correspondencia entre cada objetivo y las secciones del notebook que aportan su evidencia. Las decisiones conservarán la distinción entre planificación, ejecución y resultados observados.

## Referencias

Inside Airbnb. (2026). *Buenos Aires: Detailed listings* [Conjunto de datos; recurso identificado como 2026-09-23]. https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz

Inside Airbnb. (s. f.). *Get the data*. https://insideairbnb.com/get-the-data/

GitHub. (s. f.). *Removing sensitive data from a repository*. https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

Newren, E. (s. f.). *git-filter-repo documentation*. https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt
