"""
Conversor de números romanos via parser recursivo descendente (GLC).

A gramática implementada é:

    GLC = (V, Σ, P, S)
    V = {S, Milhar, Centena, Dezena, Unidade}
    Σ = {I, V, X, L, C, D, M}
    S = <numero>

Cada método de _Parser corresponde a exatamente um não-terminal da gramática,
tornando direta a correspondência entre regras de produção e código.
"""

from __future__ import annotations


class _Parser:
    """
    Parser recursivo descendente para a gramática dos números romanos.

    Mantém internamente um cursor (_pos) sobre a cadeia de entrada.
    Cada método de parse tenta consumir o prefixo que corresponde à sua
    produção, avança o cursor e retorna o valor inteiro representado.
    Produção ε retorna 0 sem avançar o cursor.
    """

    def __init__(self, s: str) -> None:
        self._s: str = s
        self._pos: int = 0

    # ------------------------------------------------------------------
    # Auxiliares de leitura
    # ------------------------------------------------------------------

    def _restante(self) -> str:
        """Retorna o sufixo ainda não consumido da cadeia."""
        return self._s[self._pos:]

    def _consome(self, prefixo: str) -> bool:
        """Tenta consumir *prefixo* no ponto atual; retorna True se bem-sucedido."""
        if self._restante().startswith(prefixo):
            self._pos += len(prefixo)
            return True
        return False

    # ------------------------------------------------------------------
    # Não-terminal: <S>
    # ------------------------------------------------------------------

    def parse_numero(self) -> int:
        """
        Produção: <S> ::= <Milhar> <Centena> <Dezena> <Unidade>

        Ponto de entrada do parser.  Verifica ao final que toda a cadeia
        foi consumida; caso contrário, lança ValueError indicando a posição
        do primeiro caractere não reconhecido.

        Returns:
            Valor inteiro correspondente ao número romano completo.

        Raises:
            ValueError: Se a cadeia não foi totalmente consumida (estrutura
                        inválida que o AFD deveria ter rejeitado antes).
        """
        valor = 0
        # <S> → <Milhar>
        valor += self.parse_milhar()
        # <S> → <Centena>
        valor += self.parse_centena()
        # <S> → <Dezena>
        valor += self.parse_dezena()
        # <S> → <Unidade>
        valor += self.parse_unidade()

        # Garante que toda a cadeia foi consumida
        if self._pos != len(self._s):
            restante = self._restante()
            raise ValueError(
                f"Cadeia inválida: caracteres não reconhecidos a partir da "
                f"posição {self._pos}: '{restante}'"
            )
        return valor

    # ------------------------------------------------------------------
    # Não-terminal: <Milhar>
    # ------------------------------------------------------------------

    def parse_milhar(self) -> int:
        """
        Produção:
            <Milhar> ::= M M M   (3000)
                       | M M     (2000)
                       | M       (1000)
                       | ε

        As alternativas são testadas da mais longa para a mais curta
        (MMM antes de MM antes de M) para evitar que um prefixo menor
        consuma parte de um padrão maior.

        Returns:
            Valor inteiro do componente milhar (0 se ε).
        """
        # <Milhar> → M M M  (3000)
        if self._consome('MMM'):
            return 3000
        # <Milhar> → M M  (2000)
        if self._consome('MM'):
            return 2000
        # <Milhar> → M  (1000)
        if self._consome('M'):
            return 1000
        # <Milhar> → ε
        return 0

    # ------------------------------------------------------------------
    # Não-terminal: <Centena>
    # ------------------------------------------------------------------

    def parse_centena(self) -> int:
        """
        Produção:
            <Centena> ::= C M        (900)
                        | D C C C    (800)
                        | D C C      (700)
                        | D C        (600)
                        | D          (500)
                        | C D        (400)
                        | C C C      (300)
                        | C C        (200)
                        | C          (100)
                        | ε

        Ordem: padrões de 4 caracteres antes dos de 3, 2 e 1, garantindo
        que DCCC seja reconhecido antes de DCC, DCC antes de DC, etc.

        Returns:
            Valor inteiro do componente centena (0 se ε).
        """
        # <Centena> → C M  (900)
        if self._consome('CM'):
            return 900
        # <Centena> → D C C C  (800)
        if self._consome('DCCC'):
            return 800
        # <Centena> → D C C  (700)
        if self._consome('DCC'):
            return 700
        # <Centena> → D C  (600)
        if self._consome('DC'):
            return 600
        # <Centena> → D  (500)
        if self._consome('D'):
            return 500
        # <Centena> → C D  (400)
        if self._consome('CD'):
            return 400
        # <Centena> → C C C  (300)
        if self._consome('CCC'):
            return 300
        # <Centena> → C C  (200)
        if self._consome('CC'):
            return 200
        # <Centena> → C  (100)
        if self._consome('C'):
            return 100
        # <Centena> → ε
        return 0

    # ------------------------------------------------------------------
    # Não-terminal: <Dezena>
    # ------------------------------------------------------------------

    def parse_dezena(self) -> int:
        """
        Produção:
            <Dezena> ::= X C         (90)
                       | L X X X     (80)
                       | L X X       (70)
                       | L X         (60)
                       | L           (50)
                       | X L         (40)
                       | X X X       (30)
                       | X X         (20)
                       | X           (10)
                       | ε

        Returns:
            Valor inteiro do componente dezena (0 se ε).
        """
        # <Dezena> → X C  (90)
        if self._consome('XC'):
            return 90
        # <Dezena> → L X X X  (80)
        if self._consome('LXXX'):
            return 80
        # <Dezena> → L X X  (70)
        if self._consome('LXX'):
            return 70
        # <Dezena> → L X  (60)
        if self._consome('LX'):
            return 60
        # <Dezena> → L  (50)
        if self._consome('L'):
            return 50
        # <Dezena> → X L  (40)
        if self._consome('XL'):
            return 40
        # <Dezena> → X X X  (30)
        if self._consome('XXX'):
            return 30
        # <Dezena> → X X  (20)
        if self._consome('XX'):
            return 20
        # <Dezena> → X  (10)
        if self._consome('X'):
            return 10
        # <Dezena> → ε
        return 0

    # ------------------------------------------------------------------
    # Não-terminal: <Unidade>
    # ------------------------------------------------------------------

    def parse_unidade(self) -> int:
        """
        Produção:
            <Unidade> ::= I X        (9)
                        | V I I I    (8)
                        | V I I      (7)
                        | V I        (6)
                        | V          (5)
                        | I V        (4)
                        | I I I      (3)
                        | I I        (2)
                        | I          (1)
                        | ε

        Returns:
            Valor inteiro do componente unidade (0 se ε).
        """
        # <Unidade> → I X  (9)
        if self._consome('IX'):
            return 9
        # <Unidade> → V I I I  (8)
        if self._consome('VIII'):
            return 8
        # <Unidade> → V I I  (7)
        if self._consome('VII'):
            return 7
        # <Unidade> → V I  (6)
        if self._consome('VI'):
            return 6
        # <Unidade> → V  (5)
        if self._consome('V'):
            return 5
        # <Unidade> → I V  (4)
        if self._consome('IV'):
            return 4
        # <Unidade> → I I I  (3)
        if self._consome('III'):
            return 3
        # <Unidade> → I I  (2)
        if self._consome('II'):
            return 2
        # <Unidade> → I  (1)
        if self._consome('I'):
            return 1
        # <Unidade> → ε
        return 0


# ---------------------------------------------------------------------------
# Interface pública
# ---------------------------------------------------------------------------

def converter(s: str) -> int:
    """
    Converte um número romano canônico para seu equivalente inteiro.

    Usa o parser recursivo descendente baseado na GLC.  A entrada deve ter
    sido previamente validada pelo AFD; caso contrário, pode ser levantado
    um ValueError se a cadeia não for completamente consumida.

    Args:
        s: Número romano em letras maiúsculas (ex.: 'MCMXLIV').

    Returns:
        Valor inteiro correspondente (1–3999).

    Raises:
        ValueError: Se *s* contiver estrutura não reconhecida pela GLC.

    Examples:
        >>> converter('MCMXLIV')
        1944
        >>> converter('MMMCMXCIX')
        3999
        >>> converter('I')
        1
    """
    parser = _Parser(s)
    return parser.parse_numero()
