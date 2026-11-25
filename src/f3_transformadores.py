"""Etapas de F3: reutilización de F2 con estado y parámetros protegidos."""
from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy

import pandas as pd

from src import preprocesamiento as f2


def validar_tabla(datos: pd.DataFrame) -> None:
    """Rechazar entradas que no permiten una transformación verificable."""
    if not isinstance(datos, pd.DataFrame):
        raise TypeError('Se requiere un pandas.DataFrame.')
    if datos.empty:
        raise ValueError('Se requiere una tabla no vacía.')
    if not datos.columns.is_unique:
        raise ValueError('Hay nombres de columna duplicados.')


class TransformadorCotizaciones(ABC):
    """Método plantilla: validar, aprender parámetros y aplicar sobre una copia.

    Las clases hijas implementan aprender/aplicar; el control de estado es común.
    Las propiedades devuelven copias, evitando modificar parámetros desde fuera.
    """

    def __init__(self) -> None:
        self._ajustado = False
        self._parametros: dict = {}

    @property
    def nombre(self) -> str:
        return type(self).__name__

    @property
    def parametros(self) -> dict:
        return deepcopy(self._parametros)

    def ajustar(self, datos: pd.DataFrame) -> TransformadorCotizaciones:
        self._ajustado = False
        self._parametros = {}
        validar_tabla(datos)
        aprendidos = self._aprender(datos.copy(deep=True))
        self._parametros = deepcopy(aprendidos)
        self._ajustado = True
        return self

    def transformar(self, datos: pd.DataFrame) -> pd.DataFrame:
        if not self._ajustado:
            raise RuntimeError(f'{self.nombre}: ejecutar ajustar() antes de transformar().')
        validar_tabla(datos)
        resultado = self._aplicar(datos.copy(deep=True))
        validar_tabla(resultado)
        return resultado

    @abstractmethod
    def _aprender(self, datos: pd.DataFrame) -> dict:
        """Obtener los parámetros que deben permanecer fijos al transformar."""

    @abstractmethod
    def _aplicar(self, datos: pd.DataFrame) -> pd.DataFrame:
        """Aplicar los parámetros sin modificar la entrada ni volver a ajustar."""


class VerificadorCotizaciones(TransformadorCotizaciones):
    """Adaptar la lectura, las reglas de elegibilidad y la moneda de F2."""

    def _aprender(self, datos: pd.DataFrame) -> dict:
        f2.perfil_seleccion(datos)
        return {'columnas_requeridas': list(f2.REQUERIDAS), 'moneda': 'ARS'}

    def _aplicar(self, datos: pd.DataFrame) -> pd.DataFrame:
        faltan = set(self._parametros['columnas_requeridas']) - set(datos.columns)
        if faltan:
            raise ValueError(f'Faltan columnas requeridas: {sorted(faltan)}')
        return f2.preparar_vista(datos)


class PreparadorBaseAnalitica(TransformadorCotizaciones):
    """Conservar faltantes y transformaciones de F2; fijar límites IQR por tipo.

    En el conjunto de ajuste produce exactamente la base de F2. En aplicaciones
    posteriores conserva los límites aprendidos; no los recalcula con datos nuevos.
    Las marcas IQR describen atípicos: no eliminan anuncios ni imputan precios.
    """

    def _aprender(self, datos: pd.DataFrame) -> dict:
        base, _ = f2.preparar_base(datos)
        limites = {}
        for tipo, grupo in base.groupby('tipo_alojamiento', observed=True):
            q1 = float(grupo['precio_ars_noche'].quantile(.25))
            q3 = float(grupo['precio_ars_noche'].quantile(.75))
            limites[str(tipo)] = {'inferior': q1 - 1.5 * (q3 - q1),
                                  'superior': q3 + 1.5 * (q3 - q1)}
        return {'limites_iqr': limites, 'faltantes': 'conservar_con_indicador',
                'imputar_precio': False}

    def _aplicar(self, datos: pd.DataFrame) -> pd.DataFrame:
        # Se reutilizan limpieza, tipos y variables de F2. Solo se sustituyen sus
        # marcas IQR por las obtenidas con los límites guardados durante ajustar().
        base, _ = f2.preparar_base(datos)
        limites = self._parametros['limites_iqr']
        desconocidos = set(base['tipo_alojamiento']) - set(limites)
        if desconocidos:
            raise ValueError(f'Tipos sin límites IQR aprendidos: {sorted(desconocidos)}')
        inferiores = base['tipo_alojamiento'].map({k: v['inferior'] for k, v in limites.items()})
        superiores = base['tipo_alojamiento'].map({k: v['superior'] for k, v in limites.items()})
        base['precio_atipico_iqr_tipo'] = (
            base['precio_ars_noche'].lt(inferiores)
            | base['precio_ars_noche'].gt(superiores)
        )
        return base


class SelectorGrupoComparable(TransformadorCotizaciones):
    """Aprender la ventana con mayor cobertura y conservarla al transformar."""

    def _aprender(self, datos: pd.DataFrame) -> dict:
        cobertura = (datos.groupby(['entrada', 'noches'], as_index=False)
                     .size().rename(columns={'size': 'n_anuncios'}))
        cobertura = cobertura.sort_values(
            ['n_anuncios', 'entrada', 'noches'], ascending=[False, True, True])
        fila = cobertura.iloc[0]
        return {'entrada': fila['entrada'].date().isoformat(),
                'mes': str(fila['entrada'].to_period('M')),
                'noches': int(fila['noches']),
                'regla': 'Mayor cobertura; empate por fecha temprana y menor duración.'}

    def _aplicar(self, datos: pd.DataFrame) -> pd.DataFrame:
        fecha = pd.Timestamp(self._parametros['entrada'])
        return datos.loc[datos['entrada'].eq(fecha)
                         & datos['noches'].eq(self._parametros['noches'])].copy()

    def ampliar_al_mes(self, datos: pd.DataFrame) -> pd.DataFrame:
        """Aplicar la ventana mensual guardada, sin volver a elegir fecha/duración."""
        if not self._ajustado:
            raise RuntimeError('Ejecutar ajustar() antes de ampliar_al_mes().')
        validar_tabla(datos)
        mascara = (datos['entrada'].dt.to_period('M').astype(str).eq(self._parametros['mes'])
                   & datos['noches'].eq(self._parametros['noches']))
        resultado = datos.loc[mascara].copy()
        validar_tabla(resultado)
        return resultado
