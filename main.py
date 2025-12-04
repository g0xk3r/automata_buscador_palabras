import streamlit as st
import os
from nfa import NFA
from automatas import correr_automatas

st.set_page_config(layout="wide")
st.title("Buscador de palabras clave con Autómatas Finitos")

palabras_clave = [
    "acosar", "pinchar", "matar",
    "masacrar", "amenazar", "golpear",
    "atacar", "secuestrar",
]

# Modificación solicitada: Mostrar lista de palabras al inicio
st.markdown(f"**Palabras a buscar:** {', '.join(palabras_clave)}")

@st.cache_resource
def construir_nfa():
    return NFA.a_palabras_clave(palabras_clave)

@st.cache_resource
def convertir_a_dfa(_nfa: NFA):
    return _nfa.convertir_a_dfa()

nfa = construir_nfa()
dfa = convertir_a_dfa(nfa)

st.header("1. NFA (Search NFA)")
st.caption("Este es el diseño inicial: un árbol de palabras con un bucle en el inicio (Sigma) que permite reiniciar la búsqueda.")
try:
    grafo_nfa = nfa.mostrar_grafo()
    st.graphviz_chart(grafo_nfa, use_container_width=True)
except Exception as e:
    st.error(f"Error al generar el grafo del NFA: {e}")

st.divider()

st.header("2. DFA (Resultado de la Conversión)")
st.caption("Este grafo muestra todas las transiciones deterministas, incluyendo los retornos y cruces entre palabras.")

try:
    grafo_dfa = dfa.mostrar_grafo()
    st.graphviz_chart(grafo_dfa, use_container_width=True)
    with st.expander("Ver Mapeo de Estados NFA a DFA"):
        # Ordenamos la lista para que el JSON se vea limpio
        estados_mapeados = {
            f"Estado DFA {dfa_id}" : sorted(list(nfa_estados))
            for nfa_estados, dfa_id in dfa.mapa_estados.items()
        }
        st.json(estados_mapeados)
except Exception as e:
    st.error(f"Error al generar el grafo del DFA: {e}")

st.divider()

st.header("Procesamiento de Archivo de Texto")
uploaded_file = st.file_uploader("Sube un archivo de texto, HTML o XML", type=["txt", "html", "xml"])

if uploaded_file is not None:
    with open("archivo_temporal", "wb") as f:
        f.write(uploaded_file.getbuffer())
    corredor = correr_automatas(dfa)
    palabras_encontradas, vitacora = corredor.procesar_contenido("archivo_temporal")
    st.subheader(f"Resultados: {len(palabras_encontradas)} palabras clave encontradas")

    if palabras_encontradas:
        st.dataframe(palabras_encontradas)
    else:
        st.info("No se encontraron palabras clave en el archivo.")

    st.subheader("Bitácora de Procesamiento")
    with st.expander("Ver Bitácora Completa"):
        st.code(vitacora, language='text')

    os.remove("archivo_temporal")