"""O grafo como um numero, para caber a varredura inteira.

Com `n` vertices existem C(n, 2) arestas possiveis. Numerando elas de 0 em
diante, um grafo vira uma mascara de bits: o bit `k` diz se a aresta `k` esta
la. Varrer TODOS os grafos rotulados de `n` vertices e, entao, contar de 0 ate
2^C(n,2) - 1.

Com sete vertices sao 2.097.152 grafos, e cada um cabe num inteiro de 21 bits.
"""

from itertools import combinations


def arestas_possiveis(n):
    """Os pares (i, j) com i < j, na ordem em que viram bits."""
    return list(combinations(range(n), 2))


def quantos_grafos(n):
    """Quantos grafos rotulados existem com n vertices."""
    return 1 << (n * (n - 1) // 2)


def vizinhancas(mascara, n, pares=None):
    """Para cada vertice, a mascara de bits dos vizinhos dele."""
    if pares is None:
        pares = arestas_possiveis(n)
    viz = [0] * n
    for k, (i, j) in enumerate(pares):
        if mascara >> k & 1:
            viz[i] |= 1 << j
            viz[j] |= 1 << i
    return viz


def grau(mascara, n, pares=None):
    """O grau de cada vertice."""
    return [bin(v).count("1") for v in vizinhancas(mascara, n, pares)]


def quantas_arestas(mascara):
    """Quantas arestas o grafo tem."""
    return bin(mascara).count("1")


def de_arestas(pares_do_grafo, n):
    """A mascara de um grafo dado pela lista de arestas."""
    pares = arestas_possiveis(n)
    mascara = 0
    for i, j in pares_do_grafo:
        a, b = min(i, j), max(i, j)
        mascara |= 1 << pares.index((a, b))
    return mascara


def para_arestas(mascara, n):
    """A lista de arestas de uma mascara."""
    pares = arestas_possiveis(n)
    return [par for k, par in enumerate(pares) if mascara >> k & 1]
