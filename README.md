# Conversor de Números Romanos — Teoria da Computação

Projeto acadêmico que implementa a conversão de números romanos para arábicos com
fundamentação em modelos formais da Teoria da Computação.

## Abordagens implementadas

| Módulo | Modelo formal | Papel |
|---|---|---|
| `src/afd.py` | Autômato Finito Determinístico (AFD) | Validação da entrada |
| `src/glc_parser.py` | Gramática Livre de Contexto (GLC) | Conversão via parser recursivo descendente |
| `src/conversor_tradicional.py` | — | Baseline imperativo para análise comparativa |

## Escopo

Números romanos canônicos de **1 a 3999**, com regras subtrativas obrigatórias:
`IV`, `IX`, `XL`, `XC`, `CD`, `CM`.

## Requisitos

- Python 3.10 ou superior
- Sem dependências externas (somente biblioteca padrão)

## Instalação

```bash
git clone <url-do-repositorio>
cd Implementacao-e-Analise-de-um-Conversor-de-Numeros-Romanos
```

## Uso

### Modo argumento direto

```bash
python src/main.py MCMXLIV
```

Saída:
```
MCMXLIV = 1944
```

### Com comparação entre abordagens

```bash
python src/main.py MMMCMXCIX --comparar
```

Saída:
```
Resultado (GLC parser):  MMMCMXCIX = 3999
Resultado (imperativo):  MMMCMXCIX = 3999
  [OK] Ambas as abordagens concordam.
```

### Entrada inválida — diagnóstico detalhado

```bash
python src/main.py IIII
```

Saída:
```
Erro: 'IIII' não é um número romano canônico válido.
       IIII
          ^
  Caractere problemático: 'I' na posição 3
  Trajetória do AFD: q0 → qU1 → qU2 → qU3 → qERRO
```

### Modo interativo

```bash
python src/main.py
```

## Testes

```bash
python -m unittest discover tests/
``` 

Resultado esperado:
```
Ran 107 tests in 0.005s
OK
```

## Estrutura do projeto

```
├── src/
│   ├── afd.py                    # AFD validador (tabela de transição DELTA)
│   ├── glc_parser.py             # Parser recursivo descendente da GLC
│   ├── conversor_tradicional.py  # Versão imperativa para comparação
│   └── main.py                   # Programa principal (CLI)
├── tests/
│   ├── test_afd.py               # 44 testes do AFD
│   ├── test_glc_parser.py        # 47 testes do parser GLC
│   ├── test_conversor_tradicional.py  # 16 testes do conversor tradicional
│   └── casos_teste.md            # Documentação dos casos de teste
├── docs/
│   ├── especificacao_formal.md   # AFD (quíntupla) + GLC (BNF) + derivações
│   └── diagrama_afd.md           # Diagramas Mermaid do AFD por camada
└── relatorio/
    ├── relatorio.md              # Relatório final em formato artigo
    └── resumo_executivo.md       # Roteiro para apresentação oral (10–15 min)
```

## Documentação técnica

- [Especificação Formal (AFD + GLC)](docs/especificacao_formal.md)
- [Diagrama do AFD em Mermaid](docs/diagrama_afd.md)
- [Relatório Final](relatorio/relatorio.md)
- [Resumo Executivo — Roteiro de Apresentação](relatorio/resumo_executivo.md)

## Resumo técnico

| Item | Valor |
|---|---|
| Estados do AFD | 32 |
| Estados de aceitação | 30 |
| Símbolos do alfabeto Σ | 7 (I, V, X, L, C, D, M) |
| Não-terminais da GLC | 5 |
| Alternativas de produção | 29 |
| Testes unitários | 107 |
| Escopo numérico | 1–3999 |
