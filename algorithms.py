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

def solve_few_dijkstra(G: Graph) -> int:
    """
    Standard Dijkstra solver for the Few problem.

    Args:
        G (Graph): utils.Graph object.

    Returns:
        int: The minimum number of red vertices on any path from s to t.
                Returns -1 if no such path exists.
    """
    adj = defaultdict(list)
    for u, v in G.E:
        adj[u].append(v)

    INF = float('inf')
    dist = {v: INF for v in G.V}
    start_cost = 1 if G.is_red(G.s) else 0
    dist[G.s] = start_cost

    pq = [(start_cost, G.s)]  # (total_reds_so_far, node)

    while pq:
        cost_u, u = heapq.heappop(pq)
        if cost_u > dist[u]:
            continue

        if u == G.t:
            return cost_u  

        for v in adj[u]:
            add = 1 if v in G.R else 0
            cand = cost_u + add
            if cand < dist[v]:
                dist[v] = cand
                heapq.heappush(pq, (cand, v))

    # unreachable
    return -1