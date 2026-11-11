import math, random
import sudoku as S


def _trocar(s, i, j):
    s[i], s[j] = s[j], s[i]

def _resultado(melhor):
    return melhor, (S.AVALIACOES if melhor == 0 else None)


def sorteio_aleatorio(orcamento):
    melhor = math.inf
    while S.AVALIACOES < orcamento:
        melhor = min(melhor, S.conflitos(S.estado_aleatorio()))
        if melhor == 0:
            break
    return _resultado(melhor)


def hill_climbing_reinicio(orcamento):
    melhor = math.inf
    while S.AVALIACOES < orcamento:
        s = S.estado_aleatorio()
        atual = S.conflitos(s)
        while S.AVALIACOES < orcamento:
            melhor = min(melhor, atual)
            if atual == 0:
                return _resultado(0)
            menor, candidatos = atual, []
            for i, j in S.vizinhos(s):
                if S.AVALIACOES >= orcamento:
                    break
                _trocar(s, i, j)
                v = S.conflitos(s)
                _trocar(s, i, j)
                if v < menor:
                    menor, candidatos = v, [(i, j)]
                elif v == menor and v < atual:
                    candidatos.append((i, j))
            if not candidatos:
                break
            _trocar(s, *random.choice(candidatos))
            atual = menor
        melhor = min(melhor, atual)
    return _resultado(melhor)


def simulated_annealing(orcamento, T0=1.0, alfa=0.9999, Tmin=1e-3):
    melhor = math.inf
    while S.AVALIACOES < orcamento:
        s = S.estado_aleatorio()
        e = S.conflitos(s)
        T = T0
        while T > Tmin and e > 0 and S.AVALIACOES < orcamento:
            i, j = S.troca_dirigida(s)
            _trocar(s, i, j)
            e2 = S.conflitos(s)
            d = e - e2
            if d > 0 or random.random() < math.exp(d / T):
                e = e2
            else:
                _trocar(s, i, j)
            melhor = min(melhor, e)
            T *= alfa
        melhor = min(melhor, e)
        if melhor == 0:
            break
    return _resultado(melhor)


def cruzamento_blocos(p1, p2):
    # Corte entre blocos: cada bloco é copiado inteiro e continua sendo uma permutação válida.
    k = random.randint(1, S.N - 1)
    filho = list(p2)
    for b in range(k):
        for i in S.casas_do_bloco(b):
            filho[i] = p1[i]
    return filho

def mutacao(s, taxa):
    while random.random() < taxa:
        _trocar(s, *S.troca_dirigida(s))
    return s

def torneio(pop, k):
    return max(random.sample(pop, k), key=lambda ind: ind[0])[1]

def algoritmo_genetico(orcamento, tam_pop=100, taxa_cruz=0.9, taxa_mut=0.6,
                       k_torneio=3, elite=2, paciencia=50):
    melhor = math.inf
    while melhor > 0 and S.AVALIACOES < orcamento:
        pop = []
        while len(pop) < tam_pop and S.AVALIACOES < orcamento:
            s = S.estado_aleatorio()
            pop.append((S.aptidao(s), s))
        melhor = min([melhor] + [S.APTIDAO_MAXIMA - f for f, _ in pop])
        recorde, estagnado = -1, 0
        while melhor > 0 and estagnado < paciencia and S.AVALIACOES < orcamento:
            pop.sort(key=lambda ind: ind[0], reverse=True)
            if pop[0][0] > recorde:
                recorde, estagnado = pop[0][0], 0
            else:
                estagnado += 1
            nova = pop[:elite]
            while len(nova) < tam_pop and S.AVALIACOES < orcamento:
                p1, p2 = torneio(pop, k_torneio), torneio(pop, k_torneio)
                filho = cruzamento_blocos(p1, p2) if random.random() < taxa_cruz else list(p1)
                filho = mutacao(filho, taxa_mut)
                f = S.aptidao(filho)
                nova.append((f, filho))
                melhor = min(melhor, S.APTIDAO_MAXIMA - f)
                if melhor == 0:
                    break
            pop = nova
    return _resultado(melhor)


METODOS = {
    'Sorteio aleatório': sorteio_aleatorio,
    'HC + reinício': hill_climbing_reinicio,
    'Simulated Annealing': simulated_annealing,
    'Algoritmo Genético': algoritmo_genetico,
}
