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
Module for generation of random data structures.
'''

def seed(s=None):
    import time
    import numpy.random as rnd
    import random
    if s is None:
        s = int(time.time())
        rnd.seed(s)
        random.seed(s)
    else:
        rnd.seed(s)
        random.seed(s)

def randomOrderedDissimSpace(N,p,t,d1=1,steps=[1]):
    '''
    Returns a strictly ordered set of N elements where the probability
    for (i,j) in R is p, and where the expected number of ties on
    each value level is t.

    return (M,Q)
    '''
    return (randomDissimilarity(N,t,d1,steps),
            randomOrder(N,p))

def randomOrder(N,p):
    '''
    Generates an order where the initial comparability
    matrix has exactly probability p for two elements to
    be comparable; i.e. sum(Q)/(N*(N-1)/2)=p.
    '''
    import ophac.dtypes as dt
    import numpy        as np
    from numpy.random import permutation as perm
    n      = int(round(N*(N-1)//2*p))
    q      = np.zeros((N*(N-1)//2,), dtype=int)
    q[0:n] = 1
    q      = perm(q)
    quivs  = [list() for _ in range(N)]
    M      = dt.DistMatrix(list(q))
    for i in range(N):
        for j in range(i+1,N):
            if M[i,j] == 1:
                quivs[i].append(j)

    return dt.Quivers(quivs)
    

def randomOrder_old(N,p):
    import ophac.dtypes as dt
    from random import random as rnd
    from numpy.random import permutation as permute

    assert 0 <= p and p <= 1

    perm = permute(range(N))
    q    = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i+1,N):
            if rnd() <= p:
                q[perm[i]].append(perm[j])

    return dt.Quivers(quivers=q)


def randomDissimilarity(N,n,d1=1,steps=[1],scale=0.0):
    '''
    N     - Number of elements
    n     - The expected value of number of equal values on each
            dendrogram level following a uniform distribution.
    d1    - The lowest value in the dissimilarity matrix.
            Default: 1
    steps - Array of increments to be cycled
            Default: [1]
    scale - Standard deviaton of normal noise to add to the distances.
            Default: 0.0
    '''
    from ophac.dtypes     import DistMatrix
    from numpy.random     import random      as rnd
    from numpy.random     import permutation as perm
    from numpy.random     import normal      as noise
    import itertools

    M = N*(N-1)//2
    indices = list(range(0,M))
    result  = [-1]*M
    
    incs = itertools.cycle(steps)
    val  = d1
    while len(indices) > 0:
        m = max(1,int(rnd()*n*2))
        k = min(m,M)
        L = min(len(indices),k)
        I = perm(len(indices))[:L]
        I = sorted(I, reverse=True)
        for i in I:
            result[indices[i]] = val + noise(scale=scale)
            del indices[i]
        val += next(incs)

    return DistMatrix(result)

def plantedPartition(Q,N,p,dEq=0.1,dDiff=1.0,s=0.01):
    '''
    Produces planted partitions by duplicating the ordered
    set Q times N. Two equivalent elements are then registered
    as equivalent with probability p by specifying their
    dissimilarity by dEq. Otherwise, and for all non-equivalent
    elements, they are registered with dissimilarity dDiff.
    Finally, Gaussian noise is added to the dissimilarity measure
    with mean 0 and variance s.

    Q     - Base ordered set.
    N     - Number of parallel datasets. 
            Must be >= 1.
    p     - Probability for equivalent elements to be marked so. 
            Must be 0 <= p <= 1.
    dEq   - Dissimilarity for elements marked as equivalent. 
            Must be >0.
    dDiff - Dissinilarity for all other elements. 
            Must be >dEq.
    s     - Variance of Gaussian noise to add. 
            Must be >=0.

    Returns M,Q2,P where 
    M  is the produced dissimilarity measure,
    Q' is the corresponding partial order, and
    P  is the planted partition.
    '''
    import numpy as np
    from numpy.random import random as rnd
    from numpy.random import normal 
    from itertools import combinations
    import ophac.dtypes             as dt
    
    M       = N*len(Q) # num elts in produced poset
    quivers = []
    planted = [list() for _ in range(len(Q))]
    dists   = dt.DistMatrix([dDiff]*(M*(M-1)//2))

    # Concatenate all quivers into one
    # and create the planted partition
    for n in range(N):
        dn = n*len(Q)
        
        assert len(quivers) == dn
        for quiver in Q.quivers:
            quivers.append([k+dn for k in quiver])

        for k in range(len(Q)):
            planted[k].append(k+dn)
            
    Q2 = dt.Quivers(quivers)
    assert len(Q2) == M

    # Assign dissimilarities
    for plant in planted:
        for i,j in combinations(plant, 2):
            if rnd() <= p:
                dists[i,j] = dEq

    # Add some noise
    if s > 0:
        noise = np.abs(normal(loc=0, scale=s, size=len(dists.dists)))
        dists = dt.DistMatrix(noise + dists.dists)
                
    return dists,Q2,dt.Partition(planted)
