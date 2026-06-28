import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapOb={}

    def buildGraph(self):
        self._graph.clear()

        nodes=DAO.getAllNodes()
        for n in nodes:
            self._idMapOb[n.object_id]=n

        self._graph.add_nodes_from(nodes)

        allEdges=DAO.getAllEdges(self._idMapOb)
        for e in allEdges:
            self._graph.add_edge(e.o1 , e.o2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getComponenenteConnessa(self, idOggetto):
        source=self._idMapOb[idOggetto]
        compConnessa=nx.node_connected_component(self._graph,source)   #-> Restituisce un set di nodi
        return compConnessa

    def _hasNode(self, idOggetto):
        return idOggetto in self._idMapOb    #Dobbiamo vedere le chiavi del dizionario (il for se dobbiamo ciclaere sui valori)


    def getBestPath(self, idOggetto, LUN):
        self._bestPath=[]
        self._bestScore=0

        source=self._idMapOb[idOggetto]
        parziale=[source]

        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, LUN)
                parziale.pop()

        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, LUN):
        #1) Caso terminale:
        if len(parziale)==LUN:
            score=self._getScore(parziale)
            if score > self._bestScore:
                self._bestScore=self._getScore(parziale)
                self._bestPath=copy.deepcopy(parziale)
            return

        #2)Caso ricorsivo:
        for n in self._graph.neighbors(parziale[-1]): #Guardo i vicini dell'ultimo nodo aggiunto
            if n.classification== parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, LUN)
                parziale.pop()


    def _getScore(self, path):
        score=0
        for i in range(len(path)-1):
            score  += self._graph[path[i]][path[i+1]]["weight"]
        return score