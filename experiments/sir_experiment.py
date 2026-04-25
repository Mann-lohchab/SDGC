import numpy as np
import matplotlib.pyplot as plt
import random


# PARAMETERS


N = 50
AREA = 100
MAX_COLOR = 15

ALPHA = 3
BETA = 10

P = 1.0
ETA = 2.0
SIR_TH = 0.015


# NODE POSITIONS


nodes = [f"N{i}" for i in range(N)]
positions = {n: np.random.uniform(0, AREA, 2) for n in nodes}

def dist(a, b):
    return np.linalg.norm(positions[a] - positions[b])

def sir(u, v):
    d = dist(u, v)
    if d == 0:
        return float("inf")
    return P / (d ** ETA)


# BUILD CONSTRAINTS


adj = {n: [] for n in nodes}
dist2 = {n: [] for n in nodes}

for i in range(N):
    for j in range(i+1, N):
        u, v = nodes[i], nodes[j]
        s = sir(u, v)
        d = dist(u, v)

        if s >= SIR_TH:  # hard interference
            adj[u].append(v)
            adj[v].append(u)
        elif d < 30:  # soft interference
            dist2[u].append(v)
            dist2[v].append(u)

# allowed colors
allowed = {
    n: random.sample(range(MAX_COLOR), random.randint(5, 8))
    for n in nodes
}


# SDGC CORE


colors = {n: None for n in nodes}

def separation_score(v, c):
    visited = {v: 0}
    queue = [v]

    while queue:
        u = queue.pop(0)
        d = visited[u]

        if d > 3:
            break

        for w in adj[u]:
            if w not in visited:
                visited[w] = d + 1

                if colors[w] == c:
                    return d

                queue.append(w)

    return 3

def conflict_penalty(v, c):
    penalty = 0

    for u in adj[v]:
        if colors[u] == c:
            penalty += 5

    for u in dist2[v]:
        if colors[u] is not None:
            d = dist(v, u)
            if abs(colors[u] - c) < 2:
                penalty += (3 - min(3, d / 10))

    return penalty

def score(v, c):
    return ALPHA * separation_score(v, c) - BETA * conflict_penalty(v, c)


# NODE ORDER


order = sorted(nodes, key=lambda n: len(adj[n]), reverse=True)


# ASSIGN


for v in order:
    best = max(allowed[v], key=lambda c: score(v, c))
    colors[v] = best


# REPAIR


def repair(iterations=3):
    for _ in range(iterations):
        for v in nodes:
            best = max(allowed[v], key=lambda c: score(v, c))
            colors[v] = best

repair()


# METRICS


def violations():
    v = 0
    for u in nodes:
        for w in adj[u]:
            if colors[u] == colors[w]:
                v += 1
    return v // 2

print("SIR Colors used:", len(set(colors.values())))
print("Violations:", violations())


# VISUALIZATION

plt.figure(figsize=(10, 8))

for u in nodes:
    for v in adj[u]:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        plt.plot([x1, x2], [y1, y2], color='gray', alpha=0.2)

xs = [positions[n][0] for n in nodes]
ys = [positions[n][1] for n in nodes]
cs = [colors[n] for n in nodes]

sc = plt.scatter(xs, ys, c=cs, cmap='rainbow', s=120, edgecolors='black')

for n in nodes:
    x, y = positions[n]
    plt.text(x+1, y+1, n, fontsize=6)

plt.title(f"SIR SDGC (Colors={len(set(cs))}, Violations={violations()})")
plt.colorbar(sc)

plt.xlim(0, AREA)
plt.ylim(0, AREA)
plt.grid(alpha=0.2)

plt.savefig("sir_sdgc.png", dpi=300, bbox_inches='tight')
plt.show()
