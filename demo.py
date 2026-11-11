import random, sys
import sudoku as S
import metodos as M
from experimento import ORCAMENTO

APELIDOS = {'sorteio': 'Sorteio aleatório', 'hc': 'HC + reinício',
            'sa': 'Simulated Annealing', 'ag': 'Algoritmo Genético'}
PARAMS = {'Algoritmo Genético': dict(tam_pop=200, taxa_mut=0.8),
          'Simulated Annealing': dict(T0=0.5, alfa=0.99999)}

instancia = sys.argv[1] if len(sys.argv) > 1 else 'medio'
metodo = APELIDOS[sys.argv[2] if len(sys.argv) > 2 else 'ag']
semente = int(sys.argv[3]) if len(sys.argv) > 3 else 0

S.carregar(S.INSTANCIAS[instancia])
print(f'Instância "{instancia}": {sum(map(len, S.LIVRES))} casas livres, '
      f'|S| = {S.tamanho_espaco():.3e}, {S.n_vizinhos()} vizinhos por estado\n')
S.mostrar(S.DADO)

original, melhor = S.conflitos, [None]
def conflitos_com_log(s):
    v = original(s)
    if melhor[0] is None or v < melhor[0]:
        melhor[0] = v
        print(f'  avaliações = {S.AVALIACOES:>8,}   melhor conflitos = {v}'.replace(',', '.'))
    return v
S.conflitos = conflitos_com_log

print(f'\n{metodo}, semente {semente}, orçamento {ORCAMENTO:,} avaliações'.replace(',', '.'))
random.seed(semente)
S.zerar()
res, aval = M.METODOS[metodo](ORCAMENTO, **PARAMS.get(metodo, {}))
gastas = f'{S.AVALIACOES:,}'.replace(',', '.')
print(f'\nResultado: {res} conflitos, {gastas} avaliações gastas'
      + ('' if aval is None else ' (resolvido)'))
