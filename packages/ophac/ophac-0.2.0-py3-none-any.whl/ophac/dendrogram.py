# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright 2020 Daniel Bakkelund
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

'''
Plotting support for partial dendrograms
'''

def plot(ac,N,*args,**kwargs):
    '''
    Plots the (partial) dendrogram using 
    scipy.cluster.hierarchy.dendrogram.
    Note: the caller must call matplotlib.pyplot.show()
    after calling this method for the actual window to show up.
    ac - Thea AgglomerativeClustering to display
    N  - The number of elements in the clustering
    args and kwargs : additional parameters passed on to ...show(...)
    '''
    import scipy.cluster.hierarchy as sch

    Z,cutDist = _toLinkageMatrix(ac,N)

    myargs = {
        'color_threshold' : cutDist,
        'above_threshold_color' : 'none',
        }

    myargs.update(kwargs)
    
    sch.dendrogram(Z=Z, *args, **myargs)

def _toLinkageMatrix(ac,N,eps=1e-12):
    '''
    Generates a linkage matrix that is suitable for plotting
    of dendrograms through scipy.cluster.hierarchy.dendrogram
    ac - AgglomerativeClustering object returned by HC.
    N  - Number of elements being clustered
    returns (Z,L,Ncc)
    Z       - The linkage matrix
    cutDist - The distance used to render the 'fake' links to complete
              the matrix.
    '''
    import numpy as np

    L = len(ac)
    Z = np.zeros((N-1,4))
    
    # Mapping from cluster index in agg to cluster sequential index
    idxMap = list(range(N))

    # Sequential index of the next cluster to be formed
    idx = N  

    # Cluster sizes in ac indices
    sizes = [1]*N

    # Compute the partial diagram merges
    for i in range(L):
        join = ac.joins[i]
        dist = ac.dists[i]

        a,b    = (idxMap[join[0]], idxMap[join[1]])
        size   = _mergeSizes(*join,sizes=sizes)
        Z[i,:] = [a,b,dist,size]

        _updateIndices(*join,new=idx,idxMap=idxMap)
        idx += 1

    # Merge the rest at the last distance level plus an epsilon
    # to avoid over-writing lines
    dist = Z[L-1,2] + 1
    for i in range(L,N-1):
        join   = (len(sizes)-2,len(sizes)-1)
        a,b    = (idxMap[join[0]], idxMap[join[1]])
        size   = _mergeSizes(*join,sizes=sizes)
        Z[i,:] = [a,b,dist,size]
        _updateIndices(*join,new=idx,idxMap=idxMap)
        idx += 1

    return (Z,ac.dists[-1] + eps)

def _updateIndices(a,b,new,idxMap):
    idxMap[a] = new
    for i in range(b,len(idxMap)-1):
        idxMap[i] = idxMap[i+1]

    del idxMap[-1]

def _mergeSizes(a,b,sizes):
    assert a < b
    sizes[a] += sizes[b]
    for i in range(b,len(sizes)-1):
        sizes[i] = sizes[i+1]

    del sizes[-1]

    return sizes[a]
