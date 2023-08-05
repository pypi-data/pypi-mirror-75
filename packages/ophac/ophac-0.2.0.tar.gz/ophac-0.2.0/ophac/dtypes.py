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
Data structures for AHC of posets.
'''

def _getLogger(thing):
    import logging
    if isinstance(thing,str):
        return logging.getLogger(__name__ + '.' + thing)
    else:
        return logging.getLogger(__name__ + '.' + thing.__name__)

def merge(thing, joins, *args, **kwargs):
    if not isinstance(thing, DistMatrix):
        t = thing
        for i,j in joins:
            t = t.merge(i,j, *args, **kwargs)
        return t
    else:
        lnk = getLinkage(kwargs['L'])
        t = thing
        for i,j in joins:
            t = lnk(i,j,t)
        return t

class Partition:

    log = _getLogger("Partition")

    def __init__(self, data=None, n=None):
        assert (data is None) != (n is None)
        if data:
            assert len(data) > -1 # Sanity check...
            self.data = data
        else:
            self.data = [[i] for i in range(n)]

        self.log.debug('Created: %s', self.data)

    def merge(self,a,b):
        assert a < b
        data        = [None]*(len(self.data) - 1)
        data[:a]    = self.data[:a]
        data[a]     = sorted(self.data[a] + self.data[b])
        data[a+1:b] = self.data[a+1:b]
        data[b:]    = self.data[b+1:]
        return Partition(data=data)

    def __contains__(self,x):
        return x in self.data

    def __getitem__(self,i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

    def __eq__(self,other):
        if not isinstance(other, Partition):
            return False
        return self.data == other.data

    def __ne__(self,other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple([tuple(x) for x in self.data]))

    def __str__(self):
        return 'Partition(%s)' % str(self.data)

    def __repr__(self):
        return str(self)
    

class Quivers:
    def __init__(self, quivers=None, n=None, relation=None):
        assert ((quivers is None) != (n is None)) \
            and ((n is None) == (relation is None))
        
        if quivers:
            if isinstance(quivers, Quivers):
                self.quivers = [list(q) for q in quivers.quivers]
            else:
                assert len(quivers) > -1 # Sanity again...
                self.quivers = [sorted(set(q)) for q in quivers]
        else:
            import bisect
            self.quivers = [[] for _ in range(n)]
            for a,b in relation:
                i = bisect.bisect_left(self.quivers[a], b)
                self.quivers[a].insert(i,b)

        self.transitivelyClosed = False

    def merge(self,a,b):
        assert a < b
        quivers = [list(x) for x in self.quivers]
        quivers[a].extend(quivers[b])
        quivers[a] = sorted(set(quivers[a]))
        del quivers[b]

        # Reduce pointers beyond the deletion pont,
        # and redirect pointers to the deleted vertex by pointers
        # to the merged vertex
        for quiver in quivers:
            for i in range(len(quiver)):
                if quiver[i] == b:
                    quiver[i] = a
                elif quiver[i] > b:
                    quiver[i] -= 1
               
        result = Quivers(quivers=quivers)
        return result

    def canMerge(self,a,b):
        return not (self.hasPath(a,b) or self.hasPath(b,a))

    def hasPath(self,a,b,visited=None):
        if self.transitivelyClosed:
            import bisect
            i = bisect.bisect_left(self.quivers[a],b)
            return i < len(self.quivers[a]) and self.quivers[a][i] == b
        else:
            if visited is None:
                visited = set()

            visited.add(a)

            if a == b:
                return True
            for c in self.quivers[a]:
                if not c in visited:
                    if self.hasPath(c,b,visited):
                        return True

            return False

    def hasCycle(self, n=None, visiting=None, visited=None):
        if self.transitivelyClosed:
            import bisect
            for n in range(len(self)):
                i = bisect.bisect_left(self.quivers[n],n)
                if i < len(self.quivers[n]) and self.quivers[n][i] == n:
                    return True
            return False
        else:
            assert (n is None) == (visiting is None) == (visited is None)
            if n is None:
                visited  = [False]*len(self)
                visiting = [False]*len(self)
                for n in range(len(self.quivers)):
                    if not visited[n]:
                        if self.hasCycle(n,visiting,visited):
                            return True
                return False
            else:
                if visiting[n]:
                    return True

                visiting[n] = True
                for ch in self.quivers[n]:
                    if not visited[ch] and self.hasCycle(ch,visiting,visited):
                        return True

                visited[n]  = True
                visiting[n] = False
                return False

    def transitiveClosure(self,inPlace=False):
        '''
        Produces a Quivers that is transitively closed.
        If inPlace is True, this object is changed. Otherwise,
        a new Quivers object is returned.
        '''

        def _fillInDescendants(n, visited, visiting, data):
            if visiting[n]:
                raise Exception('Cycle in Quivers object detected %d -> %d' % (n,n))

            if visited[n]:
                return data[n]

            visiting[n] = True
            result      = set()
            for d in self.quivers[n]:
                result.add(d)
                if not visited[d]:
                    result.update(_fillInDescendants(d,visited,visiting,data))
                else:
                    result.update(data[d])
                
            visited[n]  = True
            visiting[n] = False
            data[n]     = sorted(result)
            return result
        

        N        = len(self)
        data     = [[]]*N
        visited  = [False]*N
        visiting = [False]*N
        for i in range(N):
            _fillInDescendants(i,visited,visiting,data)

        if inPlace:
            self.quivers = data
            self.transitivelyClosed = True
            return self
        else:
            result = Quivers(quivers=data)
            result.transitivelyClosed = True
            return result

    def connectedComponents(self):
        '''
        Returns a list of node sets, one for each connected
        component.
        '''
        visited = set()
        result  = []
        revMap  = self._genRevMap()
        for n in range(len(self)):
            if n in visited:
                continue
            # No CC containing n:
            cc = set()
            self._addToCC(cc,n,self.quivers,revMap)
            visited.update(cc)
            result.append(cc)

        return result

    def _addToCC(self,cc,n,fwd,rev):
        cc.add(n)
        for m in rev[n].union(fwd[n]):
            if not m in cc:
                self._addToCC(cc,m,fwd,rev)
        
    def _genRevMap(self):
        import collections
        revMap = collections.defaultdict(set)
        for p in range(len(self)):
            subs = self[p]
            for s in subs:
                revMap[s].add(p)
        return [revMap.get(n,set()) for n in range(len(self))]


    def degrees(self):
        '''
        Returns a sequence of pairs, one pair for every
        element, containing the elements' in- and out degree.
        '''
        Q = self
        if not self.transitivelyClosed:
            Q = self.transitiveClosure(inPlace=False)

        outs = [len(x) for x in Q.quivers]
        ins  = [0]*len(Q)
        for q in Q.quivers:
            for to in q:
                ins[to] += 1
                
        return zip(ins,outs)

    def __getitem__(self,i):
        return self.quivers[i]

    def __eq__(self,other):
        if not isinstance(other, Quivers):
            return False
        return self.quivers == other.quivers
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple([tuple(x) for x in self.quivers]))

    def __len__(self):
        return len(self.quivers)

    def __str__(self):
        return 'Quivers(%s)' % str(self.quivers)

    def __repr__(self):
        return str(self)

class DistMatrix:

    log = _getLogger('DistMatrix')
    
    def __init__(self, dists):
        from math import sqrt,floor
        if isinstance(dists, DistMatrix):
            self.dists   = list(dists.dists)
            self.n       = dists.n
        else:
            self.dists = dists
            n = 0.5 + 0.5 * sqrt(1 + 8*len(dists))
            if n != floor(n):
                raise AssertionError('n=%f for len(dists)=%d.' % (n,len(dists)))
            self.n = int(n)

        self.shape = [self.n,self.n]

        self.log.debug('Created %dx%d matrix.', self.n, self.n)

    @staticmethod
    def fromDissimilarity(N, dissimFunc):
        dists = []
        for i in range(N):
            for j in range(i+1,N):
                dists.append(dissimFunc(i,j))
        return DistMatrix(dists)

    def toNumpyArray(self):
        import numpy as np
        A = np.zeros((self.n,self.n), dtype=float)
        for i in range(0,self.n):
            for j in range(i+1,self.n):
                k = self.toLinearIndex(i,j)
                x = self.dists[k]
                A[i,j] = x
                A[j,i] = x

        return A

    def _getLinkage(self,name):
        if name == 'single':
            result = lambda a,b : min(a,b)
            result.__name__ = name
            return result
        if name == 'complete':
            result = lambda a,b : max(a,b)
            result.__name__ = name
            return result

        raise ValueError(str(name) + ' is not a valid linkage strategy.')

    def __getitem__(self,*args):
        if type(args[0]) is tuple:
            if args[0][0] < args[0][1]:
                a = args[0][0]
                b = args[0][1]
            else:
                a = args[0][1]
                b = args[0][0]

            if a == b:
                return 0.0

            return self.dists[self.toLinearIndex(a,b)]
        else:
            return self.dists[args[0]]

    def __setitem__(self,*args):
        if type(args[0]) is tuple:
            if args[0][0] < args[0][1]:
                a = args[0][0]
                b = args[0][1]
            else:
                a = args[0][1]
                b = args[0][0]
            x = args[1]

            if a == b:
                assert x == 0.0
                return self

            i = self.toLinearIndex(a,b)
            self.dists[i] = x
            return self
        else:
            self.dists[args[0]] = args[1]
            return self

    def spectrum(self,includeZero=False):
        result = sorted(set(self.dists))
        if includeZero:
            result.insert(0,0)
        return result

    def max(self):
        return max(self.dists)

    def min(self):
        return min(self.dists)

    def norm(self,ord=2):
        '''
        Returns the L_{ord,ord} norm of this dissimilarity as if it
        were an NxN matrix.
        '''
        import numpy.linalg as npl
        scale = 2.0**(1/float(ord))
        return scale * npl.norm(self.dists,ord=ord)

    def __add__(self,other):
        assert isinstance(other, DistMatrix)
        assert other.n == self.n
        data = [other.dists[i] + self.dists[i] for i in range(len(self.dists))]
        return DistMatrix(data)

    def __sub__(self,other):
        assert isinstance(other, DistMatrix)
        assert other.n == self.n
        data = [self.dists[i] - other.dists[i] for i in range(len(self.dists))]
        return DistMatrix(data)

    def __mul__(self,other):
        if isinstance(other,DistMatrix):
            raise Exception('Matrix multiplication not supported.')
        else:
            data = list(self.dists)
            for i in range(len(data)):
                data[i] = data[i]*other

            return DistMatrix(data)

    def __rmul__(self,other):
        return self*other

    def __div__(self,other):
        return self * (1.0/other)

    def __truediv__(self,other):
        return self * (1.0/other)

    def getSortedIndexPairs(self):
        '''
        Returns a list of pairs on the form
        (d,(i,j)), where d is the dissimilarity d(i,j).
        The entries are sorted w.r.t. accending values of d.
        '''
        import itertools
        pairs   = itertools.combinations(range(self.n),2)
        entries = zip(self.dists, pairs)
        key     = lambda a : a[0]
        return sorted(entries, key=key)

    def getChunkedIndexPairs(self):
        '''
        Returns a list of Chunk objects, each having two attributes:
        dist:  the dissimilarity of the chunked pairs
        pairs: a list of index pair tuples (i,j)
        The list is sorted in accending order, so popping elements will
        provide the next chunk of minimal links.
        '''
        pairs = self.getSortedIndexPairs()
        if len(pairs) == 0:
            return []

        class Chunk:
            def __str__(self):
                return 'Chunk[%1.3f,%s]' % (self.dist, str(self.pairs))
            def __repr__(self):
                return str(self)
            def __len__(self):
                return len(self.pairs)

        result = []
        chunk  = Chunk()
        chunk.dist  = pairs[-1][0]
        chunk.pairs = [pairs[-1][1]]
        result.append(chunk)
        for pair in pairs[-2::-1]:
            if pair[0] == chunk.dist:
                chunk.pairs.append(pair[1])
            else:
                chunk = Chunk()
                chunk.dist  = pair[0]
                chunk.pairs = [pair[1]]
                result.append(chunk)
        
        return result

    def toLinearIndex(self,*args):
        assert len(args) == 2
        i = args[0]
        j = args[1]
        assert i < j
        
        N = self.n*(self.n-1)//2        # Half matrix size
        r = (self.n-i)*(self.n-i-1)//2  # Half matrix size including and below point
        h = j-i-1                       # Number of cells to the right of the diagonal
        return N - r + h


    def toMatrixIndex(self,k):
        from math import sqrt,floor
        n = self.n
        i = n - 2 - int(floor(sqrt(-8*k + 4*n*(n-1)-7)/2.0 - 0.5))
        j = k + i + 1 - n*(n-1)//2 + (n-i)*(n-i-1)//2
        assert i >= 0 and j >= 0
        return i,j

    def __eq__(self,other):
        if not hasattr(other, 'dists'):
            return NotImplemented
        
        return self.dists == other.dists

    def __ne__(self,other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __hash__(self):
        return hash(tuple(self.dists))

    def __str__(self):
        return 'DistMatrix(%s)' % str(self.dists)

    def __repr__(self):
        return str(self)

class BasicLinkage:

    log = _getLogger('BasicLinkage')

    def __init__(self, linkage):
        self.lnk = linkage
        self.log.debug('Created with linkage %s', self.lnk)

    def __call__(self,i,j,M):
        self.log.debug('%s-merging (%d,%d)', self.lnk, i, j)
        assert i < j
        linkage = self.lnk
        dists  = [None]*((M.n-1)*(M.n-2)//2)
        lindex = 0
        for s in range(M.n):
            if s == j:
                continue
            for t in range(s+1,M.n):
                if t == j:
                    continue
                elif s == i:
                    dists[lindex] = linkage(i,j,t,M)
                    lindex += 1
                elif t == i:
                    dists[lindex] = linkage(i,j,s,M)
                    lindex += 1
                else:
                    dists[lindex] = M[s,t]
                    lindex += 1

        return DistMatrix(dists=dists)


def getLinkage(L):
    if L == 'single':
        return BasicLinkage(SingleLinkage())
    elif L == 'complete':
        return BasicLinkage(CompleteLinkage())
    else:
        raise Error('Unknow linkage: "%d"' % L)

def SingleLinkage():
    class SL:
        def __call__(self,i,j,x,M):
            return min(M[i,x],M[j,x])
        def __repr__(self):
            return 'SL'
        def __str__(self):
            return 'SL'
    return SL()

def CompleteLinkage():
    class CL:
        def __call__(self,i,j,x,M):
            return max(M[i,x], M[j,x])
        def __repr__(self):
            return 'CL'
        def __str__(self):
            return 'CL'
    return CL()
    
def AverageLinkage(sizes):
    class AL:
        def __call__(self,i, j, x, M):
            '''
            (i,j) - to be merged
            x     - compute distance to
            M     - old distances
            '''
            a = sizes[i] * M[i,x]
            b = sizes[j] * M[j,x]
            s = sizes[i] + sizes[j]
            return float(a+b)/s

        def __repr__(self):
            return 'AL'
        def __str__(self):
            return 'AL'
    return AL()

class AgglomerativeClustering:
    '''
    Return type for clustering. 
    '''
    def __init__(self,joins=None,dists=None):
        assert (joins is None) == (dists is None)
        if joins:
            assert len(joins) == len(dists)
            self.joins = joins
            self.dists = dists
        else:
            self.joins = []
            self.dists = []

    def isMonotone(self, tolerance=0.0):
        for a,b in zip(self.dists[:-1], self.dists[1:]):
            if b - a < -tolerance:
                return False
        return True

    def __add__(self,other):
        '''
        Concatenation of agglomerative clustering results.
        '''
        joins = list(self.joins)
        joins.extend(other.joins)
        dists = list(self.dists)
        dists.extend(other.dists)
        return AgglomerativeClustering(joins,dists)

    def __eq__(self,other):
        if not isinstance(other, AgglomerativeClustering):
            return False
        return self.joins == other.joins and self.dists == other.dists

    def __ne__(self,other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((hash(tuple(self.joins)),
                     hash(tuple(self.dists))))

    def __getitem__(self, x):
        return AgglomerativeClustering(self.joins[x],self.dists[x])
            

    def __len__(self):
        assert len(self.dists) == len(self.joins)
        return len(self.dists)

    def __str__(self):
        return 'AgglomerativeClustering(joins=%s, dists=%s)' % \
            (str(self.joins), str(self.dists))

    def __repr__(self):
        return str(self)

# Alias
AC = AgglomerativeClustering
