import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

X, y = make_blobs(n_samples=20, centers=4, cluster_std=0.60, random_state=0)

model = AgglomerativeClustering(n_clusters=4)
model.fit(X)


def plot_dendrogram(model, **kwargs):
    linkage_matrix = linkage(model.children_, method='ward')
    dendrogram(linkage_matrix, **kwargs)


plt.figure(figsize=(10, 5))
plt.title('Hierarchy')
plot_dendrogram(model)
plt.xlabel("Points")
plt.ylabel("Distance")
plt.show()