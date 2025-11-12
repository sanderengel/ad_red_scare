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
    print(f"{result['instance_name']:30} | N={result['N'] or 'N/A':>4} | S={result['S'] or 'N/A':>5} | "
          f"F={result['F'] or 'N/A':>4} | M={result['M'] or 'N/A':>4} | A={result['A'] or 'N/A':>5}")

# Create DataFrame and optionally save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv('results.csv', index=False)
print(f"\nResults saved to results.csv")


