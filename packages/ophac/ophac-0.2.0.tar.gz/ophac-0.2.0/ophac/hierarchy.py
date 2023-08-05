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

def linkage(D, G=None, L='complete', p=1, K=1.0e-12):
    '''
    Performs order preserving hierarchical clustering.
    
    D - Condensed dissimilarity measure. That is, for a set of N elements,
        D is a 1-dimensional array of N(N-1)/2 elements, corresponding to the
        upper half of the dissimilarity matrix laid out row-wise.
    G - Order relation given as a jagged 2D-array as follows:
        if A = G[i] is the i-th array in G, then, for each k in A this is 
        interpreted as i<k in the strict partial order. Default is None,
        meaning that the hierarchical clustering will be performed without
        regard to any order relation.
    L - Linkage function. One of 'single', 'complete' or 'average'.
        Default is 'complete'.
    p - Order of norm. A number greater or equal to 1. Defaults to 1.
    K - The epsilon of the ultrametric completion. Defaults to 1.0e-12.

    The method returns a list of ophac.dtypes.AgglomerativeClusering (AC) objects, 
    each object has two members: "dists" and "joins". The joins hold the order 
    of merges of the clustering, the the dists are the distances for the 
    different joins.

    The AC objects can be passed on as follows to obtain relevant information.
    In the following, ac is an AC object, N is the number of elements in the base set
    and K is the ultrametric completion distance (epsilon). Unless you have used
    a non-default value of K, this may be omitted.

    * To create the corresponding ultrametric:
    import ophaq.ultrametric as ult
    U = ult.ultrametric(ac, N, K)

    * To obtain the k-th partition
    import ophaq.dtypes as dt
    kthPartition = dt.merge(dt.Partition(n=N), ac.joins[:k])

    * To obtain the k-th induced order relation
    import ophac.dtypes as dt
    kthInducedOrder = dt.merge(dt.Quivers(G), ac.joins[:k])

    * To plot the corresponding (partial) dendrogram
    import matplotlib.pyplot as plt
    import ophaq.dendrogram  as dend
    fix,ax = plt.subplots(1,1)
    dend.plot(ac, N, ax=ax)
    plt.show()

    The  dend.plot(...) method uses scipy.cluster.hierarchy.dendrogram for 
    the plotting, and passes any additional arguments on to that method.
    '''
    import ophac.hac as hac
    import logging
    import time
    
    log = logging.getLogger(__name__ + '.' + linkage.__name__)
    M = hac.DistMatrix(D)
    log.info('Clustering %d elements.', M.n)
    Q = None
    if G is not None:
        Q = hac.Quivers(G)
        log.info('No order relation specified.')

    start    = time.time()
    hc       = hac.HAC(lnk=L, ord=p, dK=K)
    acs      = hc.generate(M,Q)
    duration = time.time() - start
    log.info('Produced %d equivalent clusterings in %1.3f s.', len(acs), duration)
    return acs
