"""Lectura y diagnóstico inicial de F1, sin modificar el dataset original."""

from __future__ import annotations

import hashlib
import importlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import Any

import numpy as np
import pandas as pd


def calcular_sha256(ruta: Path) -> str:
    """Calcular la huella del archivo sin cargarlo completo en memoria."""
    huella = hashlib.sha256()
    with Path(ruta).open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            huella.update(bloque)
    return huella.hexdigest()


def verificar_entorno(raiz: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Registrar intérprete, aislamiento y dependencias directas declaradas.

    Se admiten líneas de requirements.txt sin versión o fijadas mediante ==.
    Otras sintaxis se señalan para evitar validar restricciones parcialmente.
    """
    raiz = Path(raiz).resolve()
    requisitos = raiz / "requirements.txt"
    esperado = (raiz / ".venv").resolve()
    pip = subprocess.run(
        [sys.executable, "-m", "pip", "check"], capture_output=True,
        text=True, timeout=120, check=False,
    )
    entorno = pd.DataFrame([
        {"componente": "Python", "valor": platform.python_version()},
        {"componente": "Intérprete del kernel", "valor": sys.executable},
        {"componente": "Plataforma", "valor": platform.platform()},
        {"componente": "Entorno virtual activo", "valor": sys.prefix != sys.base_prefix},
        {"componente": "Kernel en .venv del proyecto", "valor": Path(sys.prefix).resolve() == esperado},
        {"componente": "Python de la serie 3.13", "valor": sys.version_info[:2] == (3, 13)},
        {"componente": "pip check correcto", "valor": pip.returncode == 0},
        {"componente": "Salida de pip check", "valor": (pip.stdout + pip.stderr).strip()},
    ])
    registros = []
    for numero, texto in enumerate(requisitos.read_text(encoding="utf-8-sig").splitlines(), 1):
        linea = texto.split("#", 1)[0].strip()
        if not linea:
            continue
        coincidencia = re.fullmatch(r"([A-Za-z0-9_.-]+)(?:==([A-Za-z0-9_.+!-]+))?", linea)
        if coincidencia is None:
            raise ValueError(f"Sintaxis de requisito no contemplada en línea {numero}: {linea}")
        nombre, fijada = coincidencia.groups()
        instalada = None
        error = ""
        try:
            instalada = version(nombre)
            importlib.import_module(nombre.replace("-", "_"))
        except (PackageNotFoundError, ImportError) as exc:
            error = f"{type(exc).__name__}: {exc}"
        registros.append({
            "dependencia": nombre, "declaracion": linea,
            "version_instalada": instalada, "importacion_correcta": not error,
            "version_fijada": fijada is not None,
            "cumple_declaracion": not error and (fijada is None or instalada == fijada),
            "observacion": error or ("Versión fijada" if fijada else "Versión sin fijar en requirements.txt"),
        })
    if not registros:
        raise ValueError("requirements.txt no contiene dependencias verificables.")
    return entorno, pd.DataFrame(registros)


def consultar_git(raiz: Path) -> dict[str, Any]:
    """Consultar la rama y el commit reales; no modifica el repositorio."""
    raiz = Path(raiz).resolve()

    def ejecutar(*argumentos: str) -> str:
        resultado = subprocess.run(
            ["git", "-C", str(raiz), *argumentos], capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=20, check=True,
        )
        return resultado.stdout.strip()

    try:
        if ejecutar("rev-parse", "--is-inside-work-tree") != "true":
            return {"disponible": False, "observacion": "La ubicación no corresponde a un árbol de trabajo Git."}
        # El prefijo vacío identifica la raíz sin comparar rutas impresas por Git.
        # Evita diferencias de representación, codificación o alias en Windows.
        if ejecutar("rev-parse", "--show-prefix"):
            return {"disponible": False, "observacion": "La raíz indicada no es la raíz del repositorio Git."}
        return {
            "disponible": True,
            "rama": ejecutar("branch", "--show-current") or "HEAD separado",
            "commit": ejecutar("rev-parse", "HEAD"),
            "cambios_sin_confirmar": bool(ejecutar("status", "--porcelain")),
        }
    except (OSError, subprocess.SubprocessError) as exc:
        return {"disponible": False, "observacion": f"No se pudo consultar Git: {type(exc).__name__}"}


def cargar_dataset(ruta: Path) -> pd.DataFrame:
    """Leer el CSV original comprimido, sin seleccionar ni transformar columnas."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el dataset: {ruta}")
    datos = pd.read_csv(ruta, sep=",", encoding="utf-8", compression="infer", low_memory=False)
    if datos.empty:
        raise ValueError("El dataset no contiene filas.")
    return datos


def huella_tabla(datos: pd.DataFrame) -> str:
    """Detectar cambios en valores, orden, columnas y tipos durante la ejecución."""
    metadatos = json.dumps(
        {"columnas": list(datos.columns), "tipos": [str(t) for t in datos.dtypes]},
        ensure_ascii=False,
    ).encode("utf-8")
    valores = pd.util.hash_pandas_object(datos, index=True).to_numpy().tobytes()
    return hashlib.sha256(metadatos + valores).hexdigest()


def resumir_dataset(datos: pd.DataFrame) -> pd.DataFrame:
    """Medir dimensiones, duplicados y cobertura general de la fuente leída."""
    if "id" not in datos:
        raise KeyError("Se requiere la columna id para reconocer la unidad de análisis.")
    return pd.DataFrame([
        {"indicador": "Filas", "valor": len(datos)},
        {"indicador": "Columnas", "valor": datos.shape[1]},
        {"indicador": "Filas duplicadas exactas", "valor": int(datos.duplicated().sum())},
        {"indicador": "Identificadores id ausentes", "valor": int(datos["id"].isna().sum())},
        {"indicador": "Identificadores id repetidos", "valor": int(datos["id"].duplicated().sum())},
        {"indicador": "Columnas completamente vacías", "valor": int(datos.isna().all().sum())},
        {"indicador": "Columnas con más de 60 % de faltantes", "valor": int((datos.isna().mean() > 0.60).sum())},
    ])


def perfilar_variables(datos: pd.DataFrame, ruta_diccionario: Path) -> pd.DataFrame:
    """Combinar el perfil observado con los roles del diccionario manual."""
    diccionario = pd.read_csv(ruta_diccionario, sep=";", encoding="utf-8-sig")
    requeridas = {"variable", "rol_analitico", "uso_propuesto", "base_definicion"}
    if not requeridas.issubset(diccionario.columns):
        raise ValueError(f"El diccionario requiere las columnas: {sorted(requeridas)}")
    if diccionario["variable"].duplicated().any():
        raise ValueError("El diccionario contiene nombres de variable repetidos.")
    if set(diccionario["variable"]) != set(datos.columns):
        raise ValueError("Las variables del dataset y del diccionario no coinciden.")
    registros = []
    for nombre in datos.columns:
        serie = datos[nombre]
        finitos = None
        if pd.api.types.is_numeric_dtype(serie):
            # NumPy cuenta valores finitos; esta vista diagnóstica no altera la serie.
            finitos = int(np.count_nonzero(np.isfinite(serie.to_numpy(dtype=float, na_value=np.nan))))
        registros.append({
            "variable": nombre, "tipo_leido": str(serie.dtype),
            "n_faltantes": int(serie.isna().sum()),
            "porcentaje_faltantes": float(100 * serie.isna().mean()),
            "valores_distintos": int(serie.nunique(dropna=True)),
            "n_numericos_finitos": finitos,
        })
    perfil = pd.DataFrame(registros)
    return perfil.merge(
        diccionario[["variable", "rol_analitico", "uso_propuesto", "base_definicion"]],
        on="variable", how="left", sort=False, validate="one_to_one",
    )


def observar_cotizaciones(datos: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Reconocer moneda y fechas en vistas temporales, sin limpiar la fuente."""
    necesarias = ["price", "price_quote_price_per_night", "price_quote_raw",
                  "price_quote_checkin_date", "price_quote_checkout_date", "last_scraped"]
    faltantes = set(necesarias) - set(datos.columns)
    if faltantes:
        raise KeyError(f"Faltan columnas para reconocer las cotizaciones: {sorted(faltantes)}")
    monedas: dict[str, int] = {}
    estados = {"JSON ausente": 0, "JSON no válido": 0, "Estructura inesperada": 0,
               "JSON con moneda informada": 0, "JSON sin moneda informada": 0}
    for valor in datos["price_quote_raw"]:
        if valor is None or (isinstance(valor, float) and np.isnan(valor)) or valor is pd.NA:
            estados["JSON ausente"] += 1
            continue
        try:
            objeto = json.loads(valor)
        except (TypeError, ValueError):
            estados["JSON no válido"] += 1
            continue
        cotizacion = objeto.get("quote") if isinstance(objeto, dict) else None
        if not isinstance(cotizacion, dict):
            estados["Estructura inesperada"] += 1
            continue
        moneda = cotizacion.get("currency")
        if not isinstance(moneda, str) or not moneda.strip():
            estados["JSON sin moneda informada"] += 1
        else:
            estados["JSON con moneda informada"] += 1
            monedas[moneda] = monedas.get(moneda, 0) + 1
    fechas = []
    vistas = {}
    for nombre in ["last_scraped", "price_quote_checkin_date", "price_quote_checkout_date"]:
        vista = pd.to_datetime(datos[nombre], format="%Y-%m-%d", errors="coerce")
        vistas[nombre] = vista
        fechas.append({
            "variable": nombre,
            "fecha_minima": None if vista.isna().all() else vista.min().date().isoformat(),
            "fecha_maxima": None if vista.isna().all() else vista.max().date().isoformat(),
            "n_ausentes_en_original": int(datos[nombre].isna().sum()),
            "n_no_interpretables_no_nulos": int((datos[nombre].notna() & vista.isna()).sum()),
        })
    noches = (vistas["price_quote_checkout_date"] - vistas["price_quote_checkin_date"]).dt.days
    resumen = [{"indicador": k, "valor": v} for k, v in estados.items()]
    resumen += [
        {"indicador": "price ausente", "valor": int(datos["price"].isna().sum())},
        {"indicador": "Precio numérico por noche ausente", "valor": int(datos["price_quote_price_per_night"].isna().sum())},
        {"indicador": "Estancias con duración calculable", "valor": int(noches.notna().sum())},
        {"indicador": "Estancias con duración no positiva", "valor": int((noches <= 0).sum())},
        {"indicador": "Duración mínima observada, noches", "valor": None if noches.isna().all() else float(noches.min())},
        {"indicador": "Duración máxima observada, noches", "valor": None if noches.isna().all() else float(noches.max())},
    ]
    return {
        "resumen": pd.DataFrame(resumen),
        "monedas": pd.DataFrame([{"moneda": k, "n_cotizaciones": v} for k, v in sorted(monedas.items())],
                                columns=["moneda", "n_cotizaciones"]),
        "fechas": pd.DataFrame(fechas),
    }


def tabla_a_registros(tabla: pd.DataFrame) -> list[dict[str, Any]]:
    """Obtener registros JSON con tipos nativos y ausencias representadas como null."""
    return json.loads(tabla.to_json(orient="records", force_ascii=False))


def guardar_evidencia(ruta: Path, contenido: dict[str, Any]) -> None:
    """Guardar documentación de ejecución; no genera ni sobrescribe datos procesados."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(contenido, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
