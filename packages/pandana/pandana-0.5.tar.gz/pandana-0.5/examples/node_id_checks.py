import os
import time

import numpy as np
import pandas as pd
import pandana.network as pdna
import scipy
from sklearn.neighbors import KDTree

print()
print('Initializing Pandana network...')
print()

storef = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../pandana/tests/osm_sample.h5'))

store = pd.HDFStore(storef, "r")
nodes, edges = store.nodes, store.edges
net = pdna.Network(nodes.x, nodes.y, edges["from"], edges.to, edges[["weight"]])
store.close()
print()
print()

print('Comparing KDTree implementations in SciPy and Scikit-Learn...')

df = pd.DataFrame({'x':nodes.x, 'y':nodes.y})

scipy_tree = scipy.spatial.KDTree(df.values)
print(scipy_tree.data)

sklearn_tree = KDTree(df.values)
print(sklearn_tree.data)

distances, indexes = sklearn_tree.query(df.values)
print(np.transpose(indexes)[0])

print(scipy_tree.query(df.values))
print(sklearn_tree.query(df.values))

distances, indexes = scipy_tree.query(df.values)
print(indexes)

net.plot(pd.Series(distances))

print('Running live node id code...')

node_ids = net.get_node_ids(nodes.x, nodes.y)
t0 = time.time()
net.set(node_ids, variable=nodes.x, name='longitude')
single = time.time()-t0

t0 = time.time()
net.precompute(10000)
multi = time.time()-t0

print('Your execution time ratio: {}'.format(single/multi))
print()