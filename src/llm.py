import ollama
from search import search

def generate_response(query):
    """Genera una respuesta basada en los fragmentos recuperados."""
    results = search(query, top_k=5)  # Buscar en la base de datos

    if not results:  # Verificar si `results` es None o vacío
        return "⚠️ No se encontraron documentos relevantes para la consulta."

    context = "\n\n".join([f"- {contenido_texto}" for _, _, contenido_texto in results])
    print(f"Chunks obtenidos:\n{context}")
    prompt = f"""
    Eres un asistente en español que responde preguntas basándose en el siguiente contexto:

    {context}

    Pregunta: {query}
    Respuesta en español:
    """

    response = ollama.chat(model="llama3.2:3b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

if __name__ == "__main__":
    consulta = input("🔎 Ingrese su consulta: ")
    respuesta = generate_response(consulta)
    
    print("\n🤖 Respuesta del LLM:\n", respuesta)
