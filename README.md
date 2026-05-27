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

### Modo interativo

```bash
python src/main.py
```

### Modo argumento direto

```bash
python src/main.py MCMXCIX
```

### Com comparação entre abordagens

```bash
python src/main.py MCMXCIX --comparar
```

## Testes

```bash
python -m unittest discover tests/
``` 

## Estrutura do projeto

```
├── src/
│   ├── afd.py                    # AFD validador (tabela de transição)
│   ├── glc_parser.py             # Parser recursivo descendente da GLC
│   ├── conversor_tradicional.py  # Versão imperativa para comparação
│   └── main.py                   # Programa principal (CLI)
├── tests/
│   ├── test_afd.py
│   ├── test_glc_parser.py
│   ├── test_conversor_tradicional.py
│   └── casos_teste.md            # Documentação dos casos de teste
├── docs/
│   ├── especificacao_formal.md   # AFD (quíntupla) + GLC (BNF)
│   └── diagrama_afd.md           # Diagrama em Mermaid
└── relatorio/
    └── relatorio.md              # Relatório final em formato artigo
```

## Documentação técnica

- [Especificação Formal (AFD + GLC)](docs/especificacao_formal.md)
- [Diagrama do AFD](docs/diagrama_afd.md)
- [Relatório Final](relatorio/relatorio.md)
