from algorithms import *

def grid(G):
    alternate_result = None # Not solved yet
    few_result = solve_few_dijkstra(G)
    many_result = None # Not solved yet
    none_result = solve_none_bfs(G)
    some_result = solve_some_bfs(G)
    result = {
        'instance_name': G.instance_name,
        'n': G.n,
        'A': alternate_result,
        'F': few_result,
        'M': many_result,
        'N': none_result,
        'S': some_result
    }
    return result
