"""Casos normales, límites y errores del flujo F2, sin depender del archivo real."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from src.preprocesamiento import (
    ejecutar_preprocesamiento, exportar_y_verificar, extraer_cotizacion,
    interpretar_price, preparar_base, preparar_vista, seleccionar_cohortes,
    validar_base,
)


def ejemplo():
    filas = []
    for i, (entrada, salida, precio) in enumerate([
        ('2026-09-27', '2026-09-28', 100),
        ('2026-09-27', '2026-09-28', 200),
        ('2026-09-28', '2026-09-29', 300),
        ('2026-09-27', '2026-09-29', 400),
    ]):
        q = {'currency': 'ARS', 'price_per_night': str(precio), 'total_price': str(precio * 2),
             'requested_checkin_date': entrada, 'requested_checkout_date': salida}
        filas.append({'id': i + 1, 'host_id': 99, 'last_scraped': '2026-09-25',
                      'neighbourhood_cleansed': 'Barrio A', 'room_type': 'Entire home/apt',
                      'accommodates': 2, 'price': f'${precio:,.2f}',
                      'price_quote_price_per_night': float(precio), 'price_quote_total_price': float(precio * 2),
                      'price_quote_checkin_date': entrada, 'price_quote_checkout_date': salida,
                      'price_quote_raw': json.dumps({'quote': q}),
                      'bedrooms': 1, 'beds': 2 if i else None, 'review_scores_rating': 4.8})
    return pd.DataFrame(filas)


class PreprocesamientoTests(unittest.TestCase):
    def test_flujo_no_muta_y_cuadra_cohorte_exportacion(self):
        datos = ejemplo()
        original = datos.copy(deep=True)
        r = ejecutar_preprocesamiento(datos)
        pd.testing.assert_frame_equal(datos, original)
        self.assertEqual(r['principal']['id'].tolist(), ['1', '2'])
        self.assertEqual(len(r['sensibilidad']), 3)
        self.assertTrue(r['base']['camas'].isna().any())  # Sin imputación silenciosa.
        self.assertTrue(r['tablas']['validacion']['cumple'].all())
        self.assertTrue(r['indicadores_tipo'].drop(columns='id').sum(axis=1).eq(1).all())
        with tempfile.TemporaryDirectory() as carpeta:
            salida = exportar_y_verificar(r['base'], Path(carpeta) / 'base.csv')
            self.assertTrue(salida['cumple'].all())

    def test_precio_rechaza_separadores_ambiguos_y_no_oculta_diferencias_grandes(self):
        valores = pd.Series(['$1,234.50', '$12,34', '1.234,50', None, '-10', 'Infinity'])
        r = interpretar_price(valores)
        self.assertEqual(r.iloc[0], 1234.5)
        self.assertTrue(r.iloc[1:].isna().all())
        d = ejemplo()
        d.loc[0, 'price'] = '$100000001.00'
        d.loc[0, 'price_quote_price_per_night'] = 100000000
        # La concordancia entre campos no debe usar tolerancia relativa.
        r = ejecutar_preprocesamiento(d)
        m = r['tablas']['comparacion_precios'].set_index('indicador')['valor']
        self.assertEqual(m['difieren_mas_0_01_ARS'], 1)

    def test_moneda_json_fechas_y_precio_invalidos_excluyen_con_conteos(self):
        d = ejemplo()
        d.loc[0, 'price_quote_raw'] = '{mal JSON'
        d.loc[1, 'price_quote_price_per_night'] = np.inf
        d.loc[2, 'price_quote_checkout_date'] = '2026-09-27'
        v = preparar_vista(d)
        self.assertEqual(v['elegible'].tolist(), [False, False, False, True])
        r = ejecutar_preprocesamiento(d)
        perdidas = r['tablas']['exclusiones']['n_excluidos_en_este_paso'].sum()
        self.assertEqual(perdidas + len(r['base']), len(d))

    def test_usd_y_json_distinto_no_se_equiparan_a_ars(self):
        d = ejemplo()
        q = json.loads(d.loc[0, 'price_quote_raw'])
        q['quote']['currency'] = 'USD'
        d.loc[0, 'price_quote_raw'] = json.dumps(q)
        q = json.loads(d.loc[1, 'price_quote_raw'])
        q['quote']['price_per_night'] = '999'
        d.loc[1, 'price_quote_raw'] = json.dumps(q)
        v = preparar_vista(d)
        self.assertFalse(v.loc[0, 'elegible'])
        self.assertFalse(v.loc[1, 'elegible'])
        self.assertEqual(extraer_cotizacion('[]')['estado_json'], 'estructura_inesperada')
        self.assertEqual(extraer_cotizacion(None)['estado_json'], 'ausente')

    def test_id_duplicado_columnas_ausentes_y_cero_filas_se_rechazan(self):
        d = ejemplo()
        d.loc[1, 'id'] = d.loc[0, 'id']
        with self.assertRaisesRegex(ValueError, 'id repetidos'):
            preparar_vista(d)
        with self.assertRaisesRegex(ValueError, 'Faltan columnas'):
            preparar_vista(ejemplo().drop(columns='price'))
        with self.assertRaisesRegex(ValueError, 'no contiene filas'):
            preparar_vista(ejemplo().iloc[:0])

    def test_dominios_y_categorias_inesperadas(self):
        d = ejemplo()
        d.loc[0, 'accommodates'] = 0
        d.loc[1, 'room_type'] = 'Tipo desconocido'
        d.loc[2, 'neighbourhood_cleansed'] = ''
        v = preparar_vista(d)
        self.assertEqual(v['elegible'].sum(), 1)
        d.loc[3, 'price_quote_price_per_night'] = 0
        with self.assertRaisesRegex(ValueError, 'No quedan cotizaciones'):
            ejecutar_preprocesamiento(d)

    def test_sin_nulos_y_categoria_unica_no_exigen_imputar(self):
        d = ejemplo()
        d['beds'] = 2
        r = ejecutar_preprocesamiento(d)
        alt = r['tablas']['alternativas_faltantes']
        self.assertTrue(alt['n_ausentes_o_invalidos'].eq(0).all())
        self.assertTrue(alt['n_rellenos'].eq(0).all())
        self.assertTrue(r['base']['precio_atipico_iqr_tipo'].eq(False).all())

    def test_complementarias_totalmente_nulas_y_fuera_de_rango(self):
        d = ejemplo()
        d['beds'] = np.nan
        d.loc[0, 'bedrooms'] = -1
        d.loc[1, 'review_scores_rating'] = 6
        r = ejecutar_preprocesamiento(d)
        self.assertEqual(len(r['base']), len(d))
        self.assertTrue(r['base']['camas'].isna().all())
        self.assertTrue(pd.isna(r['base'].loc[0, 'dormitorios']))
        self.assertTrue(pd.isna(r['base'].loc[1, 'valoracion']))

    def test_desempate_no_depende_de_precio_ni_orden(self):
        b, _ = preparar_base(preparar_vista(ejemplo()))
        b = b.iloc[[0, 2]].copy()
        b.loc[b.index[0], 'precio_ars_noche'] = 999999
        a = seleccionar_cohortes(b)[3]
        c = seleccionar_cohortes(b.iloc[::-1])[3]
        self.assertEqual(a, c)
        self.assertEqual(a['fecha_entrada_principal'], '2026-09-27')

    def test_validacion_detecta_alteracion_de_transformacion(self):
        r = ejecutar_preprocesamiento(ejemplo())
        b = r['base'].copy()
        b.loc[0, 'precio_log1p'] += 1
        with self.assertRaisesRegex(ValueError, 'log_precio_reversible'):
            validar_base(b)


if __name__ == '__main__':
    unittest.main()
