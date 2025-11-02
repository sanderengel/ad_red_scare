from collections import deque, defaultdict
from utils import Graph
import os
import sys

DATA_DIR = os.path.join("red-scare", "data")

def build_adjacency(g: Graph):
    # Undirected adjacency, deduplicate neighbors, skip self-loops
    adj = defaultdict(list)
    seen = defaultdict(set)
    for u, v in g.E:
        if u == v:
            continue
        if v not in seen[u]:
            adj[u].append(v)
            seen[u].add(v)
        if u not in seen[v]:
            adj[v].append(u)
            seen[v].add(u)
    return adj


def SolveNone(g: Graph) -> int:
    # NONE BFS dont take the edge if in R and is neither start or end
    adj = build_adjacency(g)
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


def SolveSome(g: Graph) -> bool:
    # Some
    adj = build_adjacency(g)
    start_seen_red = g.s in g.R
    q = deque([(g.s, start_seen_red)])
    visited = {(g.s, start_seen_red)}
    while q:
        u, seen_red = q.popleft()
        if u == g.t and seen_red:
            return True
        for v in adj[u]:
            next_seen_red = seen_red or (v in g.R)
            state = (v, next_seen_red)
            if state in visited:
                continue
            visited.add(state)
            q.append(state)
    return False


def SolveMany(g: Graph) -> int:
    adj = build_adjacency(g)

    if g.s == g.t:
        return int(g.s in g.R)

    def reach(start, graph):
        seen = {start}
        dq = deque([start])
        while dq:
            u = dq.popleft()
            for v in graph.get(u, []):
                if v not in seen:
                    seen.add(v)
                    dq.append(v)
        return seen

    reach_s = reach(g.s, adj)
    if g.t not in reach_s:
        return -1
    reach_t = reach(g.t, adj)
    bi = reach_s & reach_t
    adj_bi = {u: [v for v in adj[u] if v in bi] for u in bi}
    red = {v for v in bi if v in g.R}

    # Identify non-red connected components
    comp_of = {}
    comps = []
    for u in bi:
        if u in red or u in comp_of:
            continue
        idx = len(comps)
        comps.append([])
        dq = deque([u])
        comp_of[u] = idx
        while dq:
            x = dq.popleft()
            comps[idx].append(x)
            for y in adj_bi.get(x, []):
                if y in red or y in comp_of:
                    continue
                comp_of[y] = idx
                dq.append(y)

    def map_node(u):
        if u in red:
            return ("R", u)
        return ("C", comp_of[u])

    cadj = defaultdict(set)
    nodes_c = set()
    for u in bi:
        U = map_node(u)
        nodes_c.add(U)
        for v in adj_bi.get(u, []):
            V = map_node(v)
            if U != V:
                cadj[U].add(V)
                cadj[V].add(U)
                nodes_c.add(V)

    s0 = map_node(g.s)
    t0 = map_node(g.t)

    red_nodes_c = [("R", r) for r in red]
    red_index = {rn: i for i, rn in enumerate(red_nodes_c)}

    def popcount(x: int) -> int:
        return x.bit_count() if hasattr(int, "bit_count") else bin(x).count("1")

    red_mask = {u: (1 << red_index[u]) if u in red_index else 0 for u in nodes_c}
    work = deque(nodes_c)
    inq = {u: True for u in nodes_c}
    while work:
        u = work.popleft()
        inq[u] = False
        base = red_mask[u]
        for v in cadj.get(u, []):
            base |= red_mask[v]
        if base != red_mask[u]:
            red_mask[u] = base
            for v in cadj.get(u, []):
                if not inq.get(v, False):
                    work.append(v)
                    inq[v] = True

    def seen_mask_add(mask: int, v):
        if v in red_index:
            return mask | (1 << red_index[v])
        return mask

    def potential(v, seen_mask):
        return int(v in red_index) + popcount(red_mask[v] & ~seen_mask_add(seen_mask, v))

    def ordered_neighbors(u, seen_mask):
        nbrs = list(cadj.get(u, []))
        nbrs.sort(key=lambda x: -potential(x, seen_mask))
        return nbrs

    best = -1
    sys.setrecursionlimit(max(sys.getrecursionlimit(), len(nodes_c) + 500))

    def dfs(u, red_count, visited, seen_mask):
        nonlocal best
        upper = red_count + popcount(red_mask[u] & ~seen_mask)
        if upper <= best:
            return
        if u == t0:
            if red_count > best:
                best = red_count
            return
        for v in ordered_neighbors(u, seen_mask):
            if v in visited:
                continue
            new_seen = seen_mask_add(seen_mask, v)
            visited.add(v)
            dfs(v, red_count + int(v in red_index), visited, new_seen)
            visited.remove(v)

    start_seen = seen_mask_add(0, s0)
    dfs(s0, int(s0 in red_index), {s0}, start_seen)
    return best


def SolveFew(g: Graph) -> int:
    # Few: Minimum number of red vertices on any path (0-1 BFS)
    adj = build_adjacency(g)
    q = deque([g.s])
    best = {g.s: int(g.s in g.R)}
    while q:
        u = q.popleft()
        if u == g.t:
            return best[u]
        cur = best[u]
        for v in adj[u]:
            cost = cur + int(v in g.R)
            if v not in best or cost < best[v]:
                best[v] = cost
                if v in g.R:
                    q.append(v)
                else:
                    q.appendleft(v)
    return -1


def SolveAlternate(g: Graph) -> bool:
    # Alternate: alternating red/non-red path
    adj = build_adjacency(g)
    start_is_red = g.s in g.R
    q = deque([(g.s, start_is_red)])
    seen = {(g.s, start_is_red)}
    while q:
        u, last_red = q.popleft()
        if u == g.t:
            return True
        for v in adj[u]:
            vr = v in g.R
            if vr == last_red:
                continue
            st = (v, vr)
            if st in seen:
                continue
            seen.add(st)
            q.append(st)
    return False


if __name__ == "__main__":
    # Only process walls files
    wall_prefixes = ("wall", "walls")
    wall_files = [os.path.join(DATA_DIR, f)
                  for f in os.listdir(DATA_DIR)
                  if f.endswith(".txt") and f.lower().startswith(wall_prefixes)]
    wall_files.sort()
    if not wall_files:
        print("No walls files found. Place files named like 'walls-*.txt' or 'wall-*.txt' in the data folder.")
    else:
        print(f"Processing {len(wall_files)} walls files:\n")
        for path in wall_files:
            g = Graph(path)
            ans_none = SolveNone(g)
            ans_some = SolveSome(g)
            ans_many = SolveMany(g)
            ans_few = SolveFew(g)
            ans_alt = SolveAlternate(g)
            line = (f"{os.path.basename(path)}: "
                    f"None={ans_none}, Some={ans_some}, "
                    f"Many={ans_many}, Few={ans_few}, Alt={ans_alt}")
            print(line)
