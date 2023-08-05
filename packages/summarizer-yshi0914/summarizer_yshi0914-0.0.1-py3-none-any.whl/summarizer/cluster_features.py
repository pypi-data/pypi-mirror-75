from typing import List

import numpy as np
from numpy import ndarray
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()

class ClusterFeatures(object):
    """
    Basic handling of clustering features.
    """

    def __init__(
        self,
        features: ndarray,
        algorithm: str = 'DBSCAN',
        pca_k: int = None,
        random_state: int = 12345
    ):
        """
        :param features: the embedding matrix created by bert parent
        :param algorithm: Which clustering algorithm to use
        :param random_state: Random state
        """
        self.features = features
        self.algorithm = algorithm
        self.pca_k = pca_k
        self.random_state = random_state

    def __get_model(self, k: int):
        """
        Retrieve clustering model

        :param k: min num of points
        :return: Clustering model

        """
        ## *********** Auto set up min_samples & Auto detect epsilon
        neigh = NearestNeighbors(n_neighbors=k)
        nbrs = neigh.fit(self.features)
        distances, indices = nbrs.kneighbors(self.features)
        distances = np.sort(distances, axis=0)
        distances = distances[:,1]
        plt.plot(distances)
        ## plt.show()
        plt.savefig('distanceGraph.png')
        print('Distance graph is saved as: distanceGraph.png')
        input_eps = input("After viewing the graph, please enter the suitable epsilon for the DBSCAN: ")
        input_eps = float(input_eps)
        return DBSCAN(eps=input_eps, min_samples=k)

    def __find_closest_args(self, corePoints: np.ndarray):
        """
        Find the closest arguments to centroid
        :param corePoints: corePoints to find closest
        :return: Closest arguments
        """

        centroid_min = 1e10
        cur_arg = -1
        args = {}
        used_idx = []

        for j, corePoint in enumerate(corePoints):

            for i, feature in enumerate(self.features):
                value = np.linalg.norm(feature - corePoint)

                if value < centroid_min and i not in used_idx:
                    cur_arg = i
                    centroid_min = value

            used_idx.append(cur_arg)
            args[j] = cur_arg
            centroid_min = 1e10
            cur_arg = -1

        return args

    def cluster(self, ratio: float = 0.1) -> List[int]:
        """
        Clusters sentences based on the ratio
        :param ratio: Ratio to use for clustering
        :return: Sentences index that qualify for summary
        """

        k = 1 if ratio * len(self.features) < 1 else int(len(self.features) * ratio)
        model = self.__get_model(k).fit(self.features)
        corePoints = model.components_;
        cluster_args = self.__find_closest_args(corePoints)
        sorted_values = sorted(cluster_args.values())
        return sorted_values

    def __call__(self, ratio: float = 0.1) -> List[int]:
        return self.cluster(ratio)
