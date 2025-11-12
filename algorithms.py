import heapq
from collections import deque
from detect_DAG import is_DAG
from graph import Graph

def solve_none_bfs(G: Graph) -> int:
    """
    Standard BFS solver for the None problem.
    
    Args:
        G (Graph): utils.Graph object.

    Returns:
        int: Length of the shortest path avoiding red vertices.
                Returns -1 if no such path exists.
    """
    # Get adjacency list
    adj = G.get_adjacency_list()

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
    # Get adjacency list
    adj = G.get_adjacency_list()

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
    # Get adjacency list
    adj = G.get_adjacency_list()

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
        for v in adj[u]:
            new_cost = current_cost + (1 if G.is_red(v) else 0)
            if new_cost < distance[v]: # found better
                distance[v] = new_cost
                heapq.heappush(priority_queue, (new_cost, v))

    return -1  # end node unreachable

def solve_alternate(G: Graph) -> bool:
    # Get adjacency list
    adj = G.get_adjacency_list()

    start_red = G.s in G.R
    q = deque([(G.s, start_red)])
    seen = {(G.s, start_red)}
    while q:
        u, last_red = q.popleft()
        if u == G.t:
            return True
        for v in adj[u]:
            v_red = v in G.R
            if v_red == last_red:
                continue
            state = (v, v_red)
            if state in seen:
                continue
            seen.add(state)
            q.append(state)
    return False

def _kahn_topological_sort(G: Graph, adj: dict):
    """
    Compute topological order of the vertices in input DAG G using Kahn's Algorithm.
    """
    # Get in-degrees and adjacency list
    in_degrees = G.get_in_degrees()

    # Initialize queue with all zero in-degree
    in_degree_zero = [v for v, d in in_degrees.items() if d == 0]
    q = deque(in_degree_zero)

    # Initialize ordering
    order = []

    # Process queue to build the ordering
    while q:

        # Get next instance in queue and add to order
        u = q.popleft()
        order.append(u)

        # Iterate over u's neighbors
        for v in adj.get(u, []):

            # Decrement v's degree
            in_degrees[v] -= 1

            # If v's in-degree is now zero, add to queue
            if in_degrees[v] == 0:
                q.append(v)

    # Check if length of order is correct
    if len(order) != G.n:
        raise ValueError('Graph contains a cycle and cannot be topologically sorted.')
    
    return order

def solve_many(G: Graph) -> int | str:
    # Check if not a DAG
    if not is_DAG(G): # We cannot solve these
        return '?'
    
    # Get adjacency list
    adj = G.get_adjacency_list()

    # Define weight function, w(u) == 1 if red, else 0
    def w(u):
        return int(G.is_red(u))

    # Compute topological order using kahn's algorithm
    order = _kahn_topological_sort(G, adj)

    # Initialize distance dict L, L(s) = w(s) and L(-inf) for all v != s
    L = {u: w(u) if u == G.s else -float('inf') for u in G.V}

    # Iterate through vertices in topological order to get edges
    for u in order:

        # Iterate through u's neighbors to update L
        for v in adj.get(u, []):
            L[v] = max(L[v], L[u] + w(v))

    # L[t] is now the maximum number of red vertices on any path
    max_red = L[G.t]

    # If max red is still -inf, t is unreachable and we return -1
    if max_red == -float('inf'):
        return '-1'
    
    return max_red
        

