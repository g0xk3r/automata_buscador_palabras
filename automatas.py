from dfa import DFA
from bs4 import BeautifulSoup

class correr_automatas:
    def __init__(self, dfa: DFA):
        self.dfa = dfa
        self.vitacora_contenido = []
        self.palabras_encontradas = []

    def leer_archivo(self, ruta_archivo: str):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                if ruta_archivo.endswith('.html') or ruta_archivo.endswith('.xml'):
                    nuevo_legible = BeautifulSoup(contenido, 'html.parser')
                    return nuevo_legible.get_text()
                return contenido
        except Exception as error:
            print(f"Error: El archivo '{ruta_archivo}' causó: {error}")
            return ""

    def procesar_contenido(self, ruta_archivo: str):
        texto = self.leer_archivo(ruta_archivo)
        self.vitacora_contenido = ["Iniciando procesamiento del archivo.\n"]
        self.palabras_encontradas = []
        estado_actual = self.dfa.estado_inicial
        buffer_actual = ""
        linea = 1
        columna = 1

        for caracter in texto:
            estado_original = estado_actual
            if caracter in self.dfa.transiciones.get(estado_actual, {}):
                estado_actual = self.dfa.transiciones[estado_actual][caracter]
                buffer_actual += caracter