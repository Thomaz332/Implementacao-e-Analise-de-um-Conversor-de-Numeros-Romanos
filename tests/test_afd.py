"""
Testes unitários para src/afd.py.

Cobertura:
  - Todos os casos válidos obrigatórios (spec §5)
  - Todos os casos inválidos obrigatórios (spec §5)
  - Casos de fronteira: menor (I=1) e maior (MMMCMXCIX=3999)
  - Verificação do histórico de estados para trajetórias conhecidas
  - Verificação da posição do erro
  - Consistência estrutural do AFD (estados, alfabeto, DELTA completo)
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from afd import (
    validar,
    executar,
    posicao_erro,
    ESTADOS,
    ALFABETO,
    DELTA,
    ESTADO_INICIAL,
    ESTADOS_ACEITACAO,
)


class TestValidarCasosValidos(unittest.TestCase):
    """Casos que o AFD deve aceitar (F contém o estado final)."""

    VALIDOS = [
        ('I',          1),
        ('II',         2),
        ('III',        3),
        ('IV',         4),
        ('V',          5),
        ('IX',         9),
        ('X',         10),
        ('XL',        40),
        ('XLII',      42),
        ('XC',        90),
        ('XCIX',      99),
        ('C',        100),
        ('CD',       400),
        ('CM',       900),
        ('D',        500),
        ('M',       1000),
        ('MMXXIV',  2024),
        ('MMMCMXCIX', 3999),
    ]

    def test_todos_aceitos(self):
        for romano, _ in self.VALIDOS:
            with self.subTest(romano=romano):
                self.assertTrue(validar(romano), f"'{romano}' deveria ser válido")

    def test_fronteira_minima(self):
        self.assertTrue(validar('I'))

    def test_fronteira_maxima(self):
        self.assertTrue(validar('MMMCMXCIX'))

    def test_todos_os_milhares(self):
        for romano in ('M', 'MM', 'MMM'):
            with self.subTest(romano=romano):
                self.assertTrue(validar(romano))

    def test_centenas_canonicas(self):
        casos = ['C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
        for romano in casos:
            with self.subTest(romano=romano):
                self.assertTrue(validar(romano))

    def test_dezenas_canonicas(self):
        casos = ['X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
        for romano in casos:
            with self.subTest(romano=romano):
                self.assertTrue(validar(romano))

    def test_unidades_canonicas(self):
        casos = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
        for romano in casos:
            with self.subTest(romano=romano):
                self.assertTrue(validar(romano))


class TestValidarCasosInvalidos(unittest.TestCase):
    """Casos que o AFD deve rejeitar."""

    def test_cadeia_vazia(self):
        # Vazio: não representa nenhum número; q0 ∉ F
        self.assertFalse(validar(''))

    def test_quatro_Is(self):
        # IIII: quarta repetição de I viola regra (máximo 3 repetições aditivas)
        self.assertFalse(validar('IIII'))

    def test_VV(self):
        # VV: V nunca se repete
        self.assertFalse(validar('VV'))

    def test_LL(self):
        # LL: L nunca se repete
        self.assertFalse(validar('LL'))

    def test_DD(self):
        # DD: D nunca se repete
        self.assertFalse(validar('DD'))

    def test_VX(self):
        # VX: V está na camada unidade; X na dezena — após V, a camada dezena
        # já foi superada; X aqui é inválido
        self.assertFalse(validar('VX'))

    def test_IC(self):
        # IC: par subtrativo inválido — I só pode subtrair V e X
        self.assertFalse(validar('IC'))

    def test_IL(self):
        # IL: par subtrativo inválido — I só pode subtrair V e X
        self.assertFalse(validar('IL'))

    def test_XM(self):
        # XM: par subtrativo inválido — X só pode subtrair L e C
        self.assertFalse(validar('XM'))

    def test_AB(self):
        # AB: caracteres fora do alfabeto Σ
        self.assertFalse(validar('AB'))

    def test_MMMM(self):
        # MMMM: quarto M excede o valor máximo 3999; qM3 + M → qERRO
        self.assertFalse(validar('MMMM'))

    def test_minusculas(self):
        # abc: minúsculas não pertencem a Σ
        self.assertFalse(validar('abc'))

    def test_digitos(self):
        # 123: dígitos não pertencem a Σ
        self.assertFalse(validar('123'))

    def test_IXX(self):
        # IXX: IX é o par subtrativo 9; X seguinte é inválido após qIX
        self.assertFalse(validar('IXX'))

    def test_VIV(self):
        # VIV: VI = 6, mas o V seguinte é inválido (V não pode aparecer
        # novamente na camada unidade)
        self.assertFalse(validar('VIV'))

    def test_mistura_validos_invalidos(self):
        # Palavras mistas com letras romanas mas padrão inválido
        for invalido in ('IIM', 'MIM', 'CMM', 'XCX', 'CDC', 'IVI'):
            with self.subTest(invalido=invalido):
                self.assertFalse(validar(invalido))


class TestExecutarHistorico(unittest.TestCase):
    """Verifica que o histórico de estados percorridos está correto."""

    def test_historico_XIV(self):
        # X(10) → T1, I(1) → U1, V → IV(4): XIV = 14
        aceito, hist = executar('XIV')
        self.assertTrue(aceito)
        self.assertEqual(hist, ['q0', 'qT1', 'qU1', 'qIV'])

    def test_historico_IIII_erro(self):
        # III = 3 (qU3), quarto I → qERRO
        aceito, hist = executar('IIII')
        self.assertFalse(aceito)
        self.assertEqual(hist, ['q0', 'qU1', 'qU2', 'qU3', 'qERRO'])

    def test_historico_MMMCMXCIX(self):
        # MMM(3000) → CM(900) → XC(90) → IX(9) = 3999
        aceito, hist = executar('MMMCMXCIX')
        self.assertTrue(aceito)
        self.assertEqual(
            hist,
            ['q0', 'qM1', 'qM2', 'qM3', 'qC1', 'qCM', 'qT1', 'qXC', 'qU1', 'qIX'],
        )

    def test_historico_MMXXIV(self):
        # MM(2000) → XX(20) → IV(4) = 2024
        aceito, hist = executar('MMXXIV')
        self.assertTrue(aceito)
        self.assertEqual(hist, ['q0', 'qM1', 'qM2', 'qT1', 'qT2', 'qU1', 'qIV'])

    def test_historico_vazio(self):
        # Cadeia vazia: permanece em q0 (não-aceitante)
        aceito, hist = executar('')
        self.assertFalse(aceito)
        self.assertEqual(hist, ['q0'])

    def test_historico_caracter_invalido(self):
        # Primeiro caractere fora de Σ → qERRO imediato
        aceito, hist = executar('A')
        self.assertFalse(aceito)
        self.assertEqual(hist, ['q0', 'qERRO'])

    def test_comprimento_historico(self):
        # O histórico deve ter len(s) + 1 elementos (estado inicial + um por símbolo)
        for s in ('I', 'XIV', 'MMMCMXCIX', 'IIII'):
            with self.subTest(s=s):
                _, hist = executar(s)
                self.assertEqual(len(hist), len(s) + 1)


class TestPosicaoErro(unittest.TestCase):
    """Verifica detecção da posição do caractere problemático."""

    def test_sem_erro(self):
        _, hist = executar('XIV')
        self.assertIsNone(posicao_erro('XIV', hist))

    def test_quarto_I(self):
        # IIII: erro no índice 3 (o quarto 'I')
        _, hist = executar('IIII')
        self.assertEqual(posicao_erro('IIII', hist), 3)

    def test_quarto_M(self):
        # MMMM: erro no índice 3 (o quarto 'M')
        _, hist = executar('MMMM')
        self.assertEqual(posicao_erro('MMMM', hist), 3)

    def test_caracter_invalido_posicao_zero(self):
        # 'A': erro logo no primeiro símbolo (índice 0)
        _, hist = executar('ABC')
        self.assertEqual(posicao_erro('ABC', hist), 0)

    def test_IC_posicao_um(self):
        # IC: I(0) válido → qU1; C(1) → qERRO (IC não é par subtrativo válido)
        _, hist = executar('IC')
        self.assertEqual(posicao_erro('IC', hist), 1)

    def test_VIV_posicao_dois(self):
        # VIV: V(0)→qV, I(1)→qVI1, V(2)→qERRO
        _, hist = executar('VIV')
        self.assertEqual(posicao_erro('VIV', hist), 2)


class TestConsistenciaAFD(unittest.TestCase):
    """Verifica invariantes estruturais do AFD."""

    def test_estado_inicial_em_K(self):
        self.assertIn(ESTADO_INICIAL, ESTADOS)

    def test_estados_aceitacao_subset_K(self):
        self.assertTrue(ESTADOS_ACEITACAO.issubset(ESTADOS))

    def test_q0_nao_e_aceitante(self):
        # Cadeia vazia não é válida; q0 não deve ser estado de aceitação
        self.assertNotIn('q0', ESTADOS_ACEITACAO)

    def test_qERRO_nao_e_aceitante(self):
        self.assertNotIn('qERRO', ESTADOS_ACEITACAO)

    def test_delta_cobre_todos_os_estados(self):
        # Cada estado deve ter uma entrada em DELTA
        for estado in ESTADOS:
            with self.subTest(estado=estado):
                self.assertIn(estado, DELTA)

    def test_delta_destinos_validos(self):
        # Todos os destinos de DELTA devem ser estados conhecidos
        for origem, transicoes in DELTA.items():
            for simbolo, destino in transicoes.items():
                with self.subTest(origem=origem, simbolo=simbolo):
                    self.assertIn(destino, ESTADOS)

    def test_delta_simbolos_validos(self):
        # Todos os símbolos em DELTA devem pertencer a Σ
        for origem, transicoes in DELTA.items():
            for simbolo in transicoes:
                with self.subTest(origem=origem, simbolo=simbolo):
                    self.assertIn(simbolo, ALFABETO)

    def test_qERRO_e_sumidouro(self):
        # qERRO deve ter transição para qERRO para todos os símbolos do alfabeto
        for simbolo in ALFABETO:
            with self.subTest(simbolo=simbolo):
                self.assertEqual(DELTA['qERRO'].get(simbolo), 'qERRO')


if __name__ == '__main__':
    unittest.main(verbosity=2)
