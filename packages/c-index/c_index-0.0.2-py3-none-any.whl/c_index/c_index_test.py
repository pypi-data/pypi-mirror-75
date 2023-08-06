# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 19:35:50 2020

@author: z003vrzk
"""

# Python imports
import unittest

# Third party imports
import numpy as np
from sklearn.datasets import make_blobs

from scipy.spatial.distance import pdist

# Local imports
from c_index import (calc_Nw,
                     calc_c_index,
                     calc_cindex_clusterSim_implementation,
                     calc_cindex_nbclust_implementation,
                     calc_smin_smax,
                     calc_sw,
                     pdist,
                     pdist_array,
                     simple_cluster_points,
                     validate_distance_input,
                     )

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

    def test_simple_cluster_points(self):
        """Not much to test here - just a helper fuction for plotting clustered
        points.
        Kmeans is a stoicastic method..."""

        cluster_labels = simple_cluster_points(self.X,
                                               n_clusters=2,
                                               clusterer='kmeans')
        self.assertTrue(isinstance(cluster_labels, np.ndarray))
        return None

    def test_calc_c_index(self):
        """calc_c_index call signature and output type"""
        X = self.X
        cluster_labels = self.cluster_labels
        cindex = calc_c_index(X, cluster_labels)

        self.assertAlmostEqual(cindex, 0, places=3)
        self.assertTrue(isinstance(cindex, float))

        return None

    def test_pdist_array(self):
        """Convert a list of points into an upper triangular array of distance
        measurements
        """

        # data
        X = self.X

        # Test the call signature
        distances_array = pdist_array(X)

        """The distance array should be square and rank 2"""
        self.assertEqual(np.ndim(distances_array), 2)
        self.assertTrue(distances_array.shape[0] == distances_array.shape[1])

        """The array should be uppper triangular with zeros in the bottom
        diagonal AND along the diagonal"""
        msg='Not all elements of the distance array are Zero'
        lower_indicies = np.tril_indices(X.shape[0], 0)
        self.assertTrue(np.all(distances_array[lower_indicies] == 0))
        assert np.all(distances_array[lower_indicies] == 0), msg

        """Test the calculated distance of each item in array"""
        distances = pdist(X)
        for m in range(0, distances_array.shape[0]): # Row axis
            for n in range(m+1, distances_array.shape[1]): # Column axis
                dist = np.linalg.norm(X[m] - X[n])
                assert(np.allclose(dist, distances_array[m,n]))
                self.assertAlmostEqual(dist, distances_array[m,n], places=3)


        return None

    def test_calc_cindex_nbclust_implementation(self):

        X = self.X
        cluster_labels = self.cluster_labels
        cindex = calc_c_index(X, cluster_labels)

        # nbclust implementaiton takes an array of pointwise differences
        distances_array = pdist_array(X)

        # Test cindex signature and return type
        cindex = calc_cindex_nbclust_implementation(distances_array,
                                                    cluster_labels)
        self.assertAlmostEqual(cindex, 0.403,places=3)
        self.assertTrue(isinstance(cindex, float))
        return None

    def test_calc_cindex_clusterSim_implementation(self):

        # nbclust inplementaiton takes an array of pointwise differences
        distances_array = pdist_array(self.X)

        # Test cindex signature and return type
        cindex = calc_cindex_clusterSim_implementation(distances_array,
                                                       self.cluster_labels)

        self.assertAlmostEqual(cindex, 0.0346,places=3)
        self.assertTrue(isinstance(cindex, float))
        return None

    def test_calc_Nw(self):

        cluster_labels = self.cluster_labels

        # Total Number of pairs of observations belonging to same cluster
        Nw = calc_Nw(cluster_labels)

        self.assertTrue(Nw == int(30))
        self.assertTrue(isinstance(Nw, int))

        return None

    def test_calc_smin_smax(self):

        # Total Number of pairs of observations belonging to same cluster
        Nw = calc_Nw(self.cluster_labels)

        # Distances between all pairs of points in dataset
        distances = pdist(self.X, metric='euclidean')

        # Sum of Nw smallest distances between all poirs of points
        # Sum of Nw largest distances between all pairs of points
        Smin, Smax = calc_smin_smax(distances, Nw)

        self.assertTrue(isinstance(Smin, float))
        self.assertTrue(isinstance(Smax, float))
        self.assertAlmostEqual(Smin, 24.540, places=3)
        self.assertAlmostEqual(Smax, 254.136, places=3)

        return None

    def test_calc_sw(self):
        X = self.X
        cluster_labels = self.cluster_labels

        # Sum of within-cluster distances
        Sw = calc_sw(X, cluster_labels)

        self.assertTrue(isinstance(Sw, float))
        self.assertAlmostEqual(Sw, 24.5402, places=3)

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
    cindicies_nbclust_implem = []
    cindicies_clusterSim_implem = []


    clusters = np.arange(2,6)
    for n_clusters in clusters:
        # Cluster data points
        cluster_labels = simple_cluster_points(X, n_clusters, clusterer='kmeans')

        # Calculate Cindex for varying number of clusters (correct implementation)
        cindex = calc_c_index(X, cluster_labels)
        cindicies_py.append(cindex)

        # Calculate Cindex for varying number of clusters (NbClust implementation)
        distances = pdist(X, metric='euclidean')
        distances_array = np.zeros((X.shape[0], X.shape[0]))
        upper_indicies = np.triu_indices(X.shape[0], 1)
        distances_array[upper_indicies] = distances
        cindex = calc_cindex_nbclust_implementation(distances_array, cluster_labels)
        cindicies_nbclust_implem.append(cindex)

        # Calculate Cindex from clusterSim implementation...
        cindex = calc_cindex_clusterSim_implementation(distances_array, cluster_labels)
        cindicies_clusterSim_implem.append(cindex)


    # Plot C index
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(111)
    ax.plot(clusters, cindicies_py, label='Python Implementation')
    ax.plot(clusters, cindicies_nbclust_implem, label='NbClust Implementation')
    ax.plot(clusters, cindicies_clusterSim_implem, label='ClusterSim Implementation')
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
    cindicies_nbclust_implem = []
    cindicies_clusterSim_implem = []


    clusters = np.arange(2,6)
    for n_clusters in clusters:
        # Cluster data points
        cluster_labels = simple_cluster_points(X, n_clusters, clusterer='kmeans')

        # Calculate Cindex for varying number of clusters (correct implementation)
        cindex = calc_c_index(X, cluster_labels)
        cindicies_py.append(cindex)

        # Calculate Cindex for varying number of clusters (NbClust implementation)
        distances = pdist(X, metric='euclidean')
        distances_array = np.zeros((X.shape[0], X.shape[0]))
        upper_indicies = np.triu_indices(X.shape[0], 1)
        distances_array[upper_indicies] = distances
        cindex = calc_cindex_nbclust_implementation(distances_array, cluster_labels)
        cindicies_nbclust_implem.append(cindex)

        # Calculate Cindex from clusterSim implementation...
        cindex = calc_cindex_clusterSim_implementation(distances_array, cluster_labels)
        cindicies_clusterSim_implem.append(cindex)


    # Plot C index
    fig2 = plt.figure(2)
    ax = fig2.add_subplot(111)
    ax.plot(clusters, cindicies_py, label='Python Implementation')
    ax.plot(clusters, cindicies_nbclust_implem, label='NbClust Implementation')
    ax.plot(clusters, cindicies_clusterSim_implem, label='ClusterSim Implementation')
    ax.set_xlabel('Number of clusters')
    ax.set_ylabel('C Index')
    ax.set_title('C Index')
    ax.legend()

    return None





