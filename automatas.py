from dfa import DFA
from bs4 import BeautifulSoup

class correr_automatas:
    def __init__(self, dfa: DFA):
        self.dfa = dfa
        self.bitacora_contenido = []
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
                if estado_actual == 0:
                    buffer_actual = ""
                else:
                    buffer_actual += caracter

                mensaje_vitacora = f"Linea {linea}, Columna {columna}: Caracter '{caracter}'. Transicion {estado_original} -> {estado_actual}"
                if estado_actual in self.dfa.estados_finales:
                    encontrado = {
                        'palabra': buffer_actual,
                        'linea': linea,
                        'columna_fin': columna,
                        'columna_inicio': columna - len(buffer_actual) + 1
                    }
                    self.palabras_encontradas.append(encontrado)
                    mensaje_vitacora += f" [PALABRA ENCONTRADA: {buffer_actual}]"
                    estado_actual = 0
                    buffer_actual = ""
                self.vitacora_contenido.append(mensaje_vitacora)
            else:
                self.vitacora_contenido.append(f"Linea {linea}, Columna {columna}: Caracter '{caracter}'. No es parte del alfabeto clave. Reinicio.\n")
                buffer_actual = ""
                estado_actual = self.dfa.estado_inicial
            if caracter == '\n':
                linea += 1
                columna = 1
            else:
                columna += 1

        self.vitacora_contenido.append("\nProcesamiento del archivo finalizado.")
        return self.palabras_encontradas, "\n".join(self.vitacora_contenido)