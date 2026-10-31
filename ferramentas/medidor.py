"""Roda as varreduras e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # inclui K4 em sete vertices

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time
from math import comb

from turan.cliques import maior_clique
from turan.extremal import (
    arestas_de_turan,
    extremais,
    mantel,
    partes_de_turan,
    varrer,
)
from turan.grafo import para_arestas, quantos_grafos

COMPLETO = "--completo" in sys.argv
ATE_TRIANGULO = 7
ATE_K4 = 7 if COMPLETO else 6


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def main():
    comeco = time.time()

    print("## Sem triangulo: a varredura contra Mantel\n")
    print("| n | grafos varridos | maximo medido | n^2/4 | arestas do Turan | batem |")
    print("|---|---|---|---|---|---|")
    extremos = {}
    for n in range(2, ATE_TRIANGULO + 1):
        e = varrer(n, 3)
        extremos[n] = e
        print(
            "| %d | %s | %d | %d | %d | %s |"
            % (
                n,
                milhar(e.total),
                e.maximo,
                mantel(n),
                arestas_de_turan(n, 2),
                "sim" if e.maximo == mantel(n) == arestas_de_turan(n, 2) else "NAO",
            )
        )

    print("\n## Quantos grafos atingem o maximo\n")
    print("| n | extremais | C(n, n/2) | metade | e o bipartido completo? |")
    print("|---|---|---|---|---|")
    for n in range(2, ATE_TRIANGULO + 1):
        e = extremos[n]
        binomial = comb(n, n // 2)
        esperado = binomial // 2 if n % 2 == 0 else binomial
        print(
            "| %d | %d | %d | %d | %s |"
            % (n, e.quantos_atingem, binomial, binomial // 2,
               "sim" if e.quantos_atingem == esperado else "NAO")
        )

    print("\n## A fatia de grafos livres de triangulo\n")
    print("| n | livres | de | fatia |")
    print("|---|---|---|---|")
    for n in range(2, ATE_TRIANGULO + 1):
        e = extremos[n]
        print("| %d | %s | %s | %.4f%% |" % (n, milhar(e.livres), milhar(e.total), 100 * e.fatia_de_livres))

    print("\n## Sem K4: a varredura contra Turan\n")
    print("| n | maximo medido | arestas do Turan com tres partes | partes | extremais |")
    print("|---|---|---|---|---|")
    for n in range(3, ATE_K4 + 1):
        e = varrer(n, 4)
        print(
            "| %d | %d | %d | %s | %d |"
            % (n, e.maximo, arestas_de_turan(n, 3), partes_de_turan(n, 3), e.quantos_atingem)
        )

    print("\n## Um extremal de perto\n")
    for n in (5, 6):
        melhores = extremais(n, 3)
        arestas = para_arestas(melhores[0], n)
        print("n=%d: %d arestas, %s" % (n, len(arestas), arestas))
        print("     maior clique do extremal: %d" % maior_clique(melhores[0], n))

    print("\n## O custo da varredura\n")
    print("| n | grafos | arestas possiveis |")
    print("|---|---|---|")
    for n in range(2, 10):
        print("| %d | %s | %d |" % (n, milhar(quantos_grafos(n)), n * (n - 1) // 2))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
