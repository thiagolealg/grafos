# Plot do grafo com Dijkstra (arestas + árvore de caminhos mínimos destacada por espessura)
import math
import matplotlib.pyplot as plt
from math import inf

# --- Dijkstra (matriz) ---
def minimum_distance(dist, visited):
    min_val = inf
    min_idx = -1
    for i, (d, v) in enumerate(zip(dist, visited)):
        if not v and d < min_val:
            min_val = d
            min_idx = i
    return min_idx

def dijkstra_matrix(graph, src=0):
    n = len(graph)
    dist = [inf] * n
    visited = [False] * n
    parent = [-1] * n
    dist[src] = 0
    for _ in range(n - 1):
        u = minimum_distance(dist, visited)
        if u == -1:
            break
        visited[u] = True
        for v in range(n):
            w = graph[u][v]
            if w > 0 and not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    return dist, parent

# --- Grafo do exemplo ---
graph = [
    [0, 1, 7, 6, 0, 0, 0],
    [1, 0, 9, 0, 0, 3, 0],
    [7, 9, 0, 0, 0, 0, 1],
    [6, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 2, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 3],
    [0, 0, 1, 0, 0, 5, 0],
]
src = 0
dist, parent = dijkstra_matrix(graph, src=src)

# --- Layout: círculo para os 7 vértices ---
n = len(graph)
positions = {}
for i in range(n):
    theta = 2 * math.pi * i / n
    positions[i] = (math.cos(theta), math.sin(theta))

# --- Arestas e pesos ---
edges = []
for i in range(n):
    for j in range(i+1, n):
        w = graph[i][j]
        if w > 0:
            edges.append((i, j, w))

spt_edges = set()
for v in range(n):
    u = parent[v]
    if u != -1:
        a, b = sorted((u, v))
        spt_edges.add((a, b))

# --- Plot ---
fig, ax = plt.subplots(figsize=(7, 7))

# Arestas gerais
for i, j, w in edges:
    x1, y1 = positions[i]
    x2, y2 = positions[j]
    ax.plot([x1, x2], [y1, y2], linewidth=1, alpha=0.6, label="Arestas" if "arestas_l" not in globals() else None)
    # Peso no ponto médio
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my, str(w), fontsize=9)

# Árvore de caminhos mínimos (destacada pela espessura)
for a, b in spt_edges:
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    ax.plot([x1, x2], [y1, y2], linewidth=3, label="Árvore de caminhos mínimos" if "spt_l" not in globals() else None)

# Nós
xs = [positions[i][0] for i in range(n)]
ys = [positions[i][1] for i in range(n)]
ax.scatter(xs, ys, s=200, label="Vértices")

# Rótulos dos nós (id e distância)
for i in range(n):
    x, y = positions[i]
    ax.text(x, y+0.07, f"{i+1}", fontsize=11, ha="center")
    d = dist[i]
    d_str = "∞" if d == float("inf") else int(d)
    ax.text(x, y-0.12, f"d={d_str}", fontsize=9, ha="center")

ax.set_title("Dijkstra (origem = 1): grafo e árvore de caminhos mínimos")
ax.set_aspect("equal")
ax.axis("off")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)

# Salva o arquivo para download opcional
out_path = "dijkstra_plot.png"
plt.tight_layout()
plt.savefig(out_path, dpi=160)
plt.show()

out_path
