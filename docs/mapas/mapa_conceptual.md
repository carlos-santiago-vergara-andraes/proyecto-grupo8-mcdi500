# Mapa conceptual: herramientas colaborativas y flujo reproducible

**Airbnb Buenos Aires | Fase 1: definición y orientación de la situación**

- **Institución:** Universidad Andrés Bello
- **Programa:** Magíster en Ciencia de Datos e Inteligencia Artificial
- **Asignatura:** MCDI500 - Programación para la Ciencia de Datos
- **Autor:** Carlos Santiago Vergara Andraes
- **Docente:** Omar Salinas
- **Fecha:** 24 de noviembre de 2026

## Problema y datos

¿Cómo varía el precio cotizado por noche en ARS según barrio, tipo y capacidad, considerando fecha y duración de estancia?

Inside Airbnb: 29.753 anuncios y 90 variables en listings.csv.gz. Unidad de análisis: anuncio. Licencia: CC BY 4.0 (Inside Airbnb, 2026). Variables numéricas, nominales, binarias, fechas y texto; incluye faltantes.

## Reflexión técnica

Se conserva el original y se vinculan funciones, notebooks y commits para que cada decisión tenga evidencia. Git registra versiones y GitHub permite revisar e integrar cambios (Chacon y Straub, 2014).

Se descarta imputar precios en la comparación principal: produciría tarifas no observadas. F2 deberá justificar faltantes, extremos y comparabilidad de fechas y noches. Se asumen moneda confirmada y categorías interpretables.

## Leyenda

- Azul oscuro: proyecto.
- Azul claro: etapas del flujo.
- Granate claro: herramientas y entorno.
- Gris: datos, documentos y evidencias.
- Recuadros: conceptos.
- Flechas continuas: relaciones etiquetadas.
- Flechas discontinuas granates: retornos por diagnóstico o validación.

## Commits proyectados

- `feat(f2): preparar datos y registrar reglas`.
- `test(f2): verificar casos y consistencia`.
- `docs: incorporar resultados y referencias`.

Los mensajes registrarán el motivo y el impacto de cada decisión. La integración a main se realizará mediante Pull Request.

## Referencias

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/en/v2

Inside Airbnb. (2026). *Buenos Aires: Detailed listings* [Conjunto de datos; recurso 2026-09-23]. https://data.insideairbnb.com/argentina/ciudad-aut%C3%B3noma-de-buenos-aires/buenos-aires/2026-09-23/data/listings.csv.gz

## Mapa conceptual

```mermaid
flowchart TB
    P["Proyecto reproducible: Airbnb Buenos Aires"]
    D["Inside Airbnb: Buenos Aires, CC BY 4.0"]
    F["F1: definición del problema y precio por noche en ARS"]
    E["Entorno: Python 3.13, .venv, requirements.txt y requirements.lock.txt"]
    R["Original local inmutable: data/raw/ fuera de Git y SHA-256"]
    C["F1: carga, perfil y diccionario de variables"]
    L["Librerías científicas: pandas, NumPy y funciones en src/"]
    G["Git: control de versiones, commits y ramas"]
    B["F2: preparación, limpieza y transformación"]
    J["Jupyter: F1/ y F2/ con código, narrativa, salidas y referencias APA 7"]
    I[".gitignore: exclusión de data/raw/, .venv y credenciales"]
    S["Datos procesados: data/processed/"]
    M["Documentación: README para reproducción; docs/ para decisiones y APA 7"]
    H["GitHub: repositorio remoto y Pull Request hacia main"]
    A["Fases posteriores: análisis, evaluación y comunicación"]
    T["Validación y pruebas: tests/ y docs/evidencias/"]
    P -- "requiere" --> D
    P -- "delimita" --> F
    P -- "se reproduce con" --> E
    P -- "se versiona con" --> G
    D -- "se adquiere como" --> R
    F -- "orienta" --> C
    E -- "configura" --> L
    R -- "alimenta" --> C
    L -- "sustentan" --> C
    L -- "se usan en" --> J
    C -- "fundamenta" --> B
    C -. "reorienta" .-> F
    C -- "se narra en" --> J
    G -- "versiona" --> C
    G -- "versiona" --> B
    G -- "excluye según" --> I
    G -- "sincroniza con" --> H
    J -- "documenta" --> B
    J -- "enlaza" --> M
    B -- "genera" --> S
    S -- "alimenta" --> A
    B -- "se valida con" --> T
    T -. "corrige" .-> B
    T -- "aportan evidencia a" --> M
    classDef root fill:#1F3A5F,stroke:#1F3A5F,color:#FFFFFF
    classDef stage fill:#EDF3F9,stroke:#1F3A5F,color:#172331
    classDef tool fill:#FCF0F2,stroke:#AA182C,color:#172331
    classDef artifact fill:#F2F4F6,stroke:#596575,color:#172331
    class P root
    class F,C,B,A stage
    class E,L,G,J,H tool
    class D,R,I,S,M,T artifact
    linkStyle 11,22 stroke:#AA182C,stroke-width:2px
```
