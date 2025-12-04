import streamlit as st
import os
from nfa import NFA
from automatas import correr_automatas

st.set_page_config(layout="wide")
st.title("Generador de Archivos de Autómatas")

palabras_clave = [
    "acosar", "pinchar", "matar",
    "masacrar", "amenazar", "golpear",
    "atacar", "secuestrar",
]

st.markdown(f"**Palabras a buscar:** {', '.join(palabras_clave)}")

@st.cache_resource
def construir_nfa():
    return NFA.a_palabras_clave(palabras_clave)

@st.cache_resource
def convertir_a_dfa(_nfa: NFA):
    return _nfa.convertir_a_dfa()
nfa = construir_nfa()
dfa = convertir_a_dfa(nfa)

st.header("1. Generación de Grafos (Archivos)")

try:
    grafo_nfa = nfa.mostrar_grafo()
    grafo_nfa.save("nfa_grafo.dot")
    st.success("Archivo 'nfa_grafo.dot' generado correctamente.")
    try:
        grafo_nfa.render("nfa_grafo", format="pdf", cleanup=True)
        st.success("Archivo 'nfa_grafo.pdf' generado correctamente.")
    except Exception as e:
        st.warning(f"Se generó el .dot, pero hubo un error al crear el PDF\n{e}")

except Exception as e:
    st.error(f"Error al procesar NFA: {e}")

try:
    grafo_dfa = dfa.mostrar_grafo()
    grafo_dfa.save("dfa_grafo.dot")
    st.success("Archivo 'dfa_grafo.dot' generado correctamente.")
    try:
        grafo_dfa.render("dfa_grafo", format="pdf", cleanup=True)
        st.success("Archivo 'dfa_grafo.pdf' generado correctamente.")
    except Exception as e:
        st.warning(f"Se generó el .dot, pero hubo un error al crear el PDF\n{e}")
    with st.expander("Datos del Mapeo"):
        estados_mapeados = {
            f"Estado DFA {dfa_id}" : sorted(list(nfa_estados))
            for nfa_estados, dfa_id in dfa.mapa_estados.items()
        }
        st.json(estados_mapeados)

except Exception as e:
    st.error(f"Error al procesar DFA\n{e}")

st.divider()

st.header("2. Procesamiento de Archivo")
uploaded_file = st.file_uploader("Sube un archivo de texto, HTML o XML", type=["txt", "html", "xml"])

if uploaded_file is not None:
    with open("archivo_temporal", "wb") as f:
        f.write(uploaded_file.getbuffer())

    corredor = correr_automatas(dfa)
    palabras_encontradas, texto_bitacora = corredor.procesar_contenido("archivo_temporal")
    st.subheader(f"Resultados: {len(palabras_encontradas)} palabras encontradas")
    if palabras_encontradas:
        st.dataframe(palabras_encontradas)
    else:
        st.info("No se encontraron palabras clave.")

    nombre_bitacora = "bitacora.txt"
    try:
        with open(nombre_bitacora, "w", encoding="utf-8") as f:
            f.write(texto_bitacora)

        st.success(f"Archivo '{nombre_bitacora}' generado exitosamente.")

    except Exception as e:
        st.error(f"Error al guardar la bitácora\n{e}")

    os.remove("archivo_temporal")