from collections import deque, defaultdict
from utils import Graph
import sys
import os
import heapq

DATA_DIR = os.path.join("red-scare", "data")

#OUT_FILE = os.path.join("red-scare","results", "grids_few_results.txt")

# NONE BFS dont take the edge if in R and is neither start or end 
def BFS_None(g: Graph) -> int:
    adj = defaultdict(list)
    for u, v in g.E:
        adj[u].append(v)

    q = deque([g.s])
    dist = {g.s: 0}

    while q:
        u = q.popleft()
        if u == g.t:
            return dist[u]
        for v in adj[u]:
            if v in dist:
                continue
            if v in g.R and v != g.t:
                continue
            dist[v] = dist[u] + 1
            q.append(v)
    return -1


# Some
def BFS_Some(g: Graph) -> bool:
    adj = defaultdict(list)
    for u, v in g.E:
        adj[u].append(v)

    start_seen_red = g.s in g.R

    q = deque([(g.s, start_seen_red)])
    visited = {(g.s, start_seen_red)}

    while q:
        u, seen_red = q.popleft()

        # if we reached t and we've seen a red somewhere on the path → success
        if u == g.t and seen_red:
            return True

        for v in adj[u]:
            next_seen_red = seen_red or (v in g.R)

            state = (v, next_seen_red)
            if state in visited:
                continue
            visited.add(state)
            q.append(state)

    # exhausted search, no s→t path that went through a red
    return False



# FEW using dijkstra red nodes have added cost +1 
def Few_dijkstra(g: Graph) -> int:
    adj = defaultdict(list)
    for u, v in g.E:
        adj[u].append(v)

    INF = 10**9
    dist = {v: INF for v in g.V}
    start_cost = 1 if g.s in g.R else 0
    dist[g.s] = start_cost

    pq = [(start_cost, g.s)]  # (total_reds_so_far, node)

    while pq:
        cost_u, u = heapq.heappop(pq)
        if cost_u > dist[u]:
            continue

        if u == g.t:
            return cost_u  

        for v in adj[u]:
            add = 1 if v in g.R else 0
            cand = cost_u + add
            if cand < dist[v]:
                dist[v] = cand
                heapq.heappush(pq, (cand, v))

    # unreachable
    return -1



files = []
for name in os.listdir(DATA_DIR):
    if name.startswith("grid") and name.endswith(".txt"):
        files.append(os.path.join(DATA_DIR, name))
files.sort()
results = []
for path in files:
    g = Graph(path)
    ans = BFS_None(g)
    line = f"{os.path.basename(path)}: {ans}"
    print(line)
    results.append(line)

#with open(OUT_FILE, "w") as f:
    #f.write("\n".join(results))

#print(f"\n✅ Results saved to {OUT_FILE}")