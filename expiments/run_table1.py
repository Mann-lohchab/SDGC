"""
Reproduces Table I from the SDGC paper.
"""

import time
import os

from sdgc.algorithm import (
    run_sdgc,
    run_greedy,
    run_dsatur,
)

from sdgc.utils import (
    load_dimacs,
    is_valid,
    num_colors,
)


# =========================================================
# PARAMETERS
# =========================================================

ALPHA = 3
BETA = 10
GAMMA = 8
K = 3
REPAIR_ITERS = 3


# =========================================================
# BENCHMARKS
# =========================================================

BENCHMARKS = [
    ("myciel4", "Sparse"),
    ("anna", "Sparse"),
    ("huck", "Sparse"),
    ("david", "Medium"),
    ("DSJC125.1", "Medium"),
    ("DSJC250.1", "Medium"),
    ("DSJC250.5", "Dense"),
    ("queen15_15", "Dense"),
]


# =========================================================
# MAIN
# =========================================================

def main():

    header = (
        f"{'Graph':<14} "
        f"{'V':>4} "
        f"{'Density':>8} "
        f"{'SDGC':>6} "
        f"{'Greedy':>7} "
        f"{'DSATUR':>8} "
        f"{'SDGC(s)':>10} "
        f"{'DSATUR(s)':>11}"
    )

    print("\nTable I — DIMACS Benchmark Coloring Results")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for name, density in BENCHMARKS:

        path = os.path.join(
            "benchmarks",
            f"{name}.col"
        )

        G = load_dimacs(path)

        # SDGC
        t0 = time.time()

        sdgc_col = run_sdgc(
            G,
            alpha=ALPHA,
            beta=BETA,
            gamma=GAMMA,
            k=K,
            repair_iters=REPAIR_ITERS,
        )

        sdgc_time = time.time() - t0

        # Greedy
        greedy_col = run_greedy(G)

        # DSATUR
        t0 = time.time()

        dsatur_col = run_dsatur(G)

        dsatur_time = time.time() - t0

        assert is_valid(
            G,
            greedy_col,
        ), f"Greedy invalid on {name}"

        assert is_valid(
            G,
            dsatur_col,
        ), f"DSATUR invalid on {name}"

        valid_flag = (
            "✓"
            if is_valid(G, sdgc_col)
            else "✗"
        )

        print(
            f"{name:<14} "
            f"{G.number_of_nodes():>4} "
            f"{density:>8} "
            f"{num_colors(sdgc_col):>5}{valid_flag} "
            f"{num_colors(greedy_col):>7} "
            f"{num_colors(dsatur_col):>8} "
            f"{sdgc_time:>10.2f} "
            f"{dsatur_time:>11.2f}"
        )

    print("=" * len(header))

    print(
        "\nNote: ✓ = valid coloring, "
        "✗ = hard constraint violation present"
    )


if __name__ == "__main__":
    main()
