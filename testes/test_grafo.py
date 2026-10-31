import unittest
from itertools import combinations

from turan.cliques import maior_clique, tem_clique, tem_triangulo
from turan.grafo import (
    arestas_possiveis,
    de_arestas,
    grau,
    para_arestas,
    quantas_arestas,
    quantos_grafos,
    vizinhancas,
)


class TestGrafoComoNumero(unittest.TestCase):
    def test_as_arestas_possiveis(self):
        self.assertEqual(arestas_possiveis(3), [(0, 1), (0, 2), (1, 2)])
        self.assertEqual(len(arestas_possiveis(7)), 21)

    def test_quantos_grafos(self):
        self.assertEqual(quantos_grafos(3), 8)
        self.assertEqual(quantos_grafos(7), 2097152)

    def test_ida_e_volta(self):
        for n in (4, 5):
            for mascara in range(quantos_grafos(n)):
                self.assertEqual(de_arestas(para_arestas(mascara, n), n), mascara)

    def test_vizinhanca_do_completo(self):
        n = 4
        completo = quantos_grafos(n) - 1
        viz = vizinhancas(completo, n)
        for v in range(n):
            esperado = ((1 << n) - 1) & ~(1 << v)
            self.assertEqual(viz[v], esperado)

    def test_grau_soma_duas_vezes_as_arestas(self):
        for n in (4, 5):
            for mascara in range(quantos_grafos(n)):
                self.assertEqual(sum(grau(mascara, n)), 2 * quantas_arestas(mascara))


class TestCliques(unittest.TestCase):
    def test_o_triangulo_mais_simples(self):
        n = 3
        self.assertTrue(tem_triangulo(de_arestas([(0, 1), (0, 2), (1, 2)], n), n))
        self.assertFalse(tem_triangulo(de_arestas([(0, 1), (0, 2)], n), n))

    def test_as_duas_implementacoes_concordam(self):
        for n in (4, 5, 6):
            for mascara in range(quantos_grafos(n)):
                self.assertEqual(
                    tem_triangulo(mascara, n),
                    tem_clique(mascara, n, 3),
                    "n=%d mascara=%d" % (n, mascara),
                )

    def test_clique_contra_a_definicao(self):
        # a definicao: existe um conjunto de r vertices todos ligados entre si
        n = 5
        pares = arestas_possiveis(n)
        for mascara in range(quantos_grafos(n)):
            presentes = {par for k, par in enumerate(pares) if mascara >> k & 1}
            for r in (2, 3, 4):
                pela_definicao = any(
                    all(tuple(sorted(p)) in presentes for p in combinations(grupo, 2))
                    for grupo in combinations(range(n), r)
                )
                self.assertEqual(
                    tem_clique(mascara, n, r, pares),
                    pela_definicao,
                    "n=%d m=%d r=%d" % (n, mascara, r),
                )

    def test_maior_clique_do_completo(self):
        for n in (3, 4, 5):
            self.assertEqual(maior_clique(quantos_grafos(n) - 1, n), n)

    def test_maior_clique_do_vazio(self):
        for n in (3, 4, 5):
            self.assertEqual(maior_clique(0, n), 1)
