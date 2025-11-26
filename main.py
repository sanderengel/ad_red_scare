import os
import pandas as pd
from graph import Graph
from algorithms import *

DATA_PATH = 'red-scare/data'
file_paths = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) 
              if os.path.isfile(os.path.join(DATA_PATH, f)) and f.endswith('.txt') 
              and not f.lower().startswith('readme') and not f.lower().startswith('results')]

# Sort by file size 
file_paths = sorted(file_paths, key=lambda x: os.path.getsize(x))

results = []

print(f"Found {len(file_paths)} files to process...") # should be 156
print("="*80)
# ✓ means the file is loaded correctly or error ✗ otherwise 
# Test for input files
for idx, file_path in enumerate(file_paths, 1):
    try:
        G = Graph(file_path)
        print(f"[{idx}/{len(file_paths)}] Processing {G.instance_name}... (n={G.n}, m={G.m}, r={G.r})")
        
        alternate_result = solve_alternate(G)
        few_result = solve_few(G)
        none_result = solve_none_bfs(G)

        many_result = some_result = '?!' # Initialize many and some as unsolvable
        if G.directed:
            # Try to solve using DP, will return '?!' internally if cyclic
            many_result = solve_many_DAG(G)
            if many_result != '?!':
                # If we got a valid solution for many, use it to infer solution for some
                some_result = str(isinstance(many_result, int) and many_result > 0).lower() # Returns str 'true' or 'false'
        else:
            some_result = solve_some_undirected(G) # Undirected, solvable for some

        result = {
            'instance_name': G.instance_name,
            'n': G.n,
            'A': alternate_result,
            'F': few_result,
            'M': many_result,
            'N': none_result,
            'S': some_result
        }

        results.append(result)
            
    except Exception as e:
        print(f"Error: {e}")
        continue

# Print results
print("\n" + "="*80)
print(f"Processed {len(results)} graphs")
print("="*80 + "\n")

# Sort results
results = sorted(results, key = lambda x: x['instance_name'])

for result in results:
    n_val = 'N/A' if result['N'] is None else result['N']
    s_val = 'N/A' if result['S'] is None else result['S']
    f_val = 'N/A' if result['F'] is None else result['F']
    m_val = 'N/A' if result['M'] is None else result['M']
    a_val = 'N/A' if result['A'] is None else result['A']

    print(f"{result['instance_name']:30} | N={n_val:>4} | S={s_val:>5} | "
          f"F={f_val:>4} | M={m_val:>4} | A={a_val:>5}")

# Create DataFrame and optionally save to txt
results_df = pd.DataFrame(results)
results_df.to_csv('results.txt', index=False)
print(f"\nResults saved to results.txt")


