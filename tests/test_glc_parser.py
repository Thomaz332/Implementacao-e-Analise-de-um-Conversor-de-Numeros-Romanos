"""
Testes unitários para src/glc_parser.py.

Cobertura:
  - Todos os casos válidos obrigatórios com valores corretos
  - Todos os 9 padrões canônicos de milhar, centena, dezena e unidade
  - Isolamento de cada não-terminal (_Parser chamado diretamente)
  - Comportamento com entrada inválida (ValueError esperado)
  - Derivações completas de exemplo do relatório
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from glc_parser import converter, _Parser


class TestConverterCasosObrigatorios(unittest.TestCase):
    """Casos válidos obrigatórios com seus valores esperados."""

    CASOS: list[tuple[str, int]] = [
        ('I',           1),
        ('II',          2),
        ('III',         3),
        ('IV',          4),
        ('V',           5),
        ('IX',          9),
        ('X',          10),
        ('XL',         40),
        ('XLII',       42),
        ('XC',         90),
        ('XCIX',       99),
        ('C',         100),
        ('CD',        400),
        ('CM',        900),
        ('D',         500),
        ('M',        1000),
        ('MMXXIV',   2024),
        ('MMMCMXCIX', 3999),
    ]

    def test_todos_os_casos(self):
        for romano, esperado in self.CASOS:
            with self.subTest(romano=romano):
                self.assertEqual(converter(romano), esperado)

    def test_fronteira_minima(self):
        self.assertEqual(converter('I'), 1)

    def test_fronteira_maxima(self):
        self.assertEqual(converter('MMMCMXCIX'), 3999)


class TestParseMilhar(unittest.TestCase):
    """Testa o não-terminal <Milhar> isoladamente."""

    def _parse(self, s: str) -> tuple[int, int]:
        """Retorna (valor, posição após parse)."""
        p = _Parser(s)
        valor = p.parse_milhar()
        return valor, p._pos

    def test_MMM(self):
        valor, pos = self._parse('MMM')
        self.assertEqual(valor, 3000)
        self.assertEqual(pos, 3)

    def test_MM(self):
        valor, pos = self._parse('MM')
        self.assertEqual(valor, 2000)
        self.assertEqual(pos, 2)

    def test_M(self):
        valor, pos = self._parse('M')
        self.assertEqual(valor, 1000)
        self.assertEqual(pos, 1)

    def test_epsilon(self):
        valor, pos = self._parse('XIV')
        self.assertEqual(valor, 0)
        self.assertEqual(pos, 0)

    def test_nao_consome_alem_de_MMM(self):
        # Quarto M não deve ser consumido por parse_milhar
        _, pos = self._parse('MMMM')
        self.assertEqual(pos, 3)


class TestParseCentena(unittest.TestCase):
    """Testa o não-terminal <Centena> isoladamente."""

    def _parse(self, s: str) -> int:
        p = _Parser(s)
        return p.parse_centena()

    def test_CM(self):
        self.assertEqual(self._parse('CM'), 900)

    def test_DCCC(self):
        self.assertEqual(self._parse('DCCC'), 800)

    def test_DCC(self):
        self.assertEqual(self._parse('DCC'), 700)

    def test_DC(self):
        self.assertEqual(self._parse('DC'), 600)

    def test_D(self):
        self.assertEqual(self._parse('D'), 500)

    def test_CD(self):
        self.assertEqual(self._parse('CD'), 400)

    def test_CCC(self):
        self.assertEqual(self._parse('CCC'), 300)

    def test_CC(self):
        self.assertEqual(self._parse('CC'), 200)

    def test_C(self):
        self.assertEqual(self._parse('C'), 100)

    def test_epsilon(self):
        self.assertEqual(self._parse('XIV'), 0)

    def test_DCCC_antes_de_DCC(self):
        # Garante que DCCC não é reconhecido como DCC + C restante
        p = _Parser('DCCC')
        v = p.parse_centena()
        self.assertEqual(v, 800)
        self.assertEqual(p._pos, 4)


class TestParseDezena(unittest.TestCase):
    """Testa o não-terminal <Dezena> isoladamente."""

    def _parse(self, s: str) -> int:
        p = _Parser(s)
        return p.parse_dezena()

    def test_XC(self):
        self.assertEqual(self._parse('XC'), 90)

    def test_LXXX(self):
        self.assertEqual(self._parse('LXXX'), 80)

    def test_LXX(self):
        self.assertEqual(self._parse('LXX'), 70)

    def test_LX(self):
        self.assertEqual(self._parse('LX'), 60)

    def test_L(self):
        self.assertEqual(self._parse('L'), 50)

    def test_XL(self):
        self.assertEqual(self._parse('XL'), 40)

    def test_XXX(self):
        self.assertEqual(self._parse('XXX'), 30)

    def test_XX(self):
        self.assertEqual(self._parse('XX'), 20)

    def test_X(self):
        self.assertEqual(self._parse('X'), 10)

    def test_epsilon(self):
        self.assertEqual(self._parse('IV'), 0)

    def test_LXXX_antes_de_LXX(self):
        p = _Parser('LXXX')
        v = p.parse_dezena()
        self.assertEqual(v, 80)
        self.assertEqual(p._pos, 4)


class TestParseUnidade(unittest.TestCase):
    """Testa o não-terminal <Unidade> isoladamente."""

    def _parse(self, s: str) -> int:
        p = _Parser(s)
        return p.parse_unidade()

    def test_IX(self):
        self.assertEqual(self._parse('IX'), 9)

    def test_VIII(self):
        self.assertEqual(self._parse('VIII'), 8)

    def test_VII(self):
        self.assertEqual(self._parse('VII'), 7)

    def test_VI(self):
        self.assertEqual(self._parse('VI'), 6)

    def test_V(self):
        self.assertEqual(self._parse('V'), 5)

    def test_IV(self):
        self.assertEqual(self._parse('IV'), 4)

    def test_III(self):
        self.assertEqual(self._parse('III'), 3)

    def test_II(self):
        self.assertEqual(self._parse('II'), 2)

    def test_I(self):
        self.assertEqual(self._parse('I'), 1)

    def test_epsilon(self):
        self.assertEqual(self._parse(''), 0)

    def test_VIII_antes_de_VII(self):
        p = _Parser('VIII')
        v = p.parse_unidade()
        self.assertEqual(v, 8)
        self.assertEqual(p._pos, 4)


class TestDerivacoesExemplo(unittest.TestCase):
    """
    Verifica as derivações mostradas na especificação formal.

    MCMXLIV:  M(1000) + CM(900) + XL(40) + IV(4) = 1944
    MMMCMXCIX: MMM(3000) + CM(900) + XC(90) + IX(9) = 3999
    """

    def test_MCMXLIV(self):
        self.assertEqual(converter('MCMXLIV'), 1944)

    def test_MMMCMXCIX(self):
        self.assertEqual(converter('MMMCMXCIX'), 3999)

    def test_MMXXIV(self):
        # MM(2000) + XX(20) + IV(4) = 2024
        self.assertEqual(converter('MMXXIV'), 2024)

    def test_XCIX(self):
        # XC(90) + IX(9) = 99
        self.assertEqual(converter('XCIX'), 99)


class TestEntradaInvalida(unittest.TestCase):
    """
    Entradas inválidas devem levantar ValueError (caracteres não consumidos).
    O AFD valida antes de chamar o parser, mas estas verificações garantem
    que o parser também se comporta corretamente como segunda linha de defesa.
    """

    def test_IIII(self):
        # parse_unidade consome III(3); I restante → ValueError
        with self.assertRaises(ValueError):
            converter('IIII')

    def test_VV(self):
        # parse_unidade consome V(5); V restante → ValueError
        with self.assertRaises(ValueError):
            converter('VV')

    def test_MMMM(self):
        # parse_milhar consome MMM(3000); M restante não encaixa → ValueError
        with self.assertRaises(ValueError):
            converter('MMMM')

    def test_IXX(self):
        # parse_unidade consome IX(9); X restante → ValueError
        with self.assertRaises(ValueError):
            converter('IXX')

    def test_VIV(self):
        # parse_unidade consome VI(6); V restante → ValueError
        with self.assertRaises(ValueError):
            converter('VIV')

    def test_IC(self):
        # parse_unidade consome I(1); C restante → ValueError
        with self.assertRaises(ValueError):
            converter('IC')


if __name__ == '__main__':
    unittest.main(verbosity=2)
