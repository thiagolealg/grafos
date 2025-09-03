# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 08:05:26 2025

@author: fdeas

Verificações de passeio, trilha, caminho; BFS para menor caminho;
e checagem de isomorfismo entre grafos, com exemplos de uso
e visualização via matplotlib + networkx.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict, Optional


# -----------------------------
# Verificações de Passeio, Trilha e Caminho
# -----------------------------
def is_walk(G: nx.Graph, seq: List) -> bool:
    """Retorna True se seq é um passeio em G (toda aresta da sequência existe)."""
    for u, v in zip(seq, seq[1:]):
        if not G.has_edge(u, v):
            return False
    return len(seq) >= 2


def is_trail(G: nx.Graph, seq: List) -> bool:
    """Retorna True se seq é uma trilha (nenhuma aresta é repetida)."""
    if not is_walk(G, seq):
        return False
    used = set()
    for u, v in zip(seq, seq[1:]):
        # arestas de grafos não-direcionados são consideradas sem ordem
        eid = tuple(sorted((u, v)))
        if eid in used:
            return False
        used.add(eid)
    return True


def is_path(G: nx.Graph, seq: List) -> bool:
    """Retorna True se seq é um caminho (nenhum vértice é repetido)."""
    if not is_walk(G, seq):
        return False
    return len(set(seq)) == len(seq)


# -----------------------------
# Caminho mais curto (BFS)
# -----------------------------
def bfs_shortest_path(G: nx.Graph, s, t) -> Optional[List]:
    """Retorna uma lista com o menor caminho (por número de arestas) entre s e t, se existir."""
    if s == t:
        return [s]
    from collections import deque
    q = deque([s])
    parent = {s: None}
    while q:
        u = q.popleft()
        for v in G.neighbors(u):
            if v not in parent:
                parent[v] = u
                if v == t:
                    # reconstrói caminho
                    path = [t]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                q.append(v)
    return None


# -----------------------------
# Isomorfismo
# -----------------------------
def isomorphism_mapping(G: nx.Graph, H: nx.Graph) -> Optional[Dict]:
    """Retorna o mapeamento de isomorfismo G->H se existirem isomorfos, senão None."""
    GM = nx.algorithms.isomorphism.GraphMatcher(G, H)
    if GM.is_isomorphic():
        return GM.mapping
    return None


# -----------------------------
# Plotagem
# -----------------------------
def plot_graph(G, title: str = "", highlight_seq: Optional[List] = None):
    pos = nx.spring_layout(G, seed=42)
    plt.figure()
    plt.title(title)
    nx.draw(G, pos, with_labels=True)
    if highlight_seq and len(highlight_seq) > 1:
        edgelist = list(zip(highlight_seq, highlight_seq[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=4)
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_seq, node_size=600)
    plt.show()


# -----------------------------
# Exemplos de uso
# -----------------------------
if __name__ == "__main__":
    # Exemplo 1: Passeio, trilha e caminho
    G1 = nx.Graph()
    G1.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'D'), ('B', 'D'), ('C', 'E')])

    walk_seq = ['A', 'B', 'D', 'C', 'D']   # passeio
    trail_seq = ['A', 'B', 'C', 'D']       # trilha
    path_seq  = ['E', 'C', 'B', 'A']       # caminho

    print("is_walk(walk_seq):",  is_walk(G1, walk_seq))
    print("is_trail(trail_seq):", is_trail(G1, trail_seq))
    print("is_path(path_seq):",   is_path(G1, path_seq))

    plot_graph(G1, "Passeio em G1", highlight_seq=walk_seq)
    plot_graph(G1, "Trilha em G1", highlight_seq=trail_seq)
    plot_graph(G1, "Caminho em G1", highlight_seq=path_seq)

    # Exemplo 2: Caminho mais curto
    shortest = bfs_shortest_path(G1, 'A', 'E')
    print("Menor caminho entre A e E:", shortest)
    plot_graph(G1, "Menor caminho de A a E", highlight_seq=shortest if shortest else None)

    # Exemplo 3: Isomorfismo
    H1 = nx.Graph()
    H1.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

    H2 = nx.Graph()
    H2.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'a'), ('a', 'c')])

    mapping = isomorphism_mapping(H1, H2)
    print("São isomorfos?", mapping is not None)
    print("Mapeamento:", mapping)

    plot_graph(H1, "Grafo H1")
    plot_graph(H2, "Grafo H2")
