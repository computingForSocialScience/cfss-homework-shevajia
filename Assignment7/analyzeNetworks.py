import pandas as pd
import networkx as nx
import numpy as np

def readEdgeList(filename):
    edgelist = pd.read_csv(filename, header = 0, names = ['artist', 'related artist'])
    if len(edgelist.columns) > 2:
        print "Warning: there are more than two columns in the file."
        edgelist = pd.read_csv(filename, 
                               header = 0,
                               names = ['artist', 'related artist'],
                               usecols = [0,1])
    else:
        pass
    return edgelist

def degree(edgeList, in_or_out):
    if in_or_out == 'in':
        degrees = edgeList['related artist'].value_counts()
    elif in_or_out == 'out':
        degrees = edgeList['artist'].value_counts()
    return degrees

def combineEdgeLists(edgeList1, edgeList2):
    combinedEdgeList = pd.concat([edgeList1, edgeList2]).drop_duplicates()
    return combinedEdgeList

def pandasToNetworkX(edgeList):
    g = nx.DiGraph()
    for artist1, artist2 in edgeList.to_records(index=False):
        g.add_edge(artist1,artist2)
    return g

def randomCentralNode(inputDiGraph):
    eigenvector_centrality = nx.eigenvector_centrality(inputDiGraph)
    denomenator = sum(dict.values(eigenvector_centrality))
    normalized_eigenvector_centrality = {key: (eigenvector_centrality[key]/denomenator) for key in dict.keys(eigenvector_centrality)}
    ramdonCentralNode = np.random.choice(normalized_eigenvector_centrality.keys(), p = normalized_eigenvector_centrality.values())
    return ramdonCentralNode