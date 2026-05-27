# Especificação Formal — Conversor de Números Romanos

## 1. Domínio e restrições da linguagem

### 1.1 Alfabeto

```
Σ = { I, V, X, L, C, D, M }
```

### 1.2 Regras canônicas dos números romanos (1–3999)

As regras abaixo definem a **forma canônica** única para cada inteiro:

| Grupo | Padrão aditivo | Padrão subtrativo |
|---|---|---|
| Milhar (1000–3000) | M, MM, MMM | — |
| Centena (100–900) | C, CC, CCC | CD, D, DC, DCC, DCCC, CM |
| Dezena (10–90) | X, XX, XXX | XL, L, LX, LXX, LXXX, XC |
| Unidade (1–9) | I, II, III | IV, V, VI, VII, VIII, IX |

**Restrições principais:**
1. Nunca quatro repetições do mesmo símbolo (`IIII`, `XXXX`, `CCCC`, `MMMM` são inválidos).
2. `V`, `L`, `D` nunca se repetem.
3. Pares subtrativos permitidos: apenas `IV`, `IX`, `XL`, `XC`, `CD`, `CM`.
4. Um símbolo menor não pode preceder um muito maior que não seja seu par subtrativo (p.ex., `IL`, `IC`, `VX` são inválidos).
5. A cadeia vazia é inválida.
6. Somente caracteres de Σ são permitidos.

---

## 2. Autômato Finito Determinístico (AFD)

### 2.1 Quíntupla formal

```
AFD = (K, Σ, δ, q₀, F)
```

- **K** (estados): veja seção 2.2
- **Σ** (alfabeto): `{I, V, X, L, C, D, M}`
- **δ** (função de transição): tabela na seção 2.3
- **q₀** (estado inicial): `q0`
- **F** (estados de aceitação): todos os estados marcados com `*` na seção 2.2

### 2.2 Estados

O AFD é estruturado por **posição na gramática**, rastreando o que já foi lido
para impedir repetições proibidas e pares subtrativos inválidos.

```
Estados de milhar (prefixo M*):
  q0   — início / nenhum milhar lido
  qM1  — leu M (1000)
  qM2  — leu MM (2000)
  qM3  — leu MMM (3000)

Estados de centena (prefixo C*):
  qC0  — espera centena (posição centena, nenhuma lida)
  qC1  — leu C (100)
  qC2  — leu CC (200)
  qC3  — leu CCC (300)
  qCD  — leu CD (400)
  qD   — leu D (500)
  qDC1 — leu DC (600)
  qDC2 — leu DCC (700)
  qDC3 — leu DCCC (800)
  qCM  — leu CM (900)

Estados de dezena (prefixo T*):
  qT0  — espera dezena
  qT1  — leu X (10)
  qT2  — leu XX (20)
  qT3  — leu XXX (30)
  qXL  — leu XL (40)
  qL   — leu L (50)
  qLX1 — leu LX (60)
  qLX2 — leu LXX (70)
  qLX3 — leu LXXX (80)
  qXC  — leu XC (90)

Estados de unidade (prefixo U*):
  qU0  — espera unidade
  qU1  — leu I (1)
  qU2  — leu II (2)
  qU3  — leu III (3)
  qIV  — leu IV (4)
  qV   — leu V (5)
  qVI1 — leu VI (6)
  qVI2 — leu VII (7)
  qVI3 — leu VIII (8)
  qIX  — leu IX (9)

Estado de erro:
  qERRO — qualquer transição inválida (sumidouro de rejeição)
```

**Estados de aceitação F:**
`F = K \ {q0, qC0, qT0, qU0, qERRO}`

Em outras palavras: qualquer estado alcançado ao consumir toda a entrada, que
não seja um dos estados intermediários de "espera" nem o estado de erro, é um
estado de aceitação. Isso garante que `M`, `MM`, `MMM`, `MC`, `MCMXCIX`, etc.,
sejam todos aceitos, enquanto strings que terminam em estado de "espera" ou erro
são rejeitadas.

### 2.3 Estratégia de transição

O AFD é organizado em **camadas sequenciais**: milhar → centena → dezena → unidade.
Cada camada só é alcançada após a anterior ser concluída ou pulada.
A transição entre camadas ocorre quando o próximo símbolo pertence à camada seguinte.

Exemplo de trajetória para `MCMXLIV`:
```
q0 -M-> qM1 -C-> qCD... não, C vem antes de M
q0 -M-> qM1 (consome M, passa para camada centena com C ainda disponível)
qC0 -C-> qC1 -M-> qCM (consome CM = 900)
qT0 -X-> qT1 -L-> qXL (consome XL = 40)
qU0 -I-> qU1 -V-> qIV (consome IV = 4)
=> aceito
```

### 2.4 Tabela de transição δ (resumida por camadas)

A tabela completa está implementada em `src/afd.py`. Abaixo a lógica por camada:

#### Camada Milhar

| Estado | I | V | X | L | C | D | M |
|---|---|---|---|---|---|---|---|
| q0 | → centena | → centena | → centena | → centena | → centena | → centena | qM1 |
| qM1 | → centena | → centena | → centena | → centena | → centena | → centena | qM2 |
| qM2 | → centena | → centena | → centena | → centena | → centena | → centena | qM3 |
| qM3 | → centena | → centena | → centena | → centena | → centena | → centena | qERRO |

> "→ centena" significa: o símbolo é redirecionado para a camada de centenas.

#### Camada Centena

| Estado | C | D | M | I/V/X/L |
|---|---|---|---|---|
| qC0 | qC1 | qD | qERRO | → dezena |
| qC1 | qC2 | qCD | qCM | → dezena |
| qC2 | qC3 | qERRO | qERRO | → dezena |
| qC3 | qERRO | qERRO | qERRO | → dezena |
| qCD | qERRO | qERRO | qERRO | → dezena |
| qD | qDC1 | qERRO | qERRO | → dezena |
| qDC1 | qDC2 | qERRO | qERRO | → dezena |
| qDC2 | qDC3 | qERRO | qERRO | → dezena |
| qDC3 | qERRO | qERRO | qERRO | → dezena |
| qCM | qERRO | qERRO | qERRO | → dezena |

#### Camada Dezena

| Estado | X | L | C | D/M | I/V |
|---|---|---|---|---|---|
| qT0 | qT1 | qL | qERRO | qERRO | → unidade |
| qT1 | qT2 | qXL | qXC | qERRO | → unidade |
| qT2 | qT3 | qERRO | qERRO | qERRO | → unidade |
| qT3 | qERRO | qERRO | qERRO | qERRO | → unidade |
| qXL | qERRO | qERRO | qERRO | qERRO | → unidade |
| qL | qLX1 | qERRO | qERRO | qERRO | → unidade |
| qLX1 | qLX2 | qERRO | qERRO | qERRO | → unidade |
| qLX2 | qLX3 | qERRO | qERRO | qERRO | → unidade |
| qLX3 | qERRO | qERRO | qERRO | qERRO | → unidade |
| qXC | qERRO | qERRO | qERRO | qERRO | → unidade |

#### Camada Unidade

| Estado | I | V | X/L/C/D/M |
|---|---|---|---|
| qU0 | qU1 | qV | qERRO |
| qU1 | qU2 | qIV | qIX (apenas X) / qERRO |
| qU2 | qU3 | qERRO | qERRO |
| qU3 | qERRO | qERRO | qERRO |
| qIV | qERRO | qERRO | qERRO |
| qV | qVI1 | qERRO | qERRO |
| qVI1 | qVI2 | qERRO | qERRO |
| qVI2 | qVI3 | qERRO | qERRO |
| qVI3 | qERRO | qERRO | qERRO |
| qIX | qERRO | qERRO | qERRO |

---

## 3. Gramática Livre de Contexto (GLC)

### 3.1 Definição formal

```
GLC = (V, Σ, P, S)
```

- **V** (variáveis / não-terminais): `{S, Milhar, Centena, Dezena, Unidade}`
- **Σ** (terminais): `{I, V, X, L, C, D, M}`
- **P** (produções): veja seção 3.2
- **S** (símbolo inicial): `S`

### 3.2 Regras de produção em BNF

```bnf
<S> ::= <Milhar> <Centena> <Dezena> <Unidade>

<Milhar> ::= M M M    (3000)
           | M M      (2000)
           | M        (1000)
           | ε

<Centena> ::= C M          (900)
            | D C C C      (800)
            | D C C        (700)
            | D C          (600)
            | D            (500)
            | C D          (400)
            | C C C        (300)
            | C C          (200)
            | C            (100)
            | ε

<Dezena> ::= X C           (90)
           | L X X X       (80)
           | L X X         (70)
           | L X           (60)
           | L             (50)
           | X L           (40)
           | X X X         (30)
           | X X           (20)
           | X             (10)
           | ε

<Unidade> ::= I X          (9)
            | V I I I      (8)
            | V I I        (7)
            | V I          (6)
            | V            (5)
            | I V          (4)
            | I I I        (3)
            | I I          (2)
            | I            (1)
            | ε
```

**Restrição adicional ao ε:** A cadeia vazia não é válida como `S` completo —
pelo menos um não-terminal deve derivar uma cadeia não-vazia.

### 3.3 Derivação de exemplo: `MCMXLIV`

```
S
⟹ Milhar Centena Dezena Unidade
⟹ M Centena Dezena Unidade          [Milhar → M]
⟹ M CM Dezena Unidade               [Centena → CM]
⟹ M CM XL Unidade                   [Dezena → XL]
⟹ M CM XL IV                        [Unidade → IV]
⟹ "MCMXLIV"                         ✓  valor = 1000 + 900 + 40 + 4 = 1944
```

### 3.4 Derivação de exemplo: `MMMCMXCIX`

```
S
⟹ Milhar Centena Dezena Unidade
⟹ MMM Centena Dezena Unidade        [Milhar → MMM]
⟹ MMM CM Dezena Unidade             [Centena → CM]
⟹ MMM CM XC Unidade                 [Dezena → XC]
⟹ MMM CM XC IX                      [Unidade → IX]
⟹ "MMMCMXCIX"                       ✓  valor = 3000 + 900 + 90 + 9 = 3999
```

---

## 4. Correspondência entre modelos formais e código

| Conceito formal | Arquivo | Elemento de código |
|---|---|---|
| AFD — quíntupla | `src/afd.py` | Constantes `ESTADOS`, `ALFABETO`, `DELTA`, `ESTADO_INICIAL`, `ESTADOS_ACEITACAO` |
| AFD — função δ | `src/afd.py` | Dicionário `DELTA` (dicionário de dicionários) |
| GLC — produções | `src/glc_parser.py` | Funções `parse_milhar()`, `parse_centena()`, `parse_dezena()`, `parse_unidade()` |
| GLC — símbolo S | `src/glc_parser.py` | Função `parse_numero()` |
| Baseline | `src/conversor_tradicional.py` | Função `converter()` com loop simples |
