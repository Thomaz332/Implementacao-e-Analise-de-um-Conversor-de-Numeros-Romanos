"""
Conversor imperativo de números romanos — abordagem baseline.

Implementação clássica por loop simples: percorre a cadeia da esquerda para
a direita e soma ou subtrai cada símbolo conforme o próximo símbolo seja
menor ou maior.  Não realiza validação formal — serve exclusivamente como
referência comparativa frente à abordagem fundamentada em modelos formais
(AFD + GLC).
"""

from __future__ import annotations

# Tabela de valores dos símbolos romanos
VALORES: dict[str, int] = {
    'I':    1,
    'V':    5,
    'X':   10,
    'L':   50,
    'C':  100,
    'D':  500,
    'M': 1000,
}


def converter(s: str) -> int:
    """
    Converte um número romano para inteiro usando o algoritmo iterativo clássico.

    Algoritmo:
        Para cada símbolo na posição i:
          - Se o símbolo seguinte (i+1) tiver valor maior, subtrair o atual.
          - Caso contrário, somar o atual.
        Isso captura automaticamente os pares subtrativos canônicos
        (IV, IX, XL, XC, CD, CM).

    Esta abordagem não valida a canonicidade da entrada: aceita silenciosamente
    formas inválidas como IIII (retorna 4) ou VX (retorna 5).  Use o AFD
    (src/afd.py) para validação antes de chamar este conversor.

    Args:
        s: Número romano em letras maiúsculas.

    Returns:
        Valor inteiro correspondente.

    Raises:
        KeyError: Se *s* contiver caractere fora do alfabeto {I, V, X, L, C, D, M}.

    Examples:
        >>> converter('MCMXLIV')
        1944
        >>> converter('MMMCMXCIX')
        3999
    """
    total = 0
    for i, simbolo in enumerate(s):
        valor_atual = VALORES[simbolo]
        # Verifica se o próximo símbolo é maior (par subtrativo)
        proximo_maior = (
            i + 1 < len(s) and VALORES[s[i + 1]] > valor_atual
        )
        if proximo_maior:
            total -= valor_atual
        else:
            total += valor_atual
    return total
