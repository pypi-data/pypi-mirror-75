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
Convert agglomerative clustering to ultrametric
'''

def ultrametric(ac, N=-1, eps=1e-12):
    '''
    ac  - The ophac.dtypes.AgglomerativeClustering object from HC
    N   - The number of elements being clustered. If ac represents a complete
          dendrogram, N need not be specified.
    eps - The ultrametric completion threshold. Defaults to 1e-12.
    returns a ophac.dtypes.DistMatrix representing an ultrametric over the N elements.
    '''
    import ophac.dtypes as clst
    import itertools

    for i in range(1,len(ac)):
        if not ac.dists[i-1] <= ac.dists[i]:
            raise AssertionError('Join distances not monotone:' + \
                                     ('d[%d]=%1.4f vs d[%d]=%1.4f. %s' % \
                                          (i-1,ac.dists[i-1],i,ac.dists[i],str(ac))))
    if N == -1:
        N = len(ac) + 1

    K = eps
    if len(ac) > 0:
        K = ac.dists[-1] + eps
    L = N*(N-1)//2
    P = clst.Partition(n=N)
    U = clst.DistMatrix([-1]*L)

    for (i,j),dist in zip(ac.joins,ac.dists):
        pi = P[i]
        pj = P[j]
        for a,b in itertools.product(pi,pj):
            if a < b:
                i1 = a
                i2 = b
            else:
                i1 = b
                i2 = a
            k = U.toLinearIndex(i1,i2)
            U.dists[k] = dist
        P = P.merge(i,j)

    basePartition = P

    while len(P) > 1:
        i,j = (len(P)-2,len(P)-1)
        for a,b in itertools.product(P[i],P[j]):
            if a < b:
                i1 = a
                i2 = b
            else:
                i1 = b
                i2 = a
            k = U.toLinearIndex(i1,i2)
            U.dists[k] = K
        P = P.merge(i,j)

    if U.max() > K: #no ultrametric...
        raise Exception('Will not produce a valid ultrametric: ' +
                        'Max ultrametric distance:%1.3f Given diam(ac) + eps = %1.3f. ' %\
                        (U.max(),K))

    if U.min() < 0: # Not all values are assigned
        raise Exception('Not all values are assigned.')

    U._basePartition = basePartition

    return U

def treeIdentical(U1,U2):
    '''
    Checks whether two ultrametrics represent the same
    hierarchical clustering in terms of partitions.
    '''
    Q1,_ = toPartitionChain(U1)
    Q2,_ = toPartitionChain(U2)
    return Q1 == Q2

def toPartitionChain(U):
    import numpy as np
    import ophac.dtypes as dt
    result = [dt.Partition(n=U.n)]
    desult = [0]
    for rho in U.spectrum(includeZero=False):
        Q = dt.Quivers([list() for _ in range(U.n)])
        for i in range(U.n):
            for j in range(i+1,U.n):
                if U[i,j] <= rho:
                    Q[i].append(j)

        Q.transitiveClosure(inPlace=True)
        done  = np.zeros((U.n,), dtype=bool)
        parts = []
        for i in range(U.n):
            if done[i]:
                continue
            else:
                part = list(Q[i])
                part.append(i)
                parts.append(sorted(part))
                for j in Q[i]:
                    done[j] = True
        
        result.append(dt.Partition(sorted(parts)))
        desult.append(rho)

    return (result,desult)

def extend(U0, P, rho, eps=1e-12):
    '''
    Extends the ultrametric by the partition P using
    the new dendrogram diameter rho.
    U0  - Ultrametric to be extended
    P   - New coarsest partition
    rho - New dendrogram diameter
    '''
    import numpy        as np
    import ophac.dtypes as dt
    
    dU0 = U0.max()
    U1  = clone(U0)
    for B in P:
        for i in range(len(B)):
            for j in range(i+1,len(B)):
                if U1[B[i],B[j]] == dU0:
                    U1[B[i],B[j]] = rho

    dists = np.array(U1.dists)
    I     = dists == dU0
    dists[I] = rho + eps

    U1 = dt.DistMatrix(list(dists))
    U1._basePartition = P
    return U1
    
    
def clone(U):
    '''
    Clones an ultrametric
    '''
    import ophac.dtypes as dt
    U2 = dt.DistMatrix(U)
    U2._basePartition = U._basePartition
    return U2
