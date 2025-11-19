def read_input(file_path, as_sets = True):
    with open(file_path, 'r') as infile:
        n, m, r = map(int, infile.readline().split()) 
        s, t = infile.readline().split()
        
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
        directed = True
        E = []
        for e in edge_lines:
            u, arrow, v = e
            E.append((u, v))
            if arrow == '--':
                E.append((v, u))
                directed = False

        if as_sets:
            V = set(V)
            R = set(R)
            E = set(E)

        return n, m, r, s, t, V, R, E, directed
