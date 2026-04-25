## Separation-Driven Graph Coloring (SDGC)

This repository implements SDGC, a heuristic graph coloring framework that formulates color assignment as a scoring problem:

score(v, c) = α · separation(v, c) − β · conflict(v, c)

The method incorporates global structure using BFS-based separation while handling diverse constraints.

### Implemented Scenarios
- SIR-based wireless frequency assignment
- Multi-constraint drone communication networks

### Features
- Separation-aware coloring
- Constraint-based scoring
- Unified assignment + repair mechanism
- Visualization of results
