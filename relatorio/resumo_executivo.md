# Resumo Executivo — Roteiro para Apresentação Oral (10–15 min)

---

## Estrutura sugerida da fala

### [0:00–1:30] Abertura — O problema e a motivação

> *"O objetivo deste trabalho é converter números romanos para arábicos.
> A pergunta que nos guia não é 'como fazer isso funcionar' — qualquer loop de 5 linhas
> faz. A pergunta é: como fazer isso com fundamentação formal, de forma que o código
> seja verificável contra uma especificação precisa?"*

- Apresente o escopo: números romanos canônicos de **1 a 3999**.
- Mostre um exemplo de entrada e saída: `MMMCMXCIX = 3999`.
- Mencione as três abordagens: AFD, GLC, e imperativo (baseline).

---

### [1:30–4:00] O AFD — Validação formal

> *"O primeiro componente é um Autômato Finito Determinístico que decide se a cadeia
> é um número romano válido."*

**O que falar:**
1. Apresente a quíntupla: `(K, Σ, δ, q₀, F)` — 32 estados, 7 símbolos.
2. Mostre a ideia das 4 camadas: milhar → centena → dezena → unidade.
3. Destaque a implementação: **DELTA é um dicionário de dicionários** — não há if/else para a lógica do autômato, tudo está na tabela.
4. Mostre o diagnóstico de erro ao vivo:

```
$ python src/main.py IIII
Erro: 'IIII' não é um número romano canônico válido.
       IIII
          ^
  Trajetória do AFD: q0 → qU1 → qU2 → qU3 → qERRO
```

**Ponto-chave para o professor:** *"A tabela δ no código é literalmente a tabela de transição da especificação formal. Não há divergência possível entre teoria e implementação."*

---

### [4:00–7:00] A GLC e o Parser — Conversão formal

> *"O segundo componente é um parser recursivo descendente derivado de uma Gramática
> Livre de Contexto. Cada função do código implementa exatamente uma produção
> gramatical."*

**O que falar:**
1. Mostre a GLC em BNF — 5 não-terminais, 29 alternativas.
2. Faça uma derivação ao vivo no quadro:
   ```
   MCMXLIV → M + CM + XL + IV = 1000+900+40+4 = 1944
   ```
3. Mostre o código da função `parse_milhar()` e aponte os comentários citando as produções.
4. Explique por que a ordem importa: `DCCC` antes de `DCC` antes de `DC`.

**Ponto-chave:** *"Cada `if self._consome(...)` corresponde a uma linha da gramática. Um professor de Teoria da Computação pode verificar o código linha a linha contra a especificação BNF."*

---

### [7:00–9:00] O Conversor Tradicional — Baseline

> *"Para comparação, implementamos também a abordagem clássica: 5 linhas de loop."*

**O que falar:**
1. Mostre o código (brevemente).
2. Destaque a diferença crítica: **não valida**, não rejeita `IIII` nem `VV`.
3. Mostre o modo `--comparar`:

```
$ python src/main.py MMMCMXCIX --comparar
Resultado (GLC parser):  MMMCMXCIX = 3999
Resultado (imperativo):  MMMCMXCIX = 3999
  [OK] Ambas as abordagens concordam.
```

---

### [9:00–11:00] Resultados e Testes

**O que falar:**
1. **107 testes unitários, todos passando** — 3 suítes cobrindo AFD, GLC e imperativo.
2. Mostre o comando: `python -m unittest discover tests/ -v`
3. Destaque os testes de consistência estrutural do AFD: verificam que todos os estados têm entrada em DELTA, todos os destinos são estados válidos, qERRO é sumidouro.

---

### [11:00–13:00] Análise Comparativa

Apresente a tabela resumo:

| Critério | AFD + GLC | Imperativo |
|---|---|---|
| Fidelidade formal | Alta | Baixa |
| Diagnóstico de erros | Detalhado | Inexistente |
| Concisão | Baixa | Alta |
| Extensibilidade | Alta | Média |
| Complexidade ciclomática de `executar()` | 3 | 3 |

**Ponto-chave:** *"A complexidade ciclomática do executar() é 3 — tão baixa quanto o imperativo. Toda a complexidade do autômato está nos dados (tabela DELTA), não no fluxo de controle. Isso é uma decisão de design consciente."*

---

### [13:00–14:30] Conclusão

> *"A abordagem formal não é a mais simples de implementar, mas é a mais verificável.
> O código é um espelho da teoria: a tabela DELTA é a função δ, as funções parse_*
> são as produções da GLC. Para um domínio em que a corretude é crítica e a
> especificação precisa ser auditável, essa é a abordagem certa."*

**Limitações a mencionar:**
- Escopo restrito a 1–3999 (sem vinculum).
- AFD projetado manualmente (para linguagens maiores, usaria gerador).

**Trabalho futuro:**
- Conversor inverso: arábico → romano.
- Extensão com vinculum para números maiores.

---

### [14:30–15:00] Encerramento e perguntas

> *"O código está disponível no repositório com toda a documentação formal.
> Estou à disposição para perguntas."*

---

## Números para memorizar

| Item | Valor |
|---|---|
| Estados do AFD | 32 |
| Estados de aceitação | 30 |
| Símbolos do alfabeto Σ | 7 |
| Não-terminais da GLC | 5 |
| Alternativas de produção | 29 |
| Testes unitários | 107 |
| Casos válidos obrigatórios | 18 |
| Casos inválidos obrigatórios | 15 |
| Escopo numérico | 1–3999 |
| Maior número romano | MMMCMXCIX (3999) |
