# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 19:40:31 2020

@author: z003vrzk
"""

# Python imports

# Third party interface
import pandas as pd
import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import numpy2ri
numpy2ri.activate()

# Global declarations
_R_MODULE_NAME = 'clusterCrit'
if not rpy2.robjects.packages.isinstalled(_R_MODULE_NAME):
    raise ImportError('{} is not installed'.format(_R_MODULE_NAME))
clusterCrit = importr(_R_MODULE_NAME)  #Import the clusterCrit package

_R_MODULE_NAME = 'clusterSim'
if not rpy2.robjects.packages.isinstalled(_R_MODULE_NAME):
    raise ImportError('{} is not installed'.format(_R_MODULE_NAME))
clusterSim = importr(_R_MODULE_NAME)  #Import the clusterSim package

#%%

def calc_c_index_clusterCrit(X, cluster_labels):
    """Calculate the CIndex directly from ClusterCrit"""

    # Convert labels to R Integer Vector
    labels_vector = rpy2.robjects.vectors.IntVector(cluster_labels)

    # Convert data to R Matrix
    data_matrix = rpy2.robjects.Matrix(X)

    intIdx = clusterCrit.intCriteria(data_matrix, labels_vector, "C_index")
    intIdx[0]

    # Calculate all indices
    # intIdx = clusterCrit.intCriteria(data_matrix, labels_vector, "all")
    # res = r_listvector_to_df(intIdx)

    """intIdx is a nested list vector of float vectors
    [rpy2.robjects.vectors.FloatVector, rpy2.robjects.vectors.FloatVector,...]
    """
    data = {}
    for name, float_vector in intIdx.items():
        data[name] = float_vector.__getitem__(0)

    df = pd.DataFrame(data=data, index=[0])

    return df


def calc_c_index_clusterSim(X, cluster_labels):

    """Cluster_labels need to be ranging from 1 to maximum clusters
    The clusterSim sums over (1,max(cl)) so if labels are below 1
    or 0 then they are skipped"""
    msg='Cluster labels minimum label must be 1, got {}'
    assert min(cluster_labels) > 0, msg.format(min(cluster_labels))
    assert min(cluster_labels) == 1, msg.format(min(cluster_labels))

    # Convert labels to R Integer Vector
    labels_vector = rpy2.robjects.vectors.IntVector(cluster_labels)

    # Convert data to R Matrix
    data_matrix = rpy2.robjects.Matrix(X)

    # Distances - this depends on your call signature in clusterSim
    """Note, clusterSim uses different distance measurements based on the
    type of data you have (ratio, interval, ordinal, nominal)
    See DISTANCE MEASURE FOR ORDINAL DATA by Marek Walesiak for GDM distance
    metric

    Lets just use the good old fashioned euclidean distance metric for ratio
    data"""
    distances = clusterSim._ddist(X, distType='euclidean')
    # distances = clusterSim.dist_SM(X) # Other distance measure
    # distances = clusterSim.dist_GDM(X) # GDM Distance measure

    result = clusterSim.index_C(distances, cluster_labels)
    result2 = clusterSim.cluster_Sim(X, 1, minClusterNo=2,maxClusterNo=10,
                             icq="C")
    result2.names

    cindex = result[0]

    return cindex # Float element from R numeric FloatVector



def r_listvector_to_df(r_list):
    """Method for converting the NbClust ListVector to a pandas dataframe.
    This method is used when only one clustering index is returned from NbClust.
    Usually an R Matrix is returned, but if only a single index is selected
    then a ListVector is returned instead
    This method assumes the ListVector has named objects
    ['All.index', 'Best.nc', 'Best.partition'].

    inputs
    -------
    r_list : (rpy2.robjects.vectors.ListVector) R List vector with names
    ['All.index', 'Best.nc', 'Best.partition']
    All.index is a list of the calculated clustering index values
    Best.nc is a rpy2.robjects.vectors.FloatVector which should have 2 values
    [best_n_clusters, index_value].
    The names of All.index FloatVector names should be
    ['Number_clusters', 'Value_Index']

    Best.partition is the best number of clusters at each of the test
    number of clusters. For example, given min_nc=2, max_nc=5, Best.Partion
    would give the best number of clusters at each of 2,3,4,5 test number of
    clusters

    outputs
    --------
    df : (pandas.DataFrame) Best number of cluster dictionary with
        values :
        columns :
        index : """

    msg = 'r_list argument is not type rpy2.robjects.vectors.ListVector'
    assert isinstance(r_list, rpy2.robjects.vectors.ListVector), msg

    values = list(r_list)
    row_names = list(r_list.names)
    df = pd.DataFrame(data=values, index=[0], columns=row_names)
    return df