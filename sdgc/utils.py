import networkx as nx


# =========================================================
# DIMACS LOADER
# =========================================================

def load_dimacs(filepath):
    """
    Load DIMACS .col graph.
    """

    G = nx.Graph()

    with open(filepath) as f:
        for line in f:
            if line.startswith("p"):
                _, _, n, _ = line.split()

                G.add_nodes_from(
                    range(1, int(n) + 1)
                )

            elif line.startswith("e"):
                _, u, v = line.split()

                G.add_edge(
                    int(u),
                    int(v),
                )

    return G


# =========================================================
# VALIDATION
# =========================================================

def is_valid(G, coloring):
    return all(
        coloring[u] != coloring[v]
        for u, v in G.edges()
    )


def num_colors(coloring):
    return len(set(coloring.values()))
