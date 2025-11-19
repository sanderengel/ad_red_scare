### Network flow to solve some

class FlowNetwork:
    def __init__(self, n):
        # Nodes are 0 to n-1
        # self.graph stores list of edges indices
        self.graph = [[] for _ in range(n)]
        # self.edges stores tuples: (u, v, capacity, flow, reverse_edge_idx) 
        self.edges = []

    def add_edge(self, u, v, cap = 1):
        # Forward edge
        forward_idx = len(self.edges)
        self.edges.append([u, v, cap, 0, forward_idx + 1])
        self.graph[u].append(forward_idx)

        # Backward edge (residual), 0 capacity
        backward_idx = len(self.edges)
        self.edges.append([v, u, 0, 0, forward_idx])
        self.graph[v].append(backward_idx)

    def reset_flow(self):
        """Fast reset of all flow values to 0, faster than creating new instance."""
        for e in self.edges:
            e[3] = 0 # Reset flow to 0

    def bfs(self, s, t, parent_edge):
        """Finds a path from s to t in residual graph using BFS."""
        visited = [False] * len(self.graph)
        q = [s]
        visited[s] = True

        while q:
            u = q.pop(0)
            if u == t:
                return True
            
            for edge_idx in self.graph[u]:
                e = self.edges[edge_idx]
                v = e[1]
                res = e[2] - e[3] # Capacity - flow

                # If there is residual capacity and not visited
                if not visited[v] and res > 0:
                    visited[v] = True
                    parent_edge[v] = edge_idx
                    q.append(v)

        return False
    
    def max_flow(self, s, t):
        flow = 0
        parent_edge = [-1] * len(self.graph)

        # While there is an augmenting path
        while self.bfs(s, t, parent_edge):
            path_flow = float('inf')
            curr = t

            # Find bottleneck capacity along the path
            while curr != s:
                idx = parent_edge[curr]
                e = self.edges[idx]
                curr = e[0] # u
                res = e[2] - e[3]
                path_flow = min(path_flow, res)

            # Update residual capacities
            flow += path_flow
            curr = t
            while curr != s:
                idx = parent_edge[curr]
                e = self.edges[idx]
                rev_idx = e[4]

                e[3] += path_flow                   # Add flow to forward
                self.edges[rev_idx][3] -= path_flow # Subtract from backward
                curr = e[0]

            # For this specific problem, we only need flow >= 2
            # We break early if we hit it
            if flow >= 2:
                return flow

        return flow