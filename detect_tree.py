from utils import Graph

def is_directed(G: Graph) -> bool:
    # For each edge, check if reverse edge exists
    for u, v in G.E:
        if (v, u) in G.E:
            return False
    return True

def has_cycle(G) -> bool:
    # Keep three sets for the vertices
    unvisited = set(G.V) # Initialize all vertices as unvisited
    visiting = set()
    visited = set()

    # Iterate over all vertices u in V
    pass



def is_tree(G: Graph) -> bool:
    # Return False if undirected
    if not is_directed(G):
        return False
    


