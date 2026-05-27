"""
Testes unitários para src/conversor_tradicional.py.

O conversor tradicional não realiza validação formal; estes testes verificam
apenas que, para entradas canônicas válidas, ele produz os mesmos valores
que o parser GLC (fidelidade funcional para o conjunto de entradas válidas).

A divergência de comportamento para entradas inválidas é intencional e
documentada — ela é justamente o que a análise comparativa explora.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conversor_tradicional import converter, VALORES


class TestConverterCasosValidos(unittest.TestCase):
    """Todos os casos válidos obrigatórios com valores esperados."""

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

    def test_pares_subtrativos(self):
        """Verifica cada par subtrativo canônico individualmente."""
        pares = [('IV', 4), ('IX', 9), ('XL', 40), ('XC', 90), ('CD', 400), ('CM', 900)]
        for romano, esperado in pares:
            with self.subTest(romano=romano):
                self.assertEqual(converter(romano), esperado)


class TestConverterCentenas(unittest.TestCase):
    """Todos os 9 valores canônicos de centena."""

    def test_centenas(self):
        casos = [
            ('C', 100), ('CC', 200), ('CCC', 300), ('CD', 400),
            ('D', 500), ('DC', 600), ('DCC', 700), ('DCCC', 800), ('CM', 900),
        ]
        for romano, esperado in casos:
            with self.subTest(romano=romano):
                self.assertEqual(converter(romano), esperado)


class TestConverterDezenas(unittest.TestCase):
    """Todos os 9 valores canônicos de dezena."""

    def test_dezenas(self):
        casos = [
            ('X', 10), ('XX', 20), ('XXX', 30), ('XL', 40),
            ('L', 50), ('LX', 60), ('LXX', 70), ('LXXX', 80), ('XC', 90),
        ]
        for romano, esperado in casos:
            with self.subTest(romano=romano):
                self.assertEqual(converter(romano), esperado)


class TestConverterUnidades(unittest.TestCase):
    """Todos os 9 valores canônicos de unidade."""

    def test_unidades(self):
        casos = [
            ('I', 1), ('II', 2), ('III', 3), ('IV', 4),
            ('V', 5), ('VI', 6), ('VII', 7), ('VIII', 8), ('IX', 9),
        ]
        for romano, esperado in casos:
            with self.subTest(romano=romano):
                self.assertEqual(converter(romano), esperado)


class TestComportamentoComEntradaInvalida(unittest.TestCase):
    """
    Documenta o comportamento do conversor tradicional para entradas inválidas.

    Ao contrário do parser GLC, o conversor tradicional não levanta exceção
    para entradas inválidas — ele simplesmente aplica sua lógica de soma/subtração
    sem verificação de canonicidade.  Este comportamento é intencional e é
    parte da análise comparativa entre as abordagens.
    """

    def test_IIII_retorna_4_sem_excecao(self):
        # Silenciosamente aceita IIII e retorna 4
        self.assertEqual(converter('IIII'), 4)

    def test_VV_retorna_10_sem_excecao(self):
        # Silenciosamente aceita VV e retorna 10
        self.assertEqual(converter('VV'), 10)

    def test_caracter_invalido_levanta_KeyError(self):
        # Único ponto de falha: caractere fora de VALORES levanta KeyError
        with self.assertRaises(KeyError):
            converter('ABC')


class TestTabelaValores(unittest.TestCase):
    """Verifica a tabela VALORES."""

    def test_todos_simbolos_presentes(self):
        for simbolo in ('I', 'V', 'X', 'L', 'C', 'D', 'M'):
            self.assertIn(simbolo, VALORES)

    def test_valores_corretos(self):
        esperados = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        for simbolo, valor in esperados.items():
            with self.subTest(simbolo=simbolo):
                self.assertEqual(VALORES[simbolo], valor)


if __name__ == '__main__':
    unittest.main(verbosity=2)
