from collections import deque
from typing import Set, Dict, Tuple, List
from dfa import DFA
class NFA:
    def __init__(self, estados: Set[int], estado_inicial: int, estado_aceptacion: Set[int], alfabeto: Set[str], transiciones: Dict[Tuple[int, str], Set[int]]):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.alfabeto = alfabeto
        self.transiciones = transiciones

    def cerradura_epsilon(self, estados: Set[int]):
        pila = list(estados)
        cerradura = set(estados)

        while pila:
            estado_actual = pila.pop()
            transiciones_epsilon = self.transiciones.get((estado_actual, ' '), set())
            for estado in transiciones_epsilon:
                if estado not in cerradura:
                    cerradura.add(estado)
                    pila.append(estado)
        return cerradura

    def mover(self, estados: Set[int], simbolo: str):
        estados_alcanzables = set()
        for estado in estados:
            transiciones_simbolo = self.transiciones.get((estado, simbolo), set())
            estados_alcanzables.update(transiciones_simbolo)
        return estados_alcanzables

    def convertir_a_dfa(self):
        estados_dfa = set()
        estado_inicial_dfa = frozenset(self.cerradura_epsilon({self.estado_inicial}))
        estados_finales_dfa = set()
        transiciones_dfa = {}
        mapa_estados_dfa: Dict[frozenset[int], int] = {estado_inicial_dfa: 0}
        id_contador_estados_dfa = 0
        cola = deque([estado_inicial_dfa])
        estados_dfa.add(estado_inicial_dfa)
        while cola:
            estado_actual_nfa = cola.popleft()
            id_estado_actual_dfa = mapa_estados_dfa[estado_actual_nfa]
            if not estado_actual_nfa.isdisjoint(self.estado_aceptacion):
                estados_finales_dfa.add(id_estado_actual_dfa)

            for simbolo in self.alfabeto:
                siguientes_estados_nfa = self.mover(estado_actual_nfa, simbolo)
                siguientes_estados_nfa_cerradura = frozenset(self.cerradura_epsilon(siguientes_estados_nfa))
                if not siguientes_estados_nfa_cerradura:
                    continue
                if siguientes_estados_nfa_cerradura not in estados_dfa:
                    estados_dfa.add(siguientes_estados_nfa_cerradura)
                    cola.append(siguientes_estados_nfa_cerradura)
                    id_contador_estados_dfa += 1
                    mapa_estados_dfa[siguientes_estados_nfa_cerradura] = id_contador_estados_dfa
                id_siguiente_estado_dfa = mapa_estados_dfa[siguientes_estados_nfa_cerradura]
                if id_estado_actual_dfa not in transiciones_dfa:
                    transiciones_dfa[id_estado_actual_dfa] = {}
                transiciones_dfa[id_estado_actual_dfa][simbolo] = id_siguiente_estado_dfa
        return DFA(
            estados=set(mapa_estados_dfa.values()),
            estado_inicial=mapa_estados_dfa[estado_inicial_dfa],
            estados_finales=estados_finales_dfa,
            alfabeto=self.alfabeto,
            transiciones=transiciones_dfa,
            mapa_estados=mapa_estados_dfa
        )

    @staticmethod
    def a_palabras_clave(palabras_clave: List[str]):
        estado_inicial = 0
        estados = {0}
        estados_finales = set()
        transiciones = {}
        alfabeto = set()
        nuevo_contador_estado = 0

        for palabra in palabras_clave:
            estado_actual = estado_inicial
            for simbolo in palabra:
                alfabeto.add(simbolo)
                if (estado_actual, simbolo) in transiciones:
                    estado_actual = list(transiciones[(estado_actual, simbolo)])[0]
                else:
                    nuevo_contador_estado += 1
                    estados.add(nuevo_contador_estado)
                    transiciones[(estado_actual, simbolo)] = {nuevo_contador_estado}
                    estado_actual = nuevo_contador_estado
            estados_finales.add(estado_actual)
        return NFA(
            estados=estados,
            estado_inicial=estado_inicial,
            estado_aceptacion=estados_finales,
            alfabeto=alfabeto,
            transiciones=transiciones
        )