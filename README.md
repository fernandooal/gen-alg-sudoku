# gen-alg-sudoku

TDE3 (Otimização) de Inteligência Artificial — PUCPR. Resolve Sudoku 9×9 como problema de
otimização com **Algoritmo Genético**, comparado a **Simulated Annealing**, **Hill Climbing
com reinício** e **sorteio aleatório**, todos com o mesmo orçamento de avaliações da função
objetivo.

Relatório completo: [`docs/RELATORIO.md`](docs/RELATORIO.md) · Ficha de projeto: [`docs/`](docs/)

## Modelagem em uma linha

Casas dadas fixas, cada bloco 3×3 é uma permutação dos dígitos que faltam nele (conflitos de
bloco são impossíveis por construção), vizinhança = trocar duas casas livres de um bloco, e
função objetivo = repetições em linhas e colunas (minimizar, ótimo = 0). O AG usa crossover
de um ponto entre blocos, mutação dirigida às casas em conflito e reinício da população
quando estagna.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `sudoku.py` | instâncias, representação, `estado_aleatorio()`, `conflitos(s)`, contador `AVALIACOES` |
| `metodos.py` | sorteio aleatório, HC com reinício, Simulated Annealing, Algoritmo Genético |
| `experimento.py` | protocolo: calibração simétrica em instância própria + comparação (30 execuções, sementes 0–29) |
| `demo.py` | execução ao vivo com o contador de avaliações na tela |
| `gerar_instancias.py` | gera as instâncias e confere solução única com um resolvedor exato |
| `resultados/` | saída do experimento (`resultados.md`, `execucoes.csv`) |

## Como rodar

Só biblioteca padrão, Python 3.10+.

```bash
python3 experimento.py            # protocolo completo (~2,5 min com multiprocessamento)
python3 experimento.py --rapido   # versão curta para conferir
python3 demo.py medio ag 0        # demo: instância, método (sorteio|hc|sa|ag), semente
```

## Resultado resumido (sucesso em 30 execuções, 200.000 avaliações)

| Método | Fácil | Médio | Difícil |
|---|---:|---:|---:|
| Sorteio aleatório | 0% | 0% | 0% |
| HC + reinício | 37% | 3% | 0% |
| Simulated Annealing | 100% | 90% | 97% |
| Algoritmo Genético | 100% | 100% | 17% |
