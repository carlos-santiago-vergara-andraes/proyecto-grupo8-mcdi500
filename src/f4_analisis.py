"""F4: cargar resultados de F3 y construir resúmenes interpretables sin limpiarlos."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.f3_medicion import resumen_vectorizado
from src.preprocesamiento import validar_base
from src.reconocimiento import calcular_sha256

ARCHIVOS_F3 = {
    'base': 'base_cotizaciones_f3.csv',
    'principal': 'grupo_principal_f3.csv',
    'sensibilidad': 'grupo_sensibilidad_f3.csv',
}
TIPOS_ES = {
    'Entire home/apt': 'Alojamiento completo',
    'Private room': 'Habitación privada',
    'Shared room': 'Habitación compartida',
    'Hotel room': 'Habitación de hotel',
}


def verificar_grupos(tablas: dict[str, pd.DataFrame], parametros: dict) -> pd.DataFrame:
    """Exigir el contrato de F2/F3 y que los grupos sean subconjuntos exactos.

    Las tolerancias se limitan a la serialización CSV (rtol=1e-12, atol=1e-7).
    La ventana proviene de F3: F4 no vuelve a elegirla ni elimina valores extremos.
    """
    for rol in ARCHIVOS_F3:
        if rol not in tablas:
            raise ValueError(f'Falta el resultado de F3: {rol}.')
        validar_base(tablas[rol])
    base = tablas['base']
    entrada = pd.Timestamp(parametros['entrada'])
    noches = int(parametros['noches'])
    if noches <= 0 or entrada.strftime('%Y-%m') != parametros['mes']:
        raise ValueError('Los parámetros de F3 no definen una ventana coherente.')
    mascaras = {
        'principal': base['entrada'].eq(entrada) & base['noches'].eq(noches),
        'sensibilidad': base['entrada'].dt.strftime('%Y-%m').eq(parametros['mes'])
                        & base['noches'].eq(noches),
    }
    controles = []
    for rol, mascara in mascaras.items():
        esperado = base.loc[mascara].sort_values('id').reset_index(drop=True)
        observado = tablas[rol].sort_values('id').reset_index(drop=True)
        pd.testing.assert_frame_equal(esperado, observado, check_dtype=False,
                                      check_exact=False, rtol=1e-12, atol=1e-7)
        controles.append({'control': f'{rol}_conserva_valores_y_seleccion_F3', 'cumple': True})
    controles.append({'control': 'principal_contenido_en_ampliacion_mensual',
                     'cumple': set(tablas['principal']['id']).issubset(tablas['sensibilidad']['id'])})
    if not all(c['cumple'] for c in controles):
        raise ValueError('Los grupos no conservan la relación registrada en F3.')
    return pd.DataFrame(controles)


def cargar_resultados_f3(raiz: Path, evidencia: Path | None = None
                         ) -> tuple[dict[str, pd.DataFrame], dict, pd.DataFrame]:
    """Requerir los CSV locales y sus huellas reales; nunca descargar sustitutos."""
    raiz = Path(raiz)
    evidencia = Path(evidencia) if evidencia else raiz / 'docs/evidencias/f3/resultados_f3.json'
    manifiesto = json.loads(evidencia.read_text(encoding='utf-8-sig'))
    huellas = manifiesto['sha256_salidas_locales']
    tablas, controles = {}, []
    for rol, nombre in ARCHIVOS_F3.items():
        archivo = raiz / 'data/processed' / nombre
        if not archivo.is_file():
            raise FileNotFoundError(f'Falta {archivo.name}. Ejecutar F3 y conservar sus CSV locales.')
        if huellas.get(nombre) != calcular_sha256(archivo):
            raise ValueError(f'SHA-256 distinto del registrado en F3: {nombre}.')
        tablas[rol] = pd.read_csv(archivo, dtype={'id': 'string', 'host_id': 'string'},
                                 parse_dates=['fecha_extraccion', 'entrada', 'salida'])
        controles.append({'control': f'sha256_F3_{rol}', 'cumple': True})
    parametros = manifiesto['parametros']['SelectorGrupoComparable']
    contrato = verificar_grupos(tablas, parametros)
    return tablas, manifiesto, pd.concat([pd.DataFrame(controles), contrato], ignore_index=True)


def _resumen(datos: pd.DataFrame, variable: str) -> pd.DataFrame:
    return resumen_vectorizado(datos, variable).drop(columns='grupo_menor_30')


def preparar_resumenes(tablas: dict[str, pd.DataFrame], minimo_grupo: int = 30) -> dict[str, pd.DataFrame]:
    """Agrupar precios en ARS originales; umbral por cobertura, no por resultado.

    La comparación de barrios fija tipo completo y capacidad 2. La comparación
    temporal fija tipo completo y muestra capacidades con n suficiente en ambos
    grupos. El grupo mensual contiene al principal: no son muestras independientes.
    """
    if isinstance(minimo_grupo, bool) or not isinstance(minimo_grupo, int) or minimo_grupo < 1:
        raise ValueError('minimo_grupo debe ser un entero positivo.')
    base, principal, mensual = (tablas[k] for k in ('base', 'principal', 'sensibilidad'))
    for tabla in (base, principal, mensual):
        validar_base(tabla)
    tipos = _resumen(principal, 'tipo_alojamiento')
    tipos['etiqueta'] = tipos['tipo_alojamiento'].map(TIPOS_ES)
    tipos['grupo_pequeno'] = tipos['n'].lt(minimo_grupo)
    completos = principal.loc[principal['tipo_alojamiento'].eq('Entire home/apt')]
    comparables = completos.loc[completos['capacidad'].eq(2)]
    if comparables.empty:
        raise ValueError('No hay alojamientos completos de capacidad 2 para comparar barrios.')
    barrios = _resumen(comparables, 'barrio')
    barrios['incluido_en_grafico'] = barrios['n'].ge(minimo_grupo)
    if not barrios['incluido_en_grafico'].any():
        raise ValueError('Ningún barrio alcanza la cobertura mínima; no se fabrica un gráfico.')
    capacidades = []
    for grupo, tabla in [('principal', completos), ('mensual', mensual.loc[mensual['tipo_alojamiento'].eq('Entire home/apt')])]:
        resumen = _resumen(tabla, 'capacidad')
        capacidades.append(resumen.assign(grupo=grupo))
    capacidades = pd.concat(capacidades, ignore_index=True)
    soporte = capacidades.pivot(index='capacidad', columns='grupo', values='n')
    seleccion = soporte.index[soporte.reindex(columns=['principal', 'mensual']).ge(minimo_grupo).all(axis=1)]
    if seleccion.empty:
        raise ValueError('No hay capacidades con cobertura suficiente en ambos grupos.')
    capacidades['incluido_en_grafico'] = capacidades['capacidad'].isin(seleccion)
    cambio = capacidades.loc[capacidades['incluido_en_grafico']].pivot(
        index='capacidad', columns='grupo', values='mediana_ARS').reset_index()
    cambio['cambio_mediana_porcentaje'] = 100 * (cambio['mensual'] / cambio['principal'] - 1)
    cobertura = pd.DataFrame([
        {'seleccion': 'base_elegible', 'n': len(base), 'denominador': len(base)},
        {'seleccion': 'principal', 'n': len(principal), 'denominador': len(base)},
        {'seleccion': 'mensual', 'n': len(mensual), 'denominador': len(base)},
        {'seleccion': 'completos_principal', 'n': len(completos), 'denominador': len(principal)},
        {'seleccion': 'completos_capacidad_2', 'n': len(comparables), 'denominador': len(completos)},
        {'seleccion': 'barrios_con_soporte', 'n': int(barrios.loc[barrios['incluido_en_grafico'], 'n'].sum()),
         'denominador': len(comparables)},
    ])
    cobertura['porcentaje'] = 100 * cobertura['n'] / cobertura['denominador']
    return {'tipos': tipos, 'barrios': barrios, 'capacidades': capacidades,
            'sensibilidad_temporal': cambio, 'cobertura': cobertura}


def verificar_resumenes(tablas: dict[str, pd.DataFrame], resumenes: dict[str, pd.DataFrame],
                        minimo_grupo: int = 30) -> pd.DataFrame:
    """Recalcular con operaciones independientes los recuentos y cuartiles publicados."""
    principal, mensual = tablas['principal'], tablas['sensibilidad']
    fuentes = {
        'tipos': (principal, 'tipo_alojamiento'),
        'barrios': (principal.loc[principal['tipo_alojamiento'].eq('Entire home/apt') & principal['capacidad'].eq(2)], 'barrio'),
    }
    controles = []
    for nombre, (fuente, columna) in fuentes.items():
        for fila in resumenes[nombre].to_dict('records'):
            valores = fuente.loc[fuente[columna].eq(fila[columna]), 'precio_ars_noche'].to_numpy()
            if len(valores) != fila['n']:
                raise AssertionError(f'Recuento distinto: {nombre}.')
            np.testing.assert_allclose([fila['q1_ARS'], fila['mediana_ARS'], fila['q3_ARS']],
                                       np.quantile(valores, [.25, .5, .75], method='linear'), rtol=0, atol=1e-7)
        controles.append({'control': f'{nombre}_recuento_y_cuartiles_independientes', 'cumple': True})
    for fila in resumenes['capacidades'].to_dict('records'):
        fuente = principal if fila['grupo'] == 'principal' else mensual
        valores = fuente.loc[fuente['tipo_alojamiento'].eq('Entire home/apt') & fuente['capacidad'].eq(fila['capacidad']), 'precio_ars_noche'].to_numpy()
        assert len(valores) == fila['n']
        np.testing.assert_allclose([fila['q1_ARS'], fila['mediana_ARS'], fila['q3_ARS']],
                                   np.quantile(valores, [.25, .5, .75]), rtol=0, atol=1e-7)
    controles.append({'control': 'capacidades_recuento_y_cuartiles_independientes', 'cumple': True})
    assert int(resumenes['tipos']['n'].sum()) == len(principal)
    assert resumenes['barrios']['incluido_en_grafico'].eq(resumenes['barrios']['n'].ge(minimo_grupo)).all()
    seleccion = resumenes['capacidades'].loc[resumenes['capacidades']['incluido_en_grafico']]
    assert seleccion['n'].ge(minimo_grupo).all() and seleccion.groupby('capacidad').size().eq(2).all()
    controles.append({'control': 'cobertura_y_umbral_de_grupos', 'cumple': True})
    return pd.DataFrame(controles)
