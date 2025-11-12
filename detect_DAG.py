from collections import deque
from graph import Graph

def _is_acyclic(G: Graph, adj: dict) -> bool:
    # Keep three sets for the vertices
    unvisited = set(G.V) # Initialize all vertices as unvisited
    visiting = set()
    visited = set()

    def _acyclic_DFS(u):
        # Move u from unvisited to visiting
        unvisited.remove(u)
        visiting.add(u)

        # Explore u's neighbors
        for v in adj.get(u, []): # .get safely handles vertices with no out-edges

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

def is_DAG(G: Graph) -> bool:
    """
    Checks if input Graph G is directed and acyclic.
    
    The structure of G ensures that undirected graphs are caught automatically 
    When checking if acyclical, since edges (u,v) and (v,u) would create a 2-cycle. 
    """
    # Get adjacency list
    adj = G.get_adjacency_list()

    return _is_acyclic(G, adj)
