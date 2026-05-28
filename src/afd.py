"""
Validador de números romanos baseado em Autômato Finito Determinístico (AFD).

Quíntupla formal:
    K  = ESTADOS            (32 estados; ver constante abaixo)
    Σ  = ALFABETO           = {I, V, X, L, C, D, M}
    δ  = DELTA              (tabela de transição: dicionário de dicionários)
    q₀ = ESTADO_INICIAL     = 'q0'
    F  = ESTADOS_ACEITACAO  = K \\ {q0, qERRO}

Organização do AFD em camadas sequenciais:
    milhar (M*) → centena (C*/D) → dezena (T*/L) → unidade (U*/V)

A camada de milhar aceita 0 a 3 Ms.  Qualquer símbolo não-M a partir de q0
ou de qM* inicia diretamente a camada correta — essa "passagem" é codificada
nas próprias linhas da tabela DELTA, sem estado intermediário extra.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Quíntupla — constantes nomeadas
# ---------------------------------------------------------------------------

ALFABETO: frozenset[str] = frozenset({'I', 'V', 'X', 'L', 'C', 'D', 'M'})

ESTADOS: frozenset[str] = frozenset({
    # Inicial (não-aceitante: cadeia vazia é inválida)
    'q0',
    # Milhar: 1 a 3 repetições de M
    'qM1', 'qM2', 'qM3',
    # Centena: C(100), CC(200), CCC(300), CD(400), D(500),
    #          DC(600), DCC(700), DCCC(800), CM(900)
    'qC1', 'qC2', 'qC3', 'qCD', 'qD', 'qDC1', 'qDC2', 'qDC3', 'qCM',
    # Dezena: X(10), XX(20), XXX(30), XL(40), L(50),
    #         LX(60), LXX(70), LXXX(80), XC(90)
    'qT1', 'qT2', 'qT3', 'qXL', 'qL', 'qLX1', 'qLX2', 'qLX3', 'qXC',
    # Unidade: I(1), II(2), III(3), IV(4), V(5),
    #          VI(6), VII(7), VIII(8), IX(9)
    'qU1', 'qU2', 'qU3', 'qIV', 'qV', 'qVI1', 'qVI2', 'qVI3', 'qIX',
    # Sumidouro de rejeição
    'qERRO',
})

ESTADO_INICIAL: str = 'q0'

# F = K \ {q0, qERRO}: qualquer estado alcançado por cadeia não-vazia válida aceita
ESTADOS_ACEITACAO: frozenset[str] = ESTADOS - {'q0', 'qERRO'}


# ---------------------------------------------------------------------------
# Construção da tabela δ
# ---------------------------------------------------------------------------

def _escape(centena: bool = True, dezena: bool = True, unidade: bool = True) -> dict[str, str]:
    """
    Retorna as transições de 'saída de camada'.

    Quando um estado já processou toda a sua camada e recebe um símbolo
    pertencente à próxima camada, ele delega o processamento diretamente
    para o estado de entrada daquela camada.  Símbolos ausentes no dict
    final levam implicitamente a 'qERRO' via DELTA[estado].get(s, 'qERRO').
    """
    trans: dict[str, str] = {}
    if centena:
        # C e D iniciam a camada de centenas
        trans.update({'C': 'qC1', 'D': 'qD'})
    if dezena:
        # X e L iniciam a camada de dezenas
        trans.update({'X': 'qT1', 'L': 'qL'})
    if unidade:
        # I e V iniciam a camada de unidades
        trans.update({'I': 'qU1', 'V': 'qV'})
    return trans


# Tabela de transição δ: DELTA[estado][símbolo] → próximo estado
# Qualquer (estado, símbolo) ausente é tratado como → 'qERRO' pela função executar().
DELTA: dict[str, dict[str, str]] = {

    # ------------------------------------------------------------------
    # Camada Milhar
    # ------------------------------------------------------------------
    # q0: estado inicial; M avança para qM1; qualquer outro símbolo válido
    #     inicia diretamente a camada correspondente (milhar = ε)
    'q0':  {'M': 'qM1',   **_escape(centena=True, dezena=True, unidade=True)},
    'qM1': {'M': 'qM2',   **_escape(centena=True, dezena=True, unidade=True)},
    'qM2': {'M': 'qM3',   **_escape(centena=True, dezena=True, unidade=True)},
    # qM3: terceiro M (3000); um quarto M viola "máximo 3 repetições" → qERRO
    'qM3': {'M': 'qERRO', **_escape(centena=True, dezena=True, unidade=True)},

    # ------------------------------------------------------------------
    # Camada Centena
    # ------------------------------------------------------------------
    # qC1 (100): pode acumular C→CC, subtrait D→CD ou M→CM
    'qC1':  {'C': 'qC2', 'D': 'qCD', 'M': 'qCM',
              **_escape(centena=False, dezena=True, unidade=True)},
    # qC2 (200): aceita mais um C→CCC; D e M já não são permitidos aqui
    'qC2':  {'C': 'qC3',
              **_escape(centena=False, dezena=True, unidade=True)},
    # qC3 (300): nenhum C/D/M adicional (CCCC proibido)
    'qC3':  {**_escape(centena=False, dezena=True, unidade=True)},
    # qCD (400): par subtrativo completo; camada centena encerrada
    'qCD':  {**_escape(centena=False, dezena=True, unidade=True)},
    # qD (500): D sozinho; aceita até 3 Cs subsequentes
    'qD':   {'C': 'qDC1',
              **_escape(centena=False, dezena=True, unidade=True)},
    # qDC1 (600)
    'qDC1': {'C': 'qDC2',
              **_escape(centena=False, dezena=True, unidade=True)},
    # qDC2 (700)
    'qDC2': {'C': 'qDC3',
              **_escape(centena=False, dezena=True, unidade=True)},
    # qDC3 (800): DCCCC proibido
    'qDC3': {**_escape(centena=False, dezena=True, unidade=True)},
    # qCM (900): par subtrativo completo
    'qCM':  {**_escape(centena=False, dezena=True, unidade=True)},

    # ------------------------------------------------------------------
    # Camada Dezena
    # ------------------------------------------------------------------
    # qT1 (10): pode acumular X→XX, subtrair L→XL ou C→XC
    'qT1':  {'X': 'qT2', 'L': 'qXL', 'C': 'qXC',
              **_escape(centena=False, dezena=False, unidade=True)},
    # qT2 (20)
    'qT2':  {'X': 'qT3',
              **_escape(centena=False, dezena=False, unidade=True)},
    # qT3 (30): XXXX proibido
    'qT3':  {**_escape(centena=False, dezena=False, unidade=True)},
    # qXL (40): par subtrativo completo
    'qXL':  {**_escape(centena=False, dezena=False, unidade=True)},
    # qL (50): aceita até 3 Xs subsequentes
    'qL':   {'X': 'qLX1',
              **_escape(centena=False, dezena=False, unidade=True)},
    # qLX1 (60)
    'qLX1': {'X': 'qLX2',
              **_escape(centena=False, dezena=False, unidade=True)},
    # qLX2 (70)
    'qLX2': {'X': 'qLX3',
              **_escape(centena=False, dezena=False, unidade=True)},
    # qLX3 (80): LXXXX proibido
    'qLX3': {**_escape(centena=False, dezena=False, unidade=True)},
    # qXC (90): par subtrativo completo
    'qXC':  {**_escape(centena=False, dezena=False, unidade=True)},

    # ------------------------------------------------------------------
    # Camada Unidade
    # ------------------------------------------------------------------
    # qU1 (1): pode acumular I→II, subtrair V→IV ou X→IX
    'qU1':  {'I': 'qU2', 'V': 'qIV', 'X': 'qIX'},
    # qU2 (2)
    'qU2':  {'I': 'qU3'},
    # qU3 (3): IIII proibido
    'qU3':  {},
    # qIV (4): par subtrativo completo
    'qIV':  {},
    # qV (5): aceita até 3 Is subsequentes
    'qV':   {'I': 'qVI1'},
    # qVI1 (6)
    'qVI1': {'I': 'qVI2'},
    # qVI2 (7)
    'qVI2': {'I': 'qVI3'},
    # qVI3 (8): VIIII proibido
    'qVI3': {},
    # qIX (9): par subtrativo completo
    'qIX':  {},

    # ------------------------------------------------------------------
    # Sumidouro de rejeição
    # ------------------------------------------------------------------
    # qERRO absorve qualquer símbolo; uma vez neste estado, não há retorno
    'qERRO': {s: 'qERRO' for s in ALFABETO},
}


# ---------------------------------------------------------------------------
# Funções públicas
# ---------------------------------------------------------------------------

def executar(s: str) -> tuple[bool, list[str]]:
    """
    Executa o AFD sobre a cadeia *s* e retorna o resultado com rastreio de estados.

    O histórico inclui o estado inicial seguido de um estado por símbolo lido,
    permitindo reconstruir exatamente qual transição causou uma rejeição.

    Args:
        s: Cadeia a ser analisada (qualquer string; caracteres fora de Σ
           provocam transição imediata para qERRO).

    Returns:
        Tupla (aceito, historico) onde:
          - aceito   : True se a cadeia é um número romano canônico válido.
          - historico: Lista de estados percorridos, começando em ESTADO_INICIAL.

    Examples:
        >>> aceito, hist = executar('XIV')
        >>> aceito
        True
        >>> hist
        ['q0', 'qT1', 'qU1', 'qIV']

        >>> aceito, hist = executar('IIII')
        >>> aceito
        False
        >>> hist
        ['q0', 'qU1', 'qU2', 'qU3', 'qERRO']
    """
    estado = ESTADO_INICIAL
    historico: list[str] = [estado]

    for simbolo in s:
        if simbolo not in ALFABETO:
            # Símbolo fora de Σ: transição direta para qERRO
            estado = 'qERRO'
        else:
            estado = DELTA[estado].get(simbolo, 'qERRO')
        historico.append(estado)

    aceito = (len(s) > 0) and (estado in ESTADOS_ACEITACAO)
    return aceito, historico


def validar(s: str) -> bool:
    """
    Retorna True se *s* é um número romano canônico válido (1–3999).

    Internamente delega a :func:`executar`; use esta função quando o histórico
    de estados não for necessário.

    Args:
        s: Cadeia a ser validada.

    Returns:
        True para cadeias válidas; False caso contrário.

    Examples:
        >>> validar('MMMCMXCIX')
        True
        >>> validar('IIII')
        False
    """
    aceito, _ = executar(s)
    return aceito


def posicao_erro(s: str, historico: list[str]) -> int | None:
    """
    Retorna o índice (0-based) do primeiro caractere problemático em *s*,
    ou None se não houver erro.

    O índice é calculado a partir do histórico: historico[0] é o estado
    inicial (antes de qualquer símbolo), historico[i+1] é o estado após
    consumir s[i].  Portanto, a primeira ocorrência de 'qERRO' em
    historico[1:] corresponde ao símbolo s[i] onde i = índice − 1.

    Args:
        s:         Cadeia analisada.
        historico: Histórico retornado por :func:`executar`.

    Returns:
        Índice 0-based do símbolo que causou a transição para qERRO,
        ou None se a cadeia foi aceita.

    Examples:
        >>> _, hist = executar('IIII')
        >>> posicao_erro('IIII', hist)
        3
    """
    for i, estado in enumerate(historico[1:], start=0):
        if estado == 'qERRO':
            return i
    return None
