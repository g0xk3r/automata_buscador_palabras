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
                buffer_actual += caracter
                mensaje_vitacora = f"Linea {linea}, Columna {columna}: Caracter '{caracter}'. Transicion {estado_original} -> {estado_actual}\n"
                if estado_actual in self.dfa.estados_finales:
                    encontrado = {
                        'palabra': buffer_actual,
                        'linea': linea,
                        'columna_fin': columna,
                        'columna_inicio': columna - len(buffer_actual) + 1
                    }
                    self.palabras_encontradas.append(encontrado)
                    mensaje_vitacora += f"(Palabra clave encontrada: {buffer_actual})"
                self.vitacora_contenido.append(mensaje_vitacora)
            else:
                self.vitacora_contenido.append(f"Linea {linea}, Columna {columna}: Caracter '{caracter}'. No hay transicion desde el estado {estado_actual}. Reiniciando al estado inicial.\n")
                buffer_actual = ""
                estado_actual = self.dfa.estado_inicial
                if caracter in self.dfa.transiciones.get(estado_actual, {}):
                    estado_actual = self.dfa.transiciones[estado_actual][caracter]
                    buffer_actual += caracter
                    self.vitacora_contenido.append(f"Procesando '{caracter}' desde {self.dfa.estado_inicial}: {self.dfa.estado_inicial} -> {estado_actual}.\n")
                    if estado_actual in self.dfa.estados_finales:
                        encontrado = {
                            'palabra': buffer_actual,
                            'linea': linea,
                            'columna_fin': columna,
                            'columna_inicio': columna
                        }
                        self.palabras_encontradas.append(encontrado)
                        self.vitacora_contenido.append(f"(Palabra clave encontrada: {buffer_actual})\n")
                else:
                    self.vitacora_contenido.append(f"Caracter '{caracter}' no inicia ninguna palabra clave.\n")
            if caracter == '\n':
                linea += 1
                columna = 1
            else:
                columna += 1
        self.vitacora_contenido.append("Procesamiento del archivo finalizado.\n")
        return self.palabras_encontradas, "\n".join(self.vitacora_contenido)