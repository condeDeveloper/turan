"""Propriedades do limite extremal, conferidas sem varrer tudo de novo."""

import unittest
from itertools import combinations

from turan.cliques import tem_clique, tem_triangulo
from turan.extremal import (
    arestas_de_turan,
    extremais,
    mantel,
    partes_de_turan,
    varrer,
)
from turan.grafo import de_arestas, quantas_arestas, quantos_grafos


def bipartido_completo(a, b):
    """O grafo completo bipartido com as partes {0..a-1} e {a..a+b-1}."""
    n = a + b
    arestas = [(i, j) for i in range(a) for j in range(a, n)]
    return de_arestas(arestas, n), n


class TestPartes(unittest.TestCase):
    def test_as_partes_somam_n(self):
        for n in range(1, 20):
            for partes in range(1, min(n, 6) + 1):
                self.assertEqual(sum(partes_de_turan(n, partes)), n, "n=%d" % n)

    def test_as_partes_diferem_no_maximo_de_um(self):
        for n in range(1, 20):
            for partes in range(1, min(n, 6) + 1):
                tamanhos = partes_de_turan(n, partes)
                self.assertLessEqual(max(tamanhos) - min(tamanhos), 1, "n=%d" % n)

    def test_duas_partes_dao_mantel(self):
        for n in range(1, 30):
            self.assertEqual(arestas_de_turan(n, 2), mantel(n), "n=%d" % n)

    def test_n_partes_dao_o_completo(self):
        for n in range(1, 12):
            self.assertEqual(arestas_de_turan(n, n), n * (n - 1) // 2, "n=%d" % n)


class TestBipartidoCompleto(unittest.TestCase):
    def test_ele_nao_tem_triangulo(self):
        for n in range(2, 9):
            mascara, total = bipartido_completo(n // 2, n - n // 2)
            self.assertFalse(tem_triangulo(mascara, total), "n=%d" % n)

    def test_ele_atinge_o_limite_de_mantel(self):
        for n in range(2, 9):
            mascara, _ = bipartido_completo(n // 2, n - n // 2)
            self.assertEqual(quantas_arestas(mascara), mantel(n), "n=%d" % n)

    def test_desbalancear_perde_aresta(self):
        for n in range(4, 10):
            balanceado = (n // 2) * (n - n // 2)
            for a in range(1, n):
                self.assertLessEqual(a * (n - a), balanceado, "n=%d a=%d" % (n, a))

    def test_qualquer_aresta_a_mais_cria_triangulo(self):
        # o bipartido completo e maximal: nao da para acrescentar nada
        for n in (4, 5, 6):
            mascara, _ = bipartido_completo(n // 2, n - n // 2)
            for bit in range(n * (n - 1) // 2):
                if mascara >> bit & 1:
                    continue
                self.assertTrue(tem_triangulo(mascara | (1 << bit), n), "n=%d" % n)


class TestVarredura(unittest.TestCase):
    def test_nenhum_extremal_tem_clique_proibida(self):
        for n in range(2, 7):
            for r in (3, 4):
                for mascara in extremais(n, r):
                    self.assertFalse(tem_clique(mascara, n, r), "n=%d r=%d" % (n, r))

    def test_nenhum_grafo_com_uma_aresta_a_mais_esta_livre(self):
        for n in range(3, 7):
            e = varrer(n, 3)
            acima = [
                m
                for m in range(quantos_grafos(n))
                if quantas_arestas(m) > e.maximo and not tem_triangulo(m, n)
            ]
            self.assertEqual(acima, [], "n=%d" % n)

    def test_o_maximo_cresce_sempre(self):
        anterior = -1
        for n in range(2, 8):
            maximo = mantel(n)
            self.assertGreater(maximo, anterior, "n=%d" % n)
            anterior = maximo

    def test_o_limite_sem_k4_vem_depois_do_sem_triangulo(self):
        for n in range(4, 7):
            sem_triangulo = varrer(n, 3).maximo
            sem_k4 = varrer(n, 4).maximo
            self.assertGreater(sem_k4, sem_triangulo, "n=%d" % n)

    def test_todo_grafo_livre_tem_no_maximo_o_limite(self):
        for n in range(2, 7):
            limite = mantel(n)
            for mascara in range(quantos_grafos(n)):
                if not tem_triangulo(mascara, n):
                    self.assertLessEqual(quantas_arestas(mascara), limite, "n=%d" % n)

    def test_a_definicao_de_triangulo(self):
        for n in (4, 5):
            for mascara in range(quantos_grafos(n)):
                arestas = set(
                    par
                    for k, par in enumerate(
                        [(i, j) for i in range(n) for j in range(i + 1, n)]
                    )
                    if mascara >> k & 1
                )
                pela_definicao = any(
                    (a, b) in arestas and (a, c) in arestas and (b, c) in arestas
                    for a, b, c in combinations(range(n), 3)
                )
                self.assertEqual(tem_triangulo(mascara, n), pela_definicao)
