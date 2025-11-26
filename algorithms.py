import heapq
from collections import deque
from graph import Graph
from network_flow import FlowNetwork

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

def solve_alternate(G: Graph) -> str:
    # Get adjacency list
    adj = G.get_adjacency_list()

    start_red = G.s in G.R
    q = deque([(G.s, start_red)])
    seen = {(G.s, start_red)}
    while q:
        u, last_red = q.popleft()
        if u == G.t:
            return 'true'
        for v in adj[u]:
            v_red = v in G.R
            if v_red == last_red:
                continue
            state = (v, v_red)
            if state in seen:
                continue
            seen.add(state)
            q.append(state)
    return 'false'

def _kahn_topological_sort(G: Graph, adj: dict):
    """Compute topological order of the vertices in input DAG G using Kahn's Algorithm."""
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

def solve_many_DAG(G: Graph) -> int | str:
    adj = G.get_adjacency_list()

    # Try to get topological order
    # If G has a cycle, will return ValueError
    try:
        order = _kahn_topological_sort(G, adj)
    except ValueError:
        # G is cyclic, so we cannot solve many
        return '?!'
    
    # Define weight function, w(u) == 1 if red, else 0
    def w(u):
        return int(G.is_red(u))

    # Initialize distance dict L, L(s) = w(s) and L(-inf) for all v != s
    L = {u: w(u) if u == G.s else -float('inf') for u in G.V}

    for u in order:                  # Iterate through vertices in topological order to get edges
        if L[u] != -float('inf'):    # Skip unreachable vertices
            for v in adj.get(u, []): # Iterate through u's neighbors to update L
                L[v] = max(L[v], L[u] + w(v))

    # L[t] is now the maximum number of red vertices on any path
    max_red = L[G.t]

    # If max red is still -inf, t is unreachable and we return -1
    if max_red == -float('inf'):
        return '-1'
    
    return max_red
        
def _is_reachable(G: Graph, s, t) -> bool:
    # Simple BFS on original graph G
    visited = set([s])
    q = [s]
    adj = G.get_adjacency_list()
    while q:
        u = q.pop(0)
        if u == t:
            return True
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)
    return False

def solve_some_undirected(G: Graph) -> str:
    # Check if s or t are red, we just need any path from s to t
    if G.is_red(G.s) or G.is_red(G.t):
        if _is_reachable(G, G.s, G.t):
            return 'true'
        return 'false'
    
    # Get adjacency list
    adj = G.get_adjacency_list()

    # Build network flow
    # We have two nodes every vertex in G, plus a super sink
    n_flow_nodes = 2 * G.n + 1
    super_sink = 2 * G.n
    fn = FlowNetwork(n_flow_nodes)

    # Base edges
    base_edges = []

    # Function creates indices for in and out vertices
    vertex_map = {u: i for i, u in enumerate(G.V)} # Create int map (coordinate compression)
    def in_out_idx(u) -> int:
        u_idx = vertex_map[u]
        return 2 * u_idx, 2 * u_idx + 1

    # Internal edges (u_in -> u_out)
    for u in G.V:
        u_in_idx, u_out_idx = in_out_idx(u)
        base_edges.append((u_in_idx, u_out_idx))

    # Graph edges (undirected u-v turns to directed flow edges)
    for u, v in G.E:
        u_in_idx, u_out_idx = in_out_idx(u)
        v_in_idx, v_out_idx = in_out_idx(v)
        base_edges.append((u_out_idx, v_in_idx))
        base_edges.append((v_out_idx, u_in_idx))

    # Add connection to super sink 
    _, s_out_idx = in_out_idx(G.s)
    _, t_out_idx = in_out_idx(G.t)
    fn.add_edge(s_out_idx, super_sink, cap = 1)
    fn.add_edge(t_out_idx, super_sink, cap = 1)

    # Iterate over every red vertex candidate
    for r in G.R:
        if r == G.s or r == G.t:
            continue # Handled in first check

        # If degree < 2, it's a dead end and cannot support two disjoint paths
        if len(adj[r]) < 2:
            continue

        # Reset flow from previous iteration
        fn.reset_flow()

        # Run max flow
        # Source is r_out (2 * r + 1)
        _, r_out_idx = in_out_idx(r)
        if fn.max_flow(r_out_idx, super_sink) >= 2:
            return 'true'
        
    return 'false'
