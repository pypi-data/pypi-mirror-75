# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:05:47 2020

@author: z003vrzk
"""

# Python imports
import unittest

# Third party imports
import numpy as np
from sklearn.datasets import make_blobs

# Local imports
from .c_index import (calc_c_index, simple_cluster_points)

from .c_index_R_interface import (calc_c_index_clusterCrit,
                                 calc_c_index_clusterSim)


#%%


class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Generate some dummy data for testing
        X is an (nxm) array where n is the number of data points and m is
        the feature space of each data point"""

        super(Test, self).__init__(*args, **kwargs)

        # Generate some data
        xs = np.array([[1,2,1.5,1.75,1.33,0.88],
                      [5,5.5,4.88,6.33,5.01,4.95]]) # Cluster 1, 2 x values
        ys = np.array([[8.9,8.5,7.89,8.25,8.85,8.29],
                      [1.25,1.14,1.85,0.85,0.79,0.96]]) # Cluster 1,2 y values
        self.X = np.stack((xs.ravel(),ys.ravel()), axis=1)
        # True labels for points in X
        self.cluster_labels = np.array([0,0,0,0,0,0,1,1,1,1,1,1])
        return None


    def test_calc_cindex_clusterCrit(self):

        X = self.X
        cluster_labels = self.cluster_labels + 1

        # Calculate Cindex from clusterCrit package...
        res = calc_c_index_clusterCrit(X, cluster_labels)
        cindex = res['c_index'][0]

        self.assertTrue(isinstance(cindex, float))

        return None

    def test_calc_cindex_clusterSim(self):

        cluster_labels = self.cluster_labels + 1

        # Calculate Cindex from clusterSim package...
        cindex = calc_c_index_clusterSim(self.X, cluster_labels)

        self.assertTrue(isinstance(cindex, float))

        return None


if __name__ == '__main__':
    unittest.main()

#%% Example 1


def example_1():
    import matplotlib.pyplot as plt

    # Generate some data
    xs = np.array([[1,2,1.5,1.75,1.33,0.88],
                  [5,5.5,4.88,6.33,5.01,4.95]]) # Cluster 1, 2 x values
    ys = np.array([[8.9,8.5,7.89,8.25,8.85,8.29],
                  [1.25,1.14,1.85,0.85,0.79,0.96]]) # Cluster 1,2 y values
    X = np.stack((xs.ravel(),ys.ravel()), axis=1)

    # Plot data
    fig1= plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.scatter(X[:,0], X[:,1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Points')

    # Calculate C Index
    cindicies_py = []
    cindices_clusterSim = []
    cindices_clusterCrit = []
    clusters = np.arange(2,6)
    for n_clusters in clusters:
        # Cluster data points
        cluster_labels = simple_cluster_points(X, n_clusters, clusterer='kmeans')

        # Calculate Cindex for varying number of clusters ('correct' implementation)
        cindex = calc_c_index(X, cluster_labels)
        cindicies_py.append(cindex)

        # Calculate Cindex from clusterCrit package...
        res = calc_c_index_clusterCrit(X, cluster_labels)
        cindex = res['c_index']
        cindices_clusterCrit.append(cindex)

        # Calculate Cindex from clusterSim package...
        cindex = calc_c_index_clusterSim(X, cluster_labels)
        cindices_clusterSim.append(cindex)


    # Plot C index
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(111)
    ax.plot(clusters, cindicies_py, label='Python Implementation')
    ax.plot(clusters, cindices_clusterSim, label='clusterSim Package')
    ax.plot(clusters, cindices_clusterCrit, label='ClsuterCrit Package')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('C Index')
    ax.set_title('C Index')
    ax.legend()
    return None

#%% Example 2

def example_2():
    import matplotlib.pyplot as plt

    # Generate some data
    X, labels = make_blobs(n_samples=50, n_features=2, centers=5, cluster_std=1)

    # Plot data
    fig1= plt.figure(1)
    ax = fig1.add_subplot(111)
    ax.scatter(X[:,0], X[:,1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Points')

    # Calculate C Index
    cindicies_py = []
    cindices_clusterSim = []
    cindices_clusterCrit = []
    clusters = np.arange(2,6)
    for n_clusters in clusters:
        # Cluster data points
        cluster_labels = simple_cluster_points(X, n_clusters, clusterer='kmeans')

        # Calculate Cindex for varying number of clusters ('correct' implementation)
        cindex = calc_c_index(X, cluster_labels)
        cindicies_py.append(cindex)

        # Calculate Cindex from clusterCrit package...
        res = calc_c_index_clusterCrit(X, cluster_labels)
        cindex = res['c_index']
        cindices_clusterCrit.append(cindex)

        # Calculate Cindex from clusterSim package...
        cindex = calc_c_index_clusterSim(X, cluster_labels)
        cindices_clusterSim.append(cindex)


    # Plot C index
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(111)
    ax.plot(clusters, cindicies_py, label='Python Implementation')
    ax.plot(clusters, cindices_clusterSim, label='clusterSim Package')
    ax.plot(clusters, cindices_clusterCrit, label='ClsuterCrit Package')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('C Index')
    ax.set_title('C Index')
    ax.legend()
    return None