from graphviz import Digraph
from typing import Set, Dict, Optional
class DFA:
    def __init__(self, estados: Set[int], estado_inicial: int, estados_finales: Set[int], alfabeto: Set[str], transiciones: Dict[int, Dict[str, int]], mapa_estados: Optional[Dict[frozenset, int]] = None):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.mapa_estados = mapa_estados

    def mostrar_grafo(self):
        punto = Digraph()
        punto.attr(rankdir='LR')
        punto.node('start', shape='point')
        for estado in self.estados:
            if estado in self.estados_finales:
                punto.node(str(estado), shape='doublecircle')
            else:
                punto.node(str(estado), shape='circle')

        punto.edge('start', str(self.estado_inicial))

        for estado_inicial, mapa_transiciones in self.transiciones.items():
            for simbolo, estado_final in mapa_transiciones.items():
                punto.edge(str(estado_inicial), str(estado_final), label=simbolo)

        return punto