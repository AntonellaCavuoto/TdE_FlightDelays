from model.model import Model
import networkx as nx
myModel = Model()
myModel.buildGraph(5)

v0 = myModel.getAllNodes()[0]
connessa = list(nx.node_connected_component(myModel._graph, v0))
v1 = connessa[10]

bestPath, bestObjFun = myModel.getCamminoOttimo(v0, v1, 4)

print(f"Cammino ottimo tra {v0} e {v1} ha peso = {bestObjFun}")
print(*bestPath, sep="\n")
