"""Resumen descriptivo equivalente por bucle y groupby; medición reproducible."""
from __future__ import annotations

import timeit
import tracemalloc
from typing import Callable

import numpy as np
import pandas as pd


def _validar_resumen(datos: pd.DataFrame, variable: str) -> None:
    if not isinstance(datos, pd.DataFrame):
        raise TypeError('Se requiere un pandas.DataFrame.')
    if datos.empty or not datos.columns.is_unique:
        raise ValueError('Se requiere una tabla no vacía con columnas únicas.')
    faltan = {variable, 'precio_ars_noche'} - set(datos.columns)
    if faltan:
        raise ValueError(f'Faltan columnas: {sorted(faltan)}')
    if datos[variable].isna().any():
        raise ValueError('La agrupación requiere categorías sin faltantes.')
    precio = datos['precio_ars_noche']
    if not pd.api.types.is_numeric_dtype(precio) or not np.isfinite(precio).all() or not precio.gt(0).all():
        raise ValueError('El precio debe ser numérico, finito y positivo.')


def resumen_por_bucle(datos: pd.DataFrame, variable: str = 'barrio') -> pd.DataFrame:
    """Versión inicial: filtrar una vez por grupo y calcular sus cuartiles."""
    _validar_resumen(datos, variable)
    filas = []
    for grupo in sorted(datos[variable].unique()):
        precios = datos.loc[datos[variable].eq(grupo), 'precio_ars_noche']
        filas.append({variable: grupo, 'n': len(precios),
                      'mediana_ARS': float(precios.median()),
                      'q1_ARS': float(precios.quantile(.25)),
                      'q3_ARS': float(precios.quantile(.75)),
                      'grupo_menor_30': len(precios) < 30})
    return pd.DataFrame(filas)


def resumen_vectorizado(datos: pd.DataFrame, variable: str = 'barrio') -> pd.DataFrame:
    """Versión candidata: agrupar una vez, sin filtrar la tabla por cada grupo."""
    _validar_resumen(datos, variable)
    grupos = datos.groupby(variable, observed=True, sort=True)['precio_ars_noche']
    resultado = grupos.agg(n='size', mediana_ARS='median')
    resultado['q1_ARS'] = grupos.quantile(.25)
    resultado['q3_ARS'] = grupos.quantile(.75)
    return resultado.reset_index().assign(grupo_menor_30=lambda x: x['n'] < 30)


def comprobar_resumenes(a: pd.DataFrame, b: pd.DataFrame) -> None:
    """Grupos/conteos exactos e importes con tolerancia absoluta de 1e-7 ARS.

    Series.quantile y GroupBy.quantile pueden diferir en el redondeo binario.
    No se usa tolerancia relativa ni se redondean precios antes de calcular.
    """
    if list(a.columns) != list(b.columns):
        raise AssertionError('Los resúmenes tienen columnas u orden distintos.')
    importes = ['mediana_ARS', 'q1_ARS', 'q3_ARS']
    pd.testing.assert_frame_equal(a.drop(columns=importes), b.drop(columns=importes),
                                  check_exact=True, check_dtype=False)
    np.testing.assert_allclose(a[importes].to_numpy(dtype=float),
                               b[importes].to_numpy(dtype=float), rtol=0, atol=1e-7)


def _pico_python(funcion: Callable[[], pd.DataFrame]) -> int:
    if tracemalloc.is_tracing():
        raise RuntimeError('Detener el trazado previo de memoria antes de medir.')
    tracemalloc.start()
    try:
        funcion()
        return tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()


def comparar_implementaciones(datos: pd.DataFrame, variable: str = 'barrio',
                             tamanos: tuple[int, ...] | None = None,
                             repeticiones: int = 5, ejecuciones: int = 3,
                             semilla: int = 2026) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Medir equivalencia, tiempo y memoria sobre las mismas submuestras.

    Incluye el tamaño real, calienta ambas versiones y alterna el orden de medición.
    timeit separa tiempo de tracemalloc para no confundir sus sobrecostos.
    """
    _validar_resumen(datos, variable)
    if (not isinstance(repeticiones, int) or not isinstance(ejecuciones, int)
            or repeticiones < 3 or ejecuciones < 1):
        raise ValueError('Se requieren al menos tres repeticiones y una ejecución.')
    if tamanos is not None and any(not isinstance(n, int) or n < 1 for n in tamanos):
        raise ValueError('Los tamaños deben ser enteros positivos.')
    tamanos = sorted({min(n, len(datos)) for n in (tamanos or (250, 2080, len(datos)))})
    if len(datos) not in tamanos:
        tamanos.append(len(datos))
    orden = np.random.default_rng(semilla).permutation(len(datos))
    versiones = {'bucle': resumen_por_bucle, 'vectorizada': resumen_vectorizado}
    registros, resumen = [], []
    for n in tamanos:
        muestra = datos.iloc[orden[:n]].copy()
        comprobar_resumenes(resumen_por_bucle(muestra, variable),
                           resumen_vectorizado(muestra, variable))
        funciones = {k: (lambda fn=v: fn(muestra, variable)) for k, v in versiones.items()}
        for funcion in funciones.values():
            funcion()  # Calentamiento, excluido de los resultados.
        for repeticion in range(repeticiones):
            nombres = list(funciones) if repeticion % 2 == 0 else list(reversed(funciones))
            for nombre in nombres:
                segundos = timeit.repeat(funciones[nombre], repeat=1, number=ejecuciones)[0] / ejecuciones
                registros.append({'filas': n, 'grupos': muestra[variable].nunique(),
                                  'version': nombre, 'repeticion': repeticion + 1,
                                  'ejecuciones_por_repeticion': ejecuciones,
                                  'segundos_por_ejecucion': segundos})
        for nombre in funciones:
            tiempos = [r['segundos_por_ejecucion'] for r in registros
                       if r['filas'] == n and r['version'] == nombre]
            picos = [_pico_python(funciones[nombre]) for _ in range(3)]
            resumen.append({'filas': n, 'grupos': muestra[variable].nunique(),
                            'version': nombre, 'tiempo_min_ms': min(tiempos) * 1000,
                            'tiempo_mediana_ms': float(np.median(tiempos)) * 1000,
                            'tiempo_max_ms': max(tiempos) * 1000,
                            'pico_python_mediana_MiB': float(np.median(picos)) / 1024**2,
                            'resumenes_equivalentes': True})
    return pd.DataFrame(resumen), pd.DataFrame(registros)
