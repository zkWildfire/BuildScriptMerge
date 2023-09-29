from build_script_group import BuildScriptGroup
from itertools import combinations
import numpy as np
from typing import List

def hierarchical_clustering(
	build_script_groups: List[BuildScriptGroup],
	threshold: float) -> List[BuildScriptGroup]:
    # Step 1: Start with each build script as a single cluster
    clusters = build_script_groups.copy()

    # Step 2: Compute initial dissimilarities
    dissimilarities = {}
    for a, b in combinations(clusters, 2):
        dissimilarities[(a, b)] = a.calculate_dissimilarity(b)

    # Step 3-5: Iteratively merge closest clusters and recompute dissimilarities
    while len(clusters) > 1:
        # Find the closest pair of clusters based on dissimilarity
        closest_pair = min(dissimilarities, key=dissimilarities.get)

        if dissimilarities[closest_pair] > threshold:
            break

        a, b = closest_pair
        new_cluster = BuildScriptGroup(
			a._build_scripts + b._build_scripts,
			a.unique_paths
		)

        # Remove old clusters and their dissimilarities
        clusters.remove(a)
        clusters.remove(b)
        dissimilarities = {k: v for k, v in dissimilarities.items() if a not in k and b not in k}

        # Compute dissimilarities between the new cluster and existing clusters
        for cluster in clusters:
            dissimilarities[(new_cluster, cluster)] = new_cluster.calculate_dissimilarity(cluster)

        # Add the new cluster
        clusters.append(new_cluster)

    return clusters

