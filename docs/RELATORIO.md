# TDE3 — Otimização: Sudoku com Algoritmo Genético e busca local

Inteligência Artificial (PCO118A) · Prof. Carlos Costa Cedro · PUCPR

**Equipe:** Angelo Piovezan, Fernando Alonso, Jafte Fagundes e Renato Gouveia

Todos os números abaixo são reproduzíveis com `python3 experimento.py` (saída em
`resultados/resultados.md` e `resultados/execucoes.csv`).

---

## 1. O problema

**Sudoku 9×9:** preencher as casas vazias de uma grade com dígitos de 1 a 9 de modo que
nenhuma linha, coluna ou bloco 3×3 repita dígito. Como otimização: **minimizar o número
de dígitos repetidos** em linhas e colunas.

**Por que busca local.** A função objetivo é barata (≈2 µs por avaliação), tem alvo
conhecido (0 conflitos) e uma modificação elementar — trocar dois dígitos de um bloco — muda
apenas duas linhas e duas colunas. A paisagem, portanto, é "localmente suave": vizinhos
diferem pouco em custo, que é o que busca local precisa.

## 2. Modelagem (ID3.1)

### Representação

Lista de 81 inteiros, linha a linha. As casas dadas ficam **fixas**, e cada bloco 3×3 é
preenchido com uma **permutação dos dígitos que faltam nele**.

**O que a representação torna impossível por construção:** (1) alterar uma casa dada;
(2) repetir dígito dentro de um bloco. Das três famílias de restrições do Sudoku, uma
inteira sai da função objetivo. É o mesmo movimento da representação B (permutação) das
oito rainhas na Aula 8, que eliminava os conflitos de linha.

### Tamanho do espaço

Se o bloco b tem `k_b` casas livres, há `k_b!` permutações para ele, e os blocos são
independentes: **|S| = ∏ k_b!**

| Instância | Dadas | Livres por bloco | Conta | \|S\| |
|---|---:|---|---|---:|
| fácil | 38 | 5,5,4,5,4,5,4,6,5 | 5!·5!·4!·5!·4!·5!·4!·6!·5! | 2,48 × 10¹⁷ |
| médio | 30 | 5,7,6,6,6,4,7,4,6 | 5!·7!·6!·6!·6!·4!·7!·4!·6! | 4,72 × 10²³ |
| difícil | 26 | 6,4,7,4,7,8,6,6,7 | 6!·4!·7!·4!·7!·8!·6!·6!·7! | 1,11 × 10²⁷ |

Para comparação, a representação ingênua (qualquer dígito em qualquer casa livre) teria
9⁴³ ≈ 1,1 × 10⁴¹ estados no fácil e 9⁵⁵ ≈ 3,0 × 10⁵² no difícil.

### Vizinhança

Trocar os valores de **duas casas livres do mesmo bloco**. Preserva a permutação do bloco.
Vizinhos por estado = Σ C(k_b, 2): **83** (fácil), **124** (médio), **148** (difícil).

Dois modos de escolher o vizinho:

- **Enumeração completa** (HC): avalia todos os vizinhos e pega o melhor.
- **Troca dirigida** (SA e mutação do AG): sorteia uma casa livre que **participa de algum
  conflito** e a troca com outra casa livre do mesmo bloco. Descobrir quais casas estão em
  conflito é uma inspeção do estado atual (que já foi avaliado), não a avaliação de um
  estado novo, então não consome orçamento. O mesmo operador é dado ao SA e ao AG para que
  a comparação entre os dois não meça a diferença entre operadores (ver seção 6).

### Recombinação

O crossover de um ponto **sobre as 81 casas não** produz estados válidos: se o corte cai no
meio de um bloco, o filho pode herdar o mesmo dígito dos dois pais naquele bloco. O plano
adotado é o **crossover de um ponto entre blocos**: sorteia-se k ∈ {1..8}, o filho herda os
blocos 0..k−1 do pai 1 e k..8 do pai 2. Como cada bloco é copiado inteiro, todo filho é
válido.

### Função objetivo

```
conflitos(s) = Σ_linhas (9 − |dígitos distintos|) + Σ_colunas (9 − |dígitos distintos|)
```

**Minimização.** O AG maximiza a aptidão = `APTIDAO_MAXIMA − conflitos`, com
`APTIDAO_MAXIMA = 2 · 9 · 8 = 144` (cada linha e coluna repete no máximo 8 dígitos).

### Alvo conhecido

Sim: **0 conflitos**. As instâncias foram geradas por `gerar_instancias.py` (semente 2025)
e um resolvedor exato confirma que cada uma tem **solução única**. Também verificamos que
as soluções encontradas pelos métodos coincidem com a do resolvedor.

## 3. Métodos

| Método | Papel | Detalhes |
|---|---|---|
| Sorteio aleatório | linha de base trivial | sorteia estados válidos até esgotar o orçamento |
| HC + reinício | linha de base | subida mais íngreme, só melhora estrita; reinicia de estado aleatório em ótimo local |
| Simulated Annealing | busca local | troca dirigida, resfriamento geométrico T ← αT; se T < 10⁻³ sem solução, reinicia de estado aleatório |
| Algoritmo Genético | método principal | torneio de 3, crossover entre blocos (taxa 0,9), mutação = troca dirigida repetida enquanto `random() < taxa_mut`, elitismo 2, **reinício da população** após 50 gerações sem melhorar o melhor indivíduo |

## 4. Protocolo experimental (ID3.3)

| Item | Valor |
|---|---|
| Unidade de custo | **avaliações da função objetivo** (contador `AVALIACOES`), nunca segundos ou gerações |
| Orçamento | **200.000 avaliações** por execução, igual para todos; o método para ao achar 0 conflitos |
| Execuções | **30** por método × instância, sementes **0 a 29** (as mesmas para todos os métodos) |
| Calibração | **6 configurações para o AG e 6 para o SA**, 10 execuções cada, numa **instância própria de calibração** (26 dadas, fora do conjunto de teste), sementes 1000–1009. Sorteio e HC não têm parâmetros |
| Critério de escolha | maior taxa de sucesso; desempate pela média de conflitos e depois pela mediana de avaliações até resolver |

Custo de cada passo em avaliações: uma geração do AG custa `tam_pop − elite = 198`
avaliações; uma iteração do SA custa 1; um passo do HC custa até 148 (vizinhança inteira).
Por isso comparar gerações, iterações ou passos seria injusto.

### Calibração

| Método | Configuração | Sucesso | Conflitos (média) | Avaliações até resolver (mediana) |
|---|---|---:|---:|---:|
| AG | pop 100, mut 0,3 | 0% | 2,20 | — |
| AG | pop 100, mut 0,6 | 40% | 1,20 | 154.422 |
| AG | pop 100, mut 0,8 | 40% | 1,20 | 126.840 |
| AG | pop 200, mut 0,3 | 30% | 1,80 | 51.780 |
| AG | pop 200, mut 0,6 | 50% | 1,00 | 99.335 |
| **AG** | **pop 200, mut 0,8** | **50%** | **1,00** | **48.690** |
| SA | T0 0,5, α 0,999 | 100% | 0,00 | 28.504 |
| SA | T0 0,5, α 0,9999 | 90% | 0,20 | 2.919 |
| **SA** | **T0 0,5, α 0,99999** | **100%** | **0,00** | **7.640** |
| SA | T0 2,0, α 0,999 | 100% | 0,00 | 36.132 |
| SA | T0 2,0, α 0,9999 | 100% | 0,00 | 13.954 |
| SA | T0 2,0, α 0,99999 | 100% | 0,00 | 101.496 |

## 5. Resultados

30 execuções por célula, 200.000 avaliações de orçamento. "Avaliações até resolver" é
calculado só sobre as execuções que resolveram.

### Fácil (43 livres, |S| ≈ 2,48 × 10¹⁷)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 17,87 ± 1,31 | 13 | 20 | — |
| HC + reinício | 37% | 1,27 ± 0,96 | 0 | 2 | 73.347 [14.785 – 195.870] |
| Simulated Annealing | **100%** | 0,00 ± 0,00 | 0 | 0 | 364 [100 – 1.633] |
| Algoritmo Genético | **100%** | 0,00 ± 0,00 | 0 | 0 | 4.412 [2.244 – 29.616] |

### Médio (51 livres, |S| ≈ 4,72 × 10²³)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 23,57 ± 1,17 | 21 | 25 | — |
| HC + reinício | 3% | 5,27 ± 1,53 | 0 | 8 | 2.357 (1 execução) |
| Simulated Annealing | 90% | 0,20 ± 0,60 | 0 | 2 | 1.092 [220 – 41.842] |
| Algoritmo Genético | **100%** | 0,00 ± 0,00 | 0 | 0 | 31.172 [5.175 – 198.847] |

### Difícil (55 livres, |S| ≈ 1,11 × 10²⁷)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 24,93 ± 1,39 | 20 | 27 | — |
| HC + reinício | 0% | 6,23 ± 1,50 | 2 | 8 | — |
| Simulated Annealing | **97%** | 0,07 ± 0,36 | 0 | 2 | 12.056 [736 – 39.316] |
| Algoritmo Genético | 17% | 1,67 ± 0,75 | 0 | 2 | 68.432 [27.149 – 196.303] |

## 6. Análise

1. **Todos os métodos batem com folga a linha de base trivial.** O sorteio aleatório, com
   200 mil tentativas, nunca fica abaixo de 13 conflitos; os métodos de busca ficam entre
   0 e 8. É a estrutura da vizinhança que está sendo explorada, não a sorte.
2. **O AG resolve o fácil e o médio em todas as 30 execuções**, superando com folga o HC com
   reinício (37% e 3%). No médio, é o único método com 100%.
3. **No difícil, o SA domina** (97% contra 17% do AG). Quando o AG não resolve, ele termina a
   1 ou 2 conflitos: chega perto, mas não fecha.
4. **O AG é mais caro que o SA quando ambos resolvem.** No fácil, a mediana é 4.412 contra 364
   avaliações; no médio, 31.172 contra 1.092. Uma geração custa 198 avaliações, e boa parte
   delas são filhos piores que os pais. O SA gasta cada avaliação refinando um único estado.
5. **Por que o AG perde no difícil.** O crossover recombina **blocos**, mas os conflitos que
   restam estão em **linhas e colunas**, que atravessam três blocos. Combinar "bons blocos"
   de dois pais costuma criar repetições novas nas fronteiras. Na reta final, o trabalho
   fica com a mutação, e o AG gasta 198 avaliações por geração para fazer o que o SA faz
   com uma.
6. **Cauda longa.** O custo para resolver varia em uma ou duas ordens de grandeza entre
   execuções do mesmo método (AG no médio: 5.175 a 198.847; SA no médio: 220 a 41.842). Quem
   precisa de tempo de resposta garantido deve olhar o pior caso, não a mediana.

### Evolução do AG: o que não funcionou

A primeira versão do AG usava a mesma representação e o mesmo crossover, mas com **mutação
cega** (troca aleatória dentro de um bloco) e **sem reinício**. Mesmo protocolo (30
execuções, sementes 0–29, 200 mil avaliações), calibrada na instância "médio":

| Versão | Fácil | Médio | Difícil |
|---|---:|---:|---:|
| AG v1 (mutação cega, sem reinício) | 30% (média 1,67 conflitos) | 0% (4,07) | 0% (4,70) |
| SA v1 (vizinho cego) | 100% | 100% | 40% |
| **AG final** (troca dirigida + reinício) | **100%** | **100%** | **17%** |
| **SA final** (troca dirigida) | **100%** | **90%** | **97%** |

O diagnóstico veio de observar onde o AG v1 parava. A população **convergia
prematuramente** para indivíduos parecidos, com 2 a 6 conflitos, e dali não saía. Duas
mudanças resolveram:

- **Reinício da população** após 50 gerações sem melhora: troca uma população convergida
  e inútil por diversidade nova. Sozinho, levou o fácil de 40% para 100% em testes
  preliminares.
- **Troca dirigida:** com 2 conflitos restantes, quase todas as trocas cegas mexem em
  casas que já estão certas. A troca dirigida concentra a mutação nas poucas casas erradas.

**Cuidado com a comparação:** a troca dirigida também melhorou o SA (difícil de 40% para
97%). Se só o AG tivesse recebido o operador novo, a tabela final mostraria o AG perto do
SA no difícil, mas a diferença viria do operador, não do método. Por isso os dois usam a
troca dirigida.

## 7. Garantias ausentes e limitações

- **Nenhum dos métodos tem garantia de encontrar a solução.** O SA usa resfriamento
  geométrico, que não satisfaz a condição do Teorema 3 (resfriamento logarítmico). O AG não
  tem garantia de convergência para o ótimo. Uma execução que termina com 2 conflitos não
  prova nada sobre a instância: sabemos que a solução existe porque o resolvedor exato a
  encontrou.
- **O AG falha em 83% das execuções no difícil**, e o SA em 10% no médio, com 200 mil
  avaliações.
- **O α escolhido para o SA (0,99999) quase não resfria dentro do orçamento:** o
  resfriamento até Tmin levaria cerca de 620 mil iterações, mais que as 200 mil
  disponíveis. Na prática o SA roda a temperatura quase constante e baixa (de 0,5 até
  ≈0,07), sem nunca reiniciar. Foi a configuração que a calibração escolheu, mas mostra que
  o resultado depende do orçamento: com orçamento muito maior, outro α seria o certo.
- **Calibração com 10 execuções por configuração:** várias configurações do SA empataram
  em 100%, e a escolha foi decidida pela mediana de avaliações. Com uma amostra tão
  pequena, essa escolha é instável.
- **Busca local não é a melhor ferramenta para Sudoku 9×9.** O resolvedor exato
  (backtracking escolhendo a casa com menos candidatos) resolve as instâncias em
  milissegundos. O trabalho mostra como os métodos se comportam numa paisagem com muitos
  platôs, não que sejam a forma recomendada de resolver Sudoku. Em grades maiores
  (16×16, 25×25) a busca exata fica cara e a comparação passaria a ser mais relevante.
- **Três instâncias, 30 execuções:** as taxas de sucesso têm intervalo de confiança largo
  (para 30 execuções, cerca de ±18 pontos percentuais em p = 0,5, com 95% de confiança).
