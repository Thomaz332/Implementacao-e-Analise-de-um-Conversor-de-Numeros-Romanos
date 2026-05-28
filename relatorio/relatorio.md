# Implementação e Análise de um Conversor de Números Romanos Fundamentado em Modelos Formais

**Disciplina:** Teoria da Computação  
**Linguagem de implementação:** Python 3.10+  
**Repositório:** `src/` (AFD, GLC parser, conversor tradicional, CLI)

---

## Resumo

Este trabalho apresenta a implementação de um conversor de números romanos para arábicos com fundamentação rigorosa em modelos formais da Teoria da Computação. A solução é estruturada em dois estágios: um Autômato Finito Determinístico (AFD) que valida se a cadeia de entrada é um número romano canônico válido no intervalo 1–3999, e um parser recursivo descendente derivado de uma Gramática Livre de Contexto (GLC) que realiza a conversão propriamente dita. Paralelamente, uma terceira implementação imperativa clássica (baseada em loop e tabela de valores) serve como linha de base para análise comparativa. O AFD é especificado formalmente pela quíntupla `(K, Σ, δ, q₀, F)` com 32 estados organizados em quatro camadas (milhar, centena, dezena, unidade) e implementado como uma tabela de transição `δ` explícita (dicionário de dicionários em Python), sem ramificações condicionais para a lógica de autômato. A GLC é definida em notação BNF com cinco não-terminais e produz um parser em que cada função implementa exatamente uma produção gramatical, tornando direta a correspondência entre teoria e código. A suíte de testes unitários cobre 107 casos, incluindo todos os casos válidos e inválidos obrigatórios especificados, além de verificações estruturais do AFD. Os resultados demonstram que a abordagem formal, embora mais extensa, oferece vantagens significativas em clareza de especificação, rastreabilidade de erros (o AFD fornece a trajetória de estados percorridos) e fidelidade à linguagem formal definida, ao custo de maior complexidade inicial de modelagem.

**Palavras-chave:** Autômato Finito Determinístico, Gramática Livre de Contexto, parser recursivo descendente, números romanos, Teoria da Computação.

---

## 1. Introdução

Os números romanos constituem um sistema de numeração posicional aditivo-subtrativo utilizado na Roma Antiga e ainda presente em contextos contemporâneos como relógios, numeração de séculos e créditos cinematográficos. Sua estrutura, embora aparentemente simples, apresenta um conjunto preciso de restrições sintáticas que a tornam um objeto de estudo adequado para a aplicação de modelos formais da Teoria da Computação.

O problema central deste trabalho é: *como implementar um conversor de números romanos que seja formalmente fundamentado, rastreável e facilmente verificável contra uma especificação precisa?* A resposta usual na prática de engenharia de software é uma abordagem imperativa — um simples laço que percorre a string e soma ou subtrai valores conforme o símbolo seguinte. Essa solução funciona corretamente para entradas válidas, mas não oferece mecanismos explícitos de rejeição de entradas inválidas nem uma especificação formal verificável.

Este trabalho propõe uma alternativa: modelar a linguagem dos números romanos com as ferramentas formais estudadas na disciplina de Teoria da Computação, implementar os modelos de forma que o código seja um reflexo direto da especificação formal, e analisar as diferenças em qualidade de software entre a abordagem formal e a abordagem imperativa.

Os objetivos específicos são:

1. Definir formalmente a linguagem dos números romanos canônicos (1–3999) como uma linguagem regular por meio de um AFD.
2. Definir uma GLC equivalente para a mesma linguagem e implementar um parser recursivo descendente.
3. Implementar a abordagem imperativa clássica como linha de base comparativa.
4. Desenvolver uma suíte de testes unitários abrangente.
5. Analisar comparativamente as três abordagens em termos de clareza, manutenibilidade e fidelidade formal.

O restante deste relatório está organizado da seguinte forma: a Seção 2 apresenta a fundamentação teórica; a Seção 3 descreve a metodologia de formalização da linguagem; a Seção 4 detalha o desenvolvimento de cada componente; a Seção 5 apresenta os resultados experimentais; a Seção 6 realiza a análise comparativa; e a Seção 7 conclui com limitações e trabalhos futuros.

---

## 2. Fundamentação Teórica

### 2.1 Linguagens Regulares e Autômatos Finitos Determinísticos

Uma linguagem formal é um conjunto de cadeias sobre um alfabeto finito Σ. As linguagens regulares constituem a classe mais simples na hierarquia de Chomsky e são precisamente as linguagens reconhecidas por autômatos finitos (AHO; SETHI; ULLMAN, 1995).

Um **Autômato Finito Determinístico (AFD)** é uma quíntupla `M = (K, Σ, δ, q₀, F)` onde:

- `K` é um conjunto finito de estados;
- `Σ` é o alfabeto de entrada;
- `δ: K × Σ → K` é a função de transição total e determinística;
- `q₀ ∈ K` é o estado inicial;
- `F ⊆ K` é o conjunto de estados de aceitação.

O AFD processa uma cadeia `w = a₁a₂...aₙ` de forma que `δ̂(q₀, w) = qₙ`; a cadeia é aceita se e somente se `qₙ ∈ F`. A propriedade de determinismo garante que para cada par `(estado, símbolo)` existe exatamente uma transição definida, eliminando ambiguidades de processamento (BARBOSA, 2021).

A representação mais natural de um AFD em código é uma **tabela de transição** — uma estrutura de dados bidimensional que mapeia `(estado, símbolo) → estado`. Em Python, isso se traduz diretamente em um dicionário de dicionários `δ[estado][símbolo]`, que é exatamente a estrutura adotada neste projeto.

### 2.2 Gramáticas Livres de Contexto e Parsers Recursivos Descendentes

Uma **Gramática Livre de Contexto (GLC)** é uma quádrupla `G = (V, Σ, P, S)` onde `V` é o conjunto de variáveis (não-terminais), `Σ` é o alfabeto de terminais, `P` é o conjunto de produções da forma `A → α` com `A ∈ V` e `α ∈ (V ∪ Σ)*`, e `S ∈ V` é o símbolo inicial. A linguagem gerada por `G`, denotada `L(G)`, é o conjunto de todas as cadeias de terminais deriváveis a partir de `S` (AHO; SETHI; ULLMAN, 1995).

Para linguagens regulares, sempre existe tanto um AFD quanto uma GLC que geram a mesma linguagem — as linguagens regulares são um subconjunto próprio das linguagens livres de contexto. Neste projeto, o mesmo conjunto de cadeias válidas (números romanos 1–3999) é descrito pelos dois formalismos, permitindo comparar suas formas de uso prático.

Um **parser recursivo descendente** é uma técnica de análise sintática descendente (*top-down*) na qual cada não-terminal da gramática corresponde a uma função de análise. A função tenta casar a entrada com as alternativas de produção do não-terminal, da mais longa para a mais curta (para evitar ambiguidades). Essa técnica é eficiente para gramáticas LL(k) — gramáticas analisáveis da esquerda para a direita com *k* símbolos de lookahead (BARBOSA, 2021).

A linguagem dos números romanos é LL(1): em cada posição, um único símbolo de lookahead é suficiente para determinar qual alternativa da gramática aplicar. Por exemplo, se o próximo símbolo é `C`, basta verificar o caractere seguinte para distinguir `C` (100), `CC` (200), `CCC` (300), `CD` (400) e `CM` (900).

### 2.3 Análise Léxica vs. Sintática

Na teoria de compiladores, a análise léxica (reconhecimento de tokens) tipicamente usa autômatos finitos, enquanto a análise sintática usa gramáticas livres de contexto e seus parsers (AHO; SETHI; ULLMAN, 1995). Neste projeto, embora a linguagem dos números romanos seja regular (e portanto reconhecível por um AFD), optou-se por implementar também uma GLC para demonstrar como os dois formalismos se complementam em um pipeline de processamento: o AFD valida, a GLC converte.

---

## 3. Metodologia

### 3.1 Definição da linguagem

O primeiro passo foi definir precisamente o conjunto de cadeias que constituem números romanos válidos. A decisão mais importante é a escolha da **forma canônica**: para cada inteiro de 1 a 3999, existe exatamente uma representação romana canônica, e o projeto trabalha exclusivamente com ela.

As regras de canonicidade são:

1. **Máximo 3 repetições aditivas:** `I`, `X`, `C`, `M` podem aparecer no máximo 3 vezes consecutivas.
2. **Símbolos únicos:** `V`, `L`, `D` aparecem no máximo uma vez cada.
3. **Pares subtrativos obrigatórios:** as formas 4, 9, 40, 90, 400 e 900 são representadas *exclusivamente* pelos pares `IV`, `IX`, `XL`, `XC`, `CD`, `CM`. Formas como `IIII` (4) ou `DCCCC` (900) são inválidas.
4. **Sequência decrescente de camadas:** milhar → centena → dezena → unidade. Um símbolo de camada inferior não pode preceder um de camada superior a não ser que formem um par subtrativo válido.

### 3.2 Escolha do formalismo

A linguagem dos números romanos é regular (pode ser descrita por uma expressão regular), o que justifica o uso de um AFD para validação. O AFD é especialmente adequado porque:

- Tem complexidade temporal O(n) no tamanho da entrada;
- A tabela de transição serve diretamente como documentação executável da especificação;
- O histórico de estados percorridos fornece diagnóstico preciso de erros.

A GLC é usada para a conversão porque a estrutura hierárquica (milhar + centena + dezena + unidade) é naturalmente expressa por regras de produção, e o parser recursivo descendente resultante tem código diretamente legível em termos das regras gramaticais.

---

## 4. Desenvolvimento

### 4.1 AFD — Especificação e Implementação

#### 4.1.1 Quíntupla formal

```
AFD = (K, Σ, δ, q₀, F)

Σ = {I, V, X, L, C, D, M}

K = {q0, qM1, qM2, qM3,
     qC1, qC2, qC3, qCD, qD, qDC1, qDC2, qDC3, qCM,
     qT1, qT2, qT3, qXL, qL, qLX1, qLX2, qLX3, qXC,
     qU1, qU2, qU3, qIV, qV, qVI1, qVI2, qVI3, qIX,
     qERRO}   — total: 32 estados

q₀ = q0

F = K \ {q0, qERRO}   — 30 estados de aceitação
```

Os estados são organizados em quatro camadas sequenciais. O prefixo do nome indica a camada: `qM*` (milhar), `qC*/qD*` (centena), `qT*/qL*/qXL/qXC` (dezena), `qU*/qV*/qIV/qIX` (unidade).

#### 4.1.2 Diagrama do AFD (por camadas)

O diagrama completo em Mermaid está em `docs/diagrama_afd.md`. Abaixo, a trajetória de dois exemplos ilustrativos:

**Exemplo 1: `IIII` (inválido)**
```
q0 -I-> qU1 -I-> qU2 -I-> qU3 -I-> qERRO  ✗
```
O quarto `I` dispara a transição para `qERRO`; estado final `qERRO ∉ F`.

**Exemplo 2: `MMMCMXCIX` (válido = 3999)**
```
q0 -M-> qM1 -M-> qM2 -M-> qM3 -C-> qC1 -M-> qCM -X-> qT1 -C-> qXC -I-> qU1 -X-> qIX  ✓
```
Estado final `qIX ∈ F`.

#### 4.1.3 Tabela de transição por camada (parcial)

**Camada Milhar:**

| Estado | I | V | X | L | C | D | M |
|--------|---|---|---|---|---|---|---|
| q0     |→qU1|→qV|→qT1|→qL|→qC1|→qD| qM1 |
| qM1    |→qU1|→qV|→qT1|→qL|→qC1|→qD| qM2 |
| qM2    |→qU1|→qV|→qT1|→qL|→qC1|→qD| qM3 |
| qM3    |→qU1|→qV|→qT1|→qL|→qC1|→qD|qERRO|

**Camada Centena (seleção):**

| Estado | C | D | M | X/L/I/V |
|--------|---|---|---|---------|
| qC1    | qC2 | qCD | qCM | →dezena/unidade |
| qC2    | qC3 | qERRO | qERRO | →dezena/unidade |
| qD     | qDC1 | qERRO | qERRO | →dezena/unidade |

A tabela completa está implementada em `src/afd.py` na constante `DELTA`.

#### 4.1.4 Implementação em Python

A estrutura `DELTA` mapeia cada estado para um dicionário de transições:

```python
DELTA: dict[str, dict[str, str]] = {
    'q0':  {'M': 'qM1', 'C': 'qC1', 'D': 'qD',
             'X': 'qT1', 'L': 'qL', 'I': 'qU1', 'V': 'qV'},
    'qM1': {'M': 'qM2', 'C': 'qC1', 'D': 'qD',
             'X': 'qT1', 'L': 'qL', 'I': 'qU1', 'V': 'qV'},
    # ... (32 estados no total)
    'qERRO': {'I': 'qERRO', 'V': 'qERRO', 'X': 'qERRO',
              'L': 'qERRO', 'C': 'qERRO', 'D': 'qERRO', 'M': 'qERRO'},
}
```

A função `executar` percorre a cadeia consultando `DELTA`:

```python
def executar(s: str) -> tuple[bool, list[str]]:
    estado = ESTADO_INICIAL
    historico = [estado]
    for simbolo in s:
        if simbolo not in ALFABETO:
            estado = 'qERRO'
        else:
            estado = DELTA[estado].get(simbolo, 'qERRO')
        historico.append(estado)
    aceito = (len(s) > 0) and (estado in ESTADOS_ACEITACAO)
    return aceito, historico
```

Observe que **não há um único `if/else` para a lógica do autômato** — toda a inteligência está na tabela `DELTA`. Isso garante que o código seja um reflexo fiel da especificação formal.

### 4.2 GLC — Especificação e Parser

#### 4.2.1 Gramática em BNF

```bnf
<S>       ::= <Milhar> <Centena> <Dezena> <Unidade>

<Milhar>  ::= M M M | M M | M | ε

<Centena> ::= C M | D C C C | D C C | D C | D
            | C D | C C C | C C | C | ε

<Dezena>  ::= X C | L X X X | L X X | L X | L
            | X L | X X X | X X | X | ε

<Unidade> ::= I X | V I I I | V I I | V I | V
            | I V | I I I | I I | I | ε
```

**Restrição extra:** pelo menos um não-terminal deve derivar cadeia não-vazia (a cadeia vazia não é gerada por `<S>`).

#### 4.2.2 Derivação de `MCMXLIV` (1944)

```
S
⟹ Milhar Centena Dezena Unidade
⟹ M Centena Dezena Unidade          [Milhar → M]
⟹ M CM Dezena Unidade               [Centena → CM]
⟹ M CM XL Unidade                   [Dezena → XL]
⟹ M CM XL IV                        [Unidade → IV]
⟹ "MCMXLIV"    ✓   1000+900+40+4 = 1944
```

#### 4.2.3 Derivação de `MMMCMXCIX` (3999)

```
S
⟹ Milhar Centena Dezena Unidade
⟹ MMM Centena Dezena Unidade        [Milhar → MMM]
⟹ MMM CM Dezena Unidade             [Centena → CM]
⟹ MMM CM XC Unidade                 [Dezena → XC]
⟹ MMM CM XC IX                      [Unidade → IX]
⟹ "MMMCMXCIX"    ✓   3000+900+90+9 = 3999
```

#### 4.2.4 Implementação: classe `_Parser`

O parser é implementado como uma classe com um cursor `_pos` sobre a cadeia. Cada método corresponde a exatamente um não-terminal:

```python
class _Parser:
    def parse_milhar(self) -> int:
        # <Milhar> → MMM (3000)
        if self._consome('MMM'): return 3000
        # <Milhar> → MM (2000)
        if self._consome('MM'):  return 2000
        # <Milhar> → M (1000)
        if self._consome('M'):   return 1000
        # <Milhar> → ε
        return 0

    def parse_centena(self) -> int:
        if self._consome('CM'):   return 900
        if self._consome('DCCC'): return 800
        if self._consome('DCC'):  return 700
        if self._consome('DC'):   return 600
        if self._consome('D'):    return 500
        if self._consome('CD'):   return 400
        if self._consome('CCC'):  return 300
        if self._consome('CC'):   return 200
        if self._consome('C'):    return 100
        return 0
    # ... (parse_dezena, parse_unidade seguem o mesmo padrão)
```

A ordem das alternativas (mais longa primeiro) é essencial para o correto funcionamento do parser LL(1): `DCCC` deve ser testado antes de `DCC`, que deve ser testado antes de `DC`.

### 4.3 Conversor Tradicional

A implementação imperativa clássica percorre a string com um índice e decide somar ou subtrair baseado na comparação com o símbolo seguinte:

```python
VALORES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def converter(s: str) -> int:
    total = 0
    for i, simbolo in enumerate(s):
        valor_atual = VALORES[simbolo]
        proximo_maior = (i + 1 < len(s) and VALORES[s[i+1]] > valor_atual)
        total = total - valor_atual if proximo_maior else total + valor_atual
    return total
```

Esta implementação é funcionalmente correta para entradas válidas, mas **não realiza nenhuma validação**: aceita silenciosamente `IIII` retornando 4, e `VV` retornando 10.

### 4.4 Arquitetura do CLI (`main.py`)

O programa principal orquestra os três módulos segundo o pipeline:

```
Entrada → AFD (validar) → [inválida: mensagem de erro com posição]
                        → [válida: GLC parser → resultado]
                                  [--comparar: também conversor tradicional]
```

---

## 5. Resultados

### 5.1 Casos válidos

```
$ python src/main.py I
I = 1

$ python src/main.py IV
IV = 4

$ python src/main.py XCIX
XCIX = 99

$ python src/main.py MMXXIV
MMXXIV = 2024

$ python src/main.py MMMCMXCIX
MMMCMXCIX = 3999
```

### 5.2 Casos inválidos com diagnóstico

```
$ python src/main.py IIII
Erro: 'IIII' não é um número romano canônico válido.
       IIII
          ^
  Caractere problemático: 'I' na posição 3
  Trajetória do AFD: q0 → qU1 → qU2 → qU3 → qERRO

$ python src/main.py MMMM
Erro: 'MMMM' não é um número romano canônico válido.
       MMMM
          ^
  Caractere problemático: 'M' na posição 3
  Trajetória do AFD: q0 → qM1 → qM2 → qM3 → qERRO

$ python src/main.py IC
Erro: 'IC' não é um número romano canônico válido.
       IC
        ^
  Caractere problemático: 'C' na posição 1
  Trajetória do AFD: q0 → qU1 → qERRO

$ python src/main.py VIV
Erro: 'VIV' não é um número romano canônico válido.
       VIV
         ^
  Caractere problemático: 'V' na posição 2
  Trajetória do AFD: q0 → qV → qVI1 → qERRO

$ python src/main.py AB
Erro: 'AB' não é um número romano canônico válido.
       AB
       ^
  Caractere problemático: 'A' na posição 0
  Trajetória do AFD: q0 → qERRO → qERRO
```

### 5.3 Modo comparação

```
$ python src/main.py MCMXLIV --comparar
Resultado (GLC parser):  MCMXLIV = 1944
Resultado (imperativo):  MCMXLIV = 1944
  [OK] Ambas as abordagens concordam.
```

### 5.4 Suíte de testes

```
$ python -m unittest discover tests/ -v

Ran 107 tests in 0.005s
OK
```

Distribuição dos testes:

| Arquivo | Testes | Cobertura |
|---|---|---|
| `test_afd.py` | 44 | Casos válidos, inválidos, histórico, posição de erro, invariantes estruturais |
| `test_glc_parser.py` | 47 | Cada não-terminal isolado, derivações completas, entradas inválidas |
| `test_conversor_tradicional.py` | 16 | Casos válidos, tabela de valores, comportamento com entradas inválidas |

---

## 6. Análise Comparativa

### 6.1 Fidelidade à especificação formal

| Critério | AFD + GLC | Imperativo |
|---|---|---|
| Especificação formal explícita | Sim (quíntupla + BNF) | Não |
| Código reflete a especificação | Diretamente (DELTA = tabela δ; funções = produções) | Indiretamente (regras implícitas no loop) |
| Verificabilidade formal | Alta (estados e transições nomeados) | Baixa |

A abordagem formal tem como principal vantagem a **correspondência direta entre especificação e código**: adicionar uma nova regra (ex.: suporte a números até 9999 com V̄, X̄) requer alterar o modelo formal e depois o código em paralelo, sem risco de divergência silenciosa.

### 6.2 Clareza e manutenibilidade

O conversor tradicional tem **5 linhas de lógica principal** — extremamente conciso. O AFD tem 32 estados e ~90 entradas na tabela; a GLC tem 29 alternativas de produção. O código formal é mais verboso, mas cada linha tem significado preciso.

Para **depuração de casos inválidos**, a vantagem da abordagem formal é clara: o AFD fornece a trajetória completa de estados (`q0 → qU1 → qU2 → qU3 → qERRO`) e a posição exata do erro. O conversor tradicional, sem mecanismo de rejeição, simplesmente retorna um valor numericamente incorreto para entradas canônicas erradas sem nenhum aviso.

### 6.3 Complexidade ciclomática estimada

A complexidade ciclomática (número de caminhos independentes) é uma métrica de complexidade estrutural do código:

| Módulo | Complexidade ciclomática estimada |
|---|---|
| `afd.executar()` | 3 (loop + 2 condicionais) |
| `glc_parser._Parser.parse_centena()` | 10 (9 alternativas + ε) |
| `glc_parser._Parser.parse_numero()` | 2 (verificação final) |
| `conversor_tradicional.converter()` | 3 (loop + 2 condicionais) |

A complexidade baixa de `afd.executar()` é notável: toda a complexidade do autômato está na **tabela `DELTA`**, não no fluxo de controle. Isso é uma vantagem de manutenção: alterar o autômato não altera o fluxo do código, apenas os dados.

### 6.4 Performance

Ambas as abordagens têm complexidade temporal O(n) no comprimento da entrada. Para os números romanos de 1–3999, o comprimento máximo é 15 caracteres (`MMMCCCXXXIII` + variações). Na prática, a diferença de desempenho é desprezível.

### 6.5 Síntese

| Critério | AFD + GLC | Imperativo |
|---|---|---|
| Concisão do código | Baixa | Alta |
| Fidelidade à teoria | Alta | Baixa |
| Diagnóstico de erros | Detalhado (trajetória) | Inexistente |
| Verificabilidade | Alta | Baixa |
| Extensibilidade | Alta | Média |
| Curva de aprendizado | Alta | Baixa |

---

## 7. Conclusão

Este trabalho demonstrou que a aplicação de modelos formais da Teoria da Computação — especificamente o AFD e a GLC — ao problema do conversor de números romanos resulta em uma solução mais rigorosa, rastreável e extensível do que a abordagem imperativa tradicional, ao custo de maior complexidade inicial de modelagem.

O principal aprendizado prático é que a **tabela de transição do AFD como estrutura de dados** (em vez de if/else aninhados) é uma decisão de design que mantém a complexidade ciclomática baixa e torna o código diretamente verificável contra a especificação formal. A distinção entre "especificação como dado" e "lógica como fluxo de controle" é um princípio valioso em engenharia de software.

**Limitações do projeto:**

1. O escopo é restrito a números romanos canônicos de 1 a 3999. Valores maiores exigiriam o sistema vinculum (barra sobre o símbolo para multiplicar por 1000).
2. O AFD foi implementado manualmente; para linguagens maiores, ferramentas como `re` (expressões regulares) ou geradores de lexers seriam mais práticas.
3. Não foram medidos tempos de execução formalmente; a análise de performance é qualitativa.

**Trabalhos futuros:**

- Extensão para o sistema vinculum (números até 3.999.000).
- Geração automática do diagrama de estados do AFD a partir da tabela `DELTA`.
- Implementação do caminho inverso: conversor de arábico para romano.
- Comparação com uma implementação baseada em expressões regulares (`re` do Python).
- Análise formal da classe de complexidade do problema (pertencimento a P, decidibilidade).

---

## Referências

AHO, A. V.; SETHI, R.; ULLMAN, J. D. **Compiladores: princípios, técnicas e ferramentas**. Rio de Janeiro: Guanabara Koogan, 1995.

BARBOSA, Cynthia S. **Compiladores**. Porto Alegre: Sagah, 2021.

HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. **Introdução à teoria de autômatos, linguagens e computação**. São Paulo: Pearson, 2003.

SIPSER, Michael. **Introdução à teoria da computação**. São Paulo: Cengage Learning, 2007.
