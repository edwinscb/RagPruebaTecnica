import streamlit as st
import requests

# URL de la API de Flask
API_URL = "http://127.0.0.1:5000/chat"

# Función para interactuar con la API de Flask
def get_response_from_api(query):
    payload = {"query": query}
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al contactar la API: {e}")
        return None

# Configuración de Streamlit
st.title("Asistente Virtual - By Edwin Castro")
st.markdown("Interactúa con el agente inteligente a través de la siguiente interfaz:")

# Caja de texto para la consulta del usuario
query = st.text_input("¿En qué puedo ayudarte?", "")

if query:
    st.write(f"🧐 **Consulta:** {query}")
    
    # Obtener la respuesta de la API
    result = get_response_from_api(query)
    
    if result:
        # Mostrar la respuesta
        st.write(f"🤖 Respuesta del Agente: {result['response']}")

        # Mostrar los chunks contextuales utilizados por el modelo
        st.subheader("Fragmentos utilizados para la respuesta:")
        for idx, chunk in enumerate(result['content']):
            st.write(f"{idx+1}. {chunk}")
