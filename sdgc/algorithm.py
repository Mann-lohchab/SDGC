from .metrics import sdgc_score


# =========================================================
# SDGC
# =========================================================

def sdgc_assign(
    G,
    v,
    coloring,
    used_colors,
    alpha,
    beta,
    gamma,
    k,
):
    candidates = list(used_colors) + [
        max(used_colors, default=-1) + 1
    ]

    best_color = max(
        candidates,
        key=lambda c: sdgc_score(
            G,
            v,
            c,
            coloring,
            used_colors,
            alpha,
            beta,
            gamma,
            k,
        )
    )

    return best_color


def run_sdgc(
    G,
    alpha=3,
    beta=10,
    gamma=8,
    k=3,
    repair_iters=3,
):
    coloring = {}
    used_colors = set()

    order = sorted(
        G.nodes(),
        key=lambda v: G.degree(v),
        reverse=True,
    )

    # Initial pass
    for v in order:
        c = sdgc_assign(
            G,
            v,
            coloring,
            used_colors,
            alpha,
            beta,
            gamma,
            k,
        )

        coloring[v] = c
        used_colors.add(c)

    # Repair phase
    for _ in range(repair_iters):
        for v in order:
            c = sdgc_assign(
                G,
                v,
                coloring,
                used_colors,
                alpha,
                beta,
                gamma,
                k,
            )

            coloring[v] = c
            used_colors.add(c)

    return coloring


# =========================================================
# GREEDY
# =========================================================

def run_greedy(G):
    order = sorted(
        G.nodes(),
        key=lambda v: G.degree(v),
        reverse=True,
    )

    coloring = {}

    for v in order:
        neighbor_colors = {
            coloring[nb]
            for nb in G.neighbors(v)
            if nb in coloring
        }

        c = 0

        while c in neighbor_colors:
            c += 1

        coloring[v] = c

    return coloring


# =========================================================
# DSATUR
# =========================================================

def run_dsatur(G):
    coloring = {}

    saturation = {
        v: 0
        for v in G.nodes()
    }

    neighbor_set = {
        v: set()
        for v in G.nodes()
    }

    uncolored = set(G.nodes())

    while uncolored:
        v = max(
            uncolored,
            key=lambda x: (
                saturation[x],
                G.degree(x),
            )
        )

        neighbor_colors = {
            coloring[nb]
            for nb in G.neighbors(v)
            if nb in coloring
        }

        c = 0

        while c in neighbor_colors:
            c += 1

        coloring[v] = c
        uncolored.remove(v)

        for nb in G.neighbors(v):
            if (
                nb in uncolored
                and c not in neighbor_set[nb]
            ):
                neighbor_set[nb].add(c)
                saturation[nb] += 1

    return coloring
