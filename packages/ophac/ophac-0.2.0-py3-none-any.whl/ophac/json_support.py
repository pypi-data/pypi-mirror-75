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
Support for loading and writing ordered dissimilarity sets to and from file.

The python data structures used in the APIs in this module, are those found
in ophac.dtypes.*
'''

def _getLogger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)

class _IdMap:
    def __getitem__(self,x):
        return x

def loadDissimSpace(data=None, fname=None, keymap=_IdMap()):
    '''
    Extracts a strictly ordered dissimilarity space from the passed source.

    If data is not None:
    The dict-like must have the following contents:

    Either:
    data['N'] -> an int-like representing the number of elements in the set
    data['R'] -> array of pairs denoting order-relations in the set
    data['M'] -> array of N(N-1)/2 non-negative elements denoting the distances

    Or:
    data['Q'] -> quivers data structure (see ophac.dtypes.Quivers for details)
    data['M'] -> array of N(N-1)/2 non-negative elements denoting the distances

    If fname is not None:
    Then fname is the name of a json file that complies to the
    above description.

    Exactly one of data or fname must be specified.

    keymap - (optional) dict-like that maps either {'N','R','M'} or {'Q','M'} 
    to appropriate keys in "data".

    Returns a pair (M,Q) where Q is a ophac.dtypes.Quivers object, and M is a
    ophac.dtypes.DistMatrix object.
    '''
    import ophac.dtypes as clst
    
    assert (data is None) != (fname is None) # Exactly one must be non-None.

    if data is None:
        import json as js
        with open(fname, 'r') as inf:
            data = js.load(inf)

    Q = None
    if keymap['R'] in data:
        N = int(data[keymap['N']])
        Q = clst.Quivers(n=N,relation=data[keymap['R']])
    else:
        assert keymap['Q'] in data # Either 'Q' or 'R' must be specified
        Q = clst.Quivers(quivers=data[keymap['Q']])

    M = clst.DistMatrix(data[keymap['M']])

    assert len(Q) == M.n
    
    return (M,Q)

def dumpClustering(acs, Q=None, N=None, fname=None):
    '''
    Dumps the given clusterings to a dict.
    If a file name is specified, the result is written to file as well.
    acs   - List of AgglomerativeClustering objects
    Q     - [optional] The initial order relation
    N     - [optional] The number of elements in the space being clustered (if Q is not specified)
    fname - [optional] file to write to
    
    The json format is as follows:
    {
    "ACS":[{"joins"=[[i,j],...],
            "dists"=[d_i,...]},
            ...],
    "Q":[[..],...],
    }

    returns a dict corresponding to the json format
    '''
    import ophac.dtypes as dt
    log = _getLogger(dumpClustering)

    if Q is None:
        Q = dt.Quivers(n=N,relation=[])
    data = {
        'ACS':[{'joins':ac.joins,'dists':ac.dists} for ac in acs],
        'Q':Q.quivers
        }
    
    if fname is not None:
        import json
        log.info('Writing to file %s', fname)
        with open(fname, 'w') as outf:
            json.dump(data, outf, indent=3)

    return data
