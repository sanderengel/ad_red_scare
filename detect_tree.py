from collections import deque
from utils import Graph

def _is_acyclic(G) -> bool:
    # Keep three sets for the vertices
    unvisited = set(G.V) # Initialize all vertices as unvisited
    visiting = set()
    visited = set()

    def _acyclic_DFS(u):
        # Move u from unvisited to visiting
        unvisited.remove(u)
        visiting.add(u)

        # Explore u's neighbors
        for v in G.adj.get(u, []): # .get safely handles vertices with no out-edges

            # Back edge to a vertex currently in recursion stack implies cyckle
            if v in visiting:
                return False
            
            # Recursively run DFS on unvisisted neighbors
            if v in unvisited and not _acyclic_DFS(v):
                return False
                
        # Move u from visiting to visited
        # The path from u and its sub-tree is fully explored and cycle-free
        visiting.remove(u)
        visited.add(u)
        return True
    
    # Main loop, starts DFS on all components
    for u in list(G.V): # Use list() to safely modify while iterating
        if u in unvisited:
            # Initiate DFS from u
            if not _acyclic_DFS(u):
                return False
            
    return True

def _get_in_degrees(G: Graph) -> dict:
    """
    Returns a dict of in-degrees for all vertices in input Graph G.
    """
    # Initialize all in-degrees as zero
    in_degrees = {u: 0 for u in G.V}

    # Iterate over edges and update in-degrees
    for _, v in G.E:
        in_degrees[v] += 1

    return in_degrees
 
def _find_unique_root(in_degrees: dict) -> bool:
    """
    Finds and returns a unique root from input in-degrees if it exists,
    i.e., exactly one vertex with in-degree zero.

    Returns None if no such unique root exists or if multiple vertices have in-degree zero.
    """
    # Get vertices with in-degree zero
    in_degree_zero = [v for v, d in in_degrees.items() if d == 0]

    # Check if only one unique root exists
    if len(in_degree_zero) == 1:
        return in_degree_zero[0]
    
    # Return None if length is 0 (no root) or > 1 (mutliple roots)
    return None

def _is_connected(G: Graph, r) -> bool:
    """
    Checks if input Graph G is fully connected, originating from input root r.
    """
    if not G.V: # Handle empty graph case
        return True
    
    # Use BFS starting at root to find all reachable vertices
    q = deque([r])
    reachable = {r}
    while q:
        u = q.popleft()
        for v in G.adj.get(u, []):
            if v not in reachable:
                reachable.add(v)
                q.append(v)

    # Check if number of reachable vertices equals the total number of vertices (n)
    return len(reachable) == G.n

def _check_for_unique_parents(in_degrees: dict, r) -> bool:
    """
    Check if all non-root vertices in input Graph G have exactly one parent.
    """
    return all(d == 1 for v, d in in_degrees.items() if v != r)

def is_DAG(G: Graph) -> bool:
    """
    Checks if input Graph G is directed and acyclic.
    
    The structure of G ensures that undirected graphs are caught automatically 
    When checking if acyclical, since edges (u,v) and (v,u) would create a 2-cycle. 
    """
    return _is_acyclic(G)

def is_tree(G: Graph) -> bool:
    """
    Checks if input Graph G is a directed tree.
    """
    # First check if G is a DAG
    if not is_DAG(G):
        return False
    
    # Get in-degrees of vertices in G
    in_degrees = _get_in_degrees(G)

    # Find unique root r
    r = _find_unique_root(in_degrees)
    if r is None: # No unique root
        return False 
    
    # Check if graph is fully connected, originating from the root
    if not _is_connected(G, r):
        return False
    
    # Check for unique parents
    if not _check_for_unique_parents(in_degrees, r):
        return False
    
    # If passes all checks, G is a tree
    return True
