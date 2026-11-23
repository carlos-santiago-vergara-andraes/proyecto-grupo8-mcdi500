"""Regresiones de la consulta de Git en rutas Unicode y carpetas internas."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import reconocimiento as rec


class TrazabilidadGitTests(unittest.TestCase):
    def respuesta_git(self, comando, **opciones):
        if "--is-inside-work-tree" in comando:
            salida = "true\n"
        elif "--show-prefix" in comando:
            salida = self.prefijo + "\n"
        elif "--show-toplevel" in comando:
            raise AssertionError("La detección de raíz no debe depender de comparar rutas impresas por Git.")
        elif "branch" in comando:
            salida = "feature/f1-definicion-entorno\n"
        elif "HEAD" in comando:
            salida = "a" * 40 + "\n"
        elif "status" in comando:
            salida = " M README.md\n"
        else:
            raise AssertionError(f"Consulta no contemplada: {comando}")
        return subprocess.CompletedProcess(comando, 0, stdout=salida, stderr="")

    def test_raiz_unicode_registra_rama_commit_y_cambios(self):
        self.prefijo = ""
        with tempfile.TemporaryDirectory() as temporal:
            raiz = Path(temporal) / "PROGRAMACIÓN PARA LA CIENCIA"
            raiz.mkdir()
            with patch.object(rec.subprocess, "run", side_effect=self.respuesta_git):
                resultado = rec.consultar_git(raiz)
        self.assertTrue(resultado["disponible"])
        self.assertEqual(resultado["rama"], "feature/f1-definicion-entorno")
        self.assertEqual(resultado["commit"], "a" * 40)
        self.assertTrue(resultado["cambios_sin_confirmar"])

    def test_subcarpeta_no_se_confunde_con_raiz(self):
        self.prefijo = "F1/"
        with tempfile.TemporaryDirectory() as temporal:
            with patch.object(rec.subprocess, "run", side_effect=self.respuesta_git):
                resultado = rec.consultar_git(Path(temporal))
        self.assertFalse(resultado["disponible"])
        self.assertIn("no es la raíz", resultado["observacion"])


if __name__ == "__main__":
    unittest.main()
