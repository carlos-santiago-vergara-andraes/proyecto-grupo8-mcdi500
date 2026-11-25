"""Carga verificada y contraste entre los resultados de F2 y F3."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src import preprocesamiento as f2
from src.reconocimiento import calcular_sha256


def cargar_referencias_f2(raiz: Path, evidencia: Path | None = None
                         ) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Leer los tres CSV locales producidos por F2 y comprobar sus huellas.

    La evidencia de F2 identifica las huellas esperadas. Los grupos se localizan
    por su sufijo para admitir los nombres descriptivos ya utilizados en el equipo.
    No se modifican los CSV ni las evidencias de la fase anterior.
    """
    raiz = Path(raiz)
    evidencia = evidencia or raiz / 'docs/evidencias/preprocesamiento_f2.json'
    manifiesto = json.loads(evidencia.read_text(encoding='utf-8-sig'))
    huellas = manifiesto['sha256_salidas_locales']
    sufijos = {'base': 'base_cotizaciones_f2.csv', 'principal': '_principal_f2.csv',
               'sensibilidad': '_sensibilidad_f2.csv'}
    referencias, verificaciones = {}, []
    for rol, sufijo in sufijos.items():
        esperadas = {valor for nombre, valor in huellas.items() if nombre.endswith(sufijo)}
        if len(esperadas) != 1:
            raise ValueError(f'La evidencia de F2 no identifica una huella única para {rol}.')
        archivos = sorted((raiz / 'data/processed').glob('*' + sufijo))
        coincidentes = [p for p in archivos if calcular_sha256(p) in esperadas]
        if not coincidentes:
            raise ValueError(f'No se encontró el CSV local verificado de F2 para {rol}. Revisar F2 y su evidencia.')
        tabla = pd.read_csv(coincidentes[0], dtype={'id': 'string', 'host_id': 'string'},
                            parse_dates=['fecha_extraccion', 'entrada', 'salida'])
        f2.validar_base(tabla)
        referencias[rol] = tabla
        verificaciones.append({'resultado_f2': rol, 'sha256_coincide': True,
                               'sha256': calcular_sha256(coincidentes[0]), 'filas': len(tabla)})
    return referencias, pd.DataFrame(verificaciones)


def comprobar_equivalencia(datos: pd.DataFrame, etapas: dict[str, pd.DataFrame],
                           referencias: dict[str, pd.DataFrame],
                           sensibilidad: pd.DataFrame) -> pd.DataFrame:
    """Distinguir igualdad estricta en memoria y equivalencia de los CSV releídos.

    Los CSV se cotejan con las tolerancias ya declaradas en F2: rtol=1e-12,
    atol=1e-7 y sin exigir dtype idéntico después de serializar a texto.
    """
    vista_f2 = f2.preparar_vista(datos)
    base_f2, _ = f2.preparar_base(vista_f2)
    pd.testing.assert_frame_equal(vista_f2, etapas['VerificadorCotizaciones'], check_exact=True)
    pd.testing.assert_frame_equal(base_f2, etapas['PreparadorBaseAnalitica'], check_exact=True)
    filas = [
        {'control': 'vista_F2_F3_exacta_en_memoria', 'cumple': True},
        {'control': 'base_F2_F3_exacta_en_memoria', 'cumple': True},
    ]
    nuevos = {'base': etapas['PreparadorBaseAnalitica'],
              'principal': etapas['SelectorGrupoComparable'], 'sensibilidad': sensibilidad}
    for rol, tabla in nuevos.items():
        pd.testing.assert_frame_equal(tabla.reset_index(drop=True),
                                      referencias[rol].reset_index(drop=True),
                                      check_dtype=False, check_exact=False,
                                      rtol=1e-12, atol=1e-7)
        filas.append({'control': f'{rol}_equivalente_CSV_F2', 'cumple': True})
    return pd.DataFrame(filas)
