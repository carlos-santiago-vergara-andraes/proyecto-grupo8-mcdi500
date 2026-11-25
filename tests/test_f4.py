"""F4: contrato, integridad, agregación, cobertura y figuras sin mutación."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.f4_analisis import (ARCHIVOS_F3, cargar_resultados_f3, preparar_resumenes,
                             verificar_grupos, verificar_resumenes)
from src.f4_visualizacion import grafico_tipos, grafico_barrios, grafico_capacidades, guardar_figuras
from src.reconocimiento import calcular_sha256


def tablas_ejemplo():
    """Datos sintéticos exclusivamente para probar contratos, sin inferencias reales."""
    n = 12
    entrada = pd.to_datetime(['2026-09-27']*8 + ['2026-09-28']*4)
    precios = np.arange(1, n+1, dtype=float)*1000
    base = pd.DataFrame({
        'id': pd.Series([str(i) for i in range(n)], dtype='string'),
        'host_id': pd.Series(['1']*n, dtype='string'),
        'fecha_extraccion': pd.Timestamp('2026-09-25'),
        'barrio': ['A','A','B','B']*3,
        'tipo_alojamiento': ['Entire home/apt']*6+['Private room']*2+['Entire home/apt']*4,
        'capacidad': [2,2,3,3,2,2,2,2,2,2,3,3],
        'precio_ars_noche': precios, 'total_cotizado_ars': precios,
        'moneda': 'ARS', 'entrada': entrada, 'salida': entrada+pd.Timedelta(days=1), 'noches': 1,
        'dormitorios': 1., 'camas': 2., 'valoracion': 4.5,
        'dormitorios_faltante': False, 'camas_faltante': False, 'valoracion_faltante': False,
        'precio_log1p': np.log1p(precios), 'precio_ars_por_plaza': precios/np.array([2,2,3,3,2,2,2,2,2,2,3,3]),
        'precio_atipico_iqr_tipo': False,
    })
    return {'base': base, 'principal': base.iloc[:8].copy(), 'sensibilidad': base.copy()}


PARAMETROS = {'entrada': '2026-09-27', 'noches': 1, 'mes': '2026-09'}


class F4Tests(unittest.TestCase):
    def setUp(self):
        self.tablas = tablas_ejemplo()

    def test_grupos_conservan_valores(self):
        self.assertTrue(verificar_grupos(self.tablas, PARAMETROS)['cumple'].all())

    def test_cambio_de_precio_de_un_subgrupo_se_rechaza(self):
        self.tablas['principal'].loc[0, 'precio_ars_noche'] = 1001.
        self.tablas['principal'].loc[0, 'precio_log1p'] = np.log1p(1001.)
        self.tablas['principal'].loc[0, 'precio_ars_por_plaza'] = 500.5
        with self.assertRaises(AssertionError):
            verificar_grupos(self.tablas, PARAMETROS)

    def test_registro_omitido_en_el_grupo_se_rechaza(self):
        self.tablas['principal'] = self.tablas['principal'].iloc[1:]
        with self.assertRaises(AssertionError):
            verificar_grupos(self.tablas, PARAMETROS)

    def test_precio_infinito_se_rechaza(self):
        self.tablas['principal'].loc[0, 'precio_ars_noche'] = np.inf
        with self.assertRaises(ValueError):
            preparar_resumenes(self.tablas, 1)

    def test_columnas_sensibles_se_rechazan(self):
        self.tablas['principal']['host_name'] = 'dato de prueba'
        with self.assertRaises(ValueError):
            preparar_resumenes(self.tablas, 1)

    def test_umbral_entero_positivo(self):
        for valor in [0, -1, True, 1.5]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                preparar_resumenes(self.tablas, valor)

    def test_sin_soporte_no_se_fabrica_grafico(self):
        with self.assertRaisesRegex(ValueError, 'cobertura mínima'):
            preparar_resumenes(self.tablas, 100)

    def test_cuartiles_exactos_y_cobertura(self):
        r = preparar_resumenes(self.tablas, 1)
        self.assertTrue(verificar_resumenes(self.tablas, r, 1)['cumple'].all())
        self.assertEqual(r['tipos']['n'].sum(), 8)
        self.assertAlmostEqual(r['cobertura'].set_index('seleccion').loc['principal', 'porcentaje'], 100*8/12)

    def test_falsificar_resumen_se_detecta(self):
        r = preparar_resumenes(self.tablas, 1)
        r['tipos'].loc[0, 'mediana_ARS'] += 1
        with self.assertRaises(AssertionError):
            verificar_resumenes(self.tablas, r, 1)

    def test_sensibilidad_utiliza_mismo_tipo_y_capacidad(self):
        r = preparar_resumenes(self.tablas, 1)
        cambio = r['sensibilidad_temporal'].set_index('capacidad')
        # Capacidad 2, completos: principal 1k,2k,5k,6k; mensual añade 9k,10k.
        self.assertEqual(cambio.loc[2,'principal'], 3500.)
        self.assertEqual(cambio.loc[2,'mensual'], 5500.)
        self.assertAlmostEqual(cambio.loc[2,'cambio_mediana_porcentaje'], 100*(5500/3500-1))

    def test_funciones_y_figuras_no_mutan_entradas(self):
        copias = {k:v.copy(deep=True) for k,v in self.tablas.items()}
        r = preparar_resumenes(self.tablas, 1)
        figs = [grafico_tipos(self.tablas['principal'], r['tipos']), grafico_barrios(r['barrios']),
                grafico_capacidades(r['capacidades'], r['sensibilidad_temporal'])]
        for fig in figs:
            self.assertTrue(fig.axes[0].get_xlabel()); self.assertTrue(fig.legends)
            plt.close(fig)
        for k in copias:
            pd.testing.assert_frame_equal(copias[k], self.tablas[k], check_exact=True)

    def test_figuras_exportadas_y_escalas(self):
        r = preparar_resumenes(self.tablas, 1)
        f = grafico_tipos(self.tablas['principal'], r['tipos'])
        self.assertEqual(f.axes[0].get_xscale(), 'log'); plt.close(f)
        f = grafico_capacidades(r['capacidades'], r['sensibilidad_temporal'])
        self.assertEqual(f.axes[0].get_ylim()[0], 0); plt.close(f)
        with tempfile.TemporaryDirectory() as ruta:
            archivos = guardar_figuras(self.tablas['principal'], r, Path(ruta))
            self.assertEqual(len(archivos), 3)
            self.assertTrue(all(a.read_bytes().startswith(b'\x89PNG') for a in archivos))

    def test_carga_hash_correcto_incorrecto_y_archivo_ausente(self):
        with tempfile.TemporaryDirectory() as ruta:
            raiz = Path(ruta); carpeta = raiz/'data/processed'; carpeta.mkdir(parents=True)
            huellas = {}
            for rol,nombre in ARCHIVOS_F3.items():
                archivo = carpeta/nombre; self.tablas[rol].to_csv(archivo,index=False)
                huellas[nombre] = calcular_sha256(archivo)
            manifiesto = raiz/'evidencia.json'
            manifiesto.write_text(json.dumps({'sha256_salidas_locales':huellas,
                'parametros':{'SelectorGrupoComparable':PARAMETROS}}),encoding='utf-8')
            # F4 debe consumir artefactos, sin ejecutar de nuevo la preparación F2.
            with (patch('src.preprocesamiento.preparar_vista',side_effect=AssertionError('F4 no reprocesa')),
                  patch('src.preprocesamiento.preparar_base',side_effect=AssertionError('F4 no reprocesa'))):
                _,_,control = cargar_resultados_f3(raiz,manifiesto)
            self.assertTrue(control['cumple'].all())
            archivo = carpeta/ARCHIVOS_F3['principal']
            with archivo.open('a') as f: f.write('\n')
            with self.assertRaisesRegex(ValueError,'SHA-256'):
                cargar_resultados_f3(raiz,manifiesto)
            archivo.unlink()
            with self.assertRaises(FileNotFoundError):
                cargar_resultados_f3(raiz,manifiesto)


if __name__ == '__main__':
    unittest.main()
