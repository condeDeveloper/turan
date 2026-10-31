"""Os numeros do README, presos."""

import unittest
from math import comb

from turan.cliques import maior_clique, tem_triangulo
from turan.extremal import (
    arestas_de_turan,
    extremais,
    mantel,
    partes_de_turan,
    varrer,
)
from turan.grafo import grau, para_arestas, quantos_grafos

SEM_TRIANGULO = {n: varrer(n, 3) for n in range(2, 8)}


class TestMantel(unittest.TestCase):
    def test_o_maximo_bate_com_a_formula(self):
        esperado = {2: 1, 3: 2, 4: 4, 5: 6, 6: 9, 7: 12}
        for n, maximo in esperado.items():
            self.assertEqual(SEM_TRIANGULO[n].maximo, maximo, "n=%d" % n)
            self.assertEqual(mantel(n), maximo, "n=%d" % n)
            self.assertEqual(arestas_de_turan(n, 2), maximo, "n=%d" % n)

    def test_quantos_grafos_foram_varridos(self):
        esperado = {2: 2, 3: 8, 4: 64, 5: 1024, 6: 32768, 7: 2097152}
        for n, total in esperado.items():
            self.assertEqual(SEM_TRIANGULO[n].total, total, "n=%d" % n)
            self.assertEqual(quantos_grafos(n), total, "n=%d" % n)


class TestExtremais(unittest.TestCase):
    def test_quantos_atingem_o_maximo(self):
        esperado = {2: 1, 3: 3, 4: 3, 5: 10, 6: 10, 7: 35}
        for n, quantos in esperado.items():
            self.assertEqual(SEM_TRIANGULO[n].quantos_atingem, quantos, "n=%d" % n)

    def test_a_contagem_e_a_do_bipartido_completo(self):
        # escolher a parte menor da C(n, n//2) rotulacoes; com n par a troca das
        # duas partes da o mesmo grafo, entao divide por dois
        for n in range(2, 8):
            binomial = comb(n, n // 2)
            esperado = binomial // 2 if n % 2 == 0 else binomial
            self.assertEqual(SEM_TRIANGULO[n].quantos_atingem, esperado, "n=%d" % n)

    def test_todo_extremal_e_bipartido_balanceado(self):
        for n in range(2, 7):
            for mascara in extremais(n, 3):
                graus = sorted(grau(mascara, n))
                esperados = sorted(
                    [n - n // 2] * (n // 2) + [n // 2] * (n - n // 2)
                )
                self.assertEqual(graus, esperados, "n=%d m=%d" % (n, mascara))
                self.assertFalse(tem_triangulo(mascara, n))
                self.assertEqual(maior_clique(mascara, n), 2 if n > 1 else 1)


class TestFatiaDeLivres(unittest.TestCase):
    def test_quantos_grafos_nao_tem_triangulo(self):
        esperado = {2: 2, 3: 7, 4: 41, 5: 388, 6: 5789, 7: 133501}
        for n, livres in esperado.items():
            self.assertEqual(SEM_TRIANGULO[n].livres, livres, "n=%d" % n)

    def test_a_fatia_despenca(self):
        esperado = {2: 100.0, 3: 87.5, 4: 64.0625, 5: 37.8906, 6: 17.6666, 7: 6.3658}
        for n, fatia in esperado.items():
            self.assertAlmostEqual(
                100 * SEM_TRIANGULO[n].fatia_de_livres, fatia, places=4, msg="n=%d" % n
            )

    def test_cai_sempre(self):
        anterior = 1.1
        for n in range(2, 8):
            fatia = SEM_TRIANGULO[n].fatia_de_livres
            self.assertLessEqual(fatia, anterior, "n=%d" % n)
            anterior = fatia


class TestSemK4(unittest.TestCase):
    def test_o_maximo_bate_com_turan_de_tres_partes(self):
        esperado = {3: (3, 1), 4: (5, 6), 5: (8, 15), 6: (12, 15)}
        for n, (maximo, extremos) in esperado.items():
            e = varrer(n, 4)
            self.assertEqual(e.maximo, maximo, "n=%d" % n)
            self.assertEqual(arestas_de_turan(n, 3), maximo, "n=%d" % n)
            self.assertEqual(e.quantos_atingem, extremos, "n=%d" % n)

    def test_as_partes_sao_equilibradas(self):
        self.assertEqual(partes_de_turan(6, 3), [2, 2, 2])
        self.assertEqual(partes_de_turan(5, 3), [2, 2, 1])
        self.assertEqual(partes_de_turan(4, 3), [2, 1, 1])
        self.assertEqual(partes_de_turan(7, 3), [3, 2, 2])

    def test_o_turan_sem_k4_tem_mais_arestas_que_sem_triangulo(self):
        for n in range(3, 8):
            self.assertGreater(arestas_de_turan(n, 3), arestas_de_turan(n, 2), "n=%d" % n)


class TestUmExtremalDePerto(unittest.TestCase):
    def test_o_primeiro_extremal_de_cinco(self):
        melhor = extremais(5, 3)[0]
        self.assertEqual(
            para_arestas(melhor, 5),
            [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
        )

    def test_o_primeiro_extremal_de_seis(self):
        melhor = extremais(6, 3)[0]
        self.assertEqual(len(para_arestas(melhor, 6)), 9)
        self.assertEqual(maior_clique(melhor, 6), 2)
