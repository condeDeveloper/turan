"""Achar clique, que e a unica pergunta que a varredura faz de cada grafo.

Duas implementacoes, de proposito:

* `tem_triangulo` e especifica e rapida: para cada aresta, pergunta se os dois
  pontos tem vizinho em comum, o que e um `and` de duas mascaras;
* `tem_clique` e geral e lenta: monta cliques crescendo um vertice de cada vez.

A primeira varre milhoes de grafos em tempo razoavel. A segunda confere a
primeira, e e usada para r maior que 3.
"""

from .grafo import arestas_possiveis, vizinhancas


def tem_triangulo(mascara, n, pares=None):
    """O grafo tem tres vertices mutuamente ligados?"""
    if pares is None:
        pares = arestas_possiveis(n)
    viz = vizinhancas(mascara, n, pares)
    for k, (i, j) in enumerate(pares):
        if mascara >> k & 1 and viz[i] & viz[j]:
            return True
    return False


def tem_clique(mascara, n, r, pares=None):
    """O grafo tem um conjunto de `r` vertices mutuamente ligados?"""
    if r <= 1:
        return n >= r
    viz = vizinhancas(mascara, n, pares)

    def crescer(atual, candidatos, faltam):
        if faltam == 0:
            return True
        resto = candidatos
        while resto:
            bit = resto & -resto
            v = bit.bit_length() - 1
            resto -= bit
            if bin(candidatos).count("1") < faltam:
                return False
            if crescer(atual | bit, candidatos & viz[v] & ~((bit << 1) - 1), faltam - 1):
                return True
        return False

    return crescer(0, (1 << n) - 1, r)


def maior_clique(mascara, n, pares=None):
    """O tamanho da maior clique do grafo."""
    r = n
    while r > 0:
        if tem_clique(mascara, n, r, pares):
            return r
        r -= 1
    return 0
