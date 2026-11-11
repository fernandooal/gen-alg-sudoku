import csv, os, random, statistics, sys, time
from itertools import product
from multiprocessing import Pool

import sudoku as S
import metodos as M

ORCAMENTO = 200_000
EXECUCOES = 30
SEMENTE_CALIBRACAO = 1000
EXECUCOES_CALIBRACAO = 10
INSTANCIA_CALIBRACAO = 'calibracao'

GRADE = {
    'Algoritmo Genético': [dict(tam_pop=p, taxa_mut=m) for p, m in product((100, 200), (0.3, 0.6, 0.8))],
    'Simulated Annealing': [dict(T0=t, alfa=a) for t, a in product((0.5, 2.0), (0.999, 0.9999, 0.99999))],
}
SAIDA = 'resultados'


def executar(tarefa):
    instancia, metodo, params, semente, orcamento = tarefa
    S.carregar(S.INSTANCIAS[instancia])
    random.seed(semente)
    S.zerar()
    melhor, aval = M.METODOS[metodo](orcamento, **params)
    return dict(instancia=instancia, metodo=metodo, params=params, semente=semente,
                conflitos=melhor, aval_solucao=aval, aval_usadas=S.AVALIACOES)

def resumir(linhas):
    c = [l['conflitos'] for l in linhas]
    a = sorted(l['aval_solucao'] for l in linhas if l['aval_solucao'] is not None)
    return dict(
        n=len(c), sucesso=len(a) / len(c),
        media=statistics.mean(c), desvio=statistics.pstdev(c), melhor=min(c), pior=max(c),
        mediana_aval=statistics.median(a) if a else None,
        min_aval=a[0] if a else None, max_aval=a[-1] if a else None,
    )

def fmt(v, casas=0):
    if v is None:
        return '—'
    return f'{v:,.{casas}f}'.replace(',', '.') if casas == 0 else f'{v:.{casas}f}'.replace('.', ',')


def calibrar(pool, orcamento, execucoes):
    escolhidos = {'Sorteio aleatório': {}, 'HC + reinício': {}}
    md = ['| Método | Configuração | Sucesso | Conflitos (média) | Avaliações até resolver (mediana) |',
          '|---|---|---:|---:|---:|']
    for metodo, configs in GRADE.items():
        tarefas = [(INSTANCIA_CALIBRACAO, metodo, p, SEMENTE_CALIBRACAO + k, orcamento)
                   for p in configs for k in range(execucoes)]
        res = pool.map(executar, tarefas)
        ranking = []
        for p in configs:
            r = resumir([l for l in res if l['params'] == p])
            ranking.append((-r['sucesso'], r['media'], r['mediana_aval'] or orcamento, p))
            md.append(f"| {metodo} | `{p}` | {100*r['sucesso']:.0f}% | {fmt(r['media'], 2)} | {fmt(r['mediana_aval'])} |")
            print(f"  {metodo:<22} {str(p):<36} sucesso {100*r['sucesso']:5.1f}%  "
                  f"média {r['media']:.2f}  mediana aval. {fmt(r['mediana_aval'])}")
        escolhidos[metodo] = min(ranking, key=lambda x: x[:3])[3]
    return escolhidos, md

def comparar(pool, escolhidos, orcamento, execucoes):
    tarefas = [(inst, m, escolhidos[m], sem, orcamento)
               for inst in S.TESTE for m in M.METODOS for sem in range(execucoes)]
    return pool.map(executar, tarefas)


def main():
    rapido = '--rapido' in sys.argv
    orcamento = 20_000 if rapido else ORCAMENTO
    execucoes = 5 if rapido else EXECUCOES
    exec_cal = 3 if rapido else EXECUCOES_CALIBRACAO
    os.makedirs(SAIDA, exist_ok=True)
    t = time.time()

    with Pool() as pool:
        print(f'Calibração em "{INSTANCIA_CALIBRACAO}", {exec_cal} execuções por configuração, '
              f'sementes {SEMENTE_CALIBRACAO}.., orçamento {orcamento}')
        escolhidos, md_cal = calibrar(pool, orcamento, exec_cal)
        print('Escolhidos:', escolhidos)

        print(f'\nComparação: {execucoes} execuções por método e instância, sementes 0..{execucoes-1}, '
              f'orçamento {orcamento} avaliações')
        res = comparar(pool, escolhidos, orcamento, execucoes)

    with open(os.path.join(SAIDA, 'execucoes.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(res[0]))
        w.writeheader()
        w.writerows(res)

    md = ['# Resultados', '',
          f'- Orçamento: **{fmt(orcamento)} avaliações** da função objetivo por execução',
          f'- Execuções: **{execucoes}** por método e instância, sementes 0..{execucoes-1} (as mesmas para todos)',
          f'- Calibração: {exec_cal} execuções por configuração na instância `{INSTANCIA_CALIBRACAO}` '
          f'(fora do conjunto de teste), sementes {SEMENTE_CALIBRACAO}..{SEMENTE_CALIBRACAO+exec_cal-1}', '',
          '## Calibração (6 configurações para AG e para SA)', '', *md_cal, '',
          f'Escolhidos: `{escolhidos}`', '', '## Comparação', '']
    for inst in S.TESTE:
        S.carregar(S.INSTANCIAS[inst])
        md += [f'### {inst} ({sum(map(len, S.LIVRES))} casas livres, |S| ≈ {S.tamanho_espaco():.2e})', '',
               '| Método | Sucesso | Conflitos: média ± desvio | Melhor | Pior | Avaliações até resolver: mediana [mín – máx] |',
               '|---|---:|---:|---:|---:|---:|']
        print(f'\n{inst}')
        for m in M.METODOS:
            r = resumir([l for l in res if l['instancia'] == inst and l['metodo'] == m])
            aval = '—' if r['mediana_aval'] is None else \
                f"{fmt(r['mediana_aval'])} [{fmt(r['min_aval'])} – {fmt(r['max_aval'])}]"
            md.append(f"| {m} | {100*r['sucesso']:.0f}% | {fmt(r['media'], 2)} ± {fmt(r['desvio'], 2)} "
                      f"| {r['melhor']} | {r['pior']} | {aval} |")
            print(f"  {m:<22} sucesso {100*r['sucesso']:5.1f}%  conflitos {r['media']:6.2f} ± {r['desvio']:5.2f}"
                  f"  [{r['melhor']}, {r['pior']}]  aval. até resolver (mediana) {aval}")
        md.append('')
    md.append(f'Tempo total de parede: {time.time() - t:.0f} s (informativo; o custo é medido em avaliações).')

    with open(os.path.join(SAIDA, 'resultados.md'), 'w') as f:
        f.write('\n'.join(md) + '\n')
    print(f'\nResultados em {SAIDA}/  ({time.time() - t:.0f} s)')


if __name__ == '__main__':
    main()
