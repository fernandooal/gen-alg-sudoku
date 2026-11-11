import math, random

N = 9
CASAS = N * N

AVALIACOES = 0

def zerar():
    global AVALIACOES
    AVALIACOES = 0


INSTANCIAS = {
    'facil':      '503609841400730090002000300097402000000010730850073024680000972720046000100090400',
    'medio':      '051007000000060000203000516060700091400000050100506270040801000000073029700004080',
    'dificil':    '000093800816204070000600000600000000285000600009130000560420030003060900000000000',
    'calibracao': '000300010732800006000004270010903000000140000203050600000000082007560000000007100',
}
TESTE = ['facil', 'medio', 'dificil']

DADO = []
LIVRES = []
FALTANTES = []
APTIDAO_MAXIMA = 2 * N * (N - 1)


def bloco_de(i):
    r, c = divmod(i, N)
    return (r // 3) * 3 + c // 3

def casas_do_bloco(b):
    r0, c0 = (b // 3) * 3, (b % 3) * 3
    return [(r0 + dr) * N + c0 + dc for dr in range(3) for dc in range(3)]

def carregar(texto):
    global DADO, LIVRES, FALTANTES
    DADO = [int(ch) for ch in texto]
    LIVRES, FALTANTES = [], []
    for b in range(N):
        casas = casas_do_bloco(b)
        presentes = {DADO[i] for i in casas if DADO[i]}
        LIVRES.append([i for i in casas if not DADO[i]])
        FALTANTES.append([d for d in range(1, N + 1) if d not in presentes])


def estado_aleatorio():
    s = list(DADO)
    for b in range(N):
        for i, d in zip(LIVRES[b], random.sample(FALTANTES[b], len(FALTANTES[b]))):
            s[i] = d
    return s

def conflitos(s):
    global AVALIACOES
    AVALIACOES += 1
    c = 0
    for k in range(N):
        c += N - len(set(s[k * N:(k + 1) * N]))
        c += N - len(set(s[k::N]))
    return c

def aptidao(s):
    return APTIDAO_MAXIMA - conflitos(s)


def vizinhos(s):
    for casas in LIVRES:
        for a in range(len(casas)):
            for b in range(a + 1, len(casas)):
                yield casas[a], casas[b]

def troca_aleatoria(s):
    blocos = [b for b in range(N) if len(LIVRES[b]) >= 2]
    return tuple(random.sample(LIVRES[random.choice(blocos)], 2))

def casas_em_conflito(s):
    # Inspeciona o estado atual sem avaliar um estado novo, por isso não conta em AVALIACOES.
    ruins = []
    for k in range(N):
        linha, coluna = s[k * N:(k + 1) * N], s[k::N]
        for c in range(N):
            if linha.count(linha[c]) > 1:
                ruins.append(k * N + c)
            if coluna.count(coluna[c]) > 1:
                ruins.append(c * N + k)
    return [i for i in ruins if not DADO[i] and len(LIVRES[bloco_de(i)]) >= 2]

def troca_dirigida(s):
    ruins = casas_em_conflito(s)
    if not ruins:
        return troca_aleatoria(s)
    i = random.choice(ruins)
    j = random.choice([j for j in LIVRES[bloco_de(i)] if j != i])
    return i, j

def n_vizinhos():
    return sum(math.comb(len(c), 2) for c in LIVRES)

def tamanho_espaco():
    return math.prod(math.factorial(len(c)) for c in LIVRES)


def mostrar(s):
    for r in range(N):
        if r and r % 3 == 0:
            print('------+-------+------')
        linha = ''
        for c in range(N):
            if c and c % 3 == 0:
                linha += '| '
            v = s[r * N + c]
            linha += (str(v) if v else '.') + ' '
        print(linha.rstrip())


carregar(INSTANCIAS['facil'])
