"""A varredura extremal, e o juiz que nao varre nada.

A pergunta de Mantel (1907) e de Turan (1941) e a mesma: entre todos os grafos
de `n` vertices que NAO tem clique de tamanho `r`, qual tem mais arestas?

A varredura responde olhando todos os 2^C(n,2) grafos. O juiz responde com o
grafo de Turan, que e o completo multipartido com as partes mais equilibradas
possiveis, e com a formula do numero de arestas dele. Os dois nao compartilham
uma linha.
"""

from .cliques import tem_clique, tem_triangulo
from .grafo import arestas_possiveis, quantas_arestas, quantos_grafos


class Extremo:
    def __init__(self, n, r, maximo, quantos_atingem, livres, total):
        self.n = n
        self.r = r
        self.maximo = maximo
        self.quantos_atingem = quantos_atingem
        self.livres = livres
        self.total = total

    @property
    def fatia_de_livres(self):
        return self.livres / self.total


def varrer(n, r=3):
    """Varre todos os grafos de `n` vertices e acha o maximo sem clique `r`."""
    pares = arestas_possiveis(n)
    total = quantos_grafos(n)
    maximo = -1
    quantos = 0
    livres = 0
    for mascara in range(total):
        if r == 3:
            if tem_triangulo(mascara, n, pares):
                continue
        elif tem_clique(mascara, n, r, pares):
            continue
        livres += 1
        arestas = quantas_arestas(mascara)
        if arestas > maximo:
            maximo, quantos = arestas, 1
        elif arestas == maximo:
            quantos += 1
    return Extremo(n, r, maximo, quantos, livres, total)


def extremais(n, r=3):
    """As mascaras dos grafos que atingem o maximo."""
    pares = arestas_possiveis(n)
    melhor = varrer(n, r).maximo
    saida = []
    for mascara in range(quantos_grafos(n)):
        if quantas_arestas(mascara) != melhor:
            continue
        if r == 3 and tem_triangulo(mascara, n, pares):
            continue
        if r != 3 and tem_clique(mascara, n, r, pares):
            continue
        saida.append(mascara)
    return saida


def partes_de_turan(n, partes):
    """Os tamanhos das partes do grafo de Turan: o mais equilibrado possivel."""
    base = n // partes
    sobra = n % partes
    return [base + 1] * sobra + [base] * (partes - sobra)


def arestas_de_turan(n, partes):
    """Quantas arestas o grafo de Turan tem, contando par a par de partes.

    Este e o juiz: nao varre grafo nenhum e nao usa a formula fechada, so soma
    o produto dos tamanhos de cada par de partes.
    """
    tamanhos = partes_de_turan(n, partes)
    total = 0
    for i in range(len(tamanhos)):
        for j in range(i + 1, len(tamanhos)):
            total += tamanhos[i] * tamanhos[j]
    return total


def mantel(n):
    """O limite de Mantel: o piso de n ao quadrado sobre quatro."""
    return n * n // 4
