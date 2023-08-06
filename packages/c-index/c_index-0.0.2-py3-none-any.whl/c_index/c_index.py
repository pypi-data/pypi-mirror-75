# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:01:32 2020

Calculate the CIndex for some hypothetical data

Cindex =
Sw − Smin
Smax − Smin , Smin ?= Smax, Cindex ∈ (0, 1), (6)

Smin = is the sum of the Nw smallest distances between all the pairs of points
in the entire data set (there are Nt such pairs);

Smax = is the sum of the Nw largest distances between all the pairs of points
in the entire data set.

@author: z003vrzk
"""

# Python imports

# Third party imports
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist


#%%

"""
##### Here is the Nb-Clust implementation of the CIndex #####
See https://cran.r-project.org/web/packages/NbClust/index.html
Note these two lines (R Code) :
    Dmin = min(v_min)
    Dmax = max(v_max)
    result <- (DU - r * Dmin)/(Dmax * r - Dmin * r)

Indice.cindex <- function (d, cl)
{
    d <- data.matrix(d)
    DU <- 0
    r <- 0
    v_max <- array(1, max(cl))
    v_min <- array(1, max(cl))
    for (i in 1:max(cl)) {
        n <- sum(cl == i)

        if (n > 1) {
            t <- d[cl == i, cl == i]
            DU = DU + sum(t)/2
            v_max[i] = max(t)

            if (sum(t == 0) == n)
                v_min[i] <- min(t[t != 0])

            else v_min[i] <- 0
            r <- r + n * (n - 1)/2
        }
    }

    Dmin = min(v_min)
    Dmax = max(v_max)
    if (Dmin == Dmax)
        result <- NA
    else result <- (DU - r * Dmin)/(Dmax * r - Dmin * r)
    result

}


##### Here is the ClusterSim implementation of the CIndex #####
See https://rdrr.io/cran/clusterSim/src/R/index.C.r
Note these two lines :
	Dmin=sum(sort(ddist)[1:r])
	Dmax=sum(sort(ddist,decreasing = T)[1:r])
They include the whole distance array, which includes all permutations of
distances between points (instead of combinations). This means the high
end and low end are double counted? I dont think that is the correct way to
calculate C Index


index.C<-function(d,cl)
{
  ddist<-d
	d<-data.matrix(d)
	DU<-0
	r<-0
	for (i in 1:max(cl))
	{
	  t<-d[cl==i,cl==i]
		n<-sum(cl==i)
		if (n>1)
		{
			DU=DU+sum(t)/2
		}
		r<-r+n*(n-1)/2
	}
	Dmin=sum(sort(ddist)[1:r])
	Dmax=sum(sort(ddist,decreasing = T)[1:r])
	if(Dmin==Dmax)
		result<-NA
	else
		result<-(DU-Dmin)/(Dmax-Dmin)
	result
}

"""


# Python implementation of CIndex equivalent to NbClust package
def calc_cindex_nbclust_implementation(distances_array, cluster_labels):
    '''
    inputs
    -------
    distances : (np.array) of shape [m,n] where m==n and are the number of
        data points being clustered
    cluster_labels : (np.array) of shape [m,] Cluster labels related to
        distances. cluster_labels must be the same length as distances.
        Each element of cluster_labels represents cluster [i] belonging
        to distances[i]

    Example Usage

    # Data
    xs = np.array([[1,2,1.5,1.75,1.33,0.88],
                  [5,5.5,4.88,6.33,5.01,4.95]]) # Cluster 1, 2 x values
    ys = np.array([[8.9,8.5,7.89,8.25,8.85,8.29],
                  [1.25,1.14,1.85,0.85,0.79,0.96]]) # Cluster 1,2 y values
    X = np.stack((xs.ravel(),ys.ravel()), axis=1)

    distance_pointwise = pdist(X, metric='euclidean')
    upper_indicies = np.triu_indices(X.shape[0], 1)
    distance_array = np.zeros((X.shape[0], X.shape[0]))
    distance_array[upper_indicies] = distance_pointwise

    # Cluster data points
    n_clusters=2
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    labels = kmeans.labels_

    # Calculate C Index
    py_result = cindex_nbclust(distance_array, labels)
    '''

    distances_array = np.array(distances_array)
    validate_distance_input(distances_array)
    # Sum of within-cluster distances
    Sw = 0
    # Total number of pairs of observations belonging to the same cluster
    intra_pairs = 0
    # Set of labels
    unique_labels = set(cluster_labels)

    v_max = []
    v_min = []

    for idx, label in enumerate(unique_labels):
        # Number of points belonging to cluster i
        n_points = np.sum(cluster_labels == label, axis=0)

        if n_points > 1:
            # Distances within cluster i
            distances_i = distances_array[np.ix_(cluster_labels==label, cluster_labels==label)]

            # Sum of within cluster distances
            Sw = Sw + np.sum(distances_i)

            # Max distance within cluster i
            v_max.append(np.max(distances_i))
            v_min.append(np.min(distances_i[distances_i != 0]))

            # Total number of pairs of observations belonging to the same cluster
            # N_w = \sum_{k=1}^{q} \frac{n_k (n_k-1)}{2}
            intra_pairs = intra_pairs + n_points * (n_points - 1) / 2

    Dmin = min(v_min) # Minimum distance
    Dmax = max(v_max) # Maximum distance
    if Dmin == Dmax:
        result = None
    else:
        result = (Sw - intra_pairs * Dmin) / (Dmax * intra_pairs - Dmin * intra_pairs)

    return result



# Python implementation of CIndex equivalent to clusterSim
def calc_cindex_clusterSim_implementation(distances_array, cluster_labels):
    '''
    inputs
    -------
    distances : (np.array) of shape [m,n] where m==n and are the number of
        data points being clustered
    cluster_labels : (np.array) of shape [m,] Cluster labels related to
        distances. cluster_labels must be the same length as distances.
        Each element of cluster_labels represents cluster [i] belonging
        to distances[i]

    Example Usage

    # Data
    xs = np.array([[1,2,1.5,1.75,1.33,0.88],
                  [5,5.5,4.88,6.33,5.01,4.95]]) # Cluster 1, 2 x values
    ys = np.array([[8.9,8.5,7.89,8.25,8.85,8.29],
                  [1.25,1.14,1.85,0.85,0.79,0.96]]) # Cluster 1,2 y values
    X = np.stack((xs.ravel(),ys.ravel()), axis=1)

    distance_pointwise = pdist(X, metric='euclidean')
    upper_indicies = np.triu_indices(X.shape[0], 1)
    distance_array = np.zeros((X.shape[0], X.shape[0]))
    distance_array[upper_indicies] = distance_pointwise

    # Cluster data points
    n_clusters=2
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    labels = kmeans.labels_

    # Calculate C Index
    py_result = cindex_nbclust(distance_array, labels)
    '''

    distances_array = np.array(distances_array)
    validate_distance_input(distances_array)
    # Sum of within-cluster distances
    Sw = 0
    # Total number of pairs of observations belonging to the same cluster
    intra_pairs = 0
    # Set of labels
    unique_labels = set(cluster_labels)

    for idx, label in enumerate(unique_labels):
        # Number of points belonging to cluster i
        n_points = np.sum(cluster_labels == label, axis=0)

        if n_points > 1:
            # Distances within cluster i
            distances_i = distances_array[np.ix_(cluster_labels==label, cluster_labels==label)]

            # Sum of within cluster distances
            Sw = Sw + np.sum(distances_i)

            # Total number of pairs of observations belonging to the same cluster
            # N_w = \sum_{k=1}^{q} \frac{n_k (n_k-1)}{2}
            intra_pairs = intra_pairs + n_points * (n_points - 1) / 2

    # Flatten distances to sort them
    flat_dist = distances_array[distances_array != 0].ravel()
    """The ClusterSim packagage incldue the whole distance array,
    which incldues all permutations of
    distances between points (instead of combinations).
    This means the high end and low end are double counted?
    I dont think that is the correct way to
    calculate C Index"""
    duplicate_distances = np.concatenate((flat_dist, flat_dist))
    indices = np.argsort(duplicate_distances)
    Dmin = np.sum(duplicate_distances[indices[:int(intra_pairs)]])
    Dmax = np.sum(duplicate_distances[indices[-int(intra_pairs):]])
    if Dmin == Dmax:
        result = None
    else:
        result = (Sw - Dmin) / (Dmax - Dmin)

    return result



def calc_c_index(X, cluster_labels, clusterer='kmeans', distance='euclidean'):
    """Calculate CIndex
    inputs
    -------
    X : (np.ndarray) an (n x m) array where n is the number of examples to cluster
        and m is the feature space of examples
    cluster_labels : (np.array) of cluster labels, each cluster_labels[i]
        related to X[i]
        ideally integer type
    output
    -------
    cindex : (float)"""



    # Total Number of pairs of observations belonging to same cluster
    Nw = calc_Nw(cluster_labels)

    # Distances between all pairs of points in dataset
    distances = pdist(X, metric='euclidean')

    # Sum of within-cluster distances
    Sw = calc_sw(X, cluster_labels)

    # Sum of Nw smallest distances between all poirs of points
    # Sum of Nw largest distances between all pairs of points
    Smin, Smax = calc_smin_smax(distances, Nw)

    # Calculate CIndex
    cindex = (Sw - Smin) / (Smax - Smin)
    return cindex


def calc_smin_smax(distances, n_incluster_pairs):
    """Calculate Smin and Smax,
    Smax is the Sum of Nw largest distances between all pairs of points
    in the entire data set, and
    Smin is the Sum of Nw smallest distances between all pairs of points
    in the entire data set

    inputs
    -------
    distances : (np.ndarray) of shape [m,] where m is the pairwise distances
        between each point [i,k] being clustered. m is calculated as
        m = n_points * (n_points - 1) / 2 where n_points is the number of points
        in the entire dataset
    n_incluster_pairs : (int) Total number of pairs of observations belonging
        to the same cluster - See calc Nw
    outputs
    -------
    Smin, Smax : (float)
    """
    n_incluster_pairs = int(n_incluster_pairs) # For indexing
    indicies = np.argsort(distances)

    Smin = np.sum(distances[indicies[:n_incluster_pairs]])
    Smax = np.sum(distances[indicies[-n_incluster_pairs:]])
    return Smin, Smax


def calc_sw(X, cluster_labels):
    """Sum of within-cluster distances"""

    labels = np.array(cluster_labels)
    labels_set = set(cluster_labels)
    n_labels = len(labels_set)

    Sw = []
    for label in labels_set:
        # Loop through each cluster and calculate within cluster distance
        pairs = np.where(labels == label)
        pairs_distance = pdist(X[pairs[0]])
        within_cluster_distance = np.sum(pairs_distance, axis=0)
        Sw.append(within_cluster_distance)

    return np.sum(Sw)


def calc_Nw(cluster_labels):
    """Total number of pairs of observations belonging to the same cluster

    N_w = \sum_{k=1}^{q} \frac{n_k (n_k-1)}{2}
    inputs
    -------
    labels : (iterable) of labels"""

    cluster_labels = np.array(cluster_labels)
    labels_set = set(cluster_labels)
    n_labels = len(labels_set)

    Nw = []
    for label in labels_set:
        n_examples = np.sum(np.where(cluster_labels == label, 1, 0))
        n_cluster_pairs = n_examples * (n_examples - 1) / 2 # Combinations
        Nw.append(n_cluster_pairs)

    return int(np.sum(Nw))


def simple_cluster_points(X, n_clusters, clusterer='kmeans'):
    """Cluster data points
    inputs
    -------
    X : (np.array) of shape [m,n] where m is the number of examples/instances
    to be clustered, and n is the feature space of each example
    clusterer : (str) of clustering algorithm. # TODO only kmeans is supported
        right now...
    outputs
    -------
    labels : (np.array) of cluster assignments"""

    # Cluster data points

    if clusterer == 'kmeans':
        kmeans = KMeans(n_clusters=n_clusters).fit(X)
        labels = kmeans.labels_
    else:
        msg='clusterer argument must be kmeans, got {}'
        raise ValueError(msg.format(clusterer))

    return labels


def validate_distance_input(X):
    """Validate distnace array dimensions
    inputs
    -------
    X : (np.array) of shape [m,m] where m is the number of points to calculate
    pair-wise distances between. X should be square and 2-dimensional
    Each element i,j should be distance between points i,j.
    X[i,j] = np.linalg.norm(points[i] - points[j])
    Lower indicies should be Zero! If lower indicies are non-zero then
    pair-wise distances will be double counted"""

    """The distance array should be square and rank 2"""
    msg='Distance Array should  be 2-dimensional, got {} dimensions'
    assert(np.ndim(X) == 2), msg.format(np.ndim(X))
    msg='Distance Array should be square, got {} shape'
    assert(X.shape[0] == X.shape[1]), msg.format(X.shape)

    """The array should be uppper triangular with zeros in the bottom
    diagonal AND along the diagonal"""
    lower_indicies = np.tril_indices(X.shape[0], 0)
    if not np.all(X[lower_indicies] == 0):
        msg=('All Lower Triangular elements of the distance array should be' +
             'Zero. got {} Non-Zero Indicies')
        non_zero = np.where(X[lower_indicies] != 0)
        raise ValueError(msg.format(X[non_zero]))

    return None


def pdist_array(X):
    """The R-package functions expect an upper triangular array of """

    distances = pdist(X, metric='euclidean')
    distances_array = np.zeros((X.shape[0], X.shape[0]))
    upper_indicies = np.triu_indices(X.shape[0], 1)
    distances_array[upper_indicies] = distances

    return distances_array