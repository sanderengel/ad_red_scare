import os
from collections import defaultdict
from utils import read_input

class Graph:
    def __init__(self, file_path):
        n, m, r, s, t, V, R, E, directed = read_input(file_path)
        filename = os.path.basename(file_path)

        # Define instance name and if directed
        self.instance_name = os.path.splitext(filename)[0]
        self.directed = directed

        # Define standard attributes
        self.n = n
        self.m = m
        self.r = r
        self.s = s
        self.t = t
        self.V = V
        self.R = R
        self.E = E

    def get_in_degrees(self) -> dict:
        """
        Returns a dict of in-degrees for all vertices in input Graph G.
        """
        # Initialize all in-degrees as zero
        in_degrees = {u: 0 for u in self.V}

        # Iterate over edges and update in-degrees
        for _, v in self.E:
            in_degrees[v] += 1

        return in_degrees

    def get_adjacency_list(self) -> defaultdict:
        # Must use E to build adjacency list
        adj = defaultdict(set)
        for u, v in self.E:
            adj[u].add(v)
        return adj

    def has_edge(self, u, v):
        return (u, v) in self.E
    
    def is_red(self, u):
        return u in self.R