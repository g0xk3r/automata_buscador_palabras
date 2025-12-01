import streamlit as st
import os
from nfa import NFA
from automatas import correr_automatas

st.title("Buscador de palabras clave con Automatas Finitos")

palabras_clave = [
    "acosar", "pinchar", "matar",
    "masacrar", "amenazar", "golpear",
    "atacar", "secuestrar",
]

st.sidebar.header("Palabras Clave")
st.sidebar.json(palabras_clave)

@st.cache_resource
def construir_nfa():
    return NFA.a_palabras_clave(palabras_clave)

@st.cache_resource
def convertir_a_dfa(_nfa: NFA):
    return _nfa.convertir_a_dfa()

nfa = construir_nfa()
dfa = convertir_a_dfa(nfa)
st.header("Diagrama del DFA")

try:
    grafo_dfa = dfa.mostrar_grafo()
    st.graphviz_chart(grafo_dfa)
    with st.expander("Mapeo de Estados NFA a DFA"):
        estados_mapeados = {
            f"Estado DFA {dfa_id}" : list(nfa_estados)
            for nfa_estados, dfa_id in dfa.mapa_estados.items()
        }
        st.json(estados_mapeados)
except Exception as e:
    st.error(f"Error al generar el grafo del DFA: {e}")

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