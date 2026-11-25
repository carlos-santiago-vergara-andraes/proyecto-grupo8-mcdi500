"""F3: equivalencia, estado protegido, casos límite y fallos explícitos."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from src import preprocesamiento as f2
from src.f3_medicion import (comparar_implementaciones, comprobar_resumenes,
                             resumen_por_bucle, resumen_vectorizado)
from src.f3_pipeline import PipelineCotizaciones, construir_pipeline
from src.f3_transformadores import (PreparadorBaseAnalitica, SelectorGrupoComparable,
                                   TransformadorCotizaciones, VerificadorCotizaciones)
from src.f3_validacion import cargar_referencias_f2, comprobar_equivalencia
from src.reconocimiento import calcular_sha256


def ejemplo() -> pd.DataFrame:
    """Cotizaciones sintéticas, sin nombres, enlaces ni datos de personas."""
    filas = []
    for i, (entrada, salida, precio) in enumerate([
        ('2026-09-27', '2026-09-28', 100.), ('2026-09-27', '2026-09-28', 200.),
        ('2026-09-28', '2026-09-29', 300.), ('2026-09-27', '2026-09-29', 400.),
    ]):
        quote = {'currency': 'ARS', 'price_per_night': precio, 'total_price': precio * 2,
                 'requested_checkin_date': entrada, 'requested_checkout_date': salida}
        filas.append({'id': i + 1, 'host_id': 99, 'last_scraped': '2026-09-25',
                      'neighbourhood_cleansed': 'Barrio A', 'room_type': 'Entire home/apt',
                      'accommodates': 2, 'price': str(precio),
                      'price_quote_price_per_night': precio, 'price_quote_total_price': precio * 2,
                      'price_quote_checkin_date': entrada, 'price_quote_checkout_date': salida,
                      'price_quote_raw': json.dumps({'quote': quote}),
                      'bedrooms': 1., 'beds': np.nan if i == 0 else 2.,
                      'review_scores_rating': 4.8})
    return pd.DataFrame(filas)


class F3Tests(unittest.TestCase):
    def test_pipeline_conserva_entrada_y_base_f2_exacta(self):
        datos = ejemplo()
        original = datos.copy(deep=True)
        referencia = f2.ejecutar_preprocesamiento(datos)
        p = construir_pipeline().ajustar(datos)
        etapas = p.transformar_etapas(datos)
        pd.testing.assert_frame_equal(datos, original, check_exact=True)
        pd.testing.assert_frame_equal(etapas['PreparadorBaseAnalitica'], referencia['base'], check_exact=True)
        pd.testing.assert_frame_equal(p.transformar(datos), referencia['principal'], check_exact=True)
        self.assertTrue(etapas['PreparadorBaseAnalitica']['camas'].isna().any())
        self.assertEqual(len(p.registro_ajuste), 3)

    def test_estado_y_encapsulamiento(self):
        p = construir_pipeline()
        with self.assertRaisesRegex(RuntimeError, 'ajustar'):
            p.transformar(ejemplo())
        p.ajustar(ejemplo())
        antes = p.parametros
        externa = p.parametros
        externa['SelectorGrupoComparable']['noches'] = 999
        registro = p.registro_ajuste
        registro[0]['filas_salida'] = -1
        self.assertEqual(p.parametros, antes)
        self.assertEqual(p.registro_ajuste[0]['filas_salida'], 4)

    def test_parametros_iqr_no_se_aprenden_al_transformar(self):
        vista = f2.preparar_vista(ejemplo())
        paso = PreparadorBaseAnalitica().ajustar(vista)
        parametros = paso.parametros
        nueva = vista.iloc[[0]].copy()
        nueva.loc[:, 'precio_ars_noche'] = 1e9
        r = paso.transformar(nueva)
        self.assertTrue(r['precio_atipico_iqr_tipo'].all())
        self.assertEqual(paso.parametros, parametros)

    def test_selector_no_cambia_ventana_y_rechaza_ventana_vacia(self):
        base = f2.preparar_base(f2.preparar_vista(ejemplo()))[0]
        paso = SelectorGrupoComparable().ajustar(base)
        parametros = paso.parametros
        self.assertEqual(len(paso.ampliar_al_mes(base)), 3)
        self.assertEqual(paso.parametros, parametros)
        with self.assertRaisesRegex(ValueError, 'no vacía'):
            paso.transformar(base.loc[base['entrada'].eq(pd.Timestamp('2026-09-28'))])

    def test_una_fila_categoria_unica_y_faltantes_totales(self):
        datos = ejemplo().iloc[[0]].copy()
        datos['bedrooms'] = np.nan
        datos['beds'] = np.nan
        resultado = construir_pipeline().ajustar(datos).transformar(datos)
        self.assertEqual(len(resultado), 1)
        self.assertTrue(resultado[['dormitorios', 'camas']].isna().all().all())
        self.assertFalse(resultado['precio_atipico_iqr_tipo'].any())

    def test_errores_de_entrada_y_reajuste_fallido(self):
        p = construir_pipeline().ajustar(ejemplo())
        for invalido in [None, [1, 2]]:
            with self.assertRaises(TypeError):
                p.transformar(invalido)
        with self.assertRaises(ValueError):
            p.ajustar(ejemplo().drop(columns='price'))
        with self.assertRaises(RuntimeError):
            p.transformar(ejemplo())
        for clase in [VerificadorCotizaciones, PreparadorBaseAnalitica, SelectorGrupoComparable]:
            with self.subTest(clase=clase.__name__):
                with self.assertRaises(RuntimeError):
                    clase().transformar(ejemplo())
        with self.assertRaises(TypeError):
            PipelineCotizaciones([])
        with self.assertRaises(TypeError):
            TransformadorCotizaciones()

    def test_polimorfismo_admite_etapa_alternativa(self):
        class Identidad(TransformadorCotizaciones):
            def _aprender(self, datos):
                return {'filas_ajuste': len(datos)}
            def _aplicar(self, datos):
                return datos
        datos = pd.DataFrame({'a': [1, 2]})
        p = PipelineCotizaciones([Identidad()]).ajustar(datos)
        pd.testing.assert_frame_equal(p.transformar(datos), datos)

    def test_equivalencia_de_resumenes_incluye_grupos_pequenos(self):
        datos = pd.DataFrame({'barrio': ['B', 'A', 'A', 'B', 'C'],
                              'precio_ars_noche': [20., 10., 30., 40., 50.]})
        comprobar_resumenes(resumen_por_bucle(datos), resumen_vectorizado(datos))
        esperado = resumen_vectorizado(datos)
        self.assertEqual(esperado['mediana_ARS'].tolist(), [20., 30., 50.])
        self.assertTrue(esperado['grupo_menor_30'].all())
        alterado = esperado.copy()
        alterado.loc[0, 'n'] += 1
        with self.assertRaises(AssertionError):
            comprobar_resumenes(esperado, alterado)
        redondeo = esperado.copy()
        redondeo.loc[0, 'q1_ARS'] += 1e-8
        comprobar_resumenes(esperado, redondeo)
        redondeo.loc[0, 'q1_ARS'] += 1e-4
        with self.assertRaises(AssertionError):
            comprobar_resumenes(esperado, redondeo)

    def test_resumen_rechaza_nulos_infinitos_y_campos_ausentes(self):
        correcto = pd.DataFrame({'barrio': ['A'], 'precio_ars_noche': [10.]})
        malos = [correcto.iloc[:0], correcto.drop(columns='barrio'),
                 correcto.assign(barrio=None), correcto.assign(precio_ars_noche=np.inf)]
        for funcion in [resumen_por_bucle, resumen_vectorizado]:
            for datos in malos:
                with self.subTest(funcion=funcion.__name__):
                    with self.assertRaises(ValueError):
                        funcion(datos)

    def test_medicion_incluye_tamano_real_y_repeticiones(self):
        datos = pd.DataFrame({'barrio': ['A', 'B', 'A'], 'precio_ars_noche': [10., 20., 30.]})
        tabla, registros = comparar_implementaciones(datos, tamanos=(1,), repeticiones=3, ejecuciones=1)
        self.assertEqual(set(tabla['filas']), {1, 3})
        self.assertEqual(len(registros), 12)
        self.assertTrue(tabla['resumenes_equivalentes'].all())
        self.assertTrue(tabla['tiempo_min_ms'].gt(0).all())
        with self.assertRaises(ValueError):
            comparar_implementaciones(datos, repeticiones=0)

    def test_csv_verificado_y_contraste_f2_f3_detectan_alteracion(self):
        datos = ejemplo()
        referencia = f2.ejecutar_preprocesamiento(datos)
        p = construir_pipeline().ajustar(datos)
        etapas = p.transformar_etapas(datos)
        selector = SelectorGrupoComparable().ajustar(referencia['base'])
        ampliada = selector.ampliar_al_mes(referencia['base'])
        with tempfile.TemporaryDirectory() as carpeta:
            raiz = Path(carpeta)
            (raiz / 'docs/evidencias').mkdir(parents=True)
            (raiz / 'data/processed').mkdir(parents=True)
            huellas = {}
            for rol, nombre in [('base', 'base_cotizaciones_f2.csv'),
                                 ('principal', 'grupo_principal_f2.csv'),
                                 ('sensibilidad', 'grupo_sensibilidad_f2.csv')]:
                destino = raiz / 'data/processed' / nombre
                f2.exportar_y_verificar(referencia[rol], destino)
                huellas[nombre] = calcular_sha256(destino)
            (raiz / 'docs/evidencias/preprocesamiento_f2.json').write_text(
                json.dumps({'sha256_salidas_locales': huellas}))
            referencias, registro = cargar_referencias_f2(raiz)
            self.assertTrue(registro['sha256_coincide'].all())
            self.assertTrue(comprobar_equivalencia(datos, etapas, referencias, ampliada)['cumple'].all())
            alteradas = deepcopy(etapas)
            alteradas['PreparadorBaseAnalitica'].loc[0, 'precio_ars_noche'] += 1
            with self.assertRaises(AssertionError):
                comprobar_equivalencia(datos, alteradas, referencias, ampliada)
            (raiz / 'data/processed/base_cotizaciones_f2.csv').write_text('archivo alterado')
            with self.assertRaisesRegex(ValueError, 'verificado'):
                cargar_referencias_f2(raiz)


if __name__ == '__main__':
    unittest.main()
