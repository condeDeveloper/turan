# O teorema de Mantel e o de Turán

Quantas arestas cabem num grafo de `n` vértices **sem formar um triângulo**?
Willem Mantel respondeu em 1907: `⌊n²/4⌋`, e o recorde é do bipartido completo
mais equilibrado. Pál Turán generalizou em 1941 para cliques de qualquer
tamanho.

Aqui o teorema não é citado: ele é **varrido**. Todos os grafos rotulados de até
sete vértices são gerados um por um — 2.097.152 deles — e o máximo é medido. O
juiz é o grafo de Turán, construído à parte, que não olha nenhum grafo da
varredura. Python puro, sem dependência nenhuma.

## Os quatro achados

1. **O máximo medido bate com `⌊n²/4⌋` nos seis tamanhos varridos**, de dois a
   sete vértices, somando **2.131.018 grafos** olhados um a um. Nenhum grafo
   livre de triângulo passou do limite, e isso também está em teste: não é só o
   recorde que bate, é a tabela inteira.
2. **A quantidade de grafos extremais é exatamente a contagem de rotulações do
   bipartido completo.** São `C(n, ⌊n/2⌋)` quando `n` é ímpar e metade disso
   quando é par — 3, 3, 10, 10, 35 —, o que mostra, por contagem, que **todo**
   extremal é o mesmo grafo com outros rótulos.
3. **A fatia de grafos livres de triângulo despenca.** Com três vértices são
   87,5%; com sete, **6,37%**. O triângulo deixa de ser evitável muito antes de
   o grafo ficar grande.
4. **O bipartido completo balanceado é maximal, não só máximo.** Qualquer
   aresta acrescentada a ele cria um triângulo — conferido aresta por aresta,
   para todo lugar vazio, até seis vértices.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### Sem triângulo: a varredura contra Mantel

| n | grafos varridos | máximo medido | n²/4 | arestas do Turán | batem |
|---|---|---|---|---|---|
| 2 | 2 | 1 | 1 | 1 | sim |
| 3 | 8 | 2 | 2 | 2 | sim |
| 4 | 64 | 4 | 4 | 4 | sim |
| 5 | 1.024 | 6 | 6 | 6 | sim |
| 6 | 32.768 | 9 | 9 | 9 | sim |
| 7 | 2.097.152 | 12 | 12 | 12 | sim |

### Quantos grafos atingem o máximo

| n | extremais | C(n, ⌊n/2⌋) | é o bipartido completo? |
|---|---|---|---|
| 2 | 1 | 2 | sim |
| 3 | 3 | 3 | sim |
| 4 | 3 | 6 | sim |
| 5 | 10 | 10 | sim |
| 6 | 10 | 20 | sim |
| 7 | 35 | 35 | sim |

Com `n` par a troca das duas partes devolve o mesmo grafo, e por isso a contagem
é a metade do binomial.

### A fatia de grafos livres de triângulo

| n | livres | de | fatia |
|---|---|---|---|
| 2 | 2 | 2 | 100,0000% |
| 3 | 7 | 8 | 87,5000% |
| 4 | 41 | 64 | 64,0625% |
| 5 | 388 | 1.024 | 37,8906% |
| 6 | 5.789 | 32.768 | 17,6666% |
| 7 | 133.501 | 2.097.152 | 6,3658% |

### Sem K4: a varredura contra Turán

| n | máximo medido | arestas do Turán com três partes | partes | extremais |
|---|---|---|---|---|
| 3 | 3 | 3 | [1, 1, 1] | 1 |
| 4 | 5 | 5 | [2, 1, 1] | 6 |
| 5 | 8 | 8 | [2, 2, 1] | 15 |
| 6 | 12 | 12 | [2, 2, 2] | 15 |

Com `--completo` entra o caso de sete vértices, que usa a busca geral de clique
e é bem mais lento que o teste de triângulo.

### O custo da varredura

| n | grafos | arestas possíveis |
|---|---|---|
| 6 | 32.768 | 15 |
| 7 | 2.097.152 | 21 |
| 8 | 268.435.456 | 28 |
| 9 | 68.719.476.736 | 36 |

Sete vértices levam 8 segundos. Oito levariam 128 vezes mais, e por isso a
tabela para em sete em vez de repetir o valor que a fórmula daria.

## O que as medidas me corrigiram

- **Achei que o número de extremais fosse sempre `C(n, ⌊n/2⌋)`.** Com `n` par é
  a metade: trocar as duas partes de lugar devolve exatamente o mesmo grafo
  rotulado. A tabela mostrou 3 onde eu esperava 6, e 10 onde eu esperava 20.
- **Esperava que a fatia de grafos livres de triângulo caísse devagar.** Ela cai
  de 87,5% para 6,37% em quatro passos. Com oito vértices já seria fração de
  milésimo: evitar triângulo é raro muito antes de o grafo ser grande.
- **Escrevi primeiro só o teste de triângulo e quase deixei assim.** A busca
  geral de clique é dezenas de vezes mais lenta, mas é ela que confere o atalho:
  as duas foram comparadas **grafo a grafo** em todos os 33.856 grafos de até
  seis vértices, e é esse teste que sustenta a varredura rápida de sete.
- **Esperava que o `maior_clique` de um extremal fosse 1.** É **2**: o grafo tem
  arestas, e cada aresta já é uma clique de dois. Livre de triângulo quer dizer
  clique máxima 2, não clique máxima 1.

## Como está organizado

```
turan/grafo.py      o grafo como máscara de bits, para a varredura caber
turan/cliques.py    o teste rápido de triângulo e a busca geral de clique
turan/extremal.py   a varredura extremal e o grafo de Turán, que é o juiz
ferramentas/medidor.py  roda tudo e imprime as tabelas acima
testes/             37 testes
```

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # inclui K4 em sete vértices
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
