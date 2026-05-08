from collections import deque


def bfs_separation(G, v, color, coloring, k):
    """
    BFS up to depth k.
    Returns hop distance to nearest vertex with same color.
    """

    visited = {v: 0}
    queue = deque([v])

    while queue:
        node = queue.popleft()
        d = visited[node]

        if d >= k:
            continue

        for nb in G.neighbors(node):
            if nb not in visited:
                visited[nb] = d + 1

                if coloring.get(nb) == color:
                    return visited[nb]

                queue.append(nb)

    return k


def conflict_penalty(G, v, color, coloring):
    """
    Hard adjacency penalty.
    """

    return 5 * sum(
        1
        for nb in G.neighbors(v)
        if coloring.get(nb) == color
    )


def sdgc_score(
    G,
    v,
    color,
    coloring,
    used_colors,
    alpha,
    beta,
    gamma,
    k,
):
    sep = bfs_separation(
        G,
        v,
        color,
        coloring,
        k,
    )

    conf = conflict_penalty(
        G,
        v,
        color,
        coloring,
    )

    new = 0 if color in used_colors else 1

    return (
        alpha * sep
        - beta * conf
        - gamma * new
    )
