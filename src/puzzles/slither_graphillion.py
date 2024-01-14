from graphillion import GraphSet
import graphillion.tutorial as tl

def A140517(n):
    if n == 0: return 0
    universe = tl.grid(n, n)
    GraphSet.set_universe(universe)
    cycles = GraphSet.cycles()
    return cycles.len()

print(A140517(10))

