# Documentação dos Casos de Teste

Este documento justifica cada caso de teste — válido e inválido — com base
nas regras formais da linguagem dos números romanos canônicos (1–3999).

---

## Casos Válidos

| Entrada | Valor | Justificativa |
|---|---|---|
| `I` | 1 | Menor número romano possível; unidade simples. |
| `II` | 2 | Duas unidades aditivas; permitido (máximo 3 repetições). |
| `III` | 3 | Três unidades aditivas; limite superior do padrão aditivo. |
| `IV` | 4 | Par subtrativo canônico I antes de V; única forma válida de 4. |
| `V` | 5 | Símbolo único; V nunca se repete mas pode aparecer sozinho. |
| `IX` | 9 | Par subtrativo canônico I antes de X; única forma válida de 9. |
| `X` | 10 | Símbolo de dezena; forma mais simples de 10. |
| `XL` | 40 | Par subtrativo canônico X antes de L; única forma válida de 40. |
| `XLII` | 42 | Composição: XL(40) + II(2); combina subtrativo e aditivo. |
| `XC` | 90 | Par subtrativo canônico X antes de C; única forma válida de 90. |
| `XCIX` | 99 | XC(90) + IX(9); dois pares subtrativos em camadas distintas. |
| `C` | 100 | Símbolo de centena; forma mais simples de 100. |
| `CD` | 400 | Par subtrativo canônico C antes de D; única forma válida de 400. |
| `CM` | 900 | Par subtrativo canônico C antes de M; única forma válida de 900. |
| `D` | 500 | Símbolo único de centena; D nunca se repete. |
| `M` | 1000 | Símbolo de milhar; forma mais simples de 1000. |
| `MMXXIV` | 2024 | MM(2000) + XX(20) + IV(4); número do ano atual. |
| `MMMCMXCIX` | 3999 | Maior número romano canônico: MMM(3000)+CM(900)+XC(90)+IX(9). |

---

## Casos Inválidos

### 1. `""` (cadeia vazia)

**Regra violada:** A linguagem dos números romanos não inclui a cadeia vazia —
todo número tem pelo menos um símbolo.  No AFD, a cadeia vazia termina no
estado inicial `q0`, que não é um estado de aceitação (`q0 ∉ F`).

---

### 2. `IIII`

**Regra violada:** Nenhum símbolo aditivo pode se repetir mais de três vezes
consecutivamente.  A forma canônica de 4 é `IV`, não `IIII`.
No AFD: `q0→qU1→qU2→qU3→qERRO` (quarto I dispara transição para `qERRO`).
No parser GLC: `parse_unidade()` consome `III`(3), deixando `I` sem produção
correspondente → `ValueError`.

---

### 3. `VV`

**Regra violada:** Os símbolos `V`, `L` e `D` (valores únicos por posição)
nunca se repetem — cada um ocorre no máximo uma vez e na posição correta.
No AFD: `q0→qV→qERRO` (segundo V dispara `qERRO`).

---

### 4. `LL`

**Regra violada:** Mesmo que `VV` — `L` não pode se repetir.
No AFD: `q0→qL→qERRO` (segundo L dispara `qERRO`, pois `qL` só aceita X
como próximo símbolo de dezena).

---

### 5. `DD`

**Regra violada:** `D` não pode se repetir.
No AFD: `q0→qD→qERRO` (segundo D dispara `qERRO`, pois `qD` só aceita C
como continuação ou símbolos de dezena/unidade).

---

### 6. `VX`

**Regra violada:** Após `V` (camada unidade), não é possível retornar à camada
dezena.  As camadas são estritamente sequenciais: milhar → centena → dezena →
unidade.  Além disso, `VX` não é um par subtrativo válido — `V` não pode
preceder `X`.  No AFD: `q0→qV→qERRO` (V está na camada unidade; X não é
transição válida a partir de `qV`).

---

### 7. `IC`

**Regra violada:** Par subtrativo inválido.  `I` só pode subtrair `V` e `X`
(formando `IV`=4 e `IX`=9).  `I` antes de `C` não é um par reconhecido.
No AFD: `q0→qU1→qERRO` (a partir de `qU1`, apenas `V`→`qIV` e `X`→`qIX`
são transições válidas; `C` → `qERRO`).

---

### 8. `IL`

**Regra violada:** Par subtrativo inválido pelo mesmo motivo de `IC`.
`I` só subtrai `V` e `X`; `IL` não é um par canônico.
No AFD: `q0→qU1→qERRO` (`L` não é transição válida a partir de `qU1`).

---

### 9. `XM`

**Regra violada:** Par subtrativo inválido.  `X` só pode subtrair `L` e `C`
(formando `XL`=40 e `XC`=90).  `X` antes de `M` não é canônico.
No AFD: `q0→qT1→qERRO` (`M` não é transição válida a partir de `qT1`).

---

### 10. `AB`

**Regra violada:** Caracteres fora do alfabeto `Σ = {I, V, X, L, C, D, M}`.
`A` e `B` não pertencem ao alfabeto dos números romanos.
No AFD: `q0→qERRO` imediatamente (primeiro símbolo fora de Σ).

---

### 11. `MMMM`

**Regra violada:** O valor máximo representável na notação canônica sem vinculum
é 3999 (MMMCMXCIX).  Quatro Ms representariam 4000, que está fora do escopo.
Também viola a regra de máximo 3 repetições aditivas.
No AFD: `q0→qM1→qM2→qM3→qERRO` (a partir de `qM3`, M → `qERRO`).

---

### 12. `abc`

**Regra violada:** Letras minúsculas não pertencem a Σ (o alfabeto é
estritamente maiúsculo).  No AFD: `q0→qERRO` imediatamente.

---

### 13. `123`

**Regra violada:** Dígitos não pertencem a Σ.
No AFD: `q0→qERRO` imediatamente.

---

### 14. `IXX`

**Regra violada:** `IX` é um par subtrativo completo que representa 9.
Após `IX`, o número romano na camada unidade está encerrado; um `X`
adicional viola a estrutura sequencial das camadas (não é possível retornar
à camada dezena após a unidade) e também viola a proibição de caracteres
após um par subtrativo completo.
No AFD: `q0→qU1→qIX→qERRO` (`X` não é transição válida a partir de `qIX`).
No parser GLC: `parse_unidade()` consome `IX`(9); `X` restante → `ValueError`.

---

### 15. `VIV`

**Regra violada:** `VI` representa 6 (V + I aditivo); o `V` seguinte não pode
aparecer novamente na camada unidade (V não se repete) e também não forma
um par subtrativo válido nessa posição.
No AFD: `q0→qV→qVI1→qERRO` (a partir de `qVI1`, V não é transição válida).
No parser GLC: `parse_unidade()` consome `VI`(6); `V` restante → `ValueError`.

---

## Resumo das regras violadas por categoria

| Categoria | Casos | Regra |
|---|---|---|
| Cadeia vazia | `""` | ε ∉ L (linguagem não inclui cadeia vazia) |
| Repetição excessiva | `IIII`, `MMMM` | Máximo 3 repetições aditivas |
| Símbolo único repetido | `VV`, `LL`, `DD` | V, L, D ocorrem no máximo uma vez |
| Par subtrativo inválido | `VX`, `IC`, `IL`, `XM` | Apenas IV, IX, XL, XC, CD, CM são válidos |
| Pós-par inválido | `IXX`, `VIV` | Nada pode seguir um par subtrativo na mesma camada |
| Fora do alfabeto | `AB`, `abc`, `123` | Σ = {I, V, X, L, C, D, M} apenas |
