import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import pylab as graphplot
import snap
from collections import Counter

def getval(S,interest):
	for item in S:
		if S.GetDat(item) == interest:
			return item

followerFile = pd.read_csv("follows.csv") 
interestFile = pd.read_csv("interests.csv")
#followerFile = followerFile1.iloc[:50,:] 

# number of users in the follower system.Create a list from all the available customer lists i.e. follower list,folowee list and the ids in interest list
ListOfAllUsers = list()
ListOfAllUsers.append(followerFile.iloc[:,0].values)
ListOfAllUsers.append(followerFile.iloc[:,1].values)
ListOfAllUsers.append(interestFile.iloc[:,0].values)
ListOfAllUsers = [item for sublist in ListOfAllUsers for item in sublist]
ListOfUsers = list()
ListOfUsers.append([k for k in set(ListOfAllUsers)])
Interests = list()
Interests.append([k for k in set(interestFile.iloc[:,1])])

	#ListOfUsers=list((set(ListOfAllUsers)))[1]
print 'Number of users in the social network are : ',len(set(ListOfAllUsers))
print 'Number of followees in the social network are :',len(set(followerFile.iloc[:,1].values))

print 'Number of interest categories in the social network database : ',len(set(interestFile.iloc[:,1].values))

followerFile = followerFile.sort_values(by=['follower_id'],ascending = True)
G1 = snap.TNGraph.New()
for i in range(len(ListOfUsers[0])):
	G1.AddNode(ListOfUsers[0][i])
for i in range(len(followerFile)):
	G1.AddEdge(followerFile.iloc[i,0],followerFile.iloc[i,1])

S = snap.TIntStrH()
GI = snap.TNGraph.New()
for i in range(len(ListOfUsers[0])):
	GI.AddNode(ListOfUsers[0][i])
print "interests= ", len(Interests[0])
for i in range(len(Interests[0])):
	S.AddDat((10000+i),Interests[0][i])
	GI.AddNode(10000+i)
for i in range(len(followerFile)):
	GI.AddEdge(interestFile.iloc[i,0],getval(S,interestFile.iloc[i,1]))

snap.DrawGViz(G1, snap.gvlDot, "reco.png", "Network Diagram",True, snap.TIntStrH())


snap.PlotInDegDistr(G1, "Indeg", "Directed graph - in-degree")
snap.PlotOutDegDistr(G1, "Outdeg", "Directed graph - out-degree")

# vector of pairs of integers (size, count)
ComponentDist = snap.TIntPrV()
# get distribution of connected components (component size, count)
snap.GetWccSzCnt(G1, ComponentDist)
for comp in ComponentDist:
    print "Size: %d - Number of Components: %d" % (comp.GetVal1(), comp.GetVal2())
Count = snap.CntUniqDirEdges(G1)
print "Directed Graph: Count of unique directed edges is %d" % Count

# get degree distribution pairs (degree, count)
snap.GetOutDegCnt(G1, ComponentDist)
print "Degree Distribution Pairs-"
xval = []
yval = []
for item in ComponentDist:
    print "%d nodes with out-degree %d" % (item.GetVal2(), item.GetVal1())
    xval.append(item.GetVal1())
    yval.append(item.GetVal2())
bins = np.arange(len(yval))
plt.hist(yval,xval,alpha=0.5,label='Nodes with Out degree')
plt.title('Distribution of Out degree by Nodes')
plt.xlabel('Out degree')
plt.ylabel('Number of Nodes')
plt.xticks(bins,rotation = 90)
plt.show()

# vector of floats
EigV = snap.TFltV()
# get first eigenvector of graph adjacency matrix
snap.GetEigVec(snap.ConvertGraph(snap.PUNGraph, G1), EigV)
print "Leading Eigen vector of adjacency graph-"
for Val in EigV:
    print Val

# get diameter of G8
print "Diameter of the network =",snap.GetBfsFullDiam(G1, 100)
TriadV = snap.TIntTrV()
# count the number of triads in G8, get the clustering coefficient of G8
print "Number of Triads in the network = ",
snap.GetTriads(G1, TriadV)
for triple in TriadV:
    print "For Node Id: ",triple.Val1(),",Number of open Triads are: ", triple.Val2(),", Number of closed Triads are: ", triple.Val3()

print "Clustering Co-efficient of the network =",snap.GetClustCf(G1)


# get a subgraph induced on nodes {0,1,2,3,4,5}
SubG = snap.GetSubGraph(G1, snap.TIntV.GetV(2,4,6,8,10,12,14,16,20))
snap.DrawGViz(SubG, snap.gvlDot, "recosub.png", "Partial Network Diagram",True, snap.TIntStrH())
# get 3-core of G

# get largest weakly connected component
WccG = snap.GetMxWcc(G1)
snap.DrawGViz(WccG, snap.gvlDot, "weakconn.png", "largest weakly connected component",True, snap.TIntStrH())



Core3 = snap.GetKCore(SubG, 3)
snap.DrawGViz(Core3, snap.gvlDot, "recocore.png", "Partial Network Diagram",True, snap.TIntStrH())










