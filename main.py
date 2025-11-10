class NFA:
    def __init__(self, estados: set[int], estado_inicial: int, estado_aceptacion: set[int], alfabeto: set[str], transiciones: dict[tuple[int, str], set[int]]):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.alfabeto = alfabeto