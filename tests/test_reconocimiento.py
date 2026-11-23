"""Comprobaciones de entradas, casos límite y conservación de datos en F1.

Ejecutar desde la raíz: python -m unittest discover -s tests -v
"""

from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import reconocimiento as rec


class ReconocimientoTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.raiz = Path(self.temporal.name)

    def tearDown(self):
        self.temporal.cleanup()

    def diccionario(self, nombres):
        ruta = self.raiz / "diccionario.csv"
        pd.DataFrame({
            "variable": nombres, "rol_analitico": ["nominal"] * len(nombres),
            "uso_propuesto": ["diagnóstico"] * len(nombres),
            "base_definicion": ["P"] * len(nombres),
        }).to_csv(ruta, sep=";", encoding="utf-8-sig", index=False)
        return ruta

    def test_lectura_gzip_conserva_archivo_y_valores(self):
        ruta = self.raiz / "fuente.csv.gz"
        esperado = pd.DataFrame({"id": [1, 2], "barrio": ["Núñez", "Palermo"]})
        esperado.to_csv(ruta, compression="gzip", index=False)
        antes = rec.calcular_sha256(ruta)
        observado = rec.cargar_dataset(ruta)
        pd.testing.assert_frame_equal(observado, esperado)
        self.assertEqual(rec.calcular_sha256(ruta), antes)
        ruta.write_bytes(ruta.read_bytes() + b"cambio")
        self.assertNotEqual(rec.calcular_sha256(ruta), antes)

    def test_archivo_ausente_o_sin_filas(self):
        with self.assertRaises(FileNotFoundError):
            rec.cargar_dataset(self.raiz / "ausente.csv")
        ruta = self.raiz / "sin_filas.csv"
        ruta.write_text("id,barrio\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no contiene filas"):
            rec.cargar_dataset(ruta)

    def test_perfil_cubre_nulos_constantes_e_infinito_sin_mutar(self):
        datos = pd.DataFrame({"id": [1, 2, 3], "vacia": [np.nan] * 3,
                              "constante": ["a"] * 3, "medida": [1.0, np.inf, np.nan]})
        copia = datos.copy(deep=True)
        huella = rec.huella_tabla(datos)
        perfil = rec.perfilar_variables(datos, self.diccionario(list(datos.columns))).set_index("variable")
        self.assertEqual(perfil.loc["vacia", "porcentaje_faltantes"], 100)
        self.assertEqual(perfil.loc["constante", "valores_distintos"], 1)
        self.assertEqual(perfil.loc["medida", "n_numericos_finitos"], 1)
        pd.testing.assert_frame_equal(datos, copia)
        self.assertEqual(rec.huella_tabla(datos), huella)

    def test_diccionario_distinto_o_duplicado_se_rechaza(self):
        datos = pd.DataFrame({"id": [1]})
        with self.assertRaisesRegex(ValueError, "no coinciden"):
            rec.perfilar_variables(datos, self.diccionario(["otra"]))
        with self.assertRaisesRegex(ValueError, "repetidos"):
            rec.perfilar_variables(datos, self.diccionario(["id", "id"]))

    def test_cotizaciones_incluye_json_invalido_y_fechas_incoherentes(self):
        datos = pd.DataFrame({
            "price": ["$1.00"] * 5,
            "price_quote_price_per_night": [1.0] * 5,
            "price_quote_raw": ['{"quote":{"currency":"ARS"}}', None, 'no es JSON',
                                '{"quote":null}', '{"quote":{}}'],
            "price_quote_checkin_date": ["2026-09-25"] * 5,
            "price_quote_checkout_date": ["2026-09-27", "2026-09-25", "fecha inválida",
                                          "2026-09-27", "2026-09-27"],
            "last_scraped": ["2026-09-25"] * 5,
        })
        copia = datos.copy(deep=True)
        resultado = rec.observar_cotizaciones(datos)
        resumen = resultado["resumen"].set_index("indicador")["valor"]
        for estado in ["JSON ausente", "JSON no válido", "Estructura inesperada",
                       "JSON con moneda informada", "JSON sin moneda informada"]:
            self.assertEqual(resumen[estado], 1)
        self.assertEqual(resumen["Estancias con duración no positiva"], 1)
        fechas = resultado["fechas"].set_index("variable")
        self.assertEqual(fechas.loc["price_quote_checkout_date", "n_no_interpretables_no_nulos"], 1)
        pd.testing.assert_frame_equal(datos, copia)

    def test_columnas_requeridas_y_evidencia_json(self):
        with self.assertRaises(KeyError):
            rec.resumir_dataset(pd.DataFrame({"otra": [1]}))
        with self.assertRaises(KeyError):
            rec.observar_cotizaciones(pd.DataFrame({"id": [1]}))
        ruta = self.raiz / "evidencias" / "prueba.json"
        rec.guardar_evidencia(ruta, {"tabla": rec.tabla_a_registros(pd.DataFrame({"valor": [np.nan]}))})
        self.assertIn('"valor": null', ruta.read_text(encoding="utf-8"))
        self.assertNotIn("NaN", ruta.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
