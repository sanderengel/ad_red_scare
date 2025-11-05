import os
import pandas as pd

from utils import Graph
from word_graph import word_graph
from grid import grid

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
        print(f"[{idx}/{len(file_paths)}] Processing {G.instance_name}... (n={G.n}, m={G.m}, r={G.r})", end=" ")
        
        # Word graphs (rusty, common, bht)
        if G.type in ['rusty', 'common', 'bht']:
            result = word_graph(G)
            results.append(result)
            print("✓")
        
        # Grid graphs
        elif G.type == 'grid':
            result = grid(G)
            results.append(result)
            print("✓")
        
        # Small world graphs
        elif G.type == 'smallworld':
            result = word_graph(G)
            results.append(result)
            print("✓")
        
        # Wall graphs
        elif G.type == 'wall':
            result = word_graph(G)
            results.append(result)
            print("✓")
        
        # Increase graphs
        elif G.type == 'increase':
            result = word_graph(G) 
            results.append(result)
            print("✓")
        
        # Ski graphs
        elif G.type == 'ski':
            result = word_graph(G) 
            results.append(result)
            print("✓")
        
        # GNM random graphs
        elif G.type == 'gnm':
            result = word_graph(G) 
            results.append(result)
            print("✓")
        
        else:
            result = word_graph(G)  
            results.append(result)
            print("✓")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        continue

# Print results
print("\n" + "="*80)
print(f"Processed {len(results)} graphs")
print("="*80 + "\n")

for result in results:
    print(f"{result['instance_name']:30} | N={result['N'] or 'N/A':>4} | S={result['S'] or 'N/A':>5} | "
          f"F={result['F'] or 'N/A':>4} | M={result['M'] or 'N/A':>4} | A={result['A'] or 'N/A':>5}")

# Create DataFrame and optionally save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv('results.csv', index=False)
print(f"\nResults saved to results.csv")


