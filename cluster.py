import time
import json
from string import ascii_lowercase
from math import sqrt
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import warnings

t0 = time.time()
data_dir = "Data/"
input_file = data_dir+"nodes.json"
result_file = data_dir+"clusters.json"

with open(input_file, 'r') as f:
	nodes = json.load(f)
print(input_file+" file loaded")
print("Time lapsed : "+str(time.time()-t0))

n_samples = len(nodes)
X = np.zeros((n_samples,26) , dtype=np.int)
# , dtype=np.int
for i in range(n_samples):
	j = 0
	for c in ascii_lowercase:
		if c in nodes[i]:
			X[i][j] = nodes[i][c]
		j += 1
# X = X.tolist()
print("Vector array made")
print("Time lapsed : "+str(time.time()-t0))

batch_size = 2*sqrt(n_samples)
n_clusters = 1000
mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters, batch_size=batch_size, n_init=10, max_no_improvement=10, verbose=0)
warnings.filterwarnings("ignore")
mbk.fit(X)
mbk_means_labels = mbk.labels_
mbk_means_cluster_centers = mbk.cluster_centers_
# mbk_means_labels_unique = np.unique(mbk_means_labels)

print("Mini batch clustering completed")
print("Time lapsed : "+str(time.time()-t0))

clusters = {}
for i in range(n_clusters):
	clusters[str(i)] = {}
	clusters[str(i)]['label'] = i
	clusters[str(i)]['center'] = mbk_means_cluster_centers[i].tolist()
	clusters[str(i)]['points'] = []

for i in range(n_samples):
	node = nodes[i]
	label = mbk_means_labels[i]
	clusters[str(label)]['points'].append(node)

# print(json.dumps(clusters,indent=2))
print("Nodes appended to their cluster")
print("Time lapsed : "+str(time.time()-t0))

with open(result_file, 'w') as outfile:
	json.dump(clusters,outfile)
with open(data_dir+'clusters_indented.json', 'w') as outfile:
	json.dump(clusters,outfile,indent=2)

print("Cluster result saved")
print("Time lapsed : "+str(time.time()-t0))