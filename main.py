import os
import pandas as pd

from utils import Graph
from word_graphs import word_graphs
# More imports for other graph types ...
# ...
# ...

DATA_PATH = 'red-scare/data'
file_paths = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]
print(file_paths)

results = []

for file_path in file_paths:
    if file_path.endswith('.txt'):
        G = Graph(file_path)

        if G.type == 'rusty':
            # TODO: do something, pass G to the function
            # result = something
            pass

        # elif G.type == ....

        # ....

        # results.append(result)

results_df = pd.DataFrame(results)