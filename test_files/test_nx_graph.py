import networkx as nx
from statistics import mean

Graphe = nx.read_edgelist("Human_HighQuality_nx.txt")
print(round(nx.degree(Graphe, nbunch="1433B_HUMAN")))
print(round(nx.clustering(Graphe,"1433B_HUMAN"),4))
print(round(nx.density(Graphe),8))
print(mean(nx.average_neighbor_degree(Graphe).values()))
print(mean(nx.average_degree_connectivity(Graphe)))