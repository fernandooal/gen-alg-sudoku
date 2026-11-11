# Resultados

- Orçamento: **200.000 avaliações** da função objetivo por execução
- Execuções: **30** por método e instância, sementes 0..29 (as mesmas para todos)
- Calibração: 10 execuções por configuração na instância `calibracao` (fora do conjunto de teste), sementes 1000..1009

## Calibração (6 configurações para AG e para SA)

| Método | Configuração | Sucesso | Conflitos (média) | Avaliações até resolver (mediana) |
|---|---|---:|---:|---:|
| Algoritmo Genético | `{'tam_pop': 100, 'taxa_mut': 0.3}` | 0% | 2,20 | — |
| Algoritmo Genético | `{'tam_pop': 100, 'taxa_mut': 0.6}` | 40% | 1,20 | 154.422 |
| Algoritmo Genético | `{'tam_pop': 100, 'taxa_mut': 0.8}` | 40% | 1,20 | 126.840 |
| Algoritmo Genético | `{'tam_pop': 200, 'taxa_mut': 0.3}` | 30% | 1,80 | 51.780 |
| Algoritmo Genético | `{'tam_pop': 200, 'taxa_mut': 0.6}` | 50% | 1,00 | 99.335 |
| Algoritmo Genético | `{'tam_pop': 200, 'taxa_mut': 0.8}` | 50% | 1,00 | 48.690 |
| Simulated Annealing | `{'T0': 0.5, 'alfa': 0.999}` | 100% | 0,00 | 28.504 |
| Simulated Annealing | `{'T0': 0.5, 'alfa': 0.9999}` | 90% | 0,20 | 2.919 |
| Simulated Annealing | `{'T0': 0.5, 'alfa': 0.99999}` | 100% | 0,00 | 7.640 |
| Simulated Annealing | `{'T0': 2.0, 'alfa': 0.999}` | 100% | 0,00 | 36.132 |
| Simulated Annealing | `{'T0': 2.0, 'alfa': 0.9999}` | 100% | 0,00 | 13.954 |
| Simulated Annealing | `{'T0': 2.0, 'alfa': 0.99999}` | 100% | 0,00 | 101.496 |

Escolhidos: `{'Sorteio aleatório': {}, 'HC + reinício': {}, 'Algoritmo Genético': {'tam_pop': 200, 'taxa_mut': 0.8}, 'Simulated Annealing': {'T0': 0.5, 'alfa': 0.99999}}`

## Comparação

### facil (43 casas livres, |S| ≈ 2.48e+17)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 17,87 ± 1,31 | 13 | 20 | — |
| HC + reinício | 37% | 1,27 ± 0,96 | 0 | 2 | 73.347 [14.785 – 195.870] |
| Simulated Annealing | 100% | 0,00 ± 0,00 | 0 | 0 | 364 [100 – 1.633] |
| Algoritmo Genético | 100% | 0,00 ± 0,00 | 0 | 0 | 4.412 [2.244 – 29.616] |

### medio (51 casas livres, |S| ≈ 4.72e+23)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 23,57 ± 1,17 | 21 | 25 | — |
| HC + reinício | 3% | 5,27 ± 1,53 | 0 | 8 | 2.357 [2.357 – 2.357] |
| Simulated Annealing | 90% | 0,20 ± 0,60 | 0 | 2 | 1.092 [220 – 41.842] |
| Algoritmo Genético | 100% | 0,00 ± 0,00 | 0 | 0 | 31.172 [5.175 – 198.847] |

### dificil (55 casas livres, |S| ≈ 1.11e+27)

| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |
|---|---:|---:|---:|---:|---:|
| Sorteio aleatório | 0% | 24,93 ± 1,39 | 20 | 27 | — |
| HC + reinício | 0% | 6,23 ± 1,50 | 2 | 8 | — |
| Simulated Annealing | 97% | 0,07 ± 0,36 | 0 | 2 | 12.056 [736 – 39.316] |
| Algoritmo Genético | 17% | 1,67 ± 0,75 | 0 | 2 | 68.432 [27.149 – 196.303] |

Tempo total de parede: 142 s (informativo; o custo é medido em avaliações).
