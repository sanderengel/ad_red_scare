import heapq
from collections import deque, defaultdict
from utils import Graph

def solve_none_bfs(G: Graph) -> int:
    """
    Standard BFS solver for the None problem.
    
    Args:
        G (Graph): utils.Graph object.

    Returns:
        int: Length of the shortest path avoiding red vertices.
                Returns -1 if no such path exists.
    """
    # Build adj dict
    adj = defaultdict(list)
    for u, v in G.E:
        adj[u].append(v)

    # Build queue and distance dict
    q = deque([G.s])
    dist = {G.s: 0}

    while q:
        u = q.popleft()        
        if u == G.t:            
            return dist[u]
        for v in adj[u]:            
            if v in dist:                
                continue
            if G.is_red(v) and v != G.t:                
                continue            
            dist[v] = dist[u] + 1
            q.append(v)
    return -1

def solve_some_bfs(G: Graph) -> bool:
    """
    Standard solver for the Some problem.

    Args:
        G (Graph): utils.Graph object.

    Returns:
        bool: True if any path exists passing through at least one red vertex,
                else False.
    """
    adj = defaultdict(list)
    for u, v in G.E:
        adj[u].append(v)

    start_seen_red = G.is_red(G.s)

    q = deque([(G.s, start_seen_red)])
    visited = {(G.s, start_seen_red)}

    while q:
        u, seen_red = q.popleft()

        # if we reached t and we've seen a red somewhere on the path → success
        if u == G.t and seen_red:
            return True

        for v in adj[u]:
            next_seen_red = seen_red or (v in G.R)

            state = (v, next_seen_red)
            if state in visited:
                continue
            visited.add(state)
            q.append(state)

    # exhausted search, no s→t path that went through a red
    return False


def solve_few_dijkstra_pairweights(G) -> int:
    """
    Dijkstra where each edge (u -> v) has weight:
        w(u,v) = (u is red) + (v is red)
               = 2 if both red, 1 if exactly one red, 0 if both black.

    Returns:
        int: Minimum total edge-weight from s to t, or -1 if unreachable.
    """
    adj = defaultdict(list)
    for u, v in G.E:
        adj[u].append(v)

    def edge_weight(u, v) -> int:
        return (1 if G.is_red(u) else 0) + (1 if G.is_red(v) else 0)

    INF = float('inf')
    dist = {v: INF for v in G.V}
    dist[G.s] = 0

    pq = [(0, G.s)]  # (cost_so_far, node)

    while pq:
        cost_u, u = heapq.heappop(pq)
        if cost_u > dist[u]:
            continue

        if u == G.t:
            return cost_u

        for v in adj[u]:
            w = edge_weight(u, v)
            cand = cost_u + w
            if cand < dist[v]:
                dist[v] = cand
                heapq.heappush(pq, (cand, v))

    return -1