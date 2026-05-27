# Diagrama do AFD — Conversor de Números Romanos

O diagrama abaixo representa o Autômato Finito Determinístico (AFD) organizado em
quatro camadas sequenciais: milhar → centena → dezena → unidade.

Para clareza visual, o diagrama é dividido por camada. As setas entre camadas
representam o redirecionamento do próximo símbolo para a camada seguinte.

---

## Camada 1 — Milhar

```mermaid
stateDiagram-v2
    direction LR

    [*] --> q0
    q0 --> qM1 : M
    qM1 --> qM2 : M
    qM2 --> qM3 : M
    qM3 --> qERRO : M

    note right of q0 : Estado inicial
    note right of qM3 : MMM = 3000 (máximo)
```

---

## Camada 2 — Centena

```mermaid
stateDiagram-v2
    direction LR

    [*] --> qC0
    qC0 --> qC1 : C
    qC0 --> qD  : D

    qC1 --> qC2 : C
    qC1 --> qCD : D
    qC1 --> qCM : M

    qC2 --> qC3 : C
    qC3 --> qERRO : C

    qD  --> qDC1 : C
    qDC1 --> qDC2 : C
    qDC2 --> qDC3 : C
    qDC3 --> qERRO : C

    qERRO --> qERRO : I,V,X,L,C,D,M

    note right of qCD  : CD = 400
    note right of qD   : D  = 500
    note right of qDC1 : DC = 600
    note right of qDC2 : DCC = 700
    note right of qDC3 : DCCC = 800
    note right of qCM  : CM = 900
```

---

## Camada 3 — Dezena

```mermaid
stateDiagram-v2
    direction LR

    [*] --> qT0
    qT0 --> qT1 : X
    qT0 --> qL  : L

    qT1 --> qT2 : X
    qT1 --> qXL : L
    qT1 --> qXC : C

    qT2 --> qT3 : X
    qT3 --> qERRO : X

    qL  --> qLX1 : X
    qLX1 --> qLX2 : X
    qLX2 --> qLX3 : X
    qLX3 --> qERRO : X

    qERRO --> qERRO : I,V,X,L,C,D,M

    note right of qXL  : XL = 40
    note right of qL   : L  = 50
    note right of qLX1 : LX = 60
    note right of qLX2 : LXX = 70
    note right of qLX3 : LXXX = 80
    note right of qXC  : XC = 90
```

---

## Camada 4 — Unidade

```mermaid
stateDiagram-v2
    direction LR

    [*] --> qU0
    qU0 --> qU1 : I
    qU0 --> qV  : V

    qU1 --> qU2 : I
    qU1 --> qIV : V
    qU1 --> qIX : X

    qU2 --> qU3 : I
    qU3 --> qERRO : I

    qV  --> qVI1 : I
    qVI1 --> qVI2 : I
    qVI2 --> qVI3 : I
    qVI3 --> qERRO : I

    qERRO --> qERRO : I,V,X,L,C,D,M

    state "qIV ✓" as qIV
    state "qIX ✓" as qIX
    state "qU1 ✓" as qU1
    state "qU2 ✓" as qU2
    state "qU3 ✓" as qU3
    state "qV ✓"  as qV
    state "qVI1 ✓" as qVI1
    state "qVI2 ✓" as qVI2
    state "qVI3 ✓" as qVI3

    note right of qIV  : IV = 4
    note right of qV   : V  = 5
    note right of qVI1 : VI = 6
    note right of qVI2 : VII = 7
    note right of qVI3 : VIII = 8
    note right of qIX  : IX = 9
```

---

## Visão geral — fluxo entre camadas

```mermaid
flowchart LR
    ENTRADA["Entrada: s"]
    M["Camada Milhar\nq0 → qM1/qM2/qM3"]
    C["Camada Centena\nqC0 → qCD/qCM/..."]
    D["Camada Dezena\nqT0 → qXL/qXC/..."]
    U["Camada Unidade\nqU0 → qIV/qIX/..."]
    ACE["ACEITO ✓"]
    REJ["REJEITADO ✗\n(qERRO ou estado\nde espera no fim)"]

    ENTRADA --> M
    M -->|"símbolo ≠ M"| C
    M -->|"fim da cadeia"| ACE
    C -->|"símbolo ∈ {X,L,I,V}"| D
    C -->|"fim da cadeia"| ACE
    D -->|"símbolo ∈ {I,V}"| U
    D -->|"fim da cadeia"| ACE
    U -->|"fim da cadeia"| ACE
    M --> REJ
    C --> REJ
    D --> REJ
    U --> REJ
```

---

## Notas sobre o diagrama

1. **Estados de aceitação**: marcados com `✓` na camada de unidade; nas camadas
   anteriores, qualquer estado (exceto `qERRO` e estados de "espera" `qC0`, `qT0`, `qU0`)
   é de aceitação quando a cadeia termina nele.

2. **Transições implícitas para qERRO**: qualquer símbolo não listado em um estado
   leva implicitamente a `qERRO`. O estado `qERRO` é um sumidouro: todas as suas
   transições retornam a ele mesmo.

3. **Redirecionamento entre camadas**: quando a camada de milhar recebe um símbolo
   que não é `M`, ela passa o controle para a camada de centena com esse símbolo.
   O mesmo padrão se repete entre centena→dezena e dezena→unidade.
