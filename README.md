# SDGC — Separation-Driven Graph Coloring

> A unified scoring-based heuristic for constraint-aware graph coloring.  
> Companion code for the paper *"Separation-Driven Graph Coloring: A Unified Scoring Framework for Constraint-Aware Optimization"* — Lohchab & Yadav, SRM University Delhi NCR.

---

## Overview

SDGC formulates graph coloring as a **scoring maximization problem** rather than a pure constraint satisfaction task. Every color assignment — both in the initial pass and the repair phase — is governed by a single composite scoring function:

```
score(v, c) = α · sep(v, c)  −  β · conf(v, c)  −  γ · new(c)
```

| Term | Role |
|------|------|
| `sep(v, c)` | BFS-based separation: rewards reusing colors that are far away in the graph |
| `conf(v, c)` | Conflict penalty: penalizes adjacency violations |
| `new(c)` | Regularization: discourages introducing unnecessary new colors |

---

## Results (Table I)

| Graph | Vertices | Density | SDGC | Greedy | DSATUR | SDGC Time (s) | DSATUR Time (s) |
|-------|----------|---------|------|--------|--------|---------------|-----------------|
| myciel4 | 23 | Sparse | 5 | 6 | 5 | 0.03 | 0.01 |
| anna | 138 | Sparse | 11 | 12 | 11 | 0.19 | 0.07 |
| huck | 74 | Sparse | 11 | 12 | 11 | 0.11 | 0.04 |
| david | 87 | Medium | 12 | 13 | 11 | 0.15 | 0.05 |
| DSJC125.1 | 125 | Medium | 18 | 21 | 17 | 0.41 | 0.12 |
| DSJC250.1 | 250 | Medium | 30 | 33 | 28 | 1.24 | 0.39 |
| DSJC250.5 | 250 | Dense | 46 | 44 | 41 | 3.81 | 0.94 |
| queen15\_15 | 225 | Dense | 28 | 26 | 24 | 1.87 | 0.51 |

---

## Repository Structure

```
SDGC/
│
├── sdgc/                        # Core library
│   ├── __init__.py
│   ├── algorithm.py             # SDGC, Greedy, DSATUR implementations
│   ├── metrics.py               # sep(), conf(), scoring function
│   └── utils.py                 # Graph loaders, validators, helpers
│
├── benchmarks/                  # DIMACS benchmark graphs (.col files)
│   ├── myciel4.col
│   ├── anna.col
│   ├── huck.col
│   ├── david.col
│   ├── DSJC125.1.col
│   ├── DSJC250.1.col
│   ├── DSJC250.5.col
│   └── queen15_15.col
│
├── experiments/
│   └── run_table1.py            # Reproduces Table I from the paper
│
├── paper/
│   └── SDGC_paper.pdf           # Published manuscript
│
├── tests/
│   └── test_algorithms.py       # Unit tests for scoring and coloring logic
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Quickstart

### 1. Clone and install

```bash
git clone https://github.com/Mann-lohchab/SDGC.git
cd SDGC
pip install -r requirements.txt
```

### 2. Run the benchmark (Table I)

```bash
python experiments/run_table1.py
```

### 3. Use on your own graph

```python
import networkx as nx
from sdgc.algorithm import run_sdgc

G = nx.petersen_graph()
coloring = run_sdgc(G, alpha=3, beta=10, gamma=8, k=3, repair_iters=3)

print(f"Colors used: {len(set(coloring.values()))}")
```

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `alpha` | `3` | Weight on separation metric |
| `beta` | `10` | Weight on conflict penalty |
| `gamma` | `8` | Regularization penalty for new colors |
| `k` | `3` | BFS depth bound for separation |
| `repair_iters` | `3` | Number of repair-phase passes |

---

## Benchmark Data

The DIMACS `.col` files are **not** bundled in this repository due to file size. Download them from the official DIMACS archive and place them in `benchmarks/`:

> http://mat.tepper.cmu.edu/COLOR/instances.html

The loader in `sdgc/utils.py` handles the standard DIMACS format automatically.

---

## Requirements

```
networkx>=3.0
numpy>=1.24
```

Install via:

```bash
pip install -r requirements.txt
```

---

## Citation

If you use this code in your work, please cite:

```bibtex
@article{lohchab2024sdgc,
  title   = {Separation-Driven Graph Coloring: A Unified Scoring Framework
             for Constraint-Aware Optimization},
  author  = {Lohchab, Mann and Yadav, R.P.},
  year    = {2024},
  institution = {SRM University Delhi NCR}
}
```

---

## License

MIT License. See [`LICENSE`](LICENSE) for details.
