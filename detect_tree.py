from utils import Graph

def is_directed(G: Graph) -> bool:
    # For each edge, check if reverse edge exists
    for u, v in G.E:
        if (v, u) in G.E:
            return False
    return True


def is_tree(G: Graph) -> bool:
    return is_directed

