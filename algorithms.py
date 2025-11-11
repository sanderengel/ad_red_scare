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

# Cost 1 if arriving at red node
def solve_few(G):
    adjacency = defaultdict(list)
    for u, v in G.E:
        adjacency[u].append(v)

    INF = 10**18
    distance = {v: INF for v in G.V}
    distance[G.s] = 1 if G.is_red(G.s) else 0

    # Run Dijkstra's - using minheap
    priority_queue = [(distance[G.s], G.s)]

    while priority_queue:
        current_cost, u = heapq.heappop(priority_queue)
        if current_cost != distance[u]: # detect old distance
            continue

        if u == G.t:
            return current_cost
        
        # try to look for a better distance
        for v in adjacency[u]:
            new_cost = current_cost + (1 if G.is_red(v) else 0)
            if new_cost < distance[v]: # found better
                distance[v] = new_cost
                heapq.heappush(priority_queue, (new_cost, v))

    return -1  # end node unreachable

def build_adjacency(g: Graph):
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

def solve_alternate(g: Graph) -> bool:
    adj = build_adjacency(g)
    start_red = g.s in g.R
    q = deque([(g.s, start_red)])
    seen = {(g.s, start_red)}
    while q:
        u, last_red = q.popleft()
        if u == g.t:
            return True
        for v in adj[u]:
            v_red = v in g.R
            if v_red == last_red:
                continue
            state = (v, v_red)
            if state in seen:
                continue
            seen.add(state)
            q.append(state)
    return False
