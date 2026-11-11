import random

N = 9
DADAS = {'facil': 38, 'medio': 30, 'dificil': 26, 'calibracao': 26}


def candidatos(g, i):
    r, c = divmod(i, N)
    usados = set(g[r * N:(r + 1) * N]) | set(g[c::N])
    r0, c0 = (r // 3) * 3, (c // 3) * 3
    usados |= {g[(r0 + dr) * N + c0 + dc] for dr in range(3) for dc in range(3)}
    return [d for d in range(1, N + 1) if d not in usados]

def contar_solucoes(g, limite=2):
    vazias = [i for i in range(N * N) if not g[i]]
    if not vazias:
        return 1
    i = min(vazias, key=lambda k: len(candidatos(g, k)))
    total = 0
    for d in candidatos(g, i):
        g[i] = d
        total += contar_solucoes(g, limite - total)
        g[i] = 0
        if total >= limite:
            break
    return total

def solucao_completa(rng):
    base = [[(3 * (r % 3) + r // 3 + c) % N + 1 for c in range(N)] for r in range(N)]
    digitos = rng.sample(range(1, N + 1), N)
    bandas = rng.sample(range(3), 3)
    linhas = [b * 3 + r for b in bandas for r in rng.sample(range(3), 3)]
    pilhas = rng.sample(range(3), 3)
    colunas = [p * 3 + c for p in pilhas for c in rng.sample(range(3), 3)]
    return [digitos[base[r][c] - 1] for r in linhas for c in colunas]

def gerar(rng, dadas):
    while True:
        g = solucao_completa(rng)
        ordem = rng.sample(range(N * N), N * N)
        for i in ordem:
            if sum(1 for v in g if v) <= dadas:
                break
            v, g[i] = g[i], 0
            if contar_solucoes(list(g)) != 1:
                g[i] = v
        if sum(1 for v in g if v) == dadas:
            return g


if __name__ == '__main__':
    rng = random.Random(2025)
    for nome, dadas in DADAS.items():
        g = gerar(rng, dadas)
        assert contar_solucoes(list(g)) == 1
        print(f"    '{nome}':{' ' * (11 - len(nome))}'{''.join(map(str, g))}',")
