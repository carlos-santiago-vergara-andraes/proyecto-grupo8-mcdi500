"""Composición de etapas: mismo contrato para todas las clases hijas."""
from __future__ import annotations

from copy import deepcopy

import pandas as pd

from src.f3_transformadores import (
    PreparadorBaseAnalitica, SelectorGrupoComparable, TransformadorCotizaciones,
    VerificadorCotizaciones, validar_tabla,
)


class PipelineCotizaciones:
    """Orquestar etapas por polimorfismo; no decidir por el tipo de cada paso."""

    def __init__(self, pasos: list[TransformadorCotizaciones]) -> None:
        if not pasos or not all(isinstance(p, TransformadorCotizaciones) for p in pasos):
            raise TypeError('Se requiere una lista no vacía de transformadores.')
        nombres = [p.nombre for p in pasos]
        if len(nombres) != len(set(nombres)):
            raise ValueError('Los nombres de las etapas deben ser distintos.')
        self._pasos = deepcopy(tuple(pasos))
        self._ajustado = False
        self._registro: list[dict] = []

    @property
    def parametros(self) -> dict:
        return {p.nombre: p.parametros for p in self._pasos}

    @property
    def registro_ajuste(self) -> list[dict]:
        return deepcopy(self._registro)

    def ajustar(self, datos: pd.DataFrame) -> PipelineCotizaciones:
        self._ajustado = False
        self._registro = []
        validar_tabla(datos)
        intermedio = datos.copy(deep=True)
        for paso in self._pasos:
            n_entrada = len(intermedio)
            intermedio = paso.ajustar(intermedio).transformar(intermedio)
            self._registro.append({'etapa': paso.nombre, 'filas_entrada': n_entrada,
                                   'filas_salida': len(intermedio),
                                   'columnas_salida': intermedio.shape[1]})
        self._ajustado = True
        return self

    def transformar_etapas(self, datos: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Retornar etapas para auditoría sin almacenar anuncios en el objeto."""
        if not self._ajustado:
            raise RuntimeError('Ejecutar ajustar() antes de transformar().')
        validar_tabla(datos)
        resultado = datos.copy(deep=True)
        etapas = {}
        for paso in self._pasos:
            resultado = paso.transformar(resultado)
            etapas[paso.nombre] = resultado.copy(deep=True)
        return etapas

    def transformar(self, datos: pd.DataFrame) -> pd.DataFrame:
        etapas = self.transformar_etapas(datos)
        return next(reversed(etapas.values()))


def construir_pipeline() -> PipelineCotizaciones:
    """Declarar el orden del flujo descriptivo, sin cambiar las reglas de F2."""
    return PipelineCotizaciones([
        VerificadorCotizaciones(), PreparadorBaseAnalitica(), SelectorGrupoComparable(),
    ])
