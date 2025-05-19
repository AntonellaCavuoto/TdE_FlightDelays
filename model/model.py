import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestObjFunction = 0
        self._bestPath = []
        self._graph = nx.Graph()
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def getCamminoOttimo(self, v0, v1, t):  # t = numero massimo tratte
        self._bestPath = []  # dove carico percorso migliore
        self._bestObjFunction = 0

        parziale = [v0]  # lista di aeroporti visualizzati

        self._ricorsione(parziale, v1, t)

        return self._bestPath, self._bestObjFunction

    def _ricorsione(self, parziale, v1, t):
        # verificare se parziale è una possibile soluzione
        # verificare se parziale è meglio del best
        # esco
        if parziale[-1] == v1:  # ultimo aeroporto in parziale è l'aeroporto di arrivo
            if self.getObjFun(parziale) > self._bestObjFunction:
                # ho trovato una soluzione migliore
                self._bestObjFunction = self.getObjFun(parziale)
                self._bestPath = copy.deepcopy(parziale)
        if len(parziale) == t+1:  # supero il limite
            return

        # Posso ancora aggiungere nodi
        # prendo i vicini dell'ultimo nodo e aggiungo un nodo alla volta

        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:  # nodo non visitato
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()

    def getObjFun(self, listOfNodes):
        objVal = 0
        for i in range(0, len(listOfNodes) - 1):
            objVal += self._graph[listOfNodes[i]][listOfNodes[i + 1]]["weight"]
        return objVal

    def buildGraph(self, nMin):
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # self.addAllArchiV1()
        self.addAllArchiV2()
        print("N nodi:", len(self._graph.nodes), "N archi:", self._graph.number_of_edges())

    def addAllArchiV1(self):
        allEdges = DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                if self._graph.has_edge(e.aeroportoP, e.aeroportoD):  # se l'arco c'è già
                    self._graph[e.aeroportoP][e.aeroportoD]["weight"] += e.peso
                else:
                    self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)

    def addAllArchiV2(self):
        allEdges = DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._graph and e.aeroportoD in self._graph:
                self._graph.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)
                # faccio un controllo in meno

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNodes(self):
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getSortedNeighbors(self, node):
        neighbors = self._graph.neighbors(node)  # == self._graph[node]
        neighTuples = []

        for n in neighbors:
            neighTuples.append((n, self._graph[node][n]["weight"]))

        neighTuples.sort(key=lambda x: x[1], reverse=True)  # sorto con secondo elemento (peso)

        return neighTuples

    def getPath(self, v0, v1):
        path = nx.dijkstra_path(self._graph, v0, v1, weight=None)  # cammino che minimizza
        # path = nx.shortest_path(self._graph, v0, v1)
        #
        # Mydict = dict(nx.bfs_predecessors(self._graph, v0))
        # path = [v1]
        # while path[0] != v0:
        #     path.insert(0, Mydict[path[0]])  # prendo ultimo elemento fino a quando non arrivo a v0
        return path
