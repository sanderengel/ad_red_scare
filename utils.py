def read_input(file_path, as_sets = True):
    with open(file_path, 'r') as infile:
        n, m, r = map(int, infile.readline().split()) # Read the first line and unpack n, m, r
        s, t = infile.readline().split() # Read the second line and unpack s, t
        
        vertex_lines = [infile.readline().strip() for _ in range(n)]
        V = []
        R = []
        for line in vertex_lines:
            if line[-1] == '*':
                u = line.split()[0]
                R.append(u)
            else:
                u = line.strip()
            V.append(u)

        if r != len(R):
            raise ValueError('Len of R does not match value of r')
        
        edge_lines = [tuple(infile.readline().split()) for _ in range(m)]
        E = []
        for e in edge_lines:
            u, arrow, v = e
            E.append((u, v))
            if arrow == '--':
                E.append((v, u))

        if as_sets:
            V = set(V)
            R = set(R)
            E = set(E)

        return n, m, r, s, t, V, R, E

class Graph:
    def __init__(self, file_path):
        n, m, r, s, t, V, R, E = read_input(file_path)
        self.type = file_path.split('-')[0]
        self.n = n
        self.m = m
        self.r = r
        self.s = s
        self.t = t
        self.V = V
        self.R = R
        self.E = E

    def has_edge(self, u, v):
        return (u, v) in self.E
    
    def is_red(self, u):
        return u in self.R
